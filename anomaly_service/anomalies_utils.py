import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# Charge les variables d'environnement
load_dotenv(dotenv_path="config.env")

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "ferme"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", 5432)
    )

def get_recent_measurements():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, sensor_id, plant_id, temperature, humidity, cycle_id
        FROM measurements
        WHERE analyzed = FALSE
        ORDER BY timestamp ASC
        LIMIT 100
    """)
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "sensor_id": r[1],
            "plant_id": r[2],
            "temperature": r[3],
            "humidity": r[4],
            "cycle_id": r[5]
        }
        for r in rows
    ]

def detect_anomalies(measurements):
    anomalies = []
    for m in measurements:
        if m["temperature"] > 40 or m["humidity"] < 20:
            anomalies.append({
                "sensor_id": m["sensor_id"],
                "plant_id": m["plant_id"],
                "cycle_id": m["cycle_id"],
                "timestamp": datetime.utcnow(),
                "type": "Valeur hors plage",
                "details": f"Temp={m['temperature']}, Hum={m['humidity']}",
                "severity": "warning"
            })
    return anomalies

def insert_anomalies(anomalies):
    if not anomalies:
        return
    conn = get_db_connection()
    cur = conn.cursor()
    for a in anomalies:
        cur.execute(
            """
            INSERT INTO anomalies 
            (sensor_id, plant_id, cycle_id, timestamp, type, details, severity)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (a["sensor_id"], a["plant_id"], a["cycle_id"], a["timestamp"],
             a["type"], a["details"], a["severity"])
        )
    conn.commit()
    conn.close()

def mark_as_analyzed(measurement_ids):
    if not measurement_ids:
        return
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE measurements SET analyzed = TRUE WHERE id = ANY(%s)",
        (measurement_ids,)
    )
    conn.commit()
    conn.close()

def get_all_anomalies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, sensor_id, plant_id, cycle_id, timestamp, type, details, severity
        FROM anomalies
        ORDER BY timestamp DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "sensor_id": r[1],
            "plant_id": r[2],
            "cycle_id": r[3],
            "timestamp": str(r[4]),
            "type": r[5],
            "details": r[6],
            "severity": r[7]
        }
        for r in rows
    ]

def get_anomalies_by_plant(plant_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, sensor_id, plant_id, cycle_id, timestamp, type, details, severity
        FROM anomalies
        WHERE plant_id = %s
        ORDER BY timestamp DESC
    """, (plant_id,))
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "sensor_id": r[1],
            "plant_id": r[2],
            "cycle_id": r[3],
            "timestamp": str(r[4]),
            "type": r[5],
            "details": r[6],
            "severity": r[7]
        }
        for r in rows
    ]
