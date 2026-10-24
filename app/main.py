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
    # فیلدهای جدید
    full_name = db.Column(db.String(200), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    province = db.Column(db.String(50), nullable=True)
    shipping_cost = db.Column(db.Numeric(10, 2), default=0)
    receipt_image = db.Column(db.String(300), nullable=True)
    coupon_code = db.Column(db.String(50), nullable=True)
    discount_amount = db.Column(db.Numeric(10, 2), default=0)
    
    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')

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



class ProductSpecification(db.Model):
    __tablename__ = 'product_specifications'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    spec_key = db.Column(db.String(100), nullable=False)
    spec_value = db.Column(db.String(200), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    product = db.relationship('Product', backref='specifications')


# ===== صفحه پرداخت =====
@app.route('/order/<int:order_id>/payment')
@login_required
def payment_page(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    return render_template('payment.html', order=order)


# ===== تأیید پرداخت =====
@app.route('/order/<int:order_id>/confirm-payment', methods=['POST'])
@login_required
def confirm_payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))

    order.status = 'pending_confirmation'
    db.session.commit()

    flash('✅ درخواست تأیید پرداخت شما ثبت شد. پس از بررسی، سفارش شما پردازش می‌شود.', 'success')
    return redirect(url_for('order_detail', order_id=order.id))



# ===== دانلود فیش =====
@app.route('/admin/order/<int:order_id>/receipt/download')
@login_required
def admin_download_receipt(order_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    order = Order.query.get_or_404(order_id)
    if not order.receipt_image:
        flash('فیشی برای این سفارش آپلود نشده!', 'error')
        return redirect(url_for('admin_order_detail', order_id=order_id))
    filepath = os.path.join('app', 'interfaces', order.receipt_image.lstrip('/'))
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    flash('فایل فیش پیدا نشد!', 'error')
    return redirect(url_for('admin_order_detail', order_id=order_id))


# ===== حذف فیش =====
@app.route('/admin/order/<int:order_id>/receipt/delete', methods=['POST'])
@login_required
def admin_delete_receipt(order_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    order = Order.query.get_or_404(order_id)
    if order.receipt_image:
        filepath = os.path.join('app', 'interfaces', order.receipt_image.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
        order.receipt_image = None
        db.session.commit()
        flash('✅ فیش با موفقیت حذف شد!', 'success')
    return redirect(url_for('admin_order_detail', order_id=order_id))



# ===== آپلود فیش توسط مشتری =====
@app.route('/order/<int:order_id>/upload-receipt', methods=['POST'])
@login_required
def upload_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))

    receipt = request.files.get('receipt')
    if receipt and receipt.filename:
        receipts_dir = os.path.join('app', 'interfaces', 'static', 'receipts')
        os.makedirs(receipts_dir, exist_ok=True)

        import uuid
        ext = os.path.splitext(receipt.filename)[1]
        filename = f"receipt_{order.order_number}_{uuid.uuid4().hex[:8]}{ext}"
        filepath = os.path.join(receipts_dir, filename)
        receipt.save(filepath)
        order.receipt_image = f"/static/receipts/{filename}"
        db.session.commit()
        flash('✅ فیش با موفقیت آپلود شد!', 'success')
    else:
        flash('❌ لطفاً یک عکس انتخاب کنید!', 'error')

    return redirect(url_for('payment_page', order_id=order.id))



# ===== حذف فیش توسط مشتری =====
@app.route('/order/<int:order_id>/receipt/delete', methods=['POST'])
@login_required
def customer_delete_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))

    if order.receipt_image:
        filepath = os.path.join('app', 'interfaces', order.receipt_image.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
        order.receipt_image = None
        db.session.commit()
        flash('✅ فیش با موفقیت حذف شد!', 'success')

    return redirect(url_for('payment_page', order_id=order.id))


@app.route('/apply-coupon', methods=['POST'])
def apply_coupon():
    coupon_code = request.form.get('coupon_code', '').strip().upper()
    if not coupon_code:
        flash('کد تخفیف را وارد کنید!', 'error')
        return redirect(url_for('cart'))
    
    coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()
    if not coupon:
        flash('کد تخفیف نامعتبر است!', 'error')
        return redirect(url_for('cart'))
    
    # ذخیره کد و اطلاعات در سشن
    session['coupon'] = {
        'code': coupon.code,
        'discount_type': coupon.discount_type,
        'discount_value': float(coupon.discount_value),
        'max_discount_amount': float(coupon.max_discount_amount) if coupon.max_discount_amount else None
    }
    session.modified = True
    
    if coupon.discount_type == 'percent':
        flash(f'✅ کد تخفیف {coupon.discount_value}٪ اعمال شد!', 'success')
    else:
        flash(f'✅ کد تخفیف {coupon.discount_value} تومانی اعمال شد!', 'success')
        
    return redirect(url_for('cart'))
    
    coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()
    if not coupon:
        flash('کد تخفیف نامعتبر است!', 'error')
        return redirect(url_for('cart'))
    
    # ذخیره کد و درصد در سشن
    session['coupon'] = {
        'code': coupon.code,
        'discount_percent': float(coupon.discount_percent)
    }
    session.modified = True
    flash(f'✅ کد تخفیف {coupon.discount_percent}٪ اعمال شد!', 'success')
    return redirect(url_for('cart'))

@app.route('/remove-coupon', methods=['POST'])
def remove_coupon():
    session.pop('coupon', None)
    session.modified = True
    flash('کد تخفیف حذف شد!', 'success')
    return redirect(url_for('cart'))


# ===== حذف عکس محصول =====
@app.route('/admin/products/<int:product_id>/delete-image', methods=['POST'])
@login_required
def admin_delete_product_image(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    if product.image_url:
        # حذف فایل از هاست
        filepath = os.path.join('app', 'interfaces', product.image_url.lstrip('/'))
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"خطا در حذف فایل: {e}")
        
        # حذف از دیتابیس
        product.image_url = None
        db.session.commit()
        flash('✅ عکس محصول با موفقیت حذف شد!', 'success')
    else:
        flash('این محصول عکسی ندارد!', 'error')
        
    return redirect(url_for('admin_product_edit', product_id=product.id))



@app.route('/admin/test-upload', methods=['POST'])
@login_required
def test_upload():
    if not current_user.is_admin:
        return "دسترسی غیرمجاز", 403
    
    image = request.files.get('image')
    if image and image.filename != '':
        return f"✅ عکس دریافت شد! نام فایل: {image.filename}"
    return "❌ هیچ عکسی دریافت نشد!"



# ===== مدل تصاویر گالری محصول =====
class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    product = db.relationship('Product', backref=db.backref('gallery_images', cascade='all, delete-orphan'))


# ===== روت‌های گالری تصاویر =====
@app.route('/admin/products/<int:product_id>/gallery/upload', methods=['POST'])
@login_required
def admin_upload_gallery_image(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    images = request.files.getlist('gallery_images')
    
    uploaded_count = 0
    if images:
        upload_dir = os.path.join('app', 'interfaces', 'static', 'images', 'products')
        os.makedirs(upload_dir, exist_ok=True)
        
        import uuid
        for image in images:
            if image and image.filename != '':
                ext = os.path.splitext(image.filename)[1].lower()
                filename = f"gallery_{uuid.uuid4().hex[:10]}{ext}"
                filepath = os.path.join(upload_dir, filename)
                image.save(filepath)
                
                # ذخیره در دیتابیس
                new_img = ProductImage(
                    product_id=product.id,
                    image_url=f"/static/images/products/{filename}",
                    display_order=0
                )
                db.session.add(new_img)
                uploaded_count += 1
    
    db.session.commit()
    flash(f'✅ {uploaded_count} تصویر به گالری اضافه شد!', 'success')
    return redirect(url_for('admin_product_edit', product_id=product.id))


@app.route('/admin/gallery-image/<int:image_id>/delete', methods=['POST'])
@login_required
def admin_delete_gallery_image(image_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    image = ProductImage.query.get_or_404(image_id)
    product_id = image.product_id
    
    # حذف فایل فیزیکی
    filepath = os.path.join('app', 'interfaces', image.image_url.lstrip('/'))
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"خطا در حذف فایل: {e}")
    
    db.session.delete(image)
    db.session.commit()
    
    flash('✅ تصویر از گالری حذف شد!', 'success')
    return redirect(url_for('admin_product_edit', product_id=product_id))


# ===== مدیریت مشخصات فنی =====
@app.route('/admin/products/<int:product_id>/specifications')
@login_required
def admin_product_specifications(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    specs = ProductSpecification.query.filter_by(product_id=product_id).order_by(ProductSpecification.display_order).all()
    return render_template('admin/specifications.html', product=product, specs=specs)

@app.route('/admin/products/<int:product_id>/specifications/create', methods=['POST'])
@login_required
def admin_specification_create(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    spec_key = request.form.get('spec_key')
    spec_value = request.form.get('spec_value')
    display_order = request.form.get('display_order', 0)
    
    if not spec_key or not spec_value:
        flash('عنوان و مقدار مشخصات الزامی است!', 'error')
        return redirect(url_for('admin_product_specifications', product_id=product_id))
    
    try:
        spec = ProductSpecification(
            product_id=product_id,
            spec_key=spec_key,
            spec_value=spec_value,
            display_order=int(display_order) if display_order else 0
        )
        db.session.add(spec)
        db.session.commit()
        flash('✅ مشخصات با موفقیت اضافه شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_product_specifications', product_id=product_id))

@app.route('/admin/specifications/<int:spec_id>/delete', methods=['POST'])
@login_required
def admin_specification_delete(spec_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    spec = ProductSpecification.query.get_or_404(spec_id)
    product_id = spec.product_id
    
    try:
        db.session.delete(spec)
        db.session.commit()
        flash('✅ مشخصات حذف شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_product_specifications', product_id=product_id))


# ===== صفحه تماس با ما =====
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        contact_info = request.form.get('contact')
        message = request.form.get('message')
        
        # اینجا می‌تونید پیام رو توی دیتابیس ذخیره کنید یا ایمیل بفرستید
        # فعلاً فقط یه پیام موفقیت نشون می‌دیم
        flash(f'✅ پیام شما با موفقیت دریافت شد. {name} عزیز، به زودی با شما تماس می‌گیریم.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html')


def create_app():
    return app


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'), nullable=True)
    product_name = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    product = db.relationship('Product')
    variant = db.relationship('ProductVariant')

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
    discount_percent = db.Column(db.Numeric(5, 2), nullable=False)
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
    variant_id = request.form.get('variant_id', type=int)

    product = db.session.get(Product, product_id)

    if not product:
        flash('محصول مورد نظر یافت نشد!', 'error')
        return redirect(url_for('products'))

    if quantity > product.quantity:
        flash(f'تعداد درخواستی بیشتر از موجودی است! (موجودی: {product.quantity})', 'error')
        return redirect(url_for('product_detail', product_id=product_id))

    cart = session.get('cart', {})

    # کلید سبد: product_id:variant_id
    if variant_id:
        cart_key = f"{product_id}:{variant_id}"
    else:
        cart_key = str(product_id)

    if cart_key in cart:
        cart[cart_key] += quantity
    else:
        cart[cart_key] = quantity

    session['cart'] = cart
    session.modified = True

    flash(f'{product.name} به سبد خرید اضافه شد!', 'success')
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for cart_key, quantity in list(cart.items()):
        try:
            # جدا کردن product_id و variant_id
            parts = cart_key.split(':')
            product_id = int(parts[0])
            variant_id = int(parts[1]) if len(parts) > 1 else None

            product = Product.query.filter_by(id=product_id).first()
            if product:
                variant_info = None
                if variant_id:
                    variant = ProductVariant.query.get(variant_id)
                    if variant:
                        variant_info = {
                            'id': variant.id,
                            'name': variant.name,
                            'value': variant.value,
                            'color_code': variant.color_code,
                            'price_adjustment': float(variant.price_adjustment)
                        }

                # محاسبه قیمت نهایی با تغییر قیمت رنگ
                final_price = float(product.price)
                if variant_info:
                    final_price += variant_info['price_adjustment']

                item_total = final_price * quantity
                total_price += item_total
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'item_total': item_total,
                    'final_price': final_price,
                    'variant': variant_info
                })
            else:
                cart.pop(cart_key, None)
                session['cart'] = cart
                session.modified = True
        except Exception as e:
            print(f"❌ خطا: {e}")

    # تخفیف
    coupon_data = session.get('coupon')
    discount_amount = 0
    coupon_code = None
    
    if coupon_data:
        coupon_code = coupon_data.get('code')
        discount_type = coupon_data.get('discount_type', 'percent')
        discount_value = coupon_data.get('discount_value', 0)
        max_discount = coupon_data.get('max_discount_amount')
        
        # محاسبه بر اساس نوع تخفیف
        if discount_type == 'percent':
            discount_amount = (float(total_price) * discount_value) / 100
            if max_discount and discount_amount > max_discount:
                discount_amount = max_discount
        else:
            discount_amount = discount_value
            
        if discount_amount > float(total_price):
            discount_amount = float(total_price)
            
        total_price = Decimal(str(float(total_price) - discount_amount))
    else:
        total_price = Decimal(str(total_price))

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
        price = request.form.get('price', '').replace(',', '').strip()
        quantity = request.form.get('quantity', 0)
        category_id = request.form.get('category_id', type=int)
        material = request.form.get('material')
        discount_price = request.form.get('discount_price', '').replace(',', '').strip()
        
        if not name or not price:
            flash('نام و قیمت الزامی است!', 'error')
            return redirect(url_for('admin_product_create'))
        
        try:
            import re as regex_module
            import uuid
            
            # ساخت slug
            slug = regex_module.sub(r'[^\w\-]', '-', name.lower()) if name else ''
            slug = slug[:100] if slug else str(len(Product.query.all()) + 1)
            
            # ذخیره عکس
            image_url = None
            image = request.files.get('image')
            if image and image.filename != '':
                upload_dir = os.path.join('app', 'interfaces', 'static', 'images', 'products')
                os.makedirs(upload_dir, exist_ok=True)
                ext = os.path.splitext(image.filename)[1].lower()
                filename = f"{uuid.uuid4().hex[:10]}{ext}"
                filepath = os.path.join(upload_dir, filename)
                image.save(filepath)
                image_url = f"/static/images/products/{filename}"
                print(f"✅ عکس ذخیره شد: {filepath}")

            # ساخت محصول
            product = Product(
                name=name,
                slug=slug,
                description=description,
                price=Decimal(str(price.replace(',', '').strip())),
                quantity=int(quantity) if quantity else 0,
                category_id=category_id if category_id else None,
                material=material,
                discount_price=Decimal(str(discount_price.replace(',', '').strip())) if discount_price and discount_price.replace(',', '').strip() else None,
                image_url=image_url,
                is_available=request.form.get('in_stock') == '1',
                status='published' if request.form.get('is_active') == '1' else 'draft'
            )
            
            db.session.add(product)
            db.session.commit()
            
            flash('✅ محصول با موفقیت اضافه شد!', 'success')
            return redirect(url_for('admin_product_variants', product_id=product.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'خطا: {str(e)}', 'error')
            print(f"❌ خطا در ساخت محصول: {e}")
    
    categories = Category.query.all()
    return render_template('admin/product_form.html', product=None, categories=categories)

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def admin_product_edit(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price', '').replace(',', '').strip()
        quantity = request.form.get('quantity', 0)
        category_id = request.form.get('category_id', type=int)
        material = request.form.get('material')
        discount_price = request.form.get('discount_price', '').replace(',', '').strip()
        
        try:
            import re as regex_module
            import uuid
            
            product.name = name
            product.slug = regex_module.sub(r'[^\w\-]', '-', name.lower())[:100]
            product.description = description
            price = price.replace(',', '').strip() if price else '0'
            product.price = Decimal(str(price))
            product.quantity = int(quantity) if quantity else 0
            product.category_id = category_id if category_id else None
            product.material = material
            # فیکس قیمت با تخفیف
            discount_price = discount_price.replace(',', '').strip() if discount_price else ''
            if discount_price:
                try:
                    product.discount_price = Decimal(str(discount_price))
                except:
                    product.discount_price = None
            else:
                product.discount_price = None
            product.is_available = request.form.get('in_stock') == '1'
            product.status = 'published' if request.form.get('is_active') == '1' else 'draft'
            
            # آپلود عکس جدید
            image = request.files.get('image')
            if image and image.filename != '':
                upload_dir = os.path.join('app', 'interfaces', 'static', 'images', 'products')
                os.makedirs(upload_dir, exist_ok=True)
                ext = os.path.splitext(image.filename)[1].lower()
                filename = f"{uuid.uuid4().hex[:10]}{ext}"
                filepath = os.path.join(upload_dir, filename)
                image.save(filepath)
                product.image_url = f"/static/images/products/{filename}"
                print(f"✅ عکس آپدیت شد: {filepath}")
            
            db.session.commit()
            flash('✅ محصول با موفقیت ویرایش شد!', 'success')
            return redirect(url_for('admin_products'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'خطا: {str(e)}', 'error')
            print(f"❌ خطا در ویرایش محصول: {e}")
    
    categories = Category.query.all()
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
@login_required
def checkout():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0

    for cart_key, quantity in list(cart.items()):
        try:
            parts = cart_key.split(':')
            product_id = int(parts[0])
            variant_id = int(parts[1]) if len(parts) > 1 else None

            product = Product.query.get(product_id)
            if product:
                variant_info = None
                if variant_id:
                    variant = ProductVariant.query.get(variant_id)
                    if variant:
                        variant_info = {
                            'id': variant.id,
                            'name': variant.name,
                            'value': variant.value,
                            'color_code': variant.color_code,
                            'price_adjustment': float(variant.price_adjustment)
                        }

                final_price = float(product.price)
                if variant_info:
                    final_price += variant_info['price_adjustment']

                item_total = final_price * quantity
                total_price += item_total
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'item_total': item_total,
                    'final_price': final_price,
                    'variant': variant_info
                })
        except Exception as e:
            print(f"❌ خطا: {e}")

    # محاسبه تخفیف
    coupon_data = session.get('coupon')
    total_discount = 0
    coupon_code = None
    
    if coupon_data:
        coupon_code = coupon_data.get('code')
        discount_type = coupon_data.get('discount_type', 'percent')
        discount_value = coupon_data.get('discount_value', 0)
        max_discount = coupon_data.get('max_discount_amount')
        
        if discount_type == 'percent':
            total_discount = (float(total_price) * discount_value) / 100
            if max_discount and total_discount > max_discount:
                total_discount = max_discount
        else:
            total_discount = discount_value
            
        if total_discount > float(total_price):
            total_discount = float(total_price)
            
        total_price = Decimal(str(float(total_price) - total_discount))

    # محاسبه هزینه پست
    shipping_cost = 0
    try:
        from postal_rates import calculate_shipping
        shipping_cost = calculate_shipping('تهران')
    except:
        shipping_cost = 0

    total_with_shipping = float(total_price) + shipping_cost

    # POST - ثبت سفارش
    if request.method == 'POST':
        try:
            import random
            import string
            order_number = ''.join(random.choices(string.digits, k=10))

            total_amount = 0
            for item in cart_items:
                total_amount += item['item_total']

            order = Order(
                order_number=order_number,
                user_id=current_user.id,
                total_amount=Decimal(str(total_price + shipping_cost)),
                shipping_address=request.form.get('address', ''),
                phone=request.form.get('phone', ''),
                full_name=request.form.get('full_name', ''),
                postal_code=request.form.get('postal_code', ''),
                province=request.form.get('province', 'تهران'),
                shipping_cost=Decimal(str(shipping_cost)),
                coupon_code=coupon_code if coupon_data else None,
                discount_amount=Decimal(str(total_discount)),
                status='pending'
            )
            db.session.add(order)
            db.session.flush()

            for item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['product'].id,
                    variant_id=item['variant']['id'] if item['variant'] else None,
                    product_name=item['product'].name,
                    product_price=Decimal(str(item['final_price'])),
                    quantity=item['quantity'],
                    total_price=Decimal(str(item['item_total']))
                )
                db.session.add(order_item)

            db.session.commit()

            session['cart'] = {}
            session.pop('coupon', None)
            session.modified = True

            flash(f'سفارش {order_number} با موفقیت ثبت شد!', 'success')
            return redirect(url_for('payment_page', order_id=order.id))

        except Exception as e:
            db.session.rollback()
            flash(f'خطا در ثبت سفارش: {str(e)}', 'error')
            return redirect(url_for('checkout'))

    return render_template('checkout.html',
                          cart_items=cart_items,
                          total_price=total_price,
                          shipping_cost=shipping_cost,
                          total_with_shipping=total_with_shipping)

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



# ===== مدل مشخصات فنی =====
