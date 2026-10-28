main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# اگر روت قدیمی است و colors رو نمی‌فرستد، اصلاحش می‌کنیم
old_route = "return render_template('admin/variants.html', product=product, variants=variants)"
new_route = "global_colors = Color.query.order_by(Color.name).all()\n    return render_template('admin/variants.html', product=product, variants=variants, colors=global_colors)"

if old_route in content:
    content = content.replace(old_route, new_route)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ روت پایتون آپدیت شد تا لیست رنگ‌ها را ارسال کند")
else:
    if 'colors=global_colors' in content:
        print("✅ روت پایتون از قبل درست است")
    else:
        print("⚠️ روت پایتون پیدا نشد، ممکن است ساختارش تغییر کرده باشد")
