import os
os.environ['DATABASE_URL'] = 'mysql+pymysql://root:1234@localhost/پیریما_db'

from app.main import app, db, Product
from random import randint

with app.app_context():
    products = Product.query.all()
    for product in products:
        product.sales_count = randint(5, 50)
        product.view_count = randint(20, 200)
    db.session.commit()
    print("✅ داده‌های تستی برای محصولات ایجاد شد.")
