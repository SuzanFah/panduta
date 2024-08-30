from flask import Flask, render_template # type: ignore

# Initialize Flask application
app = Flask(__name__, static_folder='static')

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
    app.run(debug=True, port=8000)  # Specify port 8000
