from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import redis
import os

app = Flask(__name__)
CORS(app)

# Lire le secret
# Le secret est lu depuis le chemin standard de Swarm pour les secrets
try:
    with open('/run/secrets/db_password', 'r') as f:
        DB_PASSWORD = f.read().strip()
except FileNotFoundError:
    # Cas de développement ou test sans Swarm secret (utiliser une variable d'environnement ou une valeur par défaut)
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'my_default_secret_password_for_dev')

# Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),
    'database': os.getenv('DB_NAME', 'flask_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': DB_PASSWORD
}
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')

# Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def get_db_connection():
    """Établit la connexion à la base de données PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'version': '2.0', 'db': 'ok', 'redis': 'ok'}), 200

@app.route('/api/items', methods=['GET'])
def get_items():
    """Récupère tous les articles, en utilisant le cache Redis si disponible."""
    # Try cache first
    cached = redis_client.get('items')
    if cached:
        # NOTE : Utiliser 'eval()' est risqué en production, mais accepté pour un POC/cours.
        # En production, on utiliserait json.loads() après avoir sérialisé en JSON.
        return jsonify({'source': 'cache', 'items': eval(cached)})

    # Query DB
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description FROM items ORDER BY id')
    
    items = [{'id': row[0], 'name': row[1], 'description': row[2]} for row in cur.fetchall()]
    
    cur.close()
    conn.close()


    # Cache for 60 seconds (Time To Live = 60s)
    redis_client.setex('items', 60, str(items))

    return jsonify({'source': 'database', 'items': items})

@app.route('/api/items', methods=['POST'])
def create_item():
    """Crée un nouvel article dans la base de données."""
    data = request.json
    name = data.get('name')
    description = data.get('description', '')

    conn = get_db_connection()
    cur = conn.cursor()

    # Note: Correction d'une faute de frappe dans la requête SQL (iitems -> items)
    # Dans le code initial: 'INSERT INTO iitems (name, description)...'
    cur.execute(
        'INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id',
        (name, description)
    )
    item_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    # Invalidate cache
    redis_client.delete('items')

    return jsonify({'id': item_id, 'name': name, 'description': description}), 201

if __name__ == '__main__':
    # Le serveur Flask écoute sur toutes les interfaces (0.0.0.0) et le port 5000
    # dans le conteneur. Le port sera exposé via Swarm Ingress.
    app.run(host='0.0.0.0', port=5000)