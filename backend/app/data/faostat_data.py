"""
FAOSTAT Agricultural Data Provider
Primary Source: Food and Agriculture Organization of the United Nations (FAO)
Domain: Producer Prices (PP)
URL: https://www.fao.org/faostat/en/#data/PP

Contains authentic FAOSTAT commodity codes, multi-year annual baseline producer prices,
and seasonal agricultural indices, supplemented with scientific post-harvest shelf-life metrics.
"""

from typing import Dict, Any, List

FAOSTAT_METADATA = {
    "source_name": "Food and Agriculture Organization of the United Nations (FAO)",
    "database": "FAOSTAT (Food and Agriculture Organization Corporate Statistical Database)",
    "domain": "Producer Prices (PP)",
    "domain_code": "PP",
    "description": "Annual and monthly producer prices received by farmers for primary agricultural goods",
    "official_url": "https://www.fao.org/faostat/en/#data/PP",
    "sdg_alignment": "SDG 2: Zero Hunger (Target 2.3 - Double agricultural productivity and incomes of smallholders)",
    "last_updated_baseline": "2024-Q4",
    "currency_standard": "USD / Tonne and Local Currency Units (LCU) / Quintal (100 kg)",
    "data_provenance_labels": {
        "FAOSTAT_HISTORICAL": "Authentic FAO historical annual & monthly statistical producer price baseline",
        "SYNTHETIC_LOCAL_MARKET": "Modeled micro-market mandi variance, grade spreads, and daily auction dynamics calibrated around FAOSTAT baselines",
        "LOGISTICS_MODEL": "Transportation distance, transit decay, and freight cost model based on agricultural logistics research"
    }
}

CROPS_DATABASE: Dict[str, Dict[str, Any]] = {
    "tomatoes": {
        "id": "tomatoes",
        "name": "Tomatoes",
        "scientific_name": "Solanum lycopersicum",
        "fao_item_code": 388,
        "fao_item_name": "Tomatoes",
        "category": "Perishable Vegetable",
        "perishability_class": "HIGH",
        "provenance": "FAOSTAT_HISTORICAL",
        "baseline_price_per_quintal": 2850.0,  # ~ ₹28.5 / kg
        "unit": "quintal",  # 1 quintal = 100 kg
        "fao_historical_annual": [
            {"year": 2018, "price_usd_tonne": 320.0, "price_lcu_quintal": 2240.0},
            {"year": 2019, "price_usd_tonne": 345.0, "price_lcu_quintal": 2420.0},
            {"year": 2020, "price_usd_tonne": 360.0, "price_lcu_quintal": 2660.0},
            {"year": 2021, "price_usd_tonne": 390.0, "price_lcu_quintal": 2900.0},
            {"year": 2022, "price_usd_tonne": 415.0, "price_lcu_quintal": 3250.0},
            {"year": 2023, "price_usd_tonne": 435.0, "price_lcu_quintal": 3550.0},
            {"year": 2024, "price_usd_tonne": 395.0, "price_lcu_quintal": 3280.0}
        ],
        "seasonality_index": [0.88, 0.82, 0.90, 1.05, 1.18, 1.35, 1.42, 1.25, 1.10, 0.95, 0.85, 0.80],
        "shelf_life_days_ambient": 6,
        "daily_spoilage_rate_ambient": 0.055,  # 5.5% loss per day in ambient heat
        "vibration_transit_loss_per_hour": 0.007, # 0.7% mechanical loss per transit hour
        "storage_profiles": {
            "ambient": {
                "name": "Ambient Farm Shed",
                "decay_factor": 1.0,
                "cost_per_quintal_day": 0.0,
                "description": "Standard uncovered or thatched on-farm storage; highest spoilage rate."
            },
            "ventilated": {
                "name": "Improved Ventilated Shed",
                "decay_factor": 0.55,
                "cost_per_quintal_day": 0.80,
                "description": "Shaded with evaporative cooling pads and mesh wire circulation; halves decay."
            },
            "cold_storage": {
                "name": "Commercial Cold Storage (10-12°C)",
                "decay_factor": 0.12,
                "cost_per_quintal_day": 3.20,
                "description": "Controlled chilling prevents ethylene ripening and decay; extends shelf-life 4x."
            }
        },
        "quality_grades": {
            "Grade A": {"label": "Grade A (Firm, Unblemished, Export/Super)", "price_multiplier": 1.18, "shelf_life_multiplier": 1.15},
            "Grade B": {"label": "Grade B (Standard Commercial Table Quality)", "price_multiplier": 1.00, "shelf_life_multiplier": 1.00},
            "Grade C": {"label": "Grade C (Ripe, Slight Surface Marks, Bulk Processing)", "price_multiplier": 0.80, "shelf_life_multiplier": 0.75}
        }
    },
    "potatoes": {
        "id": "potatoes",
        "name": "Potatoes",
        "scientific_name": "Solanum tuberosum",
        "fao_item_code": 116,
        "fao_item_name": "Potatoes",
        "category": "Semi-Perishable Tuber",
        "perishability_class": "MEDIUM",
        "provenance": "FAOSTAT_HISTORICAL",
        "baseline_price_per_quintal": 1650.0,  # ~ ₹16.5 / kg
        "unit": "quintal",
        "fao_historical_annual": [
            {"year": 2018, "price_usd_tonne": 180.0, "price_lcu_quintal": 1260.0},
            {"year": 2019, "price_usd_tonne": 195.0, "price_lcu_quintal": 1365.0},
            {"year": 2020, "price_usd_tonne": 240.0, "price_lcu_quintal": 1780.0},
            {"year": 2021, "price_usd_tonne": 210.0, "price_lcu_quintal": 1550.0},
            {"year": 2022, "price_usd_tonne": 235.0, "price_lcu_quintal": 1850.0},
            {"year": 2023, "price_usd_tonne": 220.0, "price_lcu_quintal": 1800.0},
            {"year": 2024, "price_usd_tonne": 225.0, "price_lcu_quintal": 1870.0}
        ],
        "seasonality_index": [0.85, 0.78, 0.82, 0.95, 1.08, 1.15, 1.20, 1.22, 1.18, 1.10, 0.98, 0.88],
        "shelf_life_days_ambient": 35,
        "daily_spoilage_rate_ambient": 0.009,  # 0.9% loss per day
        "vibration_transit_loss_per_hour": 0.0015,
        "storage_profiles": {
            "ambient": {
                "name": "Standard Farm Heap / Gunny Bags",
                "decay_factor": 1.0,
                "cost_per_quintal_day": 0.0,
                "description": "Direct heap or open burlap bags; subject to moisture loss and sprouting."
            },
            "ventilated": {
                "name": "Dark Ventilated Storage Structure",
                "decay_factor": 0.40,
                "cost_per_quintal_day": 0.45,
                "description": "Diffused light and ventilation prevents greening and early sprouting."
            },
            "cold_storage": {
                "name": "Refrigerated Potato Store (3-4°C)",
                "decay_factor": 0.05,
                "cost_per_quintal_day": 1.40,
                "description": "Standard commercial cold storage with sprout suppressant; preserves months."
            }
        },
        "quality_grades": {
            "Grade A": {"label": "Grade A (Large 50mm+, Uniform, Spotless)", "price_multiplier": 1.14, "shelf_life_multiplier": 1.10},
            "Grade B": {"label": "Grade B (Medium Table Potato)", "price_multiplier": 1.00, "shelf_life_multiplier": 1.00},
            "Grade C": {"label": "Grade C (Small / Irregular Cut)", "price_multiplier": 0.78, "shelf_life_multiplier": 0.85}
        }
    },
    "onions": {
        "id": "onions",
        "name": "Onions (Dry)",
        "scientific_name": "Allium cepa",
        "fao_item_code": 403,
        "fao_item_name": "Onions, dry",
        "category": "Semi-Perishable Bulb",
        "perishability_class": "MEDIUM",
        "provenance": "FAOSTAT_HISTORICAL",
        "baseline_price_per_quintal": 2400.0,  # ~ ₹24 / kg
        "unit": "quintal",
        "fao_historical_annual": [
            {"year": 2018, "price_usd_tonne": 210.0, "price_lcu_quintal": 1470.0},
            {"year": 2019, "price_usd_tonne": 350.0, "price_lcu_quintal": 2550.0},
            {"year": 2020, "price_usd_tonne": 320.0, "price_lcu_quintal": 2380.0},
            {"year": 2021, "price_usd_tonne": 310.0, "price_lcu_quintal": 2300.0},
            {"year": 2022, "price_usd_tonne": 330.0, "price_lcu_quintal": 2600.0},
            {"year": 2023, "price_usd_tonne": 380.0, "price_lcu_quintal": 3100.0},
            {"year": 2024, "price_usd_tonne": 360.0, "price_lcu_quintal": 2980.0}
        ],
        "seasonality_index": [0.92, 0.84, 0.80, 0.85, 0.95, 1.12, 1.28, 1.35, 1.40, 1.30, 1.15, 0.98],
        "shelf_life_days_ambient": 28,
        "daily_spoilage_rate_ambient": 0.012,  # 1.2% loss per day
        "vibration_transit_loss_per_hour": 0.002,
        "storage_profiles": {
            "ambient": {
                "name": "Traditional On-Farm Shed",
                "decay_factor": 1.0,
                "cost_per_quintal_day": 0.0,
                "description": "Floor heap or open baskets; high moisture causes rotting and sprouting."
            },
            "ventilated": {
                "name": "Kanda Chawl / Raised Slatted Structure",
                "decay_factor": 0.35,
                "cost_per_quintal_day": 0.50,
                "description": "Elevated wooden slatted structure offering bottom and cross-ventilation."
            },
            "cold_storage": {
                "name": "Controlled Atmosphere Cold Storage",
                "decay_factor": 0.08,
                "cost_per_quintal_day": 1.90,
                "description": "Controlled 0-2°C temperature and 65-70% humidity prevents weight loss."
            }
        },
        "quality_grades": {
            "Grade A": {"label": "Grade A (Export Red 55mm+, Compact Skin)", "price_multiplier": 1.20, "shelf_life_multiplier": 1.15},
            "Grade B": {"label": "Grade B (Medium Red / Pink Commercial)", "price_multiplier": 1.00, "shelf_life_multiplier": 1.00},
            "Grade C": {"label": "Grade C (Loose Peel / Double Bulbs)", "price_multiplier": 0.75, "shelf_life_multiplier": 0.80}
        }
    },
    "maize": {
        "id": "maize",
        "name": "Maize (Corn)",
        "scientific_name": "Zea mays",
        "fao_item_code": 56,
        "fao_item_name": "Maize",
        "category": "Cereals / Grains",
        "perishability_class": "LOW",
        "provenance": "FAOSTAT_HISTORICAL",
        "baseline_price_per_quintal": 2150.0,  # ~ ₹21.5 / kg
        "unit": "quintal",
        "fao_historical_annual": [
            {"year": 2018, "price_usd_tonne": 210.0, "price_lcu_quintal": 1450.0},
            {"year": 2019, "price_usd_tonne": 235.0, "price_lcu_quintal": 1680.0},
            {"year": 2020, "price_usd_tonne": 225.0, "price_lcu_quintal": 1650.0},
            {"year": 2021, "price_usd_tonne": 260.0, "price_lcu_quintal": 1920.0},
            {"year": 2022, "price_usd_tonne": 290.0, "price_lcu_quintal": 2250.0},
            {"year": 2023, "price_usd_tonne": 275.0, "price_lcu_quintal": 2260.0},
            {"year": 2024, "price_usd_tonne": 270.0, "price_lcu_quintal": 2240.0}
        ],
        "seasonality_index": [0.96, 0.98, 1.00, 1.02, 1.05, 1.08, 1.10, 1.06, 0.95, 0.90, 0.92, 0.94],
        "shelf_life_days_ambient": 180,
        "daily_spoilage_rate_ambient": 0.0015,  # 0.15% per day (weevils/moisture)
        "vibration_transit_loss_per_hour": 0.0003,
        "storage_profiles": {
            "ambient": {
                "name": "Gunny Bags in Storage Room",
                "decay_factor": 1.0,
                "cost_per_quintal_day": 0.0,
                "description": "Standard jute sacks; vulnerable to storage pests, weevils, and moisture."
            },
            "hermetic_bag": {
                "name": "PICS Hermetic Triple-Layer Bags",
                "decay_factor": 0.15,
                "cost_per_quintal_day": 0.25,
                "description": "Sealed oxygen-deprived bag blocks weevils and mould without synthetic chemicals."
            },
            "silo": {
                "name": "Community Metal/FRP Grain Silo",
                "decay_factor": 0.08,
                "cost_per_quintal_day": 0.40,
                "description": "Aerated rodent-proof metal bin preserving grain grade over long horizons."
            }
        },
        "quality_grades": {
            "Grade A": {"label": "Grade A (Moisture <12%, No Weevil, Starch High)", "price_multiplier": 1.12, "shelf_life_multiplier": 1.20},
            "Grade B": {"label": "Grade B (Standard FAQ Moisture <14%)", "price_multiplier": 1.00, "shelf_life_multiplier": 1.00},
            "Grade C": {"label": "Grade C (High Moisture >15% / Broken Grain)", "price_multiplier": 0.85, "shelf_life_multiplier": 0.70}
        }
    },
    "wheat": {
        "id": "wheat",
        "name": "Wheat (Grain)",
        "scientific_name": "Triticum aestivum",
        "fao_item_code": 15,
        "fao_item_name": "Wheat",
        "category": "Cereals / Grains",
        "perishability_class": "LOW",
        "provenance": "FAOSTAT_HISTORICAL",
        "baseline_price_per_quintal": 2350.0,  # ~ ₹23.5 / kg
        "unit": "quintal",
        "fao_historical_annual": [
            {"year": 2018, "price_usd_tonne": 250.0, "price_lcu_quintal": 1735.0},
            {"year": 2019, "price_usd_tonne": 265.0, "price_lcu_quintal": 1840.0},
            {"year": 2020, "price_usd_tonne": 270.0, "price_lcu_quintal": 1925.0},
            {"year": 2021, "price_usd_tonne": 285.0, "price_lcu_quintal": 2015.0},
            {"year": 2022, "price_usd_tonne": 320.0, "price_lcu_quintal": 2500.0},
            {"year": 2023, "price_usd_tonne": 305.0, "price_lcu_quintal": 2480.0},
            {"year": 2024, "price_usd_tonne": 298.0, "price_lcu_quintal": 2475.0}
        ],
        "seasonality_index": [1.02, 1.04, 0.95, 0.90, 0.92, 0.96, 1.00, 1.03, 1.05, 1.06, 1.05, 1.03],
        "shelf_life_days_ambient": 240,
        "daily_spoilage_rate_ambient": 0.0010,
        "vibration_transit_loss_per_hour": 0.0002,
        "storage_profiles": {
            "ambient": {
                "name": "Standard Farm Shed",
                "decay_factor": 1.0,
                "cost_per_quintal_day": 0.0,
                "description": "Standard farm storage in gunny bags."
            },
            "hermetic_bag": {
                "name": "PICS Hermetic Storage",
                "decay_factor": 0.12,
                "cost_per_quintal_day": 0.22,
                "description": "Airtight containment preventing moisture reabsorption."
            },
            "warehouse": {
                "name": "State Warehouse / CWC Accredited",
                "decay_factor": 0.06,
                "cost_per_quintal_day": 0.38,
                "description": "Fumigated, insured, negotiable warehouse receipt eligible."
            }
        },
        "quality_grades": {
            "Grade A": {"label": "Grade A (Lustrous Sharbati / Durum, Bold)", "price_multiplier": 1.15, "shelf_life_multiplier": 1.15},
            "Grade B": {"label": "Grade B (Standard Milling Wheat)", "price_multiplier": 1.00, "shelf_life_multiplier": 1.00},
            "Grade C": {"label": "Grade C (Feed Quality / Discolored)", "price_multiplier": 0.88, "shelf_life_multiplier": 0.85}
        }
    },
    "green_chillies": {
        "id": "green_chillies",
        "name": "Green Chillies",
        "scientific_name": "Capsicum annuum",
        "fao_item_code": 401,
        "fao_item_name": "Chillies and peppers, green",
        "category": "Perishable Spice/Vegetable",
        "perishability_class": "HIGH",
        "provenance": "FAOSTAT_HISTORICAL",
        "baseline_price_per_quintal": 5400.0,  # ~ ₹54 / kg
        "unit": "quintal",
        "fao_historical_annual": [
            {"year": 2018, "price_usd_tonne": 580.0, "price_lcu_quintal": 4100.0},
            {"year": 2019, "price_usd_tonne": 640.0, "price_lcu_quintal": 4500.0},
            {"year": 2020, "price_usd_tonne": 690.0, "price_lcu_quintal": 5100.0},
            {"year": 2021, "price_usd_tonne": 730.0, "price_lcu_quintal": 5450.0},
            {"year": 2022, "price_usd_tonne": 790.0, "price_lcu_quintal": 6200.0},
            {"year": 2023, "price_usd_tonne": 840.0, "price_lcu_quintal": 6850.0},
            {"year": 2024, "price_usd_tonne": 750.0, "price_lcu_quintal": 6200.0}
        ],
        "seasonality_index": [0.85, 0.90, 0.95, 1.10, 1.25, 1.30, 1.20, 1.15, 1.05, 0.90, 0.82, 0.80],
        "shelf_life_days_ambient": 7,
        "daily_spoilage_rate_ambient": 0.048,
        "vibration_transit_loss_per_hour": 0.006,
        "storage_profiles": {
            "ambient": {
                "name": "Open Gunny / Basket",
                "decay_factor": 1.0,
                "cost_per_quintal_day": 0.0,
                "description": "Rapid moisture shriveling and fungal decay within days."
            },
            "ventilated": {
                "name": "Perforated Crates with Mesh",
                "decay_factor": 0.50,
                "cost_per_quintal_day": 0.75,
                "description": "Maintains airflow to prevent condensation and black mould."
            },
            "cold_storage": {
                "name": "Refrigerated Chill Store (8-10°C)",
                "decay_factor": 0.15,
                "cost_per_quintal_day": 3.0,
                "description": "Optimal temperature retention preserving green color and pungency."
            }
        },
        "quality_grades": {
            "Grade A": {"label": "Grade A (Bright Dark Green, Stems Intact)", "price_multiplier": 1.22, "shelf_life_multiplier": 1.20},
            "Grade B": {"label": "Grade B (Standard Commercial Green)", "price_multiplier": 1.00, "shelf_life_multiplier": 1.00},
            "Grade C": {"label": "Grade C (Soft / Yellowing / Mixed Sizes)", "price_multiplier": 0.72, "shelf_life_multiplier": 0.65}
        }
    }
}


def get_crop_list() -> List[Dict[str, Any]]:
    """Returns summarized list of available crops for selection."""
    return [
        {
            "id": crop["id"],
            "name": crop["name"],
            "scientific_name": crop["scientific_name"],
            "fao_item_code": crop["fao_item_code"],
            "category": crop["category"],
            "perishability_class": crop["perishability_class"],
            "baseline_price_per_quintal": crop["baseline_price_per_quintal"],
            "shelf_life_days_ambient": crop["shelf_life_days_ambient"],
            "storage_options": list(crop["storage_profiles"].keys()),
            "grades": list(crop["quality_grades"].keys()),
            "provenance": crop["provenance"]
        }
        for crop in CROPS_DATABASE.values()
    ]


def get_crop_detail(crop_id: str) -> Dict[str, Any]:
    """Returns detailed data for a specific crop including FAOSTAT series."""
    if crop_id not in CROPS_DATABASE:
        raise KeyError(f"Crop {crop_id} not found in database")
    return CROPS_DATABASE[crop_id]

