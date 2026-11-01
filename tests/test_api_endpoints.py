"""
FastAPI HTTP Endpoint Integration Tests for HarvestSense
"""

import sys
import os
import unittest
from starlette.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app.main import app


class TestApiEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("Farmer Agent", data["cooperating_agents"])

    def test_faostat_summary(self):
        res = self.client.get("/api/faostat/summary")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["metadata"]["domain_code"], "PP")
        self.assertGreater(data["supported_crops_count"], 4)

    def test_crops_endpoints(self):
        res = self.client.get("/api/crops")
        self.assertEqual(res.status_code, 200)
        crops = res.json()
        self.assertTrue(len(crops) >= 5)

        detail_res = self.client.get("/api/crops/tomatoes")
        self.assertEqual(detail_res.status_code, 200)
        detail = detail_res.json()
        self.assertEqual(detail["fao_item_code"], 388)

    def test_markets_endpoint(self):
        res = self.client.get("/api/markets")
        self.assertEqual(res.status_code, 200)
        markets = res.json()
        self.assertTrue(len(markets) >= 4)

    def test_vehicles_endpoint(self):
        res = self.client.get("/api/vehicles")
        self.assertEqual(res.status_code, 200)
        vehicles = res.json()
        self.assertTrue(len(vehicles) >= 4)

    def test_scenarios_endpoint(self):
        res = self.client.get("/api/scenarios")
        self.assertEqual(res.status_code, 200)
        scenarios = res.json()
        self.assertEqual(len(scenarios), 5)

    def test_optimize_post_endpoint(self):
        payload = {
            "crop_id": "tomatoes",
            "quantity_quintals": 18.0,
            "harvest_date": "2026-10-29",
            "quality_grade": "Grade A",
            "farmer_location": "Nashik",
            "storage_type": "ambient",
            "max_wait_days": 5,
            "preferred_vehicle": None,
            "fuel_price_modifier": 1.0
        }
        res = self.client.post("/api/optimize", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("recommended_plan", data)
        self.assertIn("agent_logs", data)
        self.assertGreater(data["recommended_plan"]["net_profit"], 0)

    def test_simulate_post_endpoint(self):
        payload = {
            "base_request": {
                "crop_id": "tomatoes",
                "quantity_quintals": 18.0,
                "harvest_date": "2026-10-29",
                "quality_grade": "Grade A",
                "farmer_location": "Nashik",
                "storage_type": "ambient",
                "max_wait_days": 5
            },
            "simulated_wait_day": 2,
            "simulated_storage_type": "ventilated",
            "fuel_price_shock_pct": 10.0,
            "market_price_shock_pct": 5.0
        }
        res = self.client.post("/api/simulate", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("delta_net_profit", data)
        self.assertIn("delta_spoilage_pct", data)
        self.assertIn("verdict", data)

    def test_frontend_serving(self):
        """Verify that the built React frontend is served at root."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        # Should contain HTML content
        self.assertIn("<!doctype html>", res.text.lower())


if __name__ == "__main__":
    unittest.main()

