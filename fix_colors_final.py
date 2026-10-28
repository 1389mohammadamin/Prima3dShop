main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ۱. اضافه کردن مدل Color
if 'class Color(db.Model)' not in content:
    model = '''
class Color(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    color_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

'''
    content = content.replace('def create_app():', model + '\ndef create_app():')
    print("✅ مدل Color به فایل اضافه شد")
else:
    print("✅ مدل Color از قبل وجود دارد")

# ۲. اضافه کردن روت مدیریت رنگ‌ها (اگر نبود)
if 'def admin_colors()' not in content:
    routes = '''
@app.route('/admin/colors', methods=['GET', 'POST'])
@login_required
def admin_colors():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form.get('name')
        color_code = request.form.get('color_code')
        if name and color_code:
            try:
                db.session.add(Color(name=name, color_code=color_code))
                db.session.commit()
                flash('✅ رنگ اضافه شد!', 'success')
            except:
                db.session.rollback()
                flash('این رنگ از قبل وجود دارد!', 'error')
        return redirect(url_for('admin_colors'))
    colors = Color.query.order_by(Color.name).all()
    return render_template('admin/colors.html', colors=colors)

@app.route('/admin/colors/<int:color_id>/delete', methods=['POST'])
@login_required
def admin_color_delete(color_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    color = Color.query.get_or_404(color_id)
    db.session.delete(color)
    db.session.commit()
    flash('✅ رنگ حذف شد!', 'success')
    return redirect(url_for('admin_colors'))

'''
    content = content.replace('def create_app():', routes + '\ndef create_app():')
    print("✅ روت‌های مدیریت رنگ‌ها اضافه شدند")
else:
    print("✅ روت‌ها از قبل وجود دارند")

# ۳. اصلاح روت variants برای ارسال لیست رنگ‌ها
old_route = "return render_template('admin/variants.html', product=product, variants=variants)"
new_route = "global_colors = Color.query.order_by(Color.name).all()\n    return render_template('admin/variants.html', product=product, variants=variants, colors=global_colors)"

if old_route in content:
    content = content.replace(old_route, new_route)
    print("✅ روت variants اصلاح شد")
elif 'colors=global_colors' in content:
    print("✅ روت variants از قبل درست است")
else:
    print("⚠️ روت variants پیدا نشد، ممکن است کد آن تغییر کرده باشد")

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n🎉 تمام! حالا سرور رو ریستارت کن.")
