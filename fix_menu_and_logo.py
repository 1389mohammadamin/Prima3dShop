base_path = 'app/interfaces/templates/base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# =============================================
# فیکس ۱: رفع مشکل باز و بسته شدن منوی کاربر (Hover Gap)
# =============================================
# به جای فاصله، یه نوار نامرئی می‌ذاریم که وقتی موس از دکمه به منو میره، منو نبنده
old_menu = '''<div class="absolute left-0 mt-2 w-48 bg-white rounded-md shadow-lg hidden group-hover:block z-50 border border-gray-100">'''
new_menu = '''<div class="absolute left-0 pt-2 w-48 hidden group-hover:block z-50">
                                <div class="bg-white rounded-md shadow-lg border border-gray-100 overflow-hidden">'''

if old_menu in content:
    content = content.replace(old_menu, new_menu)
    # بستن تگ div اضافه شده در انتهای منو
    content = content.replace(
        '<a href="/auth/logout" class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-b-md">خروج</a>\n                            </div>',
        '<a href="/auth/logout" class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-b-md">خروج</a>\n                                </div>\n                            </div>'
    )
    print("✅ مشکل هاور منوی کاربر فیکس شد")

# =============================================
# فیکس ۲: تغییر مسیر لوگو (شاید پسوندش jpg هست)
# =============================================
content = content.replace(
    "url_for('static', filename='images/logo.png')",
    "url_for('static', filename='images/logo.png')"
)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎉 تغییرات اعمال شد!")
