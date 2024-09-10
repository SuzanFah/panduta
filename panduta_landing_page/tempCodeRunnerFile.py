from flask import Flask, render_template, send_from_directory, request, jsonify
from dotenv import load_dotenv
import os
from database import db

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__, static_folder='static')

# Configuration
secret_key = os.environ.get('SECRET_KEY')
debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'

app.config['SECRET_KEY'] = secret_key
app.config['DEBUG'] = debug_mode

# Define route for the landing page
@app.route('/')
def index():
    # Render the HTML template 'index.html'
    return render_template('index.html')

@app.route('/our-story')
def our_story():
    return render_template('our-story.html')

@app.route('/why-panduta')
def why_panduta():
    return render_template('why_panduta.html')

@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html')

@app.route('/test-video')
def test_video():
     return send_from_directory('static/videos', 'panda_laundry.mp4')

@app.route('/dual-interface')
def dual_interface():
    return render_template('dual_interface.html')

# API endpoints for the dual interface system
@app.route('/api/services', methods=['GET'])
def get_services():
    return jsonify(db.get_services())

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    booking_data = request.json
    created_booking = db.create_booking(booking_data)
    return jsonify({"message": "Booking created successfully", "booking": created_booking}), 201

@app.route('/api/provider/dashboard', methods=['GET'])
def provider_dashboard():
    return jsonify(db.get_provider_dashboard())

# Run the Flask application
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8000, debug=True)
