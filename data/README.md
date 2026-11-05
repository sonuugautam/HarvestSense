# 📊 HarvestSense Agricultural, Market & Logistics Datasets

This directory contains the standalone CSV and JSON datasets used by **HarvestSense: Crop to Market Optimizer** for the **Google Solution Challenge 2026** (aligned with **UN SDG 2: Zero Hunger**).

---

## 🗂️ Dataset Files Overview

| File Name | Format | Primary Source / Provenance | Description |
| :--- | :---: | :--- | :--- |
| **`faostat_historical_producer_prices.csv`** | CSV | `FAOSTAT_HISTORICAL` | Multi-year annual baseline producer prices (2018–2024), official FAO commodity item codes, and perishability ratings. |
| **`crop_decay_and_storage_profiles.csv`** | CSV | `FAOSTAT_HISTORICAL` + Post-Harvest Studies | Shelf-life in days under ambient heat, daily biological decay percentages, transit vibration damage rates, and 5 storage structure options. |
| **`regional_wholesale_markets.csv`** | CSV | `SYNTHETIC_LOCAL_MARKET` (Calibrated on FAO) | Modeled regional wholesale mandis, transport distances, transit durations, price spreads, cess fees, and buyer liquidity ratings. |
| **`logistics_vehicle_fleets.csv`** | CSV | `LOGISTICS_MODEL` | Vehicle fleet models (trolley, pickup truck, shared FPO freight, reefer van), capacities, base fees, per-km fuel rates, and vibration factors. |
| **`harvestsense_complete_dataset.json`** | JSON | Unified Multi-Source | Complete hierarchical dataset containing all crops, seasonality vectors, markets, fleets, and FAO metadata in a single JSON structure. |

---

## 🌾 Primary Data Source: FAOSTAT (UN FAO)
- **Organization**: Food and Agriculture Organization of the United Nations (FAO)
- **Database**: FAOSTAT Corporate Statistical Database
- **Domain**: Producer Prices (`Domain Code: PP`)
- **Official URL**: [https://www.fao.org/faostat/en/#data/PP](https://www.fao.org/faostat/en/#data/PP)
- **Standard Currency / Units**: USD / Tonne and Local Currency Units (LCU) / Quintal (100 kg)

### Supported FAO Commodity Codes:
- **Tomatoes**: FAO Item Code `#388` (*Solanum lycopersicum*)
- **Potatoes**: FAO Item Code `#116` (*Solanum tuberosum*)
- **Onions (Dry)**: FAO Item Code `#403` (*Allium cepa*)
- **Maize (Corn)**: FAO Item Code `#56` (*Zea mays*)
- **Wheat (Grain)**: FAO Item Code `#15` (*Triticum aestivum*)
- **Green Chillies**: FAO Item Code `#401` (*Capsicum annuum*)

---

## 🚚 Logistics & Post-Harvest Loss Research Citations
- **World Bank** (2021): *Addressing Post-Harvest Losses in Smallholder Value Chains in South Asia and Sub-Saharan Africa*.
- **Kitinoja, L., & Kader, A. A.** (2015): *Measuring postharvest losses of fresh fruits and vegetables in developing countries*. The Postharvest Education Foundation.
- **Government of India (MoAFW)**: *Agmarknet Wholesale APMC Market Price Spread Analysis and Freight Tariffs*.
