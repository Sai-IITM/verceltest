from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import json
import os

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Dynamically locate the JSON file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Assumes JSON is in the same 'api/' folder as index.py
JSON_PATH = os.path.join(BASE_DIR, "q-vercel-latency.json")

class LatencyRequest(BaseModel):
    regions: list[str]
    threshold_ms: float

@app.post("/api/metrics")
async def get_metrics(request: LatencyRequest):
    with open(JSON_PATH, "r") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    response = {}
    
    for region in request.regions:
        region_df = df[df['region'] == region]
        if not region_df.empty:
            response[region] = {
                "avg_latency": round(region_df['latency_ms'].mean(), 2),
                "p95_latency": round(np.percentile(region_df['latency_ms'], 95), 2),
                "avg_uptime": round(region_df['uptime_pct'].mean(), 3),
                "breaches": int((region_df['latency_ms'] > request.threshold_ms).sum())
            }
    return response
