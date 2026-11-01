"""
Market Agent: Evaluates historical FAOSTAT producer prices, market price spreads,
day-to-day wholesale arrival dynamics, and grade-based price premiums across regional mandis.
"""

from typing import Dict, Any, List
import math
from datetime import datetime, timedelta
from app.data.faostat_data import get_crop_detail, FAOSTAT_METADATA
from app.data.markets_data import get_market_list, REGIONAL_MARKETS


class MarketAgent:
    def __init__(self, crop_id: str, harvest_date_str: str):
        self.crop_id = crop_id
        self.harvest_date_str = harvest_date_str
        self.crop_data = get_crop_detail(crop_id)
        self.markets = get_market_list()
        self.logs: List[Dict[str, Any]] = []

        try:
            self.harvest_date = datetime.strptime(harvest_date_str, "%Y-%m-%d")
        except Exception:
            self.harvest_date = datetime.now()

        self.current_month_index = self.harvest_date.month - 1
        self.seasonality_factor = self.crop_data["seasonality_index"][self.current_month_index]
        self.faostat_baseline = self.crop_data["baseline_price_per_quintal"]

    def analyze_market_landscape(self) -> Dict[str, Any]:
        """Provides macro and micro market intelligence across regional trading hubs."""
        self.logs.append({
            "agent": "Market Agent",
            "phase": "FAOSTAT Baseline Ingestion",
            "message": f"Retrieved FAOSTAT Producer Price baseline for {self.crop_data['name']} (FAO #{self.crop_data['fao_item_code']}): ₹{self.faostat_baseline:.2f}/quintal with monthly seasonality factor {self.seasonality_factor:.2f}.",
            "badge_type": "info",
            "detail": {
                "source": FAOSTAT_METADATA["source_name"],
                "domain": FAOSTAT_METADATA["domain"],
                "fao_item_code": self.crop_data["fao_item_code"],
                "baseline_usd_equivalent": round(self.faostat_baseline / 84.0, 2),
                "seasonality_factor": self.seasonality_factor
            }
        })

        # Evaluate wholesale spreads
        spread_summary = []
        highest_spread_market = None
        max_multiplier = 0.0

        for market in self.markets:
            effective_base = self.faostat_baseline * self.seasonality_factor * market["price_spread_multiplier"]
            spread_summary.append({
                "market_id": market["id"],
                "market_name": market["name"],
                "market_type": market["market_type"],
                "distance_km": market["distance_km"],
                "price_spread_pct": round((market["price_spread_multiplier"] - 1.0) * 100, 1),
                "estimated_base_price_per_q": round(effective_base, 2),
                "liquidity_rating": market["liquidity_rating"],
                "provenance": market["provenance"]
            })
            if market["price_spread_multiplier"] > max_multiplier:
                max_multiplier = market["price_spread_multiplier"]
                highest_spread_market = market["name"]

        self.logs.append({
            "agent": "Market Agent",
            "phase": "Wholesale Price Mapping",
            "message": f"Screened {len(self.markets)} regional markets. Highest price spread found at {highest_spread_market} (+{round((max_multiplier - 1.0) * 100, 1)}% over baseline).",
            "badge_type": "success",
            "detail": {"markets_screened": len(self.markets)}
        })

        return {
            "faostat_baseline_price": self.faostat_baseline,
            "seasonality_factor": self.seasonality_factor,
            "markets_summary": spread_summary
        }

    def predict_market_price(self, market_id: str, day_offset: int, grade: str) -> Dict[str, Any]:
        """
        Projects wholesale price for a specific market, future day, and quality grade.
        Incorporates cyclical day-of-week demand and short-term supply momentum.
        """
        market = REGIONAL_MARKETS[market_id]
        base_rate = self.faostat_baseline * self.seasonality_factor * market["price_spread_multiplier"]

        # Calculate calendar day
        target_date = self.harvest_date + timedelta(days=day_offset)
        weekday = target_date.weekday()  # 0=Monday, 5=Saturday, 6=Sunday

        # Modeled short-term market dynamics:
        # Weekend consumer demand surge in metro terminal markets (Fri/Sat/Sun)
        # Mid-week glut in local rural markets (Tue/Wed)
        daily_variation = 0.0
        if market_id == "metro_terminal_market":
            # Weekend retail replenishment surge
            if weekday in (4, 5, 6):
                daily_variation += 0.065
            # Upward price drift if holding towards peak day (+2 to +4)
            daily_variation += 0.015 * min(day_offset, 4) - 0.008 * max(0, day_offset - 4)
        elif market_id == "district_apmc_hub":
            # Bi-weekly auction cycle peak on Monday & Thursday
            if weekday in (0, 3):
                daily_variation += 0.04
            daily_variation += 0.010 * min(day_offset, 3) - 0.005 * max(0, day_offset - 3)
        elif market_id == "agro_processing_cluster":
            # Contract price is stable with small volume incentive
            daily_variation += 0.005 * min(day_offset, 5)
        else:
            # Local yard fluctuation
            daily_variation += 0.01 * math.sin(day_offset * 1.2)

        # Grade multiplier
        grade_multiplier = market["grade_sensitivity"].get(grade, 1.0)
        
        projected_price = round(base_rate * (1.0 + daily_variation) * grade_multiplier, 2)

        return {
            "market_id": market_id,
            "market_name": market["name"],
            "day_offset": day_offset,
            "target_date_str": target_date.strftime("%Y-%m-%d"),
            "target_weekday": target_date.strftime("%A"),
            "grade": grade,
            "base_faostat_anchor": self.faostat_baseline,
            "projected_price_per_quintal": projected_price,
            "price_delta_pct_vs_faostat": round(((projected_price / self.faostat_baseline) - 1.0) * 100, 1),
            "provenance": "SYNTHETIC_LOCAL_MARKET (Anchored on FAOSTAT)"
        }

