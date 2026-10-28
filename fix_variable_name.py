main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# فیکس کردن اسم متغیر (تغییر global_colors به colors در روت variants)
old_code = "global_colors = Color.query.order_by(Color.name).all()\n    return render_template('admin/variants.html', product=product, variants=variants, colors=global_colors)"
new_code = "colors = Color.query.order_by(Color.name).all()\n    return render_template('admin/variants.html', product=product, variants=variants, colors=colors)"

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ مشکل اسم متغیر در main.py فیکس شد! (global_colors -> colors)")
else:
    print("⚠️ کد قدیمی پیدا نشد، شاید از قبل تغییر کرده باشه. بررسی دستی لازمه.")
