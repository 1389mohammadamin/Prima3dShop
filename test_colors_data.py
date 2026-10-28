import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath('.')))
from app.main import create_app, db, Color, Product

app = create_app()
with app.app_context():
    # تست: آیا کد پایتون می‌تونه رنگ‌ها رو بخونه؟
    colors = Color.query.order_by(Color.name).all()
    print(f"تعداد رنگ‌ها: {len(colors)}")
    
    # تست: آیا محصول شماره ۱ وجود داره؟
    product = Product.query.get(1)
    if product:
        print(f"محصول شماره ۱: {product.name}")
    else:
        print("محصول شماره ۱ وجود ندارد!")
