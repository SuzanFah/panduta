from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = Flask(__name__)
import os
app.config['SECRET_KEY'] = os.urandom(24)
app.config['DEBUG'] = True

# Placeholder for storing laundry provider data (replace with database later)
laundry_providers = []

from wtforms import StringField, SelectMultipleField, FloatField, FileField
from wtforms.validators import DataRequired, Length, NumberRange

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
@app.route('/', methods=['GET', 'POST'])
def home():
    provider_form = LaundryProviderForm()
    if provider_form.validate_on_submit():
        new_provider = {
            'business_name': provider_form.business_name.data,
            'tax_number': provider_form.tax_number.data,
            'location': provider_form.location.data,
            'price_range': (provider_form.price_range_min.data, provider_form.price_range_max.data),
            'delivery_options': provider_form.delivery_options.data,
            'fabric_types': provider_form.fabric_types.data,
            'logo': provider_form.logo.data.filename if provider_form.logo.data else None,
            'service_area': provider_form.service_area.data,
            'services': provider_form.services.data
        }
        laundry_providers.append(new_provider)
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    
    filtered_providers = []
    if request.method == 'POST' and 'location' in request.form:
        location = request.form['location']
        delivery_option = request.form['delivery_option']
        fabric_type = request.form.get('fabric_type')
        sort_by = request.form.get('sort_by', 'rating')
        filtered_providers = [p for p in laundry_providers if p['location'] == location and delivery_option in p['delivery_options']]
        if fabric_type:
            filtered_providers = [p for p in filtered_providers if fabric_type in p['fabric_types']]
        if sort_by == 'rating':
            filtered_providers.sort(key=lambda x: x.get('rating', 0), reverse=True)
        elif sort_by == 'price_low':
            filtered_providers.sort(key=lambda x: x['price_range'][0])
        elif sort_by == 'price_high':
            filtered_providers.sort(key=lambda x: x['price_range'][1], reverse=True)
    
    return render_template('dual_interface.html', provider_form=provider_form, providers=laundry_providers, filtered_providers=filtered_providers)

@app.route('/dual-interface')
def dual_interface():
    return redirect(url_for('home'))

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', (error))
    return "500 error", 500

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
