from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.infrastructure.database.models import db, User, Product, Category, Order
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """دکوریتور برای بررسی ادمین بودن کاربر"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('شما دسترسی به این بخش ندارید!', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """داشبورد مدیریت"""
    # آمار کلی
    stats = {
        'total_products': Product.query.count(),
        'total_users': User.query.count(),
        'total_orders': Order.query.count(),
        'pending_orders': Order.query.filter_by(status='pending').count(),
        'total_revenue': db.session.query(db.func.sum(Order.total_amount)).filter_by(status='delivered').scalar() or 0,
        'new_orders_today': Order.query.filter(db.func.date(Order.created_at) == datetime.utcnow().date()).count(),
    }
    
    # آخرین سفارشات
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)

@admin_bp.route('/products')
@login_required
@admin_required
def manage_products():
    """مدیریت محصولات"""
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_product():
    """ایجاد محصول جدید"""
    if request.method == 'POST':
        # دریافت داده‌ها از فرم
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        category_id = request.form.get('category_id')
        
        # اعتبارسنجی ساده
        if not name or not price:
            flash('نام و قیمت محصول الزامی است!', 'error')
            return redirect(url_for('admin.create_product'))
        
        try:
            # ایجاد محصول جدید
            product = Product(
                name=name,
                slug=name.replace(' ', '-').lower(),  # ساده‌سازی slug
                description=description,
                price=float(price),
                quantity=int(quantity) if quantity else 0,
                category_id=int(category_id) if category_id else None,
                user_id=current_user.id,
                status='draft',
                is_available=True
            )
            
            db.session.add(product)
            db.session.commit()
            
            flash('محصول با موفقیت ایجاد شد!', 'success')
            return redirect(url_for('admin.manage_products'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'خطا در ایجاد محصول: {str(e)}', 'error')
    
    # GET - نمایش فرم
    categories = Category.query.all()
    return render_template('admin/product_form.html', categories=categories)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    """ویرایش محصول"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            product.name = request.form.get('name', product.name)
            product.description = request.form.get('description', product.description)
            product.price = float(request.form.get('price', product.price))
            product.quantity = int(request.form.get('quantity', product.quantity))
            product.category_id = int(request.form.get('category_id', product.category_id))
            product.status = request.form.get('status', product.status)
            product.is_available = bool(request.form.get('is_available'))
            
            db.session.commit()
            flash('محصول با موفقیت ویرایش شد!', 'success')
            return redirect(url_for('admin.manage_products'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'خطا در ویرایش محصول: {str(e)}', 'error')
    
    categories = Category.query.all()
    return render_template('admin/product_form.html', product=product, categories=categories)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    """حذف محصول"""
    product = Product.query.get_or_404(product_id)
    
    try:
        # ابتدا تصاویر و وابسته‌ها را حذف کنید
        for image in product.images:
            db.session.delete(image)
        
        db.session.delete(product)
        db.session.commit()
        flash('محصول با موفقیت حذف شد!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'خطا در حذف محصول: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_products'))

@admin_bp.route('/orders')
@login_required
@admin_required
def manage_orders():
    """مدیریت سفارشات"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/orders/<int:order_id>')
@login_required
@admin_required
def view_order(order_id):
    """مشاهده جزئیات سفارش"""
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/orders/update-status/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    """به‌روزرسانی وضعیت سفارش"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status and new_status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('وضعیت سفارش با موفقیت به‌روزرسانی شد!', 'success')
    
    return redirect(url_for('admin.view_order', order_id=order_id))

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    """مدیریت کاربران"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/toggle-admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """تغییر وضعیت ادمین کاربر"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('نمی‌توانید نقش خودتان را تغییر دهید!', 'error')
        return redirect(url_for('admin.manage_users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'نقش کاربر {user.username} با موفقیت تغییر کرد!', 'success')
    
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/categories')
@login_required
@admin_required
def manage_categories():
    """مدیریت دسته‌بندی‌ها"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categories/create', methods=['POST'])
@login_required
@admin_required
def create_category():
    """ایجاد دسته‌بندی جدید"""
    name = request.form.get('name')
    description = request.form.get('description')
    parent_id = request.form.get('parent_id')
    
    if not name:
        flash('نام دسته‌بندی الزامی است!', 'error')
        return redirect(url_for('admin.manage_categories'))
    
    try:
        category = Category(
            name=name,
            slug=name.replace(' ', '-').lower(),
            description=description,
            parent_id=int(parent_id) if parent_id else None
        )
        
        db.session.add(category)
        db.session.commit()
        flash('دسته‌بندی با موفقیت ایجاد شد!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'خطا در ایجاد دسته‌بندی: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_categories'))