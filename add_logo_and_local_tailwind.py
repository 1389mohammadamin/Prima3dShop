import os
import re

# =============================================
# ۱. تغییر لوگو در تمام صفحات (base.html)
# =============================================
base_path = 'app/interfaces/templates/base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن بخش لوگو (معمولاً توی هدر هست)
# به دنبال کلمه پریما استور یا PrimaStore داخل تگ a با کلاس flex می‌گردیم
logo_html = '''<a href="/" class="flex items-center gap-2 group">
                <img src="{{ url_for('static', filename='images/logo.png') }}" alt="پریما استور" class="h-10 w-10 object-contain transition-transform duration-300 group-hover:scale-110 group-hover:rotate-6">
                <span class="text-xl font-bold text-gray-800 transition-colors duration-300 group-hover:text-emerald-600">پریما استور</span>
            </a>'''

# جایگزینی با استفاده از Regex برای پیدا کردن تگ a که شامل اسم سایت هست
pattern = r'<a[^>]*href="/"[^>]*>.*?پریما استور.*?</a>'
content = re.sub(pattern, logo_html, content, flags=re.DOTALL)

# اگر با روش بالا پیدا نشد، حالت ساده‌تر رو امتحان کن
if 'logo.png' not in content:
    pattern2 = r'پریما استور'
    content = re.sub(pattern2, '<img src="{{ url_for(\'static\', filename=\'images/logo.png\') }}" class="h-10 inline-block mr-2"> پریما استور', content, count=1)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ لوگو به هدر اضافه شد")

# =============================================
# ۲. لوکال کردن Tailwind CSS
# =============================================
print("\n🔄 در حال لوکال کردن Tailwind...")

# ساخت پوشه برای فایل‌های لوکال
os.makedirs('app/interfaces/static/css', exist_ok=True)
os.makedirs('app/interfaces/static/js', exist_ok=True)

# پیدا کردن تگ اسکریپت Tailwind در base.html
tailwind_cdn = '<script src="https://cdn.tailwindcss.com"></script>'
local_css = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/tailwind.css\') }}">'

if tailwind_cdn in content:
    content = content.replace(tailwind_cdn, local_css)
    print("✅ تگ CDN با فایل لوکال جایگزین شد")
else:
    print("⚠️ تگ CDN پیدا نشد، شاید از قبل تغییر کرده باشد")

# ذخیره تغییرات base.html
with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)

# =============================================
# ۳. دانلود فایل Tailwind لوکال
# =============================================
import urllib.request

print("\n📥 دانلود Tailwind CSS...")
try:
    # دانلود Tailwind Play CDN (نسخه فشرده)
    url = "https://cdn.tailwindcss.com/3.4.1"
    urllib.request.urlretrieve(url, 'app/interfaces/static/css/tailwind.js')
    
    # ساخت یه فایل CSS ساده برای استایل‌های کاستوم
    with open('app/interfaces/static/css/tailwind.css', 'w', encoding='utf-8') as f:
        f.write('/* Tailwind Local */\n')
        
    print("✅ فایل‌های Tailwind لوکال ذخیره شدند")
except Exception as e:
    print(f"❌ خطا در دانلود Tailwind: {e}")
    print("💡 شما می‌توانید فایل tailwind.js را دستی دانلود کنید")

print("\n🎉 تمام!")
