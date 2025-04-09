from fastapi import APIRouter, HTTPException, Query
from anomalies_utils import (
    get_recent_measurements,
    detect_anomalies,
    insert_anomalies,
    get_all_anomalies,
    get_anomalies_by_plant,
    mark_as_analyzed
)

router = APIRouter()

@router.post("/api/v1/analyze")
def analyze():
    try:
        measurements = get_recent_measurements()
        if not measurements:
            return {"message": "Aucune nouvelle mesure à analyser."}

        anomalies = detect_anomalies(measurements)
        insert_anomalies(anomalies)

        measurement_ids = [m["id"] for m in measurements]
        mark_as_analyzed(measurement_ids)

        return {"message": f"{len(anomalies)} anomalies détectées."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/anomalies")
def list_anomalies():
    try:
        return get_all_anomalies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/anomalies/by-plant")
def anomalies_by_plant(plant_id: int = Query(...)):
    try:
        return get_anomalies_by_plant(plant_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
