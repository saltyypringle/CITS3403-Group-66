from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from SukiScan.config import Config
from flask_wtf import CSRFProtect
import os

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
UPLOAD_FOLDER = 'Sukiscan/static/image_checker'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def create_app(config_class=Config):
    app = Flask(__name__)
    app.secret_key = "SukiScan"
    
    if config_class:
        app.config.from_object(config_class)
    else:
        from SukiScan.config import Config
        app.config.from_object(Config)
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    
    from SukiScan.blueprints import blueprint
    app.register_blueprint(blueprint)
    
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    from SukiScan.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=generate_csrf)
    
    from SukiScan import route, forms, models 
    
    return app
