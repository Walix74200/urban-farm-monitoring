from db_conn import engine
from db_models import Base

def create_tables():
    print("📦 Création des tables dans la base de données...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données prête.")
