from flask import Flask, jsonify
import psycopg2
import random

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host="postgres",
        database="postgres",
        user="postgres",
        password="postgres"
    )

@app.route("/random_product")
def get_random_product():
    conn = get_db()
    cur = conn.cursor()
    
    # Получаем случайный ID от 1 до 50
    random_id = random.randint(1, 50)
    
    cur.execute("SELECT * FROM products WHERE id = %s", (random_id,))
    product = cur.fetchone()
    conn.close()
    
    if product:
        return jsonify({
            "id": product[0],
            "name": product[1],
            "price": float(product[2]),
            "description": product[3]
        })
    return jsonify({"error": "Product not found"}), 404

@app.route("/product/<int:product_id>")
def get_product(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    conn.close()
    
    if product:
        return jsonify({
            "id": product[0],
            "name": product[1],
            "price": float(product[2]),
            "description": product[3]
        })
    return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)