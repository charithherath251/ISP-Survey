from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS to allow any frontend to send requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
submitted_data = []

# Data model
class BehaviorData(BaseModel):
    mouseMoves: int
    keypresses: int
    scrolls: int
    clicks: int
    timing: List[int]

# API to receive behavior data
@app.post("/submit-survey")
async def submit_survey(data: BehaviorData):
    record = {
        "mouseMoves": data.mouseMoves,
        "keypresses": data.keypresses,
        "scrolls": data.scrolls,
        "clicks": data.clicks,
        "timing": data.timing[0] if data.timing else None
    }
    submitted_data.append(record)
    return {"success": True, "message": "Data recorded"}

# Webpage to view submitted behavior data
@app.get("/view-data", response_class=HTMLResponse)
async def view_data():
    html = "<h2>Submitted Behavior Data</h2><table border='1' cellpadding='6'><tr><th>Mouse</th><th>Keys</th><th>Scrolls</th><th>Clicks</th><th>Timing (ms)</th></tr>"
    for entry in submitted_data:
        html += f"<tr><td>{entry['mouseMoves']}</td><td>{entry['keypresses']}</td><td>{entry['scrolls']}</td><td>{entry['clicks']}</td><td>{entry['timing']}</td></tr>"
    html += "</table>"
    return html
