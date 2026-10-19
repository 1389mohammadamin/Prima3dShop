import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath('.')))
from app.main import create_app, db, Product, Order, OrderItem, ProductVariant, ProductSpecification, ProductImage, Category, Coupon, CouponUsage, Review, PaymentConfirmation

app = create_app()

with app.app_context():
    print("🗑️ در حال خالی کردن دیتابیس...")
    
    try:
        # حذف تصاویر گالری
        ProductImage.query.delete()
        print("✅ تصاویر گالری پاک شدند")
        
        # حذف مشخصات فنی
        ProductSpecification.query.delete()
        print("✅ مشخصات فنی پاک شدند")
        
        # حذف تنوع‌ها (رنگ‌ها)
        ProductVariant.query.delete()
        print("✅ تنوع‌ها (رنگ‌ها) پاک شدند")
        
        # حذف آیتم‌های سفارش
        OrderItem.query.delete()
        print("✅ آیتم‌های سفارش پاک شدند")
        
        # حذف سفارشات
        Order.query.delete()
        print("✅ سفارشات پاک شدند")
        
        # حذف نظرات
        Review.query.delete()
        print("✅ نظرات پاک شدند")
        
        # حذف کوپن‌ها
        CouponUsage.query.delete()
        Coupon.query.delete()
        print("✅ کوپن‌ها پاک شدند")
        
        # حذف تاییدیه‌های پرداخت
        PaymentConfirmation.query.delete()
        print("✅ تاییدیه‌های پرداخت پاک شدند")
        
        # حذف محصولات
        Product.query.delete()
        print("✅ محصولات پاک شدند")
        
        # حذف دسته‌بندی‌ها
        Category.query.delete()
        print("✅ دسته‌بندی‌ها پاک شدند")
        
        db.session.commit()
        print("\n🎉 دیتابیس با موفقیت خالی شد! (کاربر ادمین باقی ماند)")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ خطا: {e}")
