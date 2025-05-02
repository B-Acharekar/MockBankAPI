from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from utils.socketio_instance import socketio  # Ensure this is imported
from routes.account_routes import account_bp
from routes.transaction_routes import transaction_bp
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
socketio.init_app(app, cors_allowed_origins="*")

# App configuration
app.config["MAILGUN_API_KEY"] = os.getenv("MAILGUN_API_KEY")
app.config["MAILGUN_DOMAIN"] = os.getenv("MAILGUN_DOMAIN")

# Register Blueprints for routes
app.register_blueprint(account_bp, url_prefix='/api/accounts')
app.register_blueprint(transaction_bp, url_prefix='/transaction')

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Finans API is running..."})

if __name__ == '__main__':
    socketio.run(app, debug=True)  # Ensure you are calling socketio.run here
