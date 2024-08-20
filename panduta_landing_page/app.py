from flask import Flask, render_template

# Initialize Flask application
app = Flask(__name__)

# Define route for the landing page
@app.route('/')
def index():
    # Render the HTML template 'index.html'
    return render_template('index.html')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Specify port 8000
