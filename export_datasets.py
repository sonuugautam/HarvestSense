"""
Export utility to generate standalone CSV and JSON dataset files
from HarvestSense agricultural, market, and logistics data.
"""

import os
import json
import csv
import sys

# Ensure backend directory in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

from app.data.faostat_data import CROPS_DATABASE, FAOSTAT_METADATA
from app.data.markets_data import REGIONAL_MARKETS
from app.data.logistics_data import VEHICLE_OPTIONS

DATA_DIR = os.path.abspath("data")
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Export FAOSTAT Crop Baseline & Historical Prices (CSV)
csv_crops_path = os.path.join(DATA_DIR, "faostat_historical_producer_prices.csv")
with open(csv_crops_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Crop_ID", "Crop_Name", "Scientific_Name", "FAO_Item_Code", "Perishability_Class",
        "Year", "Price_USD_per_Tonne", "Price_LCU_per_Quintal", "Baseline_Reference_Price", "Data_Provenance"
    ])
    for crop_id, c in CROPS_DATABASE.items():
        baseline = c["baseline_price_per_quintal"]
        for row in c["fao_historical_annual"]:
            writer.writerow([
                crop_id, c["name"], c["scientific_name"], c["fao_item_code"], c["perishability_class"],
                row["year"], row["price_usd_tonne"], row["price_lcu_quintal"], baseline, c["provenance"]
            ])

# 2. Export Crop Perishability, Shelf-Life & Storage Multipliers (CSV)
csv_storage_path = os.path.join(DATA_DIR, "crop_decay_and_storage_profiles.csv")
with open(csv_storage_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Crop_ID", "Crop_Name", "Ambient_Shelf_Life_Days", "Daily_Ambient_Spoilage_Rate_Pct",
        "Transit_Vibration_Loss_PerHour_Pct", "Storage_Type", "Storage_Name",
        "Decay_Factor_Multiplier", "Storage_Cost_per_Quintal_Day_INR", "Description"
    ])
    for crop_id, c in CROPS_DATABASE.items():
        ambient_life = c["shelf_life_days_ambient"]
        daily_spoilage = c["daily_spoilage_rate_ambient"] * 100.0
        vibe_loss = c["vibration_transit_loss_per_hour"] * 100.0
        for s_key, s in c["storage_profiles"].items():
            writer.writerow([
                crop_id, c["name"], ambient_life, round(daily_spoilage, 2),
                round(vibe_loss, 3), s_key, s["name"], s["decay_factor"],
                s["cost_per_quintal_day"], s["description"]
            ])

# 3. Export Regional Wholesale Markets (CSV)
csv_markets_path = os.path.join(DATA_DIR, "regional_wholesale_markets.csv")
with open(csv_markets_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Market_ID", "Market_Name", "Market_Type", "Distance_KM", "Transit_Hours",
        "Base_Handling_Fee_INR_per_Q", "Entry_Cess_Rate_Pct", "Buyer_Competition_Level",
        "Price_Spread_Multiplier", "Daily_Volume_Capacity_Quintals", "Liquidity_Rating", "Provenance"
    ])
    for m in REGIONAL_MARKETS.values():
        writer.writerow([
            m["id"], m["name"], m["market_type"], m["distance_km"], m["transit_hours"],
            m["base_handling_fee_per_quintal"], round(m["entry_cess_rate"] * 100, 2),
            m["buyer_competition_level"], m["price_spread_multiplier"],
            m["daily_volume_capacity_quintals"], m["liquidity_rating"], m["provenance"]
        ])

# 4. Export Logistics Vehicle Fleets (CSV)
csv_logistics_path = os.path.join(DATA_DIR, "logistics_vehicle_fleets.csv")
with open(csv_logistics_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Vehicle_ID", "Vehicle_Name", "Capacity_Min_Quintals", "Capacity_Max_Quintals",
        "Max_Recommended_Range_KM", "Base_Booking_Fee_INR", "Cost_Per_KM_INR",
        "Loading_Unloading_Labor_INR", "Is_Refrigerated", "Transit_Vibration_Loss_Factor", "Suitable_For", "Provenance"
    ])
    for v in VEHICLE_OPTIONS.values():
        writer.writerow([
            v["id"], v["name"], v["capacity_quintals_min"], v["capacity_quintals_max"],
            v["max_recommended_range_km"], v["base_booking_fee"], v.get("cost_per_km", 0.0),
            v["loading_unloading_labor_flat"], v["is_refrigerated"],
            v["transit_vibration_loss_factor"], v["suitable_for"], v["provenance"]
        ])

# 5. Export Unified JSON Dataset
unified_dataset = {
    "metadata": FAOSTAT_METADATA,
    "crops": CROPS_DATABASE,
    "regional_markets": REGIONAL_MARKETS,
    "vehicle_fleets": VEHICLE_OPTIONS
}
json_path = os.path.join(DATA_DIR, "harvestsense_complete_dataset.json")
with open(json_path, mode="w", encoding="utf-8") as f:
    json.dump(unified_dataset, f, indent=2)

print("Export completed successfully!")
print(f"Generated 5 dataset files in: {DATA_DIR}")
