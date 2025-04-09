from db_conn import get_db
from db_models import Plant
from sqlalchemy.orm import Session

plants_data = [
    {"id": 1, "name": "Tomate"},
    {"id": 2, "name": "Salade"},
    {"id": 3, "name": "Carotte"},
    {"id": 4, "name": "Basilic"},
    {"id": 5, "name": "Menthe"},
    {"id": 6, "name": "Aubergine"},
]

def seed_plants(db: Session):
    for plant in plants_data:
        existing = db.query(Plant).filter_by(id=plant["id"]).first()
        if not existing:
            db.add(Plant(**plant))
            print(f"🌱 Ajouté : {plant['name']} (ID={plant['id']})")
        else:
            print(f"✅ Déjà présent : {plant['name']} (ID={plant['id']})")
    db.commit()

# ✅ Fonction utilisée par Docker
def seed_data():
    db = next(get_db())
    seed_plants(db)
    print("🌾 Insertion des plantes terminée.")

if __name__ == "__main__":
    seed_data()
