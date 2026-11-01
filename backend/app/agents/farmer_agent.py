"""
Farmer Agent: Analyzes crop characteristics, post-harvest perishability decay curves,
storage conditions, holding costs, and on-farm quality preservation.
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
from app.data.faostat_data import get_crop_detail


class FarmerAgent:
    def __init__(self, crop_id: str, quantity_quintals: float, harvest_date_str: str,
                 quality_grade: str, storage_type: str, farmer_location: str):
        self.crop_id = crop_id
        self.quantity = float(quantity_quintals)
        self.harvest_date_str = harvest_date_str
        self.quality_grade = quality_grade
        self.storage_type = storage_type
        self.farmer_location = farmer_location
        
        self.crop_data = get_crop_detail(crop_id)
        self.storage_profiles = self.crop_data["storage_profiles"]
        if storage_type not in self.storage_profiles:
            self.storage_type = "ambient"
            
        self.active_storage = self.storage_profiles[self.storage_type]
        self.logs: List[Dict[str, Any]] = []

    def analyze_farm_profile(self) -> Dict[str, Any]:
        """Initial assessment of the farmer's crop condition and shelf-life capacity."""
        decay_factor = self.active_storage["decay_factor"]
        effective_daily_decay = self.crop_data["daily_spoilage_rate_ambient"] * decay_factor
        ambient_shelf_life = self.crop_data["shelf_life_days_ambient"]
        extended_shelf_life = round(ambient_shelf_life / max(0.08, decay_factor), 1)
        
        # Determine risk level
        if self.crop_data["perishability_class"] == "HIGH":
            if self.storage_type == "ambient":
                risk_level = "CRITICAL"
                storage_advice = "Ambient storage will cause severe spoilage within 4-6 days. Urgent sale or refrigerated transit recommended."
            elif self.storage_type == "ventilated":
                risk_level = "MODERATE"
                storage_advice = "Ventilated structure provides ~2-3 days safety window for price peak waiting."
            else:
                risk_level = "LOW"
                storage_advice = "Cold storage provides extended holding window up to 2-3 weeks."
        elif self.crop_data["perishability_class"] == "MEDIUM":
            risk_level = "MODERATE" if self.storage_type == "ambient" else "LOW"
            storage_advice = "Tubers/bulbs have moderate resilience. Can hold for favorable price surges."
        else:
            risk_level = "LOW"
            storage_advice = "Dry grains can be safely stored. Focus on market price cycles rather than spoilage."

        self.logs.append({
            "agent": "Farmer Agent",
            "phase": "Harvest Assessment",
            "message": f"Assessed {self.quantity:.1f} quintals of {self.crop_data['name']} ({self.quality_grade}) stored under {self.active_storage['name']}.",
            "badge_type": "info",
            "detail": {
                "perishability": self.crop_data["perishability_class"],
                "effective_daily_decay_pct": round(effective_daily_decay * 100, 2),
                "safe_shelf_life_days": extended_shelf_life,
                "holding_cost_per_day": round(self.active_storage["cost_per_quintal_day"] * self.quantity, 2)
            }
        })
        
        if risk_level == "CRITICAL":
            self.logs.append({
                "agent": "Farmer Agent",
                "phase": "Storage Alert",
                "message": f"WARNING: {self.crop_data['name']} has high metabolic decay ({round(effective_daily_decay * 100, 1)}%/day). Holding beyond 2 days requires high price premium to offset losses.",
                "badge_type": "alert",
                "detail": {"advice": storage_advice}
            })

        return {
            "crop_id": self.crop_id,
            "crop_name": self.crop_data["name"],
            "scientific_name": self.crop_data["scientific_name"],
            "quantity_quintals": self.quantity,
            "quantity_kg": self.quantity * 100,
            "harvest_date": self.harvest_date_str,
            "initial_quality_grade": self.quality_grade,
            "farmer_location": self.farmer_location,
            "storage_type": self.storage_type,
            "storage_name": self.active_storage["name"],
            "storage_cost_per_quintal_day": self.active_storage["cost_per_quintal_day"],
            "holding_cost_per_day": round(self.active_storage["cost_per_quintal_day"] * self.quantity, 2),
            "effective_daily_spoilage_rate": effective_daily_decay,
            "estimated_safe_shelf_life_days": extended_shelf_life,
            "perishability_class": self.crop_data["perishability_class"],
            "risk_level": risk_level,
            "storage_advice": storage_advice
        }

    def evaluate_holding_decay(self, day: int) -> Tuple[float, float, str, float]:
        """
        Calculates for holding day t:
        - viable_fraction (1.0 - cumulative_spoilage)
        - storage_spoilage_loss_pct
        - effective_grade_at_day_t
        - accumulated_storage_cost
        """
        decay_factor = self.active_storage["decay_factor"]
        base_daily_decay = self.crop_data["daily_spoilage_rate_ambient"]
        effective_daily = base_daily_decay * decay_factor
        
        # Compound decay model with accelerated inflection past baseline shelf life
        ambient_shelf_life = self.crop_data["shelf_life_days_ambient"]
        safe_life = ambient_shelf_life / max(0.08, decay_factor)
        
        if day == 0:
            cumulative_spoilage_pct = 0.0
            viable_fraction = 1.0
            grade = self.quality_grade
        else:
            # Linear decay during safe life, accelerating if exceeded
            if day <= safe_life:
                cumulative_spoilage_pct = min(0.40, effective_daily * day * (1.0 + 0.04 * day))
            else:
                overstay_days = day - safe_life
                base_loss = effective_daily * safe_life
                accelerated_loss = overstay_days * (effective_daily * 2.8)
                cumulative_spoilage_pct = min(0.85, base_loss + accelerated_loss)
            
            viable_fraction = max(0.15, 1.0 - cumulative_spoilage_pct)
            
            # Quality grade degradation over time
            grade = self.quality_grade
            if self.storage_type == "ambient":
                if day >= 3 and grade == "Grade A":
                    grade = "Grade B"
                elif day >= 6 and grade == "Grade B":
                    grade = "Grade C"
            elif self.storage_type == "ventilated":
                if day >= 6 and grade == "Grade A":
                    grade = "Grade B"

        accumulated_holding_cost = self.active_storage["cost_per_quintal_day"] * self.quantity * day
        
        return viable_fraction, cumulative_spoilage_pct, grade, accumulated_holding_cost

