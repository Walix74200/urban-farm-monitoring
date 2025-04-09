import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db_conn import get_db
from db_models import Measurement, Sensor
import base64
import msgpack
from datetime import datetime

post_router = APIRouter()
logging.basicConfig(level=logging.INFO)

class SensorData(BaseModel):
    sensor_id: int
    plant_id: int
    timestamp: str
    temperature: float
    humidity: float
    version: str = "UNKNOWN"
    cycle_id: int

@post_router.post("/receive")
async def receive_data(request: Request, db: Session = Depends(get_db)):
    try:
        raw_base64 = await request.body()
        decoded = base64.b64decode(raw_base64)
        unpacked = msgpack.unpackb(decoded, raw=False)
        data = SensorData(**unpacked)

        sensor = db.query(Sensor).filter(Sensor.id == data.sensor_id).first()
        if not sensor:
            sensor = Sensor(
                id=data.sensor_id,
                plant_id=data.plant_id,
                version=data.version,
                last_seen=datetime.utcnow()
            )
            db.add(sensor)
            db.commit()
            db.refresh(sensor)
        else:
            sensor.last_seen = datetime.utcnow()
            sensor.version = data.version  # ✅ Mise à jour version aussi sur capteur
            db.commit()

        measurement = Measurement(
            sensor_id=data.sensor_id,
            plant_id=data.plant_id,
            cycle_id=data.cycle_id,
            timestamp=datetime.fromisoformat(data.timestamp),
            temperature=data.temperature,
            humidity=data.humidity,
            raw_data=raw_base64.decode(),
            version=data.version  # ✅ Stocker la version dans la mesure
        )
        db.add(measurement)
        db.commit()

        return {
            "status": "success",
            "message": "Mesure enregistrée.",
            "decoded": data.dict()
        }

    except ValueError as e:
        logging.error(f"[VALIDATION ERROR] {e}")
        raise HTTPException(status_code=400, detail=f"Erreur de validation : {str(e)}")
    except Exception as e:
        logging.exception("[SERVER ERROR]")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur serveur : {str(e)}")
