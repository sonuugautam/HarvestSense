"""
Server runner script for HarvestSense
"""

import sys
import os
import uvicorn

# Ensure the backend directory is in the python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting HarvestSense on http://127.0.0.1:{port} ...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=True)

