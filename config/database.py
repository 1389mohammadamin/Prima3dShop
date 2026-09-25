# config/database.py
from flask_sqlalchemy import SQLAlchemy

# فقط یک نمونه از SQLAlchemy ایجاد کنید
db = SQLAlchemy()

def init_db(app):
    """مقداردهی دیتابیس با اپلیکیشن Flask"""
    db.init_app(app)
    return db