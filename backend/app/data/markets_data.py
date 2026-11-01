"""
Wholesale Agricultural Markets & Mandis Benchmark Data
Provenance: SYNTHETIC_LOCAL_MARKET
Calibrated against real-world APMC Mandi structures, wholesale terminal price spreads,
and local buyer dynamics relative to FAOSTAT producer price baselines.
"""

from typing import Dict, Any, List

REGIONAL_MARKETS: Dict[str, Dict[str, Any]] = {
    "local_rural_mandi": {
        "id": "local_rural_mandi",
        "name": "Local Taluka Mandi Yard",
        "market_type": "Rural Primary Market (Panchayat Yard)",
        "distance_km": 14.0,
        "transit_hours": 0.8,
        "base_handling_fee_per_quintal": 22.0,
        "entry_cess_rate": 0.008,  # 0.8% cess
        "buyer_competition_level": "LOW",
        "price_spread_multiplier": 0.91,  # Tends to trade 9% below national baseline due to middlemen
        "daily_volume_capacity_quintals": 800,
        "liquidity_rating": 7.2,
        "description": "Closest local sub-yard. Minimum transit risk, but buyer pool is limited and price realization is lower.",
        "grade_sensitivity": {
            "Grade A": 1.08,
            "Grade B": 1.00,
            "Grade C": 0.85
        },
        "provenance": "SYNTHETIC_LOCAL_MARKET"
    },
    "district_apmc_hub": {
        "id": "district_apmc_hub",
        "name": "District Central APMC Market",
        "market_type": "Principal APMC Mandi Yard",
        "distance_km": 48.0,
        "transit_hours": 1.8,
        "base_handling_fee_per_quintal": 35.0,
        "entry_cess_rate": 0.012,  # 1.2% mandi tax
        "buyer_competition_level": "HIGH",
        "price_spread_multiplier": 1.05,  # 5% above baseline due to competitive open outcry / e-NAM
        "daily_volume_capacity_quintals": 5500,
        "liquidity_rating": 9.2,
        "description": "Major district trading hub. Active commission agents, high daily clearance, competitive prices.",
        "grade_sensitivity": {
            "Grade A": 1.15,
            "Grade B": 1.00,
            "Grade C": 0.80
        },
        "provenance": "SYNTHETIC_LOCAL_MARKET"
    },
    "metro_terminal_market": {
        "id": "metro_terminal_market",
        "name": "Metro Mega Wholesale Terminal",
        "market_type": "Metropolitan Consumption Terminal",
        "distance_km": 145.0,
        "transit_hours": 4.5,
        "base_handling_fee_per_quintal": 52.0,
        "entry_cess_rate": 0.018,  # 1.8% municipal cess
        "buyer_competition_level": "VERY_HIGH",
        "price_spread_multiplier": 1.22,  # 22% premium due to high urban retail purchasing power
        "daily_volume_capacity_quintals": 18000,
        "liquidity_rating": 9.8,
        "description": "State capital mega-market. Massive retail/supermarket buyer presence; top prices for Grade A produce.",
        "grade_sensitivity": {
            "Grade A": 1.25,
            "Grade B": 1.02,
            "Grade C": 0.75  # Heavy penalty for low grade due to high consumer standards
        },
        "provenance": "SYNTHETIC_LOCAL_MARKET"
    },
    "agro_processing_cluster": {
        "id": "agro_processing_cluster",
        "name": "Agro-Processing & Cold-Chain Hub",
        "market_type": "Industrial Food Processor / Aggregator",
        "distance_km": 78.0,
        "transit_hours": 2.5,
        "base_handling_fee_per_quintal": 28.0,
        "entry_cess_rate": 0.005,  # Direct factory gate 0.5%
        "buyer_competition_level": "MEDIUM",
        "price_spread_multiplier": 1.11,  # 11% premium with contracted stable off-take
        "daily_volume_capacity_quintals": 3500,
        "liquidity_rating": 8.5,
        "description": "Food processing plants (sauce, flakes, milling). Predictable price contracts, fast automated weighing.",
        "grade_sensitivity": {
            "Grade A": 1.12,
            "Grade B": 1.02,
            "Grade C": 0.88  # Better absorption of Grade B/C for pulping/flaking than retail
        },
        "provenance": "SYNTHETIC_LOCAL_MARKET"
    },
    "fpo_collective_center": {
        "id": "fpo_collective_center",
        "name": "FPO Cooperative Aggregation Center",
        "market_type": "Farmer Producer Organization Hub",
        "distance_km": 26.0,
        "transit_hours": 1.1,
        "base_handling_fee_per_quintal": 18.0,
        "entry_cess_rate": 0.0,  # FPO member exempt
        "buyer_competition_level": "MEDIUM",
        "price_spread_multiplier": 1.02,  # 2% above baseline + shared logistics rebate
        "daily_volume_capacity_quintals": 1200,
        "liquidity_rating": 8.0,
        "description": "Local farmer producer cooperative. Shared vehicle booking, zero mandi taxes, digital direct payment.",
        "grade_sensitivity": {
            "Grade A": 1.14,
            "Grade B": 1.00,
            "Grade C": 0.84
        },
        "provenance": "SYNTHETIC_LOCAL_MARKET"
    }
}


def get_market_list() -> List[Dict[str, Any]]:
    """Returns list of all modeled wholesale markets."""
    return list(REGIONAL_MARKETS.values())


def get_market_by_id(market_id: str) -> Dict[str, Any]:
    """Returns details for a specific market."""
    if market_id not in REGIONAL_MARKETS:
        raise KeyError(f"Market {market_id} not found")
    return REGIONAL_MARKETS[market_id]

