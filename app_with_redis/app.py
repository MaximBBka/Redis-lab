from flask import Flask, jsonify
import psycopg2
import redis
import random
import json

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, db=0)

def get_db():
    return psycopg2.connect(
        host="postgres",
        database="postgres",
        user="postgres",
        password="postgres"
    )

@app.route("/random_product")
def get_random_product():
    random_id = random.randint(1, 50)
    cache_key = f"product:{random_id}"
    
    # Пробуем получить из кеша
    cached = cache.get(cache_key)
    if cached:
        return jsonify(json.loads(cached))
    
    # Если нет в кеше - запрос к PostgreSQL
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (random_id,))
    product = cur.fetchone()
    conn.close()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    response = {
        "id": product[0],
        "name": product[1],
        "price": float(product[2]),
        "description": product[3]
    }
    
    # Кешируем на 10 секунд
    cache.setex(cache_key, 10, json.dumps(response))
    return jsonify(response)

@app.route("/product/<int:product_id>")
def get_product(product_id):
    # Пробуем получить из кеша
    cached = cache.get(f"product:{product_id}")
    if cached:
        return jsonify(json.loads(cached))
    
    # Если нет в кеше - идём в PostgreSQL
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    conn.close()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    # Формируем ответ
    response = {
        "id": product[0],
        "name": product[1],
        "price": float(product[2]),
        "description": product[3]
    }
    
    # Кешируем на 10 секунд
    cache.setex(f"product:{product_id}", 10, json.dumps(response))
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)