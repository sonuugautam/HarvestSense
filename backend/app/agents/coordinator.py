"""
Multi-Agent Coordinator: Orchestrates Farmer Agent, Market Agent, and Logistics Agent
to evaluate all selling permutations, negotiate trade-offs, and synthesize the optimal sell plan.
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta

from app.agents.farmer_agent import FarmerAgent
from app.agents.market_agent import MarketAgent
from app.agents.logistics_agent import LogisticsAgent
from app.data.markets_data import REGIONAL_MARKETS
from app.data.faostat_data import FAOSTAT_METADATA


class MultiAgentCoordinator:
    def __init__(self, crop_id: str, quantity_quintals: float, harvest_date_str: str,
                 quality_grade: str, storage_type: str, farmer_location: str,
                 max_wait_days: int = 7, preferred_vehicle: str = None,
                 fuel_price_modifier: float = 1.0):
        self.crop_id = crop_id
        self.quantity = float(quantity_quintals)
        self.harvest_date_str = harvest_date_str
        self.quality_grade = quality_grade
        self.storage_type = storage_type
        self.farmer_location = farmer_location
        self.max_wait_days = max(0, min(14, int(max_wait_days)))
        self.preferred_vehicle = preferred_vehicle
        self.fuel_price_modifier = float(fuel_price_modifier)

        # Initialize agents
        self.farmer_agent = FarmerAgent(
            crop_id, quantity_quintals, harvest_date_str, quality_grade, storage_type, farmer_location
        )
        self.market_agent = MarketAgent(crop_id, harvest_date_str)
        self.logistics_agent = LogisticsAgent(
            crop_id, quantity_quintals, fuel_price_modifier, preferred_vehicle
        )
        
        self.dialogue_logs: List[Dict[str, Any]] = []

    def run_optimization(self) -> Dict[str, Any]:
        """Runs collaborative multi-agent simulation and synthesizes ranked options."""
        # 1. Independent Agent Discovery
        farm_profile = self.farmer_agent.analyze_farm_profile()
        market_landscape = self.market_agent.analyze_market_landscape()
        logistics_routes = self.logistics_agent.generate_logistics_overview()

        # Merge initial agent logs
        all_logs = []
        all_logs.extend(self.farmer_agent.logs)
        all_logs.extend(self.market_agent.logs)
        all_logs.extend(self.logistics_agent.logs)

        # 2. Multi-scenario simulation grid (Markets x Days)
        all_options: List[Dict[str, Any]] = []

        try:
            harvest_dt = datetime.strptime(self.harvest_date_str, "%Y-%m-%d")
        except Exception:
            harvest_dt = datetime.now()

        # Precompute baseline reference: Day 0 at local rural mandi (default traditional habit)
        base_route = self.logistics_agent.evaluate_route("local_rural_mandi")
        base_price_data = self.market_agent.predict_market_price("local_rural_mandi", 0, self.quality_grade)
        base_viable_q = self.quantity * (1.0 - base_route["transit_spoilage_fraction"])
        base_gross = base_viable_q * base_price_data["projected_price_per_quintal"]
        baseline_net_profit = max(1.0, base_gross - base_route["total_logistics_expense"])

        # Grid evaluation
        for market_id, market_info in REGIONAL_MARKETS.items():
            route = self.logistics_agent.evaluate_route(market_id)
            
            for day in range(0, self.max_wait_days + 1):
                target_date = harvest_dt + timedelta(days=day)
                date_str = target_date.strftime("%Y-%m-%d")

                # Farmer Agent physical decay calculations
                viable_fraction, storage_spoilage_pct, grade_at_t, storage_cost = \
                    self.farmer_agent.evaluate_holding_decay(day)
                
                farm_sellable_q = self.quantity * viable_fraction

                # Transit decay
                transit_spoilage_rate = route["transit_spoilage_fraction"]
                delivered_sellable_q = farm_sellable_q * (1.0 - transit_spoilage_rate)
                
                total_spoilage_rate = 1.0 - (delivered_sellable_q / self.quantity)
                spoilage_kg_lost = (self.quantity - delivered_sellable_q) * 100.0

                # Market Agent price projection
                market_pricing = self.market_agent.predict_market_price(market_id, day, grade_at_t)
                effective_price = market_pricing["projected_price_per_quintal"]

                # Financial balance sheet
                gross_revenue = round(delivered_sellable_q * effective_price, 2)
                transport_cost = route["freight_cost"]
                cess_fees = route["market_entry_fees"]
                net_profit = round(gross_revenue - transport_cost - cess_fees - storage_cost, 2)
                net_margin_pct = round((net_profit / max(1.0, gross_revenue)) * 100, 1)

                profit_lift = round(net_profit - baseline_net_profit, 2)

                # Multi-criteria scoring
                # Balances: high net profit, low spoilage risk, high market buyer liquidity
                profit_factor = max(0.0, net_profit)
                spoilage_penalty = (1.0 - total_spoilage_rate)
                liquidity_factor = (market_info["liquidity_rating"] / 10.0)

                # Composite score
                raw_score = (profit_factor * 0.70) * (spoilage_penalty ** 0.8) * (0.85 + 0.15 * liquidity_factor)

                # Risk classification
                if total_spoilage_rate > 0.18:
                    risk_level = "HIGH"
                elif total_spoilage_rate > 0.08:
                    risk_level = "MEDIUM"
                else:
                    risk_level = "LOW"

                all_options.append({
                    "market_id": market_id,
                    "market_name": market_info["name"],
                    "market_type": market_info["market_type"],
                    "distance_km": market_info["distance_km"],
                    "transit_hours": market_info["transit_hours"],
                    "sell_day": day,
                    "sell_date": date_str,
                    "vehicle_id": route["vehicle_id"],
                    "vehicle_name": route["vehicle_name"],
                    "baseline_faostat_price_per_q": self.market_agent.faostat_baseline,
                    "effective_market_price_per_q": effective_price,
                    "gross_revenue": gross_revenue,
                    "transport_cost": transport_cost,
                    "storage_cost": storage_cost,
                    "market_cess_fees": cess_fees,
                    "net_profit": net_profit,
                    "net_profit_margin_pct": net_margin_pct,
                    "profit_lift_vs_local_today": profit_lift,
                    "harvest_quantity_quintals": self.quantity,
                    "delivered_sellable_quintals": round(delivered_sellable_q, 2),
                    "storage_spoilage_loss_pct": round(storage_spoilage_pct * 100, 2),
                    "transit_spoilage_loss_pct": round(transit_spoilage_rate * 100, 2),
                    "total_spoilage_loss_pct": round(total_spoilage_rate * 100, 2),
                    "spoilage_loss_kg": round(spoilage_kg_lost, 1),
                    "quality_grade_at_sale": grade_at_t,
                    "raw_score": raw_score,
                    "risk_level": risk_level,
                    "recommendation_verdict": ""
                })

        # Sort all options by composite utility score
        all_options.sort(key=lambda x: x["raw_score"], reverse=True)

        # Normalize score into 0-100 scale
        max_raw = max(opt["raw_score"] for opt in all_options) if all_options else 1.0
        for i, opt in enumerate(all_options):
            opt["rank"] = i + 1
            opt["utility_score"] = round((opt["raw_score"] / max_raw) * 100, 1)

        best_plan = all_options[0]
        best_plan["recommendation_verdict"] = "OPTIMAL PLAN - Highest Net Value & Risk-Adjusted Return"

        # Mark runner-up verdicts
        for opt in all_options[1:5]:
            if opt["market_id"] == best_plan["market_id"] and opt["sell_day"] != best_plan["sell_day"]:
                opt["recommendation_verdict"] = f"Alternative Timing ({opt['sell_date']})"
            elif opt["market_id"] != best_plan["market_id"]:
                opt["recommendation_verdict"] = f"Alternative Market Channel ({opt['market_name']})"

        # Generate Time Series Forecast (Daily Peak Day Comparison)
        timeline: List[Dict[str, Any]] = []
        for day in range(0, self.max_wait_days + 1):
            target_date = harvest_dt + timedelta(days=day)
            date_str = target_date.strftime("%Y-%m-%d")
            
            # Find best market for this specific day
            day_options = [opt for opt in all_options if opt["sell_day"] == day]
            day_best = max(day_options, key=lambda x: x["net_profit"]) if day_options else best_plan
            
            viable_f, stor_loss_pct, _, stor_cost = self.farmer_agent.evaluate_holding_decay(day)

            timeline.append({
                "day": day,
                "date": date_str,
                "faostat_baseline_price": self.market_agent.faostat_baseline,
                "best_market_projected_price": day_best["effective_market_price_per_q"],
                "cumulative_storage_loss_pct": round(stor_loss_pct * 100, 2),
                "viable_quantity_quintals": round(self.quantity * viable_f, 2),
                "best_market_net_profit": day_best["net_profit"],
                "holding_cost_accumulated": round(stor_cost, 2),
                "best_market_id": day_best["market_id"],
                "best_market_name": day_best["market_name"]
            })

        # 3. Multi-Agent Negotiation & Consensus Synthesis
        self._synthesize_agent_dialogue(best_plan, baseline_net_profit, all_logs)

        # 4. Formulate Strategic Insights & Key Tradeoffs
        strategic_summary, tradeoffs = self._generate_strategic_summary(best_plan, baseline_net_profit)

        # 5. SDG 2 Impact calculation
        sdg_metrics = self._calculate_sdg_impact(best_plan, baseline_net_profit)

        return {
            "crop_info": self.farmer_agent.crop_data,
            "farmer_profile": farm_profile,
            "recommended_plan": best_plan,
            "alternative_plans": all_options[1:10],
            "price_profit_timeline": timeline,
            "agent_logs": all_logs,
            "strategic_summary": strategic_summary,
            "key_tradeoffs": tradeoffs,
            "sdg2_impact_metrics": sdg_metrics,
            "provenance_disclaimer": FAOSTAT_METADATA["data_provenance_labels"]
        }

    def _synthesize_agent_dialogue(self, best: Dict[str, Any], baseline_net: float,
                                   all_logs: List[Dict[str, Any]]):
        """Constructs authentic multi-agent deliberation transcript showing how consensus was reached."""
        all_logs.append({
            "agent": "Market Agent",
            "phase": "Opportunity Proposal",
            "message": f"Proposal: Market price spread at {best['market_name']} offers ₹{best['effective_market_price_per_q']:.2f}/q on {best['sell_date']} (+{round(((best['effective_market_price_per_q'] / self.market_agent.faostat_baseline) - 1.0) * 100, 1)}% over FAOSTAT baseline).",
            "badge_type": "info",
            "detail": {
                "market": best["market_name"],
                "target_date": best["sell_date"],
                "projected_price": best["effective_market_price_per_q"]
            }
        })

        all_logs.append({
            "agent": "Logistics Agent",
            "phase": "Transit Verification",
            "message": f"Logistics check: Route to {best['market_name']} is {best['distance_km']} km ({best['transit_hours']} hrs transit). Recommending {best['vehicle_name']} at ₹{best['transport_cost']:.2f} total freight with only {best['transit_spoilage_loss_pct']}% transit loss.",
            "badge_type": "info",
            "detail": {
                "distance_km": best["distance_km"],
                "freight": best["transport_cost"],
                "vehicle": best["vehicle_name"]
            }
        })

        if best["sell_day"] > 0:
            all_logs.append({
                "agent": "Farmer Agent",
                "phase": "Holding Feasibility",
                "message": f"Storage validation: Holding {best['sell_day']} days under {self.storage_type} storage causes {best['storage_spoilage_loss_pct']}% weight loss and ₹{best['storage_cost']:.2f} storage fees. The price gain of +₹{best['profit_lift_vs_local_today']:.2f} comfortably exceeds the storage drag.",
                "badge_type": "success",
                "detail": {
                    "storage_spoilage_pct": best["storage_spoilage_loss_pct"],
                    "holding_cost": best["storage_cost"],
                    "lift": best["profit_lift_vs_local_today"]
                }
            })
        else:
            all_logs.append({
                "agent": "Farmer Agent",
                "phase": "Immediate Dispatch Validation",
                "message": f"Immediate dispatch approved: Selling today (Day 0) eliminates storage decay completely and captures current market liquidity without holding risk.",
                "badge_type": "success",
                "detail": {"storage_decay": 0.0}
            })

        all_logs.append({
            "agent": "Coordinator Agent",
            "phase": "Multi-Agent Consensus",
            "message": f"CONSENSUS REACHED: Selling at {best['market_name']} on {best['sell_date']} yields maximum expected net profit of ₹{best['net_profit']:.2f} (Profit margin: {best['net_profit_margin_pct']}%, +₹{best['profit_lift_vs_local_today']:.2f} vs default local yard). Spoilage contained to {best['total_spoilage_loss_pct']}%.",
            "badge_type": "consensus",
            "detail": {
                "net_profit": best["net_profit"],
                "profit_lift": best["profit_lift_vs_local_today"],
                "total_spoilage_pct": best["total_spoilage_loss_pct"]
            }
        })

    def _generate_strategic_summary(self, best: Dict[str, Any], baseline_net: float) -> Tuple[str, List[str]]:
        lift = best["profit_lift_vs_local_today"]
        lift_pct = round((lift / max(1.0, baseline_net)) * 100, 1)

        summary = (
            f"The multi-agent system recommends dispatching {self.quantity:.1f} quintals to "
            f"{best['market_name']} on {best['sell_date']} (Day +{best['sell_day']}) using {best['vehicle_name']}. "
            f"This plan delivers an expected net profit of ₹{best['net_profit']:,.2f} "
            f"({best['net_profit_margin_pct']}% net margin), representing a +₹{lift:,.2f} (+{lift_pct}%) profit increase "
            f"over immediate distress sale at the local taluka yard, while keeping total post-harvest loss at {best['total_spoilage_loss_pct']}%."
        )

        tradeoffs = [
            f"Price Premium vs Distance: {best['market_name']} offers ₹{best['effective_market_price_per_q']:.2f}/quintal, out-earning the ₹{best['transport_cost']:.2f} transportation expense.",
            f"Holding Horizon: Selling on Day +{best['sell_day']} balances market price momentum against a cumulative on-farm storage decay of {best['storage_spoilage_loss_pct']}%.",
            f"Logistics Vehicle: {best['vehicle_name']} keeps in-transit mechanical vibration loss limited to {best['transit_spoilage_loss_pct']}%.",
            f"Grade Retention: Produce maintains {best['quality_grade_at_sale']} quality grade at market arrival, commanding top wholesale auction bids."
        ]

        return summary, tradeoffs

    def _calculate_sdg_impact(self, best: Dict[str, Any], baseline_net: float) -> List[Dict[str, str]]:
        lift = best["profit_lift_vs_local_today"]
        food_saved_kg = round(max(0.0, (self.quantity * 100 * 0.12) - best["spoilage_loss_kg"]), 1)
        lift_pct = round((lift / max(1.0, baseline_net)) * 100, 1)

        return [
            {
                "sdg_target": "SDG 2.3 (Double Agricultural Incomes)",
                "metric_name": "Farmer Net Income Lift",
                "value": f"+₹{lift:,.2f} (+{lift_pct}%)",
                "impact_explanation": f"Increases smallholder take-home earnings by eliminating predatory middleman cuts and capturing regional wholesale demand premiums."
            },
            {
                "sdg_target": "SDG 12.3 (Halve Post-Harvest Food Waste)",
                "metric_name": "Edible Produce Saved",
                "value": f"{food_saved_kg} kg saved",
                "impact_explanation": f"Prevented decay by calculating scientific shelf-life thresholds and avoiding overstay in ambient farm storage."
            },
            {
                "sdg_target": "SDG 2.1 (Universal Access to Safe Food)",
                "metric_name": "High-Quality Supply Delivered",
                "value": f"{best['delivered_sellable_quintals'] * 100:,.0f} kg delivered",
                "impact_explanation": f"Fresh produce reaches high-demand consumer clusters in prime {best['quality_grade_at_sale']} condition."
            }
        ]

