import os

base_path = 'app/interfaces/templates/base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# =============================================
# ۱. اضافه کردن Favicon (آیکون تب مرورگر)
# =============================================
favicon_tag = '<link rel="icon" type="image/png" href="{{ url_for(\'static\', filename=\'images/logo.png\') }}">'

# اگه از قبل favicon نداره، اضافه کن
if 'rel="icon"' not in content and 'rel="shortcut icon"' not in content:
    content = content.replace('</head>', f'    {favicon_tag}\n</head>')
    print("✅ Favicon (آیکون تب) به base.html اضافه شد")

# =============================================
# ۲. اصلاح لود Tailwind
# =============================================
# چون Tailwind رو به صورت لوکال دانلود کردیم، باید مطمئن بشیم درست لود میشه
# فایل 400 کیلوبایتی که دانلود شد، نسخه کامل JS هست
if 'tailwind.js' not in content:
    content = content.replace('</head>', '    <script src="{{ url_for(\'static\', filename=\'js/tailwind.js\') }}"></script>\n</head>')
    print("✅ Tailwind لوکال به head اضافه شد")

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎉 تغییرات اعمال شد!")
