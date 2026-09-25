# app/interfaces/web/admin.py
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from functools import wraps
from config.database import db
from app.infrastructure.database.models import User, Product, Category

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            from flask import redirect, url_for, flash
            flash('لطفاً ابتدا وارد شوید.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin:
            from flask import abort
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """داشبورد مدیریت"""
    stats = {
        'total_products': Product.query.count(),
        'total_users': User.query.count(),
        'total_categories': Category.query.count(),
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/products')
@login_required
@admin_required
def products():
    """مدیریت محصولات"""
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """مدیریت کاربران"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """مدیریت دسته‌بندی‌ها"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)