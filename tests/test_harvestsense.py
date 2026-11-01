"""
End-to-End Automated Test Suite for HarvestSense
Tests all cooperating agents, FAOSTAT baselines, logistics models,
API routes, and what-if simulation scenarios.
"""

import sys
import os
import unittest
from datetime import datetime

# Insert backend directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.data.faostat_data import (
    CROPS_DATABASE, get_crop_list, get_crop_detail, FAOSTAT_METADATA
)
from app.data.markets_data import REGIONAL_MARKETS, get_market_list
from app.data.logistics_data import VEHICLE_OPTIONS, select_best_vehicle_for_load
from app.agents.farmer_agent import FarmerAgent
from app.agents.market_agent import MarketAgent
from app.agents.logistics_agent import LogisticsAgent
from app.agents.coordinator import MultiAgentCoordinator
from app.api.routes import PRELOADED_SCENARIOS


class TestHarvestSenseAgents(unittest.TestCase):

    def test_faostat_data_integrity(self):
        """Verify FAOSTAT commodities, item codes, and historical producer prices."""
        self.assertIn("tomatoes", CROPS_DATABASE)
        self.assertIn("potatoes", CROPS_DATABASE)
        self.assertIn("onions", CROPS_DATABASE)
        self.assertIn("wheat", CROPS_DATABASE)
        
        tomato = CROPS_DATABASE["tomatoes"]
        self.assertEqual(tomato["fao_item_code"], 388)
        self.assertEqual(tomato["provenance"], "FAOSTAT_HISTORICAL")
        self.assertTrue(len(tomato["fao_historical_annual"]) >= 5)
        self.assertEqual(len(tomato["seasonality_index"]), 12)
        self.assertGreater(tomato["baseline_price_per_quintal"], 1000)

    def test_farmer_agent_decay_and_storage(self):
        """Verify Farmer Agent shelf life decay curves and storage extension multipliers."""
        # Ambient storage on perishable crop
        agent_ambient = FarmerAgent(
            crop_id="tomatoes",
            quantity_quintals=18.0,
            harvest_date_str="2026-10-29",
            quality_grade="Grade A",
            storage_type="ambient",
            farmer_location="Nashik"
        )
        profile = agent_ambient.analyze_farm_profile()
        self.assertEqual(profile["risk_level"], "CRITICAL")
        self.assertEqual(profile["perishability_class"], "HIGH")

        # Evaluate decay on day 0 vs day 4
        viable_0, loss_0, grade_0, cost_0 = agent_ambient.evaluate_holding_decay(0)
        viable_4, loss_4, grade_4, cost_4 = agent_ambient.evaluate_holding_decay(4)

        self.assertEqual(viable_0, 1.0)
        self.assertEqual(loss_0, 0.0)
        self.assertEqual(grade_0, "Grade A")
        self.assertEqual(cost_0, 0.0)

        self.assertLess(viable_4, 1.0)
        self.assertGreater(loss_4, 0.15)  # Heavy spoilage under ambient conditions
        self.assertEqual(grade_4, "Grade B")  # Quality degraded to Grade B

        # Cold storage on perishable crop
        agent_cold = FarmerAgent(
            crop_id="tomatoes",
            quantity_quintals=18.0,
            harvest_date_str="2026-10-29",
            quality_grade="Grade A",
            storage_type="cold_storage",
            farmer_location="Nashik"
        )
        viable_cold_4, loss_cold_4, _, cost_cold_4 = agent_cold.evaluate_holding_decay(4)
        self.assertLess(loss_cold_4, loss_4)  # Cold storage drastically reduces loss
        self.assertGreater(cost_cold_4, 0.0)

    def test_market_agent_pricing_and_seasonality(self):
        """Verify Market Agent wholesale price spreads and FAOSTAT anchoring."""
        market_agent = MarketAgent("tomatoes", "2026-10-29")
        landscape = market_agent.analyze_market_landscape()
        
        self.assertGreater(landscape["faostat_baseline_price"], 0)
        self.assertTrue(len(landscape["markets_summary"]) >= 5)

        # Metro terminal market price projection
        metro_p = market_agent.predict_market_price("metro_terminal_market", 0, "Grade A")
        local_p = market_agent.predict_market_price("local_rural_mandi", 0, "Grade A")

        # Metro terminal should command premium over local rural yard
        self.assertGreater(metro_p["projected_price_per_quintal"], local_p["projected_price_per_quintal"])
        self.assertEqual(metro_p["provenance"], "SYNTHETIC_LOCAL_MARKET (Anchored on FAOSTAT)")

    def test_logistics_agent_route_and_transit_loss(self):
        """Verify Logistics Agent transport cost, vehicle fleet selection, and transit vibration decay."""
        logistics = LogisticsAgent("tomatoes", quantity_quintals=18.0, fuel_modifier=1.0)
        
        # Route to local yard (14 km) vs metro terminal (145 km)
        route_local = logistics.evaluate_route("local_rural_mandi")
        route_metro = logistics.evaluate_route("metro_terminal_market")

        self.assertLess(route_local["distance_km"], route_metro["distance_km"])
        self.assertLess(route_local["total_logistics_expense"], route_metro["total_logistics_expense"])
        self.assertLess(route_local["transit_spoilage_pct"], route_metro["transit_spoilage_pct"])

    def test_coordinator_full_optimization(self):
        """Verify Multi-Agent Coordinator produces optimal consensus and ranks options."""
        coordinator = MultiAgentCoordinator(
            crop_id="tomatoes",
            quantity_quintals=18.0,
            harvest_date_str="2026-10-29",
            quality_grade="Grade A",
            storage_type="ambient",
            farmer_location="Nashik Valley",
            max_wait_days=6
        )
        res = coordinator.run_optimization()

        self.assertIn("recommended_plan", res)
        self.assertIn("alternative_plans", res)
        self.assertIn("price_profit_timeline", res)
        self.assertIn("agent_logs", res)
        self.assertIn("sdg2_impact_metrics", res)

        rec = res["recommended_plan"]
        self.assertEqual(rec["rank"], 1)
        self.assertGreater(rec["net_profit"], 0)
        self.assertGreater(rec["delivered_sellable_quintals"], 0)
        self.assertLessEqual(rec["delivered_sellable_quintals"], 18.0)
        self.assertTrue(len(res["agent_logs"]) >= 5)

    def test_all_preloaded_scenarios(self):
        """Verify that every preloaded scenario executes cleanly without exceptions."""
        for scenario in PRELOADED_SCENARIOS:
            params = scenario["params"]
            coord = MultiAgentCoordinator(
                crop_id=params["crop_id"],
                quantity_quintals=params["quantity_quintals"],
                harvest_date_str=params["harvest_date"],
                quality_grade=params["quality_grade"],
                storage_type=params["storage_type"],
                farmer_location=params["farmer_location"],
                max_wait_days=params["max_wait_days"],
                preferred_vehicle=params["preferred_vehicle"],
                fuel_price_modifier=params["fuel_price_modifier"]
            )
            res = coord.run_optimization()
            self.assertIsNotNone(res["recommended_plan"])
            self.assertGreater(res["recommended_plan"]["utility_score"], 0)


if __name__ == "__main__":
    unittest.main()

