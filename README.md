# Flask Swarm Application
Stack Docker Swarm complète avec Flask, PostgreSQL, Redis et Nginx.
## Architecture
- **Backend** : Flask API (3 replicas)
- **Database** : PostgreSQL (1 replica, volume persistant)
- **Cache** : Redis (2 replicas)
- **Frontend** : Nginx (2 replicas)
## Prérequis
Utilisation
Frontend : http://localhost:8080
API : http://localhost:5000/api/items
Health : http://localhost:5000/health
Scaling
Suppression
- Docker Swarm initialisé
- Ports 5000 et 8080 disponibles
## Déploiement
```bash
# 1. Créer le secret
echo "votre_mot_de_passe" > secrets/db_password.txt
docker secret create db_password secrets/db_password.txt
# 2. Build les images
docker build -t flask-api:latest ./backend
docker build -t flask-frontend:latest ./frontend
# 3. Déployer la stack
docker stack deploy -c stack.yml flaskapp
# 4. Vérifier
docker stack services flaskapp
```

### Utilisation 
- Frontend : http://localhost:8080
- API : http://localhost:5000/api/items
- Health : http://localhost:5000/health

### Scalling
```bash
docker service scale flaskapp_backend=5
```

### Suppression 
```bash
docker stack rm flaskapp
docker secret rm db_password
```