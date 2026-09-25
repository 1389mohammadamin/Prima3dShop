from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, 
                template_folder='interfaces/templates',
                static_folder='interfaces/static')
    
    # تنظیمات
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True
    
    # وابستگی‌ها
    from config.database import db, init_db
    init_db(app)
    
    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.infrastructure.database.models import User
        return User.query.get(int(user_id))
    
    # CORS
    CORS(app)
    
    # Rate Limiting
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    limiter.init_app(app)
    
    # ثبت Blueprints
    register_blueprints(app)
    
    # ثبت خطاها
    register_error_handlers(app)
    
    return app

def register_blueprints(app):
    from app.interfaces.web.routes.main_routes import main_bp
    from app.interfaces.web.routes.admin_routes import admin_bp
    from app.interfaces.web.api.product_api import product_api_bp
    from app.interfaces.web.api.user_api import user_api_bp
    from app.interfaces.web.api.order_api import order_api_bp
    
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(product_api_bp, url_prefix='/api/products')
    app.register_blueprint(user_api_bp, url_prefix='/api/users')
    app.register_blueprint(order_api_bp, url_prefix='/api/orders')

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not Found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal Server Error'}, 500