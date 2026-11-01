"""
Pydantic Schemas for Request & Response Data Models
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class OptimizeRequest(BaseModel):
    crop_id: str = Field(..., description="Crop identifier, e.g., 'tomatoes', 'potatoes'")
    quantity_quintals: float = Field(..., gt=0, description="Harvest quantity in quintals (1 quintal = 100 kg)")
    harvest_date: str = Field(default="2026-10-29", description="Harvest date YYYY-MM-DD")
    quality_grade: str = Field(default="Grade B", description="Harvest quality: 'Grade A', 'Grade B', or 'Grade C'")
    farmer_location: str = Field(default="Rural Farm Cluster (Zone 4)", description="Origin location of the farmer")
    storage_type: str = Field(default="ambient", description="'ambient', 'ventilated', 'hermetic_bag', 'cold_storage'")
    max_wait_days: int = Field(default=7, ge=0, le=14, description="Maximum planning horizon in days (0-14)")
    preferred_vehicle: Optional[str] = Field(default=None, description="Optional forced vehicle selection")
    fuel_price_modifier: float = Field(default=1.0, ge=0.5, le=2.0, description="Multiplier for fuel/transport costs (1.0 = normal)")


class SimulationRequest(BaseModel):
    base_request: OptimizeRequest
    simulated_wait_day: int = Field(default=0, ge=0, le=14, description="Specific day to simulate (0 = today)")
    simulated_storage_type: Optional[str] = Field(default=None, description="Alternative storage to test")
    fuel_price_shock_pct: float = Field(default=0.0, description="Fuel cost increase/decrease percentage e.g. +20%")
    market_price_shock_pct: float = Field(default=0.0, description="Market price shock percentage e.g. -10%")


class AgentLog(BaseModel):
    agent: str
    phase: str
    message: str
    badge_type: str  # "info", "warning", "success", "alert", "consensus"
    detail: Optional[Dict[str, Any]] = None


class RankedMarketPlan(BaseModel):
    rank: int
    market_id: str
    market_name: str
    market_type: str
    distance_km: float
    transit_hours: float
    sell_day: int
    sell_date: str
    vehicle_id: str
    vehicle_name: str
    
    # Financial breakdown
    baseline_faostat_price_per_q: float
    effective_market_price_per_q: float
    gross_revenue: float
    transport_cost: float
    storage_cost: float
    market_cess_fees: float
    net_profit: float
    net_profit_margin_pct: float
    profit_lift_vs_local_today: float
    
    # Post-harvest & physical metrics
    harvest_quantity_quintals: float
    delivered_sellable_quintals: float
    storage_spoilage_loss_pct: float
    transit_spoilage_loss_pct: float
    total_spoilage_loss_pct: float
    spoilage_loss_kg: float
    quality_grade_at_sale: str
    
    # Multi-agent scoring
    utility_score: float
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    recommendation_verdict: str


class ForecastPoint(BaseModel):
    day: int
    date: str
    faostat_baseline_price: float
    best_market_projected_price: float
    cumulative_storage_loss_pct: float
    viable_quantity_quintals: float
    best_market_net_profit: float
    holding_cost_accumulated: float
    best_market_id: str
    best_market_name: str


class SdgImpactMetric(BaseModel):
    sdg_target: str
    metric_name: str
    value: str
    impact_explanation: str


class OptimizationResponse(BaseModel):
    crop_info: Dict[str, Any]
    farmer_profile: Dict[str, Any]
    recommended_plan: RankedMarketPlan
    alternative_plans: List[RankedMarketPlan]
    price_profit_timeline: List[ForecastPoint]
    agent_logs: List[AgentLog]
    strategic_summary: str
    key_tradeoffs: List[str]
    sdg2_impact_metrics: List[SdgImpactMetric]
    provenance_disclaimer: Dict[str, str]

