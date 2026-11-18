"""
Extra tests for HarvestSense:
  1. Crop holding horizons (how long a farmer waits before selling)
  2. Alternative vehicle freight rates (cost / spoilage across every vehicle)
  3. The newly added crop: Cauliflower
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.data.faostat_data import CROPS_DATABASE, get_crop_list
from app.data.logistics_data import VEHICLE_OPTIONS, select_best_vehicle_for_load
from app.data.markets_data import REGIONAL_MARKETS
from app.agents.farmer_agent import FarmerAgent
from app.agents.logistics_agent import LogisticsAgent
from app.agents.coordinator import MultiAgentCoordinator

HARVEST_DATE = "2026-10-29"
HORIZONS = [0, 3, 7, 14]  # holding horizons (days) tested below


def run_plan(crop_id="tomatoes", qty=18.0, grade="Grade A", storage="ventilated",
             horizon=7, vehicle=None, fuel=1.0):
    return MultiAgentCoordinator(
        crop_id=crop_id,
        quantity_quintals=qty,
        harvest_date_str=HARVEST_DATE,
        quality_grade=grade,
        storage_type=storage,
        farmer_location="Test Farm",
        max_wait_days=horizon,
        preferred_vehicle=vehicle,
        fuel_price_modifier=fuel,
    ).run_optimization()


class TestCropHoldingHorizons(unittest.TestCase):
    """Testing different crop holding horizons (0, 3, 7, 14 days)."""

    def test_timeline_length_matches_horizon(self):
        """The forecast timeline must contain one point per day, 0..horizon."""
        for horizon in HORIZONS:
            res = run_plan(horizon=horizon)
            timeline = res["price_profit_timeline"]
            self.assertEqual(len(timeline), horizon + 1, f"horizon={horizon}")
            self.assertEqual([p["day"] for p in timeline], list(range(horizon + 1)))

    def test_recommended_sell_day_within_horizon(self):
        """Recommended sell day can never exceed the allowed holding horizon."""
        for crop_id in CROPS_DATABASE:
            for horizon in HORIZONS:
                res = run_plan(crop_id=crop_id, storage="ambient", horizon=horizon)
                self.assertLessEqual(res["recommended_plan"]["sell_day"], horizon,
                                     f"{crop_id} horizon={horizon}")

    def test_zero_day_horizon_forces_immediate_sale(self):
        res = run_plan(horizon=0)
        self.assertEqual(res["recommended_plan"]["sell_day"], 0)
        for plan in res["alternative_plans"]:
            self.assertEqual(plan["sell_day"], 0)

    def test_horizon_is_clamped_to_14_days(self):
        """Coordinator clamps horizons above 14 days (schema limit)."""
        res = run_plan(horizon=30)
        self.assertEqual(len(res["price_profit_timeline"]), 15)

    def test_longer_horizon_never_hurts_best_utility(self):
        """A longer horizon only adds options, so best utility cannot drop."""
        scores = [run_plan(horizon=h)["recommended_plan"]["utility_score"] for h in HORIZONS]
        for shorter, longer in zip(scores, scores[1:]):
            self.assertGreaterEqual(longer, shorter - 1e-6)

    def test_ambient_perishable_loss_grows_with_days(self):
        """Tomatoes in ambient storage should lose more every extra day held."""
        farmer = FarmerAgent("tomatoes", 18.0, HARVEST_DATE, "Grade A", "ambient", "Nashik")
        losses = [farmer.evaluate_holding_decay(d)[1] for d in HORIZONS]
        self.assertEqual(losses[0], 0.0)
        for earlier, later in zip(losses, losses[1:]):
            self.assertGreater(later, earlier)

    def test_better_storage_reduces_loss_at_every_horizon(self):
        """Ambient > ventilated > cold storage in spoilage, at each horizon > 0."""
        def loss(storage, day):
            return FarmerAgent("tomatoes", 18.0, HARVEST_DATE, "Grade A", storage, "x") \
                .evaluate_holding_decay(day)[1]

        for day in HORIZONS[1:]:
            self.assertGreater(loss("ambient", day), loss("ventilated", day))
            self.assertGreater(loss("ventilated", day), loss("cold_storage", day))

    def test_holding_cost_scales_linearly_with_days(self):
        farmer = FarmerAgent("tomatoes", 20.0, HARVEST_DATE, "Grade B", "cold_storage", "x")
        per_day = CROPS_DATABASE["tomatoes"]["storage_profiles"]["cold_storage"]["cost_per_quintal_day"] * 20.0
        for day in HORIZONS:
            cost = farmer.evaluate_holding_decay(day)[3]
            self.assertAlmostEqual(cost, per_day * day, places=2)

    def test_ambient_storage_has_zero_holding_cost(self):
        farmer = FarmerAgent("maize", 10.0, HARVEST_DATE, "Grade B", "ambient", "x")
        self.assertEqual(farmer.evaluate_holding_decay(14)[3], 0.0)

    def test_non_perishable_grain_survives_long_horizon(self):
        """Wheat in a warehouse should keep >90% viable even after 14 days."""
        farmer = FarmerAgent("wheat", 65.0, HARVEST_DATE, "Grade A", "warehouse", "x")
        viable, loss, _, _ = farmer.evaluate_holding_decay(14)
        self.assertGreater(viable, 0.90)
        self.assertLess(loss, 0.10)

    def test_viable_fraction_never_below_floor(self):
        """Model floors viable quantity at 15% even for worst-case decay."""
        farmer = FarmerAgent("tomatoes", 18.0, HARVEST_DATE, "Grade C", "ambient", "x")
        viable = farmer.evaluate_holding_decay(14)[0]
        self.assertGreaterEqual(viable, 0.15)

    def test_all_crops_all_horizons_run_cleanly(self):
        for crop_id in CROPS_DATABASE:
            for horizon in HORIZONS:
                res = run_plan(crop_id=crop_id, storage="ambient", horizon=horizon)
                self.assertGreater(res["recommended_plan"]["delivered_sellable_quintals"], 0)


class TestAlternativeVehicleFreightRates(unittest.TestCase):
    """Testing freight cost / spoilage for every alternative vehicle."""

    MARKET = "district_apmc_hub"

    def route(self, vehicle_id, qty=18.0, market=None, fuel=1.0, crop="tomatoes"):
        return LogisticsAgent(crop, qty, fuel).evaluate_route(market or self.MARKET, vehicle_id)

    def test_every_vehicle_returns_positive_freight(self):
        for vehicle_id in VEHICLE_OPTIONS:
            r = self.route(vehicle_id)
            self.assertEqual(r["vehicle_id"], vehicle_id)
            self.assertGreater(r["freight_cost"], 0)
            self.assertGreater(r["total_logistics_expense"], r["freight_cost"])

    def test_standard_vehicle_freight_formula(self):
        """Non-pooled freight = base fee + km * rate * fuel + loading labour."""
        market_km = REGIONAL_MARKETS[self.MARKET]["distance_km"]
        for vehicle_id in ("auto_mini_cart", "pickup_mini_truck", "medium_freight_truck", "reefer_cold_van"):
            v = VEHICLE_OPTIONS[vehicle_id]
            expected = v["base_booking_fee"] + market_km * v["cost_per_km"] + v["loading_unloading_labor_flat"]
            self.assertAlmostEqual(self.route(vehicle_id)["freight_cost"], expected, places=1)

    def test_pooled_fpo_freight_formula(self):
        """Pooled freight scales with quantity: fee + q*flat + q*km*rate + labour."""
        qty = 18.0
        km = REGIONAL_MARKETS[self.MARKET]["distance_km"]
        v = VEHICLE_OPTIONS["shared_fpo_freight"]
        expected = (v["base_booking_fee"] + qty * v["cost_per_quintal_flat"]
                    + qty * km * v["cost_per_quintal_per_km"] + v["loading_unloading_labor_flat"])
        self.assertAlmostEqual(self.route("shared_fpo_freight", qty)["freight_cost"], expected, places=1)

    def test_pooled_freight_grows_with_quantity_but_truck_does_not(self):
        small = self.route("shared_fpo_freight", qty=5.0)["freight_cost"]
        large = self.route("shared_fpo_freight", qty=35.0)["freight_cost"]
        self.assertGreater(large, small)
        # Fixed-rate truck: quantity does not change the freight quote
        self.assertEqual(self.route("pickup_mini_truck", qty=5.0)["freight_cost"],
                         self.route("pickup_mini_truck", qty=20.0)["freight_cost"])

    def test_small_load_short_route_cheaper_by_auto_than_big_truck(self):
        auto = self.route("auto_mini_cart", qty=5.0, market="local_rural_mandi")["freight_cost"]
        big = self.route("medium_freight_truck", qty=5.0, market="local_rural_mandi")["freight_cost"]
        self.assertLess(auto, big)

    def test_pooled_beats_dedicated_truck_for_marginal_farmer(self):
        """6 quintals to a nearby market: shared FPO freight must be cheapest."""
        costs = {vid: self.route(vid, qty=6.0, market="local_rural_mandi")["freight_cost"]
                 for vid in VEHICLE_OPTIONS}
        self.assertEqual(min(costs, key=costs.get), "shared_fpo_freight")

    def test_long_haul_reefer_costs_more_but_cuts_spoilage(self):
        """Reefer is pricier than a pickup, yet slashes transit spoilage on perishables."""
        reefer = self.route("reefer_cold_van", qty=18.0, market="metro_terminal_market")
        pickup = self.route("pickup_mini_truck", qty=18.0, market="metro_terminal_market")
        self.assertGreater(reefer["freight_cost"], pickup["freight_cost"])
        self.assertLess(reefer["transit_spoilage_pct"], pickup["transit_spoilage_pct"])
        self.assertTrue(reefer["is_refrigerated"])

    def test_vibration_factor_orders_transit_spoilage(self):
        """Open auto bruises most; reefer least (same crop, same route)."""
        spoil = {vid: self.route(vid, qty=18.0, market="metro_terminal_market")["transit_spoilage_pct"]
                 for vid in VEHICLE_OPTIONS}
        self.assertGreater(spoil["auto_mini_cart"], spoil["pickup_mini_truck"])
        self.assertGreater(spoil["pickup_mini_truck"], spoil["medium_freight_truck"])
        self.assertLess(spoil["reefer_cold_van"], min(
            spoil[v] for v in VEHICLE_OPTIONS if v != "reefer_cold_van"))

    def test_fuel_modifier_raises_freight_for_every_vehicle(self):
        for vehicle_id in VEHICLE_OPTIONS:
            normal = self.route(vehicle_id, fuel=1.0)["freight_cost"]
            spike = self.route(vehicle_id, fuel=1.5)["freight_cost"]
            cheap = self.route(vehicle_id, fuel=0.5)["freight_cost"]
            self.assertGreater(spike, normal, vehicle_id)
            self.assertLess(cheap, normal, vehicle_id)

    def test_fuel_shock_hurts_long_routes_more(self):
        """The same fuel spike adds more rupees on a 145 km route than a 14 km one."""
        def delta(market):
            base = self.route("pickup_mini_truck", market=market, fuel=1.0)["freight_cost"]
            hot = self.route("pickup_mini_truck", market=market, fuel=1.5)["freight_cost"]
            return hot - base
        self.assertGreater(delta("metro_terminal_market"), delta("local_rural_mandi"))

    def test_market_fees_independent_of_vehicle(self):
        fees = {self.route(v)["market_entry_fees"] for v in VEHICLE_OPTIONS}
        self.assertEqual(len(fees), 1)

    def test_preferred_vehicle_override_in_coordinator(self):
        """Forcing a vehicle must be honoured in every ranked plan."""
        for vehicle_id in VEHICLE_OPTIONS:
            res = run_plan(horizon=2, vehicle=vehicle_id)
            self.assertEqual(res["recommended_plan"]["vehicle_id"], vehicle_id)
            for plan in res["alternative_plans"]:
                self.assertEqual(plan["vehicle_id"], vehicle_id)

    def test_different_vehicles_change_recommended_profit(self):
        profits = {vid: run_plan(horizon=3, vehicle=vid)["recommended_plan"]["net_profit"]
                   for vid in VEHICLE_OPTIONS}
        self.assertGreater(len(set(profits.values())), 1)

    def test_default_vehicle_heuristic(self):
        self.assertEqual(select_best_vehicle_for_load(5.0, 20.0, False), "auto_mini_cart")
        self.assertEqual(select_best_vehicle_for_load(15.0, 60.0, False), "pickup_mini_truck")
        self.assertEqual(select_best_vehicle_for_load(60.0, 145.0, False), "medium_freight_truck")
        self.assertEqual(select_best_vehicle_for_load(15.0, 145.0, True), "reefer_cold_van")
        self.assertEqual(select_best_vehicle_for_load(30.0, 100.0, False), "shared_fpo_freight")

    def test_unknown_vehicle_falls_back_to_pickup(self):
        r = LogisticsAgent("tomatoes", 18.0).evaluate_route(self.MARKET, "no_such_vehicle")
        self.assertEqual(r["vehicle_id"], "pickup_mini_truck")


class TestNewCropCauliflower(unittest.TestCase):
    """Tests for the newly added Cauliflower crop (FAO item code 393)."""

    def test_cauliflower_data_integrity(self):
        self.assertIn("cauliflower", CROPS_DATABASE)
        b = CROPS_DATABASE["cauliflower"]
        self.assertEqual(b["fao_item_code"], 393)
        self.assertEqual(b["provenance"], "FAOSTAT_HISTORICAL")
        self.assertEqual(b["perishability_class"], "HIGH")
        self.assertEqual(len(b["seasonality_index"]), 12)
        self.assertGreaterEqual(len(b["fao_historical_annual"]), 5)
        self.assertEqual(set(b["quality_grades"]), {"Grade A", "Grade B", "Grade C"})
        self.assertIn("ambient", b["storage_profiles"])

    def test_cauliflower_listed_in_crop_list(self):
        self.assertIn("cauliflower", [c["id"] for c in get_crop_list()])

    def test_cauliflower_storage_ordering(self):
        sp = CROPS_DATABASE["cauliflower"]["storage_profiles"]
        self.assertGreater(sp["ambient"]["decay_factor"], sp["ventilated"]["decay_factor"])
        self.assertGreater(sp["ventilated"]["decay_factor"], sp["cold_storage"]["decay_factor"])
        self.assertLess(sp["ventilated"]["cost_per_quintal_day"], sp["cold_storage"]["cost_per_quintal_day"])

    def test_cauliflower_full_optimization_for_each_storage(self):
        for storage in CROPS_DATABASE["cauliflower"]["storage_profiles"]:
            res = run_plan("cauliflower", qty=20.0, storage=storage, horizon=7)
            rec = res["recommended_plan"]
            self.assertGreater(rec["net_profit"], 0)
            self.assertLessEqual(rec["delivered_sellable_quintals"], 20.0)

    def test_cauliflower_ambient_is_critical_risk(self):
        profile = FarmerAgent("cauliflower", 20.0, HARVEST_DATE, "Grade A", "ambient", "Pune").analyze_farm_profile()
        self.assertEqual(profile["risk_level"], "CRITICAL")

    def test_cauliflower_long_haul_uses_reefer(self):
        self.assertEqual(select_best_vehicle_for_load(20.0, 145.0, True), "reefer_cold_van")


if __name__ == "__main__":
    unittest.main()