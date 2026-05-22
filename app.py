from flask import Flask, render_template
from flask_cors import CORS
import os

app = Flask(__name__, 
    template_folder='templates', 
    static_folder='static',
    static_url_path='/static'
)

CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///databroker229.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database - UNE SEULE FOIS
from backend import db
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Import backend routes (Blueprint) - APRÈS db.init_app
from backend.routes import api

# Register Blueprint
app.register_blueprint(api)

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

if __name__ == '__main__':
    app.run(debug=False)
