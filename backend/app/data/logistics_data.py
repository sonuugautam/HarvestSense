"""
Logistics & Transport Fleets Benchmark Data
Provenance: LOGISTICS_MODEL
Modeled from real-world smallholder transport economics, vehicle capacities,
fuel costs, and post-harvest transit decay parameters.
"""

from typing import Dict, Any, List

VEHICLE_OPTIONS: Dict[str, Dict[str, Any]] = {
    "auto_mini_cart": {
        "id": "auto_mini_cart",
        "name": "3-Wheeler Cargo Auto / Tractor Trolley",
        "capacity_quintals_min": 1.0,
        "capacity_quintals_max": 8.0,
        "max_recommended_range_km": 40.0,
        "base_booking_fee": 280.0,
        "cost_per_km": 16.50,
        "loading_unloading_labor_flat": 150.0,
        "is_refrigerated": False,
        "transit_vibration_loss_factor": 1.45,  # Unsprung, open bed increases bruising
        "suitable_for": "Small batch transport to nearby village yards",
        "provenance": "LOGISTICS_MODEL"
    },
    "pickup_mini_truck": {
        "id": "pickup_mini_truck",
        "name": "Pickup Mini-Truck (1.5T SCV - Bolero/Tata Ace)",
        "capacity_quintals_min": 5.0,
        "capacity_quintals_max": 22.0,
        "max_recommended_range_km": 160.0,
        "base_booking_fee": 650.0,
        "cost_per_km": 24.00,
        "loading_unloading_labor_flat": 350.0,
        "is_refrigerated": False,
        "transit_vibration_loss_factor": 1.00,  # Standard benchmark
        "suitable_for": "Most small-to-medium family farm harvests to district & regional mandis",
        "provenance": "LOGISTICS_MODEL"
    },
    "shared_fpo_freight": {
        "id": "shared_fpo_freight",
        "name": "Aggregated FPO Shared Route Transport",
        "capacity_quintals_min": 1.0,
        "capacity_quintals_max": 40.0,
        "max_recommended_range_km": 200.0,
        "is_pooled": True,
        "base_booking_fee": 120.0,
        "cost_per_quintal_flat": 35.0,
        "cost_per_quintal_per_km": 0.38,
        "loading_unloading_labor_flat": 100.0,
        "is_refrigerated": False,
        "transit_vibration_loss_factor": 0.95,
        "suitable_for": "Cost-effective shared transit for partial loads pooled with neighboring farms",
        "provenance": "LOGISTICS_MODEL"
    },
    "medium_freight_truck": {
        "id": "medium_freight_truck",
        "name": "Medium 6-Wheeler Freight Truck (8 Ton)",
        "capacity_quintals_min": 35.0,
        "capacity_quintals_max": 90.0,
        "max_recommended_range_km": 400.0,
        "base_booking_fee": 1600.0,
        "cost_per_km": 38.00,
        "loading_unloading_labor_flat": 750.0,
        "is_refrigerated": False,
        "transit_vibration_loss_factor": 0.85,  # Better suspension dampening on highways
        "suitable_for": "Large harvests (grains, bulk tubers) traveling to distant state terminals",
        "provenance": "LOGISTICS_MODEL"
    },
    "reefer_cold_van": {
        "id": "reefer_cold_van",
        "name": "Refrigerated Reefer Van (Cold Chain 2.5T)",
        "capacity_quintals_min": 10.0,
        "capacity_quintals_max": 25.0,
        "max_recommended_range_km": 500.0,
        "base_booking_fee": 1900.0,
        "cost_per_km": 44.00,
        "loading_unloading_labor_flat": 450.0,
        "is_refrigerated": True,
        "transit_vibration_loss_factor": 0.18,  # Chilled atmosphere eliminates heat stress & decay
        "suitable_for": "Highly perishable vegetables/fruits traveling 100+ km in hot weather",
        "provenance": "LOGISTICS_MODEL"
    }
}


def get_vehicle_list() -> List[Dict[str, Any]]:
    """Returns all modeled vehicle options."""
    return list(VEHICLE_OPTIONS.values())


def select_best_vehicle_for_load(quantity_quintals: float, distance_km: float, is_perishable: bool) -> str:
    """Heuristic rule to recommend default vehicle for given quantity and distance."""
    if is_perishable and distance_km > 100:
        return "reefer_cold_van"
    if quantity_quintals <= 7.0 and distance_km <= 35.0:
        return "auto_mini_cart"
    if quantity_quintals <= 22.0:
        return "pickup_mini_truck"
    if quantity_quintals > 35.0:
        return "medium_freight_truck"
    return "shared_fpo_freight"

