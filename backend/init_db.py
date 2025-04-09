from create_tables import Base, engine
from seeds import seed_data

print("📦 Création des tables dans la base de données...")
Base.metadata.create_all(bind=engine)
print("✅ Base de données prête.")

print("🌾 Insertion des données de départ...")
seed_data()
print("✅ Données insérées.")
