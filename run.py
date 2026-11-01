"""
Root Launcher for HarvestSense: Crop to Market Optimizer
Run with: python run.py
"""

import sys
import os
import uvicorn

# Add backend directory to sys.path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("=" * 65)
    print("🌾  HARVESTSENSE: CROP TO MARKET OPTIMIZER")
    print("     Google Solution Challenge 2026 • SDG 2: Zero Hunger")
    print("=" * 65)
    print(f"🚀  Server starting on: http://127.0.0.1:{port}")
    print(f"📑  Interactive API Docs: http://127.0.0.1:{port}/docs")
    print(f"💻  Frontend UI: http://127.0.0.1:{port}/")
    print("=" * 65)
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, app_dir=backend_dir)

