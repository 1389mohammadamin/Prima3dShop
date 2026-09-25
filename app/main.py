from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

app = Flask(__name__, 
            template_folder='interfaces/templates',
            static_folder='interfaces/static',
            static_url_path='/static')

app.config['SECRET_KEY'] = 'my-fixed-secret-key-for-session-123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), '3dshop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# ===== مدل‌ها =====
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    material = db.Column(db.String(100))
    color = db.Column(db.String(50), nullable=True)
    color_name = db.Column(db.String(50), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='published')
    image_url = db.Column(db.String(300), nullable=True)
    discount_price = db.Column(db.Numeric(10, 2), nullable=True)
    sales_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    product = db.relationship('Product')

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    product = db.relationship('Product', backref='reviews')
    user = db.relationship('User', backref='reviews')
    order = db.relationship('Order', backref='reviews')

class Coupon(db.Model):
    __tablename__ = 'coupons'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    discount_type = db.Column(db.String(20), default='percent')
    discount_value = db.Column(db.Numeric(10, 2), nullable=False)
    min_order_amount = db.Column(db.Numeric(10, 2), default=0)
    max_discount_amount = db.Column(db.Numeric(10, 2), nullable=True)
    usage_limit = db.Column(db.Integer, default=1)
    used_count = db.Column(db.Integer, default=0)
    expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    usages = db.relationship('CouponUsage', backref='coupon', cascade='all, delete-orphan')

class CouponUsage(db.Model):
    __tablename__ = 'coupon_usages'
    id = db.Column(db.Integer, primary_key=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    discount_amount = db.Column(db.Numeric(10, 2), nullable=False)
    used_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user = db.relationship('User', backref='coupon_usages')
    order = db.relationship('Order', backref='coupon_usage')

class PaymentConfirmation(db.Model):
    __tablename__ = 'payment_confirmations'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tracking_number = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    order = db.relationship('Order', backref='payment_confirmation')
    user = db.relationship('User', backref='payment_confirmations')

with app.app_context():
    db.create_all()
    print("✅ دیتابیس آماده است.")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

CORS(app)
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

# ===== فیلترهای سفارشی =====
@app.template_filter('format_currency')
def format_currency(value):
    if value is None:
        return '۰ تومان'
    try:
        return f"{int(value):,} تومان"
    except:
        return '۰ تومان'

# ===== مسیرهای اصلی =====
@app.route('/')
def index():
    best_sellers = Product.query.order_by(Product.sales_count.desc()).limit(5).all()
    latest_products = Product.query.filter_by(is_available=True, status='published').order_by(Product.created_at.desc()).limit(4).all()
    return render_template('index.html', best_sellers=best_sellers, latest_products=latest_products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# ===== مسیرهای محصولات =====
@app.route('/products')
def products():
    search = request.args.get('search', '').strip()
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    material = request.args.get('material', '')
    sort = request.args.get('sort', 'newest')
    
    query = Product.query.filter_by(is_available=True, status='published')
    
    if search:
        query = query.filter(
            db.or_(
                Product.name.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%')
            )
        )
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    if material:
        query = query.filter(Product.material.ilike(f'%{material}%'))
    
    if sort == 'newest':
        query = query.order_by(Product.id.desc())
    elif sort == 'oldest':
        query = query.order_by(Product.id.asc())
    elif sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'name_asc':
        query = query.order_by(Product.name.asc())
    else:
        query = query.order_by(Product.id.desc())
    
    all_products = query.all()
    categories = Category.query.all()
    
    materials = db.session.query(Product.material).filter(Product.material.isnot(None)).distinct().all()
    materials = [m[0] for m in materials if m[0]]
    
    return render_template('products.html', 
                          products=all_products, 
                          categories=categories,
                          materials=materials,
                          search=search,
                          category_id=category_id,
                          min_price=min_price,
                          max_price=max_price,
                          material=material,
                          sort=sort)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# ===== مسیرهای سبد خرید =====
@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = request.form.get('quantity', 1, type=int)
    
    product = db.session.get(Product, product_id)
    
    if not product:
        flash('محصول مورد نظر یافت نشد!', 'error')
        return redirect(url_for('products'))
    
    if quantity > product.quantity:
        flash(f'تعداد درخواستی بیشتر از موجودی است! (موجودی: {product.quantity})', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    cart = session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    
    session['cart'] = cart
    session.modified = True
    
    flash(f'{product.name} به سبد خرید اضافه شد!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.query.filter_by(id=int(product_id)).first()
            if product:
                item_total = product.price * quantity
                total_price += item_total
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'item_total': item_total
                })
            else:
                cart.pop(str(product_id), None)
                session['cart'] = cart
                session.modified = True
        except Exception as e:
            print(f"❌ خطا: {e}")

    coupon_data = session.get('coupon')
    discount_amount = 0
    coupon_code = None
    if coupon_data:
        discount_amount = coupon_data.get('discount_amount', 0)
        coupon_code = coupon_data.get('code')
        if discount_amount > total_price:
            discount_amount = total_price
            coupon_data['discount_amount'] = discount_amount
            session['coupon'] = coupon_data
            session.modified = True
        total_price -= discount_amount

    return render_template('cart.html', 
                          cart_items=cart_items, 
                          total_price=total_price,
                          discount_amount=discount_amount,
                          coupon_code=coupon_code)

@app.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        session.modified = True
        flash('محصول از سبد خرید حذف شد!', 'success')
    
    return redirect(url_for('cart'))

@app.route('/update-cart-item/<int:product_id>', methods=['POST'])
def update_cart_item(product_id):
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity < 1:
        flash('تعداد باید حداقل ۱ باشد!', 'error')
        return redirect(url_for('cart'))
    
    product = Product.query.get_or_404(product_id)
    
    if quantity > product.quantity:
        flash(f'تعداد درخواستی بیشتر از موجودی است!', 'error')
        return redirect(url_for('cart'))
    
    cart = session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)] = quantity
        session['cart'] = cart
        session.modified = True
        flash('تعداد محصول به‌روزرسانی شد!', 'success')
    
    return redirect(url_for('cart'))

# ===== مسیرهای احراز هویت =====
@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('خوش آمدید!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('نام کاربری یا رمز عبور اشتباه است!', 'error')
    
    return render_template('auth/login.html')

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('رمز عبور مطابقت ندارد!', 'error')
            return render_template('auth/register.html')
        
        accept_terms = request.form.get('accept_terms')
        if not accept_terms:
            flash('برای ثبت‌نام باید قوانین و مقررات را بپذیرید.', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('نام کاربری تکراری است!', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('ایمیل تکراری است!', 'error')
            return render_template('auth/register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            full_name=username,
            is_admin=False,
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        flash('ثبت‌نام با موفقیت انجام شد!', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    flash('خارج شدید!', 'success')
    return redirect(url_for('index'))

# ===== مسیرهای مدیریت =====
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    stats = {
        'total_products': Product.query.count(),
        'total_users': User.query.count(),
        'total_categories': Category.query.count(),
        'total_orders': Order.query.count(),
    }
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/products')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/create', methods=['GET', 'POST'])
@login_required
def admin_product_create():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity', 0)
        category_id = request.form.get('category_id', type=int)
        material = request.form.get('material')
        discount_price = request.form.get('discount_price')
        
        if not name or not price:
            flash('نام و قیمت الزامی است!', 'error')
            return redirect(url_for('admin_product_create'))
        
        try:
            import re
            # ساخت slug از نام محصول
            slug = re.sub(r'[^\w\-]', '-', name.lower()) if name else ''
            slug = slug[:100] if slug else str(len(Product.query.all()) + 1)
            
            product = Product(
                name=name,
                slug=slug,
                description=description,
                price=Decimal(str(price)),
                quantity=int(quantity) if quantity else 0,
                category_id=category_id if category_id else None,
                material=material,
                discount_price=Decimal(str(discount_price)) if discount_price else None
            )
            db.session.add(product)
            db.session.commit()
            
            flash('محصول با موفقیت اضافه شد!', 'success')
            return redirect(url_for('admin_product_variants', product_id=product.id))
        except Exception as e:
            db.session.rollback()
            flash(f'خطا: {str(e)}', 'error')
    
    categories = Category.query.all()
    return render_template('admin/product_form.html', product=None, categories=categories)

    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    return render_template('admin/products.html', products=products)



@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def admin_product_edit(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        try:
            product.name = request.form.get('name')
            product.description = request.form.get('description')
            product.price = Decimal(str(request.form.get('price')))
            product.quantity = int(request.form.get('quantity', 0))
            product.category_id = int(request.form.get('category_id')) if request.form.get('category_id') else None
            product.material = request.form.get('material')
            product.discount_price = Decimal(str(request.form.get('discount_price'))) if request.form.get('discount_price') else None
            product.color = request.form.get('color')
            product.color_name = request.form.get('color_name')
            product.is_available = 'is_available' in request.form
            product.status = request.form.get('status', 'published')
            
            # آپلود تصویر جدید
            if 'image' in request.files:
                image_file = request.files['image']
                if image_file and image_file.filename != '':
                    import os
                    import random
                    import string
                    from werkzeug.utils import secure_filename
                    
                    # حذف تصویر قبلی
                    if product.image_url:
                        old_path = product.image_url.replace('/static/', 'app/interfaces/static/')
                        if os.path.exists(old_path):
                            try:
                                os.remove(old_path)
                            except:
                                pass
                    
                    ext = image_file.filename.rsplit('.', 1)[1].lower() if '.' in image_file.filename else 'jpg'
                    filename = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=20))}.{ext}"
                    os.makedirs('app/interfaces/static/images/products', exist_ok=True)
                    save_path = os.path.join('app/interfaces/static/images/products', filename)
                    image_file.save(save_path)
                    product.image_url = f'/static/images/products/{filename}'
            
            db.session.commit()
            flash('محصول با موفقیت ویرایش شد!', 'success')
            return redirect(url_for('admin_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'خطا: {str(e)}', 'error')
    
    return render_template('admin/product_form.html', product=product, categories=categories)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@login_required
def admin_product_delete(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash('محصول با موفقیت حذف شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/categories')
@login_required
def admin_categories():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/create', methods=['POST'])
@login_required
def admin_category_create():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        flash('نام دسته‌بندی الزامی است!', 'error')
        return redirect(url_for('admin_categories'))
    
    try:
        category = Category(
            name=name,
            slug=name.replace(' ', '-').lower(),
            description=description
        )
        db.session.add(category)
        db.session.commit()
        flash('دسته‌بندی با موفقیت ایجاد شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def admin_category_delete(category_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    category = Category.query.get_or_404(category_id)
    
    try:
        db.session.delete(category)
        db.session.commit()
        flash('دسته‌بندی با موفقیت حذف شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_categories'))

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/toggle-status/<int:user_id>', methods=['POST'])
@login_required
def admin_user_toggle_status(user_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('نمی‌توانید وضعیت خودتان را تغییر دهید!', 'error')
        return redirect(url_for('admin_users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    flash(f'وضعیت کاربر "{user.username}" تغییر کرد!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/toggle-admin/<int:user_id>', methods=['POST'])
@login_required
def admin_user_toggle_admin(user_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('نمی‌توانید نقش خودتان را تغییر دهید!', 'error')
        return redirect(url_for('admin_users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'نقش کاربر "{user.username}" تغییر کرد!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/order/<int:order_id>')
@login_required
def admin_order_detail(order_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@app.route('/admin/order/<int:order_id>/update-status', methods=['POST'])
@login_required
def admin_update_order_status(order_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'paid', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'وضعیت سفارش به "{new_status}" تغییر کرد!', 'success')
    else:
        flash('وضعیت نامعتبر!', 'error')
    
    return redirect(url_for('admin_order_detail', order_id=order_id))

@app.route('/admin/coupons')
@login_required
def admin_coupons():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    coupons = Coupon.query.order_by(Coupon.created_at.desc()).all()
    return render_template('admin/coupons.html', coupons=coupons)

@app.route('/admin/coupons/create', methods=['GET', 'POST'])
@login_required
def admin_coupon_create():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        description = request.form.get('description')
        discount_type = request.form.get('discount_type')
        discount_value_str = request.form.get('discount_value')
        min_order_amount_str = request.form.get('min_order_amount')
        max_discount_amount_str = request.form.get('max_discount_amount')
        usage_limit_str = request.form.get('usage_limit', 1)
        expires_at = request.form.get('expires_at')
        is_active = 'is_active' in request.form
        
        if not code:
            flash('کد تخفیف الزامی است!', 'error')
            return render_template('admin/coupon_form.html')
        
        if Coupon.query.filter_by(code=code).first():
            flash('این کد تخفیف قبلاً وجود دارد!', 'error')
            return render_template('admin/coupon_form.html')
        
        try:
            discount_value = float(discount_value_str) if discount_value_str else 0
            if discount_value <= 0:
                flash('مقدار تخفیف باید بزرگتر از صفر باشد!', 'error')
                return render_template('admin/coupon_form.html')
            
            if discount_type == 'percent' and discount_value > 100:
                flash('تخفیف درصدی نمی‌تواند بیشتر از ۱۰۰ باشد!', 'error')
                return render_template('admin/coupon_form.html')
            
            min_order_amount = float(min_order_amount_str) if min_order_amount_str else 0
            if min_order_amount < 0:
                flash('حداقل مبلغ سفارش نمی‌تواند منفی باشد!', 'error')
                return render_template('admin/coupon_form.html')
            
            max_discount_amount = float(max_discount_amount_str) if max_discount_amount_str else None
            if max_discount_amount is not None and max_discount_amount < 0:
                flash('حداکثر تخفیف نمی‌تواند منفی باشد!', 'error')
                return render_template('admin/coupon_form.html')
            
            usage_limit = int(usage_limit_str) if usage_limit_str else 1
            if usage_limit < 1:
                flash('تعداد دفعات استفاده باید حداقل ۱ باشد!', 'error')
                return render_template('admin/coupon_form.html')
            
            expires_at_date = None
            if expires_at:
                try:
                    expires_at_date = datetime.strptime(expires_at, '%Y-%m-%d')
                except ValueError:
                    flash('فرمت تاریخ انقضا نامعتبر است!', 'error')
                    return render_template('admin/coupon_form.html')
            
            coupon = Coupon(
                code=code,
                description=description,
                discount_type=discount_type,
                discount_value=discount_value,
                min_order_amount=min_order_amount,
                max_discount_amount=max_discount_amount,
                usage_limit=usage_limit,
                expires_at=expires_at_date,
                is_active=is_active
            )
            db.session.add(coupon)
            db.session.commit()
            flash(f'کد تخفیف "{code}" با موفقیت ایجاد شد!', 'success')
            return redirect(url_for('admin_coupons'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'خطا: {str(e)}', 'error')
            return render_template('admin/coupon_form.html')
    
    return render_template('admin/coupon_form.html')

@app.route('/admin/coupons/<int:coupon_id>/toggle', methods=['POST'])
@login_required
def admin_coupon_toggle(coupon_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    coupon = Coupon.query.get_or_404(coupon_id)
    coupon.is_active = not coupon.is_active
    db.session.commit()
    flash(f'وضعیت کد تخفیف "{coupon.code}" تغییر کرد!', 'success')
    return redirect(url_for('admin_coupons'))

@app.route('/admin/coupons/<int:coupon_id>/delete', methods=['POST'])
@login_required
def admin_coupon_delete(coupon_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    coupon = Coupon.query.get_or_404(coupon_id)
    db.session.delete(coupon)
    db.session.commit()
    flash('کد تخفیف با موفقیت حذف شد!', 'success')
    return redirect(url_for('admin_coupons'))

@app.route('/admin/announcement', methods=['GET', 'POST'])
@login_required
def admin_announcement():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    global announcement, announcement_link, announcement_page
    
    if request.method == 'POST':
        announcement = request.form.get('announcement')
        announcement_link = request.form.get('announcement_link')
        announcement_page = request.form.get('announcement_page', 'all')
        flash('اعلان با موفقیت به‌روزرسانی شد!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/announcement.html', 
                          announcement=announcement, 
                          announcement_link=announcement_link,
                          announcement_page=announcement_page)

@app.route('/admin/discounts')
@login_required
def admin_discounts():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('admin/discounts.html', products=products)

@app.route('/admin/payment-confirmations')
@login_required
def admin_payment_confirmations():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    confirmations = PaymentConfirmation.query.order_by(PaymentConfirmation.created_at.desc()).all()
    return render_template('admin/payment_confirmations.html', confirmations=confirmations)

@app.route('/admin/payment-confirmation/<int:confirmation_id>/<action>', methods=['POST'])
@login_required
def admin_payment_confirmation_action(confirmation_id, action):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    confirmation = PaymentConfirmation.query.get_or_404(confirmation_id)
    
    if action == 'approve':
        confirmation.status = 'approved'
        confirmation.order.status = 'paid'
        flash('پرداخت تایید شد!', 'success')
    elif action == 'reject':
        confirmation.status = 'rejected'
        confirmation.order.status = 'pending'
        flash('پرداخت رد شد!', 'error')
    else:
        flash('عملیات نامعتبر!', 'error')
    
    db.session.commit()
    return redirect(url_for('admin_payment_confirmations'))

# ===== مسیرهای سفارشات و پرداخت =====
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not current_user.is_authenticated:
        flash('لطفاً ابتدا وارد حساب خود شوید.', 'warning')
        return redirect(url_for('login'))
    
    cart = session.get('cart', {})
    if not cart:
        flash('سبد خرید شما خالی است!', 'error')
        return redirect(url_for('cart'))
    
    if request.method == 'POST':
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        if not address or not phone:
            flash('لطفاً تمام اطلاعات را وارد کنید!', 'error')
            cart_items = []
            total_price = 0
            for product_id, quantity in cart.items():
                product = Product.query.get(int(product_id))
                if product:
                    item_total = product.price * quantity
                    total_price += item_total
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'item_total': item_total
                    })
            return render_template('checkout.html', cart_items=cart_items, total_price=total_price)
        
        try:
            import random
            import string
            order_number = ''.join(random.choices(string.digits, k=10))
            
            total_amount = 0
            for product_id, quantity in cart.items():
                product = Product.query.get(int(product_id))
                if product:
                    total_amount += product.price * quantity
            
            order = Order(
                user_id=current_user.id,
                order_number=order_number,
                total_amount=total_amount,
                shipping_address=address,
                phone=phone,
                status='pending'
            )
            db.session.add(order)
            db.session.flush()
            
            for product_id, quantity in cart.items():
                product = Product.query.get(int(product_id))
                if product:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        product_name=product.name,
                        product_price=product.price,
                        quantity=quantity,
                        total_price=product.price * quantity
                    )
                    db.session.add(order_item)
                    product.quantity -= quantity
            
            db.session.commit()
            
            session.pop('cart', None)
            session.modified = True
            
            flash(f'سفارش شما با شماره {order_number} با موفقیت ثبت شد!', 'success')
            return redirect(url_for('payment_confirm', order_id=order.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'خطا در ثبت سفارش: {str(e)}', 'error')
            return redirect(url_for('cart'))
    
    cart_items = []
    total_price = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
    
    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

@app.route('/payment/confirm/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment_confirm(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('شما دسترسی به این سفارش ندارید!', 'error')
        return redirect(url_for('profile'))
    
    if order.status in ['paid', 'delivered']:
        flash('این سفارش قبلاً پرداخت شده است!', 'warning')
        return redirect(url_for('order_detail', order_id=order_id))
    
    if request.method == 'POST':
        tracking_number = request.form.get('tracking_number')
        description = request.form.get('description')
        accept_terms = request.form.get('accept_terms')
        accept_terms_2 = request.form.get('accept_terms_2')
        
        if not tracking_number:
            flash('لطفاً شماره پیگیری را وارد کنید!', 'error')
            return render_template('payment_confirm.html', order=order)
        
        if not accept_terms or not accept_terms_2:
            flash('برای تایید پرداخت باید تعهدنامه و قوانین را بپذیرید!', 'error')
            return render_template('payment_confirm.html', order=order)
        
        confirmation = PaymentConfirmation(
            order_id=order.id,
            user_id=current_user.id,
            tracking_number=tracking_number,
            description=description,
            status='pending'
        )
        db.session.add(confirmation)
        
        order.status = 'payment_pending'
        db.session.commit()
        
        flash('رسید شما با موفقیت ثبت شد. پس از تایید، سفارش شما ارسال خواهد شد.', 'success')
        return redirect(url_for('order_detail', order_id=order.id))
    
    return render_template('payment_confirm.html', order=order)

@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('شما دسترسی به این سفارش ندارید!', 'error')
        return redirect(url_for('index'))
    
    return render_template('order_detail.html', order=order)

@app.route('/profile')
@login_required
def profile():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('profile.html', orders=orders)

@app.route('/debug-cart')
def debug_cart():
    cart = session.get('cart', {})
    return f"""
    <h1>Debug Cart</h1>
    <p>سبد خرید: <pre>{cart}</pre></p>
    <p>تمام Session: <pre>{dict(session)}</pre></p>
    <a href="/cart">بازگشت به سبد خرید</a>
    """

# ===== اعلان سراسری =====
announcement = None
announcement_link = None
announcement_page = "all"

@app.context_processor
def inject_announcement():
    global announcement, announcement_link, announcement_page
    from datetime import datetime
    current_page = request.endpoint or ""
    show = False
    if announcement_page == "all":
        show = True
    elif announcement_page == "home" and current_page == "index":
        show = True
    elif announcement_page == "products" and current_page == "products":
        show = True
    elif announcement_page == "product" and current_page == "product_detail":
        show = True
    return {
        "announcement": announcement if show else None,
        "announcement_link": announcement_link if show else None,
        "now": datetime.now()
    }

# ===== هندلرهای خطا =====
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

# ===== تابع create_app =====

@app.route('/admin/products/<int:product_id>/variants')
@login_required
def admin_product_variants(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    product = Product.query.get_or_404(product_id)
    variants = ProductVariant.query.filter_by(product_id=product_id).all()
    return render_template('admin/variants.html', product=product, variants=variants)

@app.route('/admin/products/<int:product_id>/variants/create', methods=['POST'])
@login_required
def admin_variant_create(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    
    name = request.form.get('name')
    value = request.form.get('value')
    color_code = request.form.get('color_code')
    price_adjustment = request.form.get('price_adjustment', 0)
    quantity = request.form.get('quantity', 0)
    sku = request.form.get('sku')
    
    if not name or not value or not sku:
        flash('نام مقدار و SKU الزامی است!', 'error')
        return redirect(url_for('admin_product_variants', product_id=product_id))
    
    try:
        variant = ProductVariant(
            product_id=product_id,
            name=name,
            value=value,
            color_code=color_code if color_code else None,
            price_adjustment=Decimal(str(price_adjustment)) if price_adjustment else 0,
            quantity=int(quantity) if quantity else 0,
            sku=sku
        )
        db.session.add(variant)
        db.session.commit()
        flash('تنوع با موفقیت اضافه شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_product_variants', product_id=product_id))

@app.route('/admin/variants/<int:variant_id>/delete', methods=['POST'])
@login_required
def admin_variant_delete(variant_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    variant = ProductVariant.query.get_or_404(variant_id)
    product_id = variant.product_id
    
    try:
        db.session.delete(variant)
        db.session.commit()
        flash('تنوع حذف شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_product_variants', product_id=product_id))


# ===== مدل تنوع محصولات =====
class ProductVariant(db.Model):
    __tablename__ = 'product_variants'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    color_code = db.Column(db.String(20), nullable=True)
    price_adjustment = db.Column(db.Numeric(10, 2), default=0.00)
    quantity = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    product = db.relationship('Product', backref='variants')

# ===== مدل مشخصات فنی =====
class ProductSpecification(db.Model):
    __tablename__ = 'product_specifications'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    spec_key = db.Column(db.String(100), nullable=False)
    spec_value = db.Column(db.String(200), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    product = db.relationship('Product', backref='specifications')

def create_app():
    return app

