# backend/wait_for_db.py

import time
import psycopg2
from psycopg2 import OperationalError
import os

print("⏳ Attente de la base de données...")

while True:
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "ferme"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432)
        )
        conn.close()
        break
    except OperationalError:
        time.sleep(1)

print("✅ Base de données prête.")

# Création des tables
import create_tables

# Insertion des plantes
import seeds
