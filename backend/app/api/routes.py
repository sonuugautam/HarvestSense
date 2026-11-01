"""
FastAPI Routes for HarvestSense Multi-Agent Optimization System
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List

from app.models.schemas import OptimizeRequest, SimulationRequest, OptimizationResponse
from app.data.faostat_data import (
    get_crop_list, get_crop_detail, CROPS_DATABASE, FAOSTAT_METADATA
)
from app.data.markets_data import get_market_list, REGIONAL_MARKETS
from app.data.logistics_data import get_vehicle_list, VEHICLE_OPTIONS
from app.agents.coordinator import MultiAgentCoordinator

router = APIRouter()

PRELOADED_SCENARIOS = [
    {
        "id": "nashik_tomatoes",
        "title": "🍅 Nashik Tomato Smallholder: Local Yard Glut vs Metro Terminal",
        "badge": "Perishable Veg (High Urgency)",
        "description": "Farmer harvested 18 quintals of Grade A tomatoes. Local taluka mandi is flooded with supply, driving down bids. Metro Terminal Market is 145 km away with strong weekend supermarket demand.",
        "params": {
            "crop_id": "tomatoes",
            "quantity_quintals": 18.0,
            "harvest_date": "2026-10-29",
            "quality_grade": "Grade A",
            "farmer_location": "Dindori Block, Nashik Valley",
            "storage_type": "ambient",
            "max_wait_days": 6,
            "preferred_vehicle": None,
            "fuel_price_modifier": 1.0
        }
    },
    {
        "id": "karnataka_onions",
        "title": "🧅 Karnataka Onion Grower: Ventilated Chawl Holding Strategy",
        "badge": "Semi-Perishable Bulb",
        "description": "Farmer has 32 quintals of Grade B onions stored in a ventilated Kanda Chawl. Local traders offering low distress rates, but prices at the District APMC are forecast to rise within 4-5 days.",
        "params": {
            "crop_id": "onions",
            "quantity_quintals": 32.0,
            "harvest_date": "2026-10-29",
            "quality_grade": "Grade B",
            "farmer_location": "Bagalkot Rural Belt",
            "storage_type": "ventilated",
            "max_wait_days": 10,
            "preferred_vehicle": "pickup_mini_truck",
            "fuel_price_modifier": 1.0
        }
    },
    {
        "id": "punjab_wheat",
        "title": "🌾 Punjab Wheat Producer: Bulk Grain Warehouse Logistics",
        "badge": "Cereal Grain (Low Perishability)",
        "description": "Farmer harvested 65 quintals of high-grade Sharbati milling wheat. Evaluating whether to hire a medium 6-wheeler freight truck to the Metro Wholesale Terminal or sell to local FPO depot.",
        "params": {
            "crop_id": "wheat",
            "quantity_quintals": 65.0,
            "harvest_date": "2026-10-29",
            "quality_grade": "Grade A",
            "farmer_location": "Ludhiana District",
            "storage_type": "warehouse",
            "max_wait_days": 12,
            "preferred_vehicle": "medium_freight_truck",
            "fuel_price_modifier": 1.0
        }
    },
    {
        "id": "guntur_chillies",
        "title": "🌶️ Guntur Green Chilli: Ambient Spoilage vs Refrigerated Transit",
        "badge": "High-Value Cash Crop",
        "description": "Farmer has 12 quintals of Grade A green chillies. Ambient temperature is 34°C causing rapid moisture loss. Evaluating reefer van vs local village traders.",
        "params": {
            "crop_id": "green_chillies",
            "quantity_quintals": 12.0,
            "harvest_date": "2026-10-29",
            "quality_grade": "Grade A",
            "farmer_location": "Tenali Rural Hub, Guntur",
            "storage_type": "ventilated",
            "max_wait_days": 5,
            "preferred_vehicle": "reefer_cold_van",
            "fuel_price_modifier": 1.0
        }
    },
    {
        "id": "bihar_maize_fpo",
        "title": "🌽 Bihar Smallholder Maize: Shared FPO Aggregation Route",
        "badge": "Pooled FPO Smallholder",
        "description": "Marginal farmer with 6 quintals of maize. Individual transport to city is uneconomical. Exploring FPO pooled collective logistics to the Agro-Processing Hub.",
        "params": {
            "crop_id": "maize",
            "quantity_quintals": 6.0,
            "harvest_date": "2026-10-29",
            "quality_grade": "Grade B",
            "farmer_location": "Purnia Maize Corridor",
            "storage_type": "hermetic_bag",
            "max_wait_days": 8,
            "preferred_vehicle": "shared_fpo_freight",
            "fuel_price_modifier": 1.0
        }
    }
]


@router.get("/health")
def get_health():
    return {
        "status": "healthy",
        "service": "HarvestSense Multi-Agent Optimizer API",
        "version": "1.0.0",
        "sdg_target": "SDG 2: Zero Hunger",
        "cooperating_agents": ["Farmer Agent", "Market Agent", "Logistics Agent", "Coordinator Agent"]
    }


@router.get("/faostat/summary")
def get_faostat_summary():
    """Returns official FAOSTAT dataset information and provenance metadata."""
    return {
        "metadata": FAOSTAT_METADATA,
        "supported_crops_count": len(CROPS_DATABASE),
        "crops": [
            {
                "id": c["id"],
                "name": c["name"],
                "fao_item_code": c["fao_item_code"],
                "baseline_price_quintal": c["baseline_price_per_quintal"],
                "provenance": c["provenance"]
            }
            for c in CROPS_DATABASE.values()
        ]
    }


@router.get("/crops")
def list_crops():
    """Returns all available crop categories and options."""
    return get_crop_list()


@router.get("/crops/{crop_id}")
def get_crop(crop_id: str):
    """Returns detailed information for a crop including FAOSTAT time series."""
    try:
        return get_crop_detail(crop_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Crop '{crop_id}' not found")


@router.get("/markets")
def list_markets():
    """Returns all modeled regional wholesale markets."""
    return get_market_list()


@router.get("/vehicles")
def list_vehicles():
    """Returns all modeled vehicle options."""
    return get_vehicle_list()


@router.get("/scenarios")
def list_scenarios():
    """Returns pre-configured realistic agricultural scenarios for 1-click demo."""
    return PRELOADED_SCENARIOS


@router.post("/optimize")
def optimize_harvest_plan(req: OptimizeRequest):
    """
    Main Multi-Agent Workflow:
    Executes Farmer, Market, and Logistics agents collaboratively to discover
    the highest net profit, lowest-spoilage sell plan across markets and timing windows.
    """
    try:
        coordinator = MultiAgentCoordinator(
            crop_id=req.crop_id,
            quantity_quintals=req.quantity_quintals,
            harvest_date_str=req.harvest_date,
            quality_grade=req.quality_grade,
            storage_type=req.storage_type,
            farmer_location=req.farmer_location,
            max_wait_days=req.max_wait_days,
            preferred_vehicle=req.preferred_vehicle,
            fuel_price_modifier=req.fuel_price_modifier
        )
        result = coordinator.run_optimization()
        return result
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=f"Invalid parameter: {str(ke)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent optimization error: {str(e)}")


@router.post("/simulate")
def simulate_scenario(req: SimulationRequest):
    """
    Interactive 'What-If' Simulation Sandbox:
    Allows farmers to test hypothesis tweaks (e.g. storage upgrade, fuel price shocks, wait days)
    and directly compares the outcome against the baseline plan.
    """
    base = req.base_request
    
    # Calculate base optimization
    base_coord = MultiAgentCoordinator(
        crop_id=base.crop_id,
        quantity_quintals=base.quantity_quintals,
        harvest_date_str=base.harvest_date,
        quality_grade=base.quality_grade,
        storage_type=base.storage_type,
        farmer_location=base.farmer_location,
        max_wait_days=base.max_wait_days,
        preferred_vehicle=base.preferred_vehicle,
        fuel_price_modifier=base.fuel_price_modifier
    )
    base_res = base_coord.run_optimization()

    # Calculate simulated optimization with modifiers
    sim_storage = req.simulated_storage_type or base.storage_type
    sim_fuel_mod = base.fuel_price_modifier * (1.0 + (req.fuel_price_shock_pct / 100.0))

    sim_coord = MultiAgentCoordinator(
        crop_id=base.crop_id,
        quantity_quintals=base.quantity_quintals,
        harvest_date_str=base.harvest_date,
        quality_grade=base.quality_grade,
        storage_type=sim_storage,
        farmer_location=base.farmer_location,
        max_wait_days=max(req.simulated_wait_day, base.max_wait_days),
        preferred_vehicle=base.preferred_vehicle,
        fuel_price_modifier=sim_fuel_mod
    )
    sim_res = sim_coord.run_optimization()

    # Find specific simulated day result
    sim_day_plan = next(
        (p for p in sim_res["alternative_plans"] if p["sell_day"] == req.simulated_wait_day),
        sim_res["recommended_plan"]
    )
    if sim_res["recommended_plan"]["sell_day"] == req.simulated_wait_day:
        sim_day_plan = sim_res["recommended_plan"]

    # Apply market price shock if specified
    if req.market_price_shock_pct != 0.0:
        multiplier = 1.0 + (req.market_price_shock_pct / 100.0)
        sim_day_plan["effective_market_price_per_q"] = round(sim_day_plan["effective_market_price_per_q"] * multiplier, 2)
        sim_day_plan["gross_revenue"] = round(sim_day_plan["delivered_sellable_quintals"] * sim_day_plan["effective_market_price_per_q"], 2)
        sim_day_plan["net_profit"] = round(
            sim_day_plan["gross_revenue"] - sim_day_plan["transport_cost"] -
            sim_day_plan["market_cess_fees"] - sim_day_plan["storage_cost"], 2
        )

    net_delta = round(sim_day_plan["net_profit"] - base_res["recommended_plan"]["net_profit"], 2)
    spoilage_delta = round(sim_day_plan["total_spoilage_loss_pct"] - base_res["recommended_plan"]["total_spoilage_loss_pct"], 2)

    return {
        "baseline_recommended": base_res["recommended_plan"],
        "simulated_plan": sim_day_plan,
        "delta_net_profit": net_delta,
        "delta_spoilage_pct": spoilage_delta,
        "simulated_storage_used": sim_storage,
        "simulated_day": req.simulated_wait_day,
        "fuel_price_shock_pct": req.fuel_price_shock_pct,
        "market_price_shock_pct": req.market_price_shock_pct,
        "verdict": (
            "Higher Net Profit" if net_delta > 0 else "Lower Net Profit"
        )
    }

