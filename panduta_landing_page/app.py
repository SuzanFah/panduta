from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Length
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'true'

laundry_providers = []

class LaundryProviderForm(FlaskForm):
    business_name = StringField('Business Name', validators=[DataRequired(), Length(min=4, max=50)])
    tax_number = StringField('Tax Registration Number', validators=[DataRequired(), Length(min=8, max=20)])
    location = StringField('Location', validators=[DataRequired(), Length(min=4, max=100)])
    price_range = StringField('Price Range', validators=[DataRequired()])
    delivery_options = StringField('Delivery Options', validators=[DataRequired()])
    fabric_types = StringField('Fabric Types Handled', validators=[DataRequired()])
    logo = FileField('Logo Upload')
    service_area = StringField('Service Area Coverage', validators=[DataRequired()])
    services = StringField('Services', validators=[DataRequired()])

@app.route('/')
def index():
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

@app.route('/dual-interface', methods=['GET', 'POST'])
def dual_interface():
    provider_form = LaundryProviderForm()
    if provider_form.validate_on_submit():
        new_provider = {
            'business_name': provider_form.business_name.data,
            'tax_number': provider_form.tax_number.data,
            'location': provider_form.location.data,
            'price_range': provider_form.price_range.data,
            'delivery_options': provider_form.delivery_options.data,
            'fabric_types': provider_form.fabric_types.data,
            'logo': provider_form.logo.data.filename if provider_form.logo.data else None,
            'service_area': provider_form.service_area.data,
            'services': provider_form.services.data
        }
        laundry_providers.append(new_provider)
        flash('Registration successful!', 'success')
        return redirect(url_for('dual_interface'))
    
    filtered_providers = []
    if request.method == 'POST' and 'location' in request.form:
        location = request.form['location']
        delivery_option = request.form['delivery_option']
        filtered_providers = [p for p in laundry_providers if p['location'] == location and delivery_option in p['delivery_options']]
    
    return render_template('dual_interface.html', provider_form=provider_form, providers=laundry_providers, filtered_providers=filtered_providers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)