import os

# ۱. اضافه کردن لینک به داشبورد ادمین
dashboard_path = 'app/interfaces/templates/admin/dashboard.html'
if os.path.exists(dashboard_path):
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '/admin/colors' not in content:
        # این کد رو با توجه به ساختار داشبوردت اضافه می‌کنیم (معمولاً یه بخش لینک‌ها داره)
        # برای اطمینان، یه دکمه شیک به پایین یا کنار اضافه می‌کنیم
        color_link = '''
        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between mt-4">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center text-xl">
                    <i class="fas fa-palette"></i>
                </div>
                <div>
                    <h3 class="font-bold text-gray-800">مدیریت رنگ‌های سراسری</h3>
                    <p class="text-sm text-gray-500">تعریف رنگ‌های پرکاربرد برای استفاده در محصولات</p>
                </div>
            </div>
            <a href="/admin/colors" class="bg-emerald-600 text-white px-6 py-2 rounded-lg hover:bg-emerald-700 transition">ورود</a>
        </div>
'''
        # اضافه کردن به انتهای بلاک content
        content = content.replace('{% endblock %}', color_link + '\n{% endblock %}')
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ لینک مدیریت رنگ‌ها به داشبورد اضافه شد")

# ۲. اضافه کردن لینک به منوی کشویی سایت (base.html)
base_path = 'app/interfaces/templates/base.html'
if os.path.exists(base_path):
    with open(base_path, 'r', encoding='utf-8') as f:
        b_content = f.read()
    
    if '/admin/colors' not in b_content:
        # پیدا کردن لینک دسته‌بندی‌ها در منو و اضافه کردن لینک رنگ‌ها بعد از آن
        target = '<a href="/admin/categories" class="block px-4 py-2 text-sm text-gray-700 hover:bg-emerald-50 hover:text-emerald-600">دسته‌بندی‌ها</a>'
        new_link = target + '\n                            <a href="/admin/colors" class="block px-4 py-2 text-sm text-gray-700 hover:bg-emerald-50 hover:text-emerald-600">مدیریت رنگ‌ها</a>'
        
        if target in b_content:
            b_content = b_content.replace(target, new_link)
            with open(base_path, 'w', encoding='utf-8') as f:
                f.write(b_content)
            print("✅ لینک مدیریت رنگ‌ها به منوی سایت اضافه شد")
        else:
            print("⚠️ لینک دسته‌بندی‌ها در منو پیدا نشد (شاید ساختار منو تغییر کرده باشد).")
