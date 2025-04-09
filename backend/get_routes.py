from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db_conn import get_db
from db_models import Measurement
from typing import Optional
from datetime import datetime

get_router = APIRouter()

@get_router.get("/measurements")
def get_measurements(
    sensor_id: Optional[int] = Query(None),
    plant_id: Optional[int] = Query(None),
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Measurement)

    if sensor_id is not None:
        query = query.filter(Measurement.sensor_id == sensor_id)

    if plant_id is not None:
        query = query.filter(Measurement.plant_id == plant_id)

    if from_date:
        try:
            from_dt = datetime.fromisoformat(from_date)
            query = query.filter(Measurement.timestamp >= from_dt)
        except:
            return {"error": "Invalid from_date format (expected ISO string)"}

    if to_date:
        try:
            to_dt = datetime.fromisoformat(to_date)
            query = query.filter(Measurement.timestamp <= to_dt)
        except:
            return {"error": "Invalid to_date format (expected ISO string)"}

    results = query.all()

    data = [
        {
            "sensor_id": m.sensor_id,
            "plant_id": m.plant_id,
            "timestamp": m.timestamp.isoformat(),
            "temperature": m.temperature,
            "humidity": m.humidity,
            "version": m.version  # ✅ Ceci est essentiel pour le frontend
        }
        for m in results
    ]

    return {"count": len(data), "data": data}
