from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

print("🚀 Starting Shopping Cart API (Basic Version)...")

# MongoDB connection
try:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:password@mongodb:27017/shopping_cart_db?authSource=admin')
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ismaster')
    print("✅ MongoDB connected")
    
    db = client.shopping_cart_db
    products_collection = db.products
    carts_collection = db.carts
    mongo_connected = True
    
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    mongo_connected = False

# Sample products
products = [
    {"id": 1, "name": "Laptop", "price": 50000, "category": "Electronics"},
    {"id": 2, "name": "Headphones", "price": 2000, "category": "Electronics"},
    {"id": 3, "name": "Mouse", "price": 800, "category": "Electronics"}
]

cart = []

@app.route('/')
def home():
    return jsonify({"message": "Shopping Cart API is running!", "database": "connected" if mongo_connected else "disconnected"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "service": "shopping-cart-api",
        "database": "connected" if mongo_connected else "disconnected"
    })

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/cart', methods=['GET'])
def get_cart():
    return jsonify({"items": cart, "total_price": 0})

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    cart.append(data)
    return jsonify({"message": "Product added to cart", "cart": cart})

@app.route('/cart/<product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    global cart
    cart = [item for item in cart if str(item.get('product_id')) != product_id]
    return jsonify({"message": "Product removed from cart", "cart": cart})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)