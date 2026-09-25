main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# چک کن مدل ProductVariant وجود داره
if 'class ProductVariant' not in content:
    model_code = '''
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
'''

    # اضافه کردن قبل از def create_app
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + model_code + '\n' + content[create_app_pos:]
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('✅ مدل ProductVariant و ProductSpecification اضافه شدند')
    else:
        print('❌ create_app پیدا نشد')
else:
    print('✅ مدل ProductVariant قبلاً وجود دارد')
