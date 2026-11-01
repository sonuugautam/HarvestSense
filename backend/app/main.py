"""
Main FastAPI Application Entrypoint for HarvestSense
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes import router as api_router

app = FastAPI(
    title="HarvestSense: Crop to Market Optimizer",
    description="Multi-Agent AI Agricultural Decision System for SDG 2 (Zero Hunger)",
    version="1.0.0"
)

# Enable CORS for local Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(api_router, prefix="/api")

# Determine path to built frontend static files
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Don't intercept API routes
        if full_path.startswith("api"):
            return None
        index_file = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"service": "HarvestSense Backend API", "docs": "/docs"}
else:
    @app.get("/")
    def root():
        return {
            "name": "HarvestSense: Crop to Market Optimizer API",
            "status": "online",
            "docs_url": "/docs",
            "sdg_alignment": "SDG 2: Zero Hunger (Target 2.3 & 12.3)"
        }

