import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initiate SQLAlchemy globally so models can import
db = SQLAlchemy()

def create_app():
    # Instantiate Flask with static and template config
    flask_app = Flask(__name__,
                      template_folder="../templates",
                      static_folder="../static",
                      static_url_path="")
    # Enable Gzip compression
    from flask_compress import Compress
    Compress(flask_app)

    # Cache headers for static files
    @flask_app.after_request
    def add_cache_headers(response):
        response.cache_control.max_age = 3600
        response.cache_control.public = True
        return response 

    # Load settings from config
    flask_app.config.from_object("config.Config")

    # Enable CORS
    CORS(flask_app)

    # Enable HTML/CSS/JS minification
    from flask_minify import minify
    minify(app=flask_app, html=True, js=True, cssless=True)

    # Bind the db to the app
    db.init_app(flask_app)

    # Register blueprints and routes
    from app.routes import api as api_blueprint
    flask_app.register_blueprint(api_blueprint)

    # Serve service worker
    @flask_app.route("/service-worker.js")
    def serve_sw():
        return send_from_directory(flask_app.static_folder, "service-worker.js")

    # Serve the main client layout at standard URLs
    @flask_app.route("/")
    @flask_app.route("/index")
    def public():
        from flask import render_template
        return render_template("public.html")

    @flask_app.route("/login")
    def login():
        from flask import render_template
        return render_template("home.html")

    @flask_app.route("/dashboard")
    def dashboard():
        from flask import render_template
        return render_template("dashboard.html")

    # Create tables automatically inside context
    with flask_app.app_context():
        try:
            db.create_all()
            print("PostgreSQL/SQLite tables verified and created successfully.")
        except Exception as e:
            print(f"Failed to bootstrap database models: {e}")

    return flask_app
