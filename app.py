from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS 
from config import mongo
from dotenv import load_dotenv
from routes.account_routes import account_bp

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register Blueprints for routes
app.register_blueprint(account_bp, url_prefix='/api/accounts')

# Pass the required route to the decorator for home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Finans API is running..."})

if __name__ == "__main__":
    app.run(debug=True)
