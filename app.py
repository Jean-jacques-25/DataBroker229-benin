from flask import Flask, render_template
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///databroker229.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Routes publiques
@app.route('/')
@app.route('/index')
def public():
    return render_template('public.html')

@app.route('/login')
def login():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# API Blueprint simple (juste pour tester)
@app.route('/api/test')
def api_test():
    return {'status': 'ok', 'message': 'API working'}

if __name__ == '__main__':
    app.run(debug=False)
