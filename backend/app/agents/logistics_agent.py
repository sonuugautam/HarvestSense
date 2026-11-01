"""
Logistics Agent: Evaluates transport vehicle selection, road transit durations,
freight expenses (fuel, distance, loading, tolls), and transit vibration spoilage.
"""

from typing import Dict, Any, List
from app.data.logistics_data import VEHICLE_OPTIONS, get_vehicle_list, select_best_vehicle_for_load
from app.data.markets_data import REGIONAL_MARKETS
from app.data.faostat_data import get_crop_detail


class LogisticsAgent:
    def __init__(self, crop_id: str, quantity_quintals: float, fuel_modifier: float = 1.0,
                 preferred_vehicle: str = None):
        self.crop_id = crop_id
        self.quantity = float(quantity_quintals)
        self.fuel_modifier = float(fuel_modifier)
        self.preferred_vehicle = preferred_vehicle
        self.crop_data = get_crop_detail(crop_id)
        self.logs: List[Dict[str, Any]] = []

    def evaluate_route(self, market_id: str, custom_vehicle_id: str = None) -> Dict[str, Any]:
        """
        Calculates transport costs, transit hours, and transit mechanical spoilage
        from farm origin to the specified target market.
        """
        market = REGIONAL_MARKETS[market_id]
        distance_km = market["distance_km"]
        transit_hours = market["transit_hours"]
        is_perishable = (self.crop_data["perishability_class"] == "HIGH")

        # Determine vehicle
        vehicle_id = custom_vehicle_id or self.preferred_vehicle or select_best_vehicle_for_load(
            self.quantity, distance_km, is_perishable
        )
        vehicle = VEHICLE_OPTIONS.get(vehicle_id, VEHICLE_OPTIONS["pickup_mini_truck"])

        # Cost calculation
        if vehicle.get("is_pooled", False):
            # Pooled FPO freight
            freight_cost = (
                vehicle["base_booking_fee"] +
                (self.quantity * vehicle["cost_per_quintal_flat"]) +
                (self.quantity * distance_km * vehicle["cost_per_quintal_per_km"] * self.fuel_modifier) +
                vehicle["loading_unloading_labor_flat"]
            )
        else:
            freight_cost = (
                vehicle["base_booking_fee"] +
                (distance_km * vehicle["cost_per_km"] * self.fuel_modifier) +
                vehicle["loading_unloading_labor_flat"]
            )

        # Market entry cess / toll
        # Estimated baseline product value for cess calculation
        nominal_value = self.quantity * self.crop_data["baseline_price_per_quintal"]
        entry_tax = nominal_value * market["entry_cess_rate"]
        handling_fee = self.quantity * market["base_handling_fee_per_quintal"]
        total_market_fees = entry_tax + handling_fee

        total_transport_and_logistics = round(freight_cost + total_market_fees, 2)

        # Transit vibration & respiration spoilage calculation
        base_hourly_vibration = self.crop_data["vibration_transit_loss_per_hour"]
        vibration_factor = vehicle["transit_vibration_loss_factor"]
        
        # High heat penalty during long daytime transit if not refrigerated
        heat_multiplier = 1.0
        if not vehicle["is_refrigerated"] and transit_hours > 3.0 and is_perishable:
            heat_multiplier = 1.4  # Trapped heat in covered bed triggers rapid ethylene breakdown

        transit_spoilage_rate = min(0.18, transit_hours * base_hourly_vibration * vibration_factor * heat_multiplier)

        return {
            "market_id": market_id,
            "market_name": market["name"],
            "distance_km": distance_km,
            "transit_hours": transit_hours,
            "vehicle_id": vehicle["id"],
            "vehicle_name": vehicle["name"],
            "is_refrigerated": vehicle["is_refrigerated"],
            "freight_cost": round(freight_cost, 2),
            "market_entry_fees": round(total_market_fees, 2),
            "total_logistics_expense": total_transport_and_logistics,
            "transit_spoilage_pct": round(transit_spoilage_rate * 100, 2),
            "transit_spoilage_fraction": transit_spoilage_rate,
            "provenance": "LOGISTICS_MODEL"
        }

    def generate_logistics_overview(self) -> List[Dict[str, Any]]:
        """Evaluates all candidate markets from a logistics feasibility perspective."""
        results = []
        for market_id, market in REGIONAL_MARKETS.items():
            route = self.evaluate_route(market_id)
            results.append(route)

        cheapest_route = min(results, key=lambda r: r["total_logistics_expense"])
        fastest_route = min(results, key=lambda r: r["transit_hours"])

        self.logs.append({
            "agent": "Logistics Agent",
            "phase": "Fleet & Route Optimization",
            "message": f"Calculated routes across {len(results)} markets for {self.quantity:.1f} quintals. Lowest logistics cost: ₹{cheapest_route['total_logistics_expense']:.2f} ({cheapest_route['market_name']}).",
            "badge_type": "info",
            "detail": {
                "fastest_market": fastest_route["market_name"],
                "fastest_time_hrs": fastest_route["transit_hours"],
                "fuel_modifier_active": self.fuel_modifier
            }
        })

        return results

