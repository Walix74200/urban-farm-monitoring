# Projet de supervision de ferme connectée (Kubernetes + FastAPI)

Ce projet est une ferme urbaine connectée composée de plusieurs microservices Docker orchestrés avec **Kubernetes**, permettant de :

- Simuler des mesures de capteurs (température, humidité)
- Les stocker dans une base de données PostgreSQL
- Détecter automatiquement des anomalies
- Afficher une **interface de supervision visuelle** avec export de données

## Architecture microservices

Chaque service est conteneurisé dans Docker et déployé via Kubernetes :

| Service              | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `postgres`           | Base de données PostgreSQL contenant les mesures des capteurs               |
| `backend`            | API FastAPI qui reçoit les mesures et les stocke dans PostgreSQL            |
| `simulateur`         | Script Python qui envoie régulièrement des mesures simulées au backend      |
| `anomaly`            | Microservice FastAPI qui détecte les anomalies dans les mesures             |
| `interface_supervision` | Interface web en FastAPI + Jinja2 affichant les plantes, mesures, anomalies |

## Étapes d'installation et d'exécution

### 1. Prérequis (à faire une seule fois)

- Installer Docker Desktop : https://www.docker.com/products/docker-desktop
- Activer Kubernetes dans les paramètres Docker
- Vérifier que le contexte Kubernetes est bien actif :
```bash
kubectl config get-contexts
kubectl config use-context docker-desktop
```

### 2. Cloner le projet
```bash
git clone https://github.com/ton-repo/urban-farm-monitoring.git
cd urban-farm-monitoring
```

### 3. Déployer les services Kubernetes
> Ces fichiers déploient chacun un service (DB, backend, etc.)

```bash
kubectl apply -f postgres-deployment.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f anomaly-deployment.yaml
kubectl apply -f simulateur-deployment.yaml
kubectl apply -f interface-deployment.yaml
```

### 4. Accéder à l’interface web
Une fois tous les pods `Running`, accède à :

👉 http://localhost:30082

Tu verras :
- Les plantes (6 au total)
- Les dernières mesures par capteur (température, humidité)
- Les anomalies détectées (températures hors normes, humidité basse...)
- Des options d’export en CSV, JSON ou PDF

---

## ⚙️ Détails techniques de chaque service

###  `simulateur`
- Envoie toutes les 2 secondes une mesure simulée à l'API `backend`
- Les données sont encodées en base64 + msgpack
- Un `cycle_id` permet d’identifier chaque batch de mesures

###  `backend`
- API REST développée avec FastAPI
- Route `POST /api/v1/receive` : reçoit et décode les données capteurs
- Route `GET /api/v1/measurements` : renvoie toutes les mesures
- Stocke les capteurs + les mesures dans PostgreSQL

###  `anomaly`
- API FastAPI qui lit les données depuis la DB PostgreSQL
- Route `GET /api/v1/anomalies` : retourne les mesures considérées comme anormales
- Une température > 40°C ou humidité < 20% est considérée comme une anomalie

###  `interface_supervision`
- Serveur FastAPI + moteur de templates Jinja2
- Affiche :
  - Plantes de la ferme (hover pour voir les données)
  - Mesures en temps réel
  - Anomalies détectées
  - Exports (CSV / JSON / PDF)
- Appelle les API `backend` et `anomaly` via `http://backend-service` et `http://anomaly-service`

---

## Rebuild ou mise à jour (ex : HTML ou Dockerfile modifié)

Depuis le dossier du service modifié (ex: `interface_supervision`) :

```bash
docker build -t lucas525/ferme-interface:latest .
docker push lucas525/ferme-interface:latest
kubectl rollout restart deployment interface-deployment
```

---

## Nettoyer tous les services
```bash
kubectl delete -f interface-deployment.yaml
kubectl delete -f simulateur-deployment.yaml
kubectl delete -f anomaly-deployment.yaml
kubectl delete -f backend-deployment.yaml
kubectl delete -f postgres-deployment.yaml
```

---

## Vérification rapide
```bash
kubectl get pods
kubectl get svc
```
Tous les pods doivent être en `Running`.

---

## Pour un autre utilisateur qui veut tester

Il suffit de :
1. Cloner le repo
2. Avoir Docker Desktop + Kubernetes activé
3. Lancer toutes les commandes `kubectl apply -f ...`
4. Accéder à http://localhost:30082

> Toutes les images Docker nécessaires sont déjà sur DockerHub (lucas525)

---

##  Auteur
Projet réalisé par Lucas Bonsergent, Mathéo Rouvière et Adam Saidane - IA Institut 2025