from flask import Flask, render_template, send_from_directory # type: ignore
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Flask application
app = Flask(__name__, static_folder='static')

# Configuration
secret_key = os.environ.get('SECRET_KEY')
debug_mode = os.environ.get('DEBUG')

app.config['SECRET_KEY'] = secret_key
app.config['DEBUG'] = debug_mode == 'True'

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
    return render_template('why-panduta.html')

@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html')

@app.route('/test-video')
def test_video():
     return send_from_directory('static/videos', 'panda_laundry.mp4')

# Run the Flask application
if __name__ == '__main__':
    app.run()

