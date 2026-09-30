main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# =============================================
# فیکس ۱: مدل Order - اضافه کردن فیلدهای جدید
# =============================================
old_order = '''class Order(db.Model):
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
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')'''

new_order = '''class Order(db.Model):
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
    
    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')'''

content = content.replace(old_order, new_order)

# =============================================
# فیکس ۲: مدل OrderItem - اضافه کردن variant_id و فیلدهای درست
# =============================================
old_order_item = '''class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    product = db.relationship('Product')'''

new_order_item = '''class OrderItem(db.Model):
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
    variant = db.relationship('ProductVariant')'''

content = content.replace(old_order_item, new_order_item)

# =============================================
# فیکس ۳: روت checkout - استفاده از فیلدهای درست
# =============================================
old_order_create = '''            order = Order(
                order_number=order_number,
                user_id=current_user.id,
                total_amount=Decimal(str(total_amount)),
                shipping_cost=Decimal(str(shipping_cost)),
                status='pending',
                full_name=request.form.get('full_name'),
                phone=request.form.get('phone'),
                address=request.form.get('address'),
                postal_code=request.form.get('postal_code'),
                province=request.form.get('province', 'تهران')
            )'''

new_order_create = '''            order = Order(
                order_number=order_number,
                user_id=current_user.id,
                total_amount=Decimal(str(total_amount + shipping_cost)),
                shipping_address=request.form.get('address', ''),
                phone=request.form.get('phone', ''),
                full_name=request.form.get('full_name', ''),
                postal_code=request.form.get('postal_code', ''),
                province=request.form.get('province', 'تهران'),
                shipping_cost=Decimal(str(shipping_cost)),
                status='pending'
            )'''

content = content.replace(old_order_create, new_order_create)

# =============================================
# فیکس ۴: OrderItem - استفاده از فیلدهای درست
# =============================================
old_order_item_create = '''                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['product'].id,
                    variant_id=item['variant']['id'] if item['variant'] else None,
                    quantity=item['quantity'],
                    price=Decimal(str(item['final_price']))
                )'''

new_order_item_create = '''                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['product'].id,
                    variant_id=item['variant']['id'] if item['variant'] else None,
                    product_name=item['product'].name,
                    product_price=Decimal(str(item['final_price'])),
                    quantity=item['quantity'],
                    total_price=Decimal(str(item['item_total']))
                )'''

content = content.replace(old_order_item_create, new_order_item_create)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ مدل Order و OrderItem فیکس شدند')
print('✅ روت checkout فیکس شد')
