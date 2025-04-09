from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
import requests
import os  # ✅ Pour utiliser les variables d’environnement

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Utilisation des variables d’environnement
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:8000/api/v1")
ANOMALY_URL = os.getenv("ANOMALY_URL", "http://anomaly-service:8001/api/v1")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    try:
        sensors = requests.get(f"{BACKEND_URL}/measurements").json()["data"]
        anomalies = requests.get(f"{ANOMALY_URL}/anomalies").json()
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "measurements": [],
            "sensors": [],
            "anomalies": [],
            "error": str(e)
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "measurements": sensors,
        "sensors": sensors,
        "anomalies": anomalies
    })

@app.get("/measurements")
def api_measurements():
    return requests.get(f"{BACKEND_URL}/measurements").json()

@app.get("/sensors")
def api_sensors():
    data = requests.get(f"{BACKEND_URL}/measurements").json()["data"]
    seen = {}
    for item in data:
        if item["sensor_id"] not in seen:
            seen[item["sensor_id"]] = {
                "sensor_id": item["sensor_id"],
                "plant_id": item["plant_id"],
                "version": item.get("version", "FR-v8")  # ✅ on prend la version si elle existe
            }
    return list(seen.values())

@app.get("/anomalies")
def api_anomalies():
    return requests.get(f"{ANOMALY_URL}/anomalies").json()
