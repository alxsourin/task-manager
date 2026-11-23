import os

import psycopg
from flask import Flask, jsonify

app = Flask(__name__)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Task Manager!",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/db-health")
def db_health():
    try:
        with psycopg.connect(**DB_CONFIG, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()

        return jsonify({"database": "connected"}), 200

    except psycopg.Error:
        return jsonify({"database": "unavailable"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
