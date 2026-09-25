# run.py
import os
import sys
from dotenv import load_dotenv

# اضافه کردن مسیر پروژه به sys.path (اگر مشکل پیدا کردن ماژول داشتید)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# بارگذاری متغیرهای محیطی
load_dotenv()

# وارد کردن تابع create_app از app.main
try:
    from app.main import create_app
except ImportError as e:
    print(f"❌ خطا در وارد کردن create_app: {e}")
    print("📍 مسیر فعلی:", os.getcwd())
    print("📁 فایل‌های موجود در app:", os.listdir('app'))
    sys.exit(1)

app = create_app()

if __name__ == '__main__':
    # اجرا در حالت توسعه
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=debug_mode
    )