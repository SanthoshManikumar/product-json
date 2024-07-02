from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

# Initialize PyMongo
app.config["MONGO_URI"] = 'mongodb+srv://santhoshsmothy:mongodb123@santhosh.uikqcvl.mongodb.net/ecommerce?retryWrites=true&w=majority'
mongo = PyMongo(app)
products_collection = mongo.db.products
cart_collection = mongo.db.cart

# Dummy product data for initial setup
dummy_products = [
    {
        "img_link": "https://images-eu.ssl-images-amazon.com/images/I/810s53kR8tL._AC_UL450_SR450,320_.jpg",
        "title": "Skybags Casual Backpack 28L",
        "description": "2 Main Compartments, Bottle Pocket, Front Pocket, Padded Shoulder Strap",
        "price": 1500.0
    },
    {
        "img_link": "https://images-eu.ssl-images-amazon.com/images/I/51+b9IWWbjL._AC_UL450_SR450,320_.jpg",
        "title": "Lifelong PVC Hex Dumbbells Pack of 2",
        "description": "Home Gym Equipment Fitness Barbell, Gym Dumbbells",
        "price": 800.0
    },
    {
        "img_link": "https://m.media-amazon.com/images/I/41Z6Wo7cJvL._SX300_SY300_QL70_FMwebp_.jpg",
        "title": "Pedigree Adult Dry Dog Food, Chicken & Vegetables, 3kg Pack",
        "description": "Healthy and balanced dog food",
        "price": 1200.0
    },
    {
        "img_link": "https://m.media-amazon.com/images/I/31JCIGzwhPL._SY300_SX300_QL70_FMwebp_.jpg",
        "title": "AMD Ryzen 5 5600 Desktop Processor",
        "description": "6 cores 12 Threads 35 MB Cache 3.5 GHz Upto 4.2 GHz",
        "price": 25000.0
    }
]

# Populate initial data if collection is empty
if products_collection.count_documents({}) == 0:
    products_collection.insert_many(dummy_products)

# Routes
@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(products_collection.find({}, {'_id': 1, 'img_link': 1, 'title': 1, 'description': 1, 'price': 1}))
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify({'products': products}), 200

@app.route('/api/cart', methods=['GET'])
def get_cart():
    cart_items = list(cart_collection.find())
    
    for item in cart_items:
        item['_id'] = str(item['_id'])
        item['title'] = str(item['title'])
        item['price'] = str(item['price'])
        item['img_link'] = str(item['img_link'])
    return jsonify({'cart': cart_items}), 200

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        title = data.get('title')
        price = data.get('price')
        img_link = data.get('imglink')
        
        cart_collection.insert_one({'title': title, 'price': price, 'img_link': img_link})
        return jsonify({"message": "Product added to cart successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/cart/<string:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    try:
        cart_collection.delete_one({"_id": ObjectId(product_id)})
        return jsonify({"message": "Product removed from cart successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
