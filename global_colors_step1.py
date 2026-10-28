import os
import sqlite3
import glob

# =============================================
# ۱. ساخت جدول Color در دیتابیس
# =============================================
print("🔄 ساخت جدول رنگ‌های سراسری...")
for db in glob.glob('**/*.db', recursive=True) + glob.glob('*.db'):
    if not os.path.exists(db): continue
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS colors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                color_code VARCHAR(20) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print(f"✅ جدول colors در {db} آماده شد")
        conn.close()
    except Exception as e:
        print(f"❌ {db}: {e}")

# =============================================
# ۲. اضافه کردن مدل Color به main.py
# =============================================
print("\n🔄 اضافه کردن مدل Color به کد...")
main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'class Color(db.Model)' not in content:
    model_code = '''
# ===== مدل رنگ‌های سراسری =====
class Color(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    color_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

'''
    # اضافه کردن قبل از def create_app
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + model_code + content[create_app_pos:]
        print("✅ مدل Color اضافه شد")

# =============================================
# ۳. اضافه کردن روت‌های مدیریت رنگ‌ها
# =============================================
if 'def admin_colors' not in content:
    color_routes = '''
# ===== مدیریت رنگ‌های سراسری =====
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
                new_color = Color(name=name, color_code=color_code)
                db.session.add(new_color)
                db.session.commit()
                flash('✅ رنگ جدید با موفقیت اضافه شد!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('خطا: این رنگ از قبل وجود دارد!', 'error')
        else:
            flash('نام و کد رنگ الزامی است!', 'error')
            
        return redirect(url_for('admin_colors'))
        
    colors = Color.query.order_by(Color.name).all()
    return render_template('admin/colors.html', colors=colors)

@app.route('/admin/colors/<int:color_id>/delete', methods=['POST'])
@login_required
def admin_color_delete(color_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
    color = Color.query.get_or_404(color_id)
    try:
        db.session.delete(color)
        db.session.commit()
        flash('✅ رنگ حذف شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
        
    return redirect(url_for('admin_colors'))

'''
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + color_routes + content[create_app_pos:]
        print("✅ روت‌های مدیریت رنگ‌ها اضافه شدند")

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

# =============================================
# ۴. ساخت قالب admin/colors.html
# =============================================
print("\n🔄 ساخت قالب مدیریت رنگ‌ها...")
colors_html = '''{% extends "base.html" %}
{% block title %}مدیریت رنگ‌ها - پریما استور{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
    <div class="flex justify-between items-center mb-8 border-b pb-4">
        <h1 class="text-2xl font-bold text-gray-800">🎨 مدیریت رنگ‌های سراسری</h1>
        <a href="/admin/products" class="text-gray-500 hover:text-emerald-600 transition text-sm"><i class="fas fa-arrow-right"></i> بازگشت</a>
    </div>

    <!-- فرم افزودن رنگ -->
    <div class="bg-gray-50 p-6 rounded-xl border border-gray-200 mb-8">
        <h3 class="font-bold mb-4">افزودن رنگ جدید به لیست</h3>
        <form method="POST" class="flex flex-col md:flex-row gap-4 items-end">
            <div class="flex-1 w-full">
                <label class="block text-sm font-semibold mb-2 text-gray-700">نام رنگ *</label>
                <input type="text" name="name" placeholder="مثلاً: قرمز، آبی" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500">
            </div>
            <div class="w-full md:w-48">
                <label class="block text-sm font-semibold mb-2 text-gray-700">کد رنگ *</label>
                <input type="color" name="color_code" value="#10b981" class="w-full h-[50px] p-1 border border-gray-300 rounded-xl cursor-pointer bg-white">
            </div>
            <button type="submit" class="w-full md:w-auto bg-emerald-600 text-white px-8 py-3 rounded-xl hover:bg-emerald-700 transition font-bold shadow-md">
                <i class="fas fa-plus ml-2"></i> افزودن
            </button>
        </form>
    </div>

    <!-- لیست رنگ‌ها -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {% for color in colors %}
        <div class="flex items-center justify-between p-4 border border-gray-200 rounded-xl bg-white shadow-sm hover:shadow-md transition">
            <div class="flex items-center gap-3">
                <span class="w-10 h-10 rounded-full border border-gray-200 shadow-inner" style="background-color: {{ color.color_code }};"></span>
                <div>
                    <p class="font-bold text-gray-800">{{ color.name }}</p>
                    <p class="text-xs text-gray-500 font-mono" dir="ltr">{{ color.color_code }}</p>
                </div>
            </div>
            <form action="/admin/colors/{{ color.id }}/delete" method="POST" onsubmit="return confirm('حذف شود؟')">
                <button type="submit" class="text-red-400 hover:text-red-600 p-2 rounded-lg hover:bg-red-50 transition"><i class="fas fa-trash-alt"></i></button>
            </form>
        </div>
        {% else %}
        <div class="col-span-full text-center py-8 text-gray-500">هنوز رنگی تعریف نشده است.</div>
        {% endfor %}
    </div>
</div>
{% endblock %}
'''
with open('app/interfaces/templates/admin/colors.html', 'w', encoding='utf-8') as f:
    f.write(colors_html)
print("✅ قالب colors.html ساخته شد")

# =============================================
# ۵. تغییر فرم افزودن تنوع به محصول (variants.html)
# =============================================
print("\n🔄 تغییر فرم افزودن رنگ در صفحه محصول...")
variants_path = 'app/interfaces/templates/admin/variants.html'
with open(variants_path, 'r', encoding='utf-8') as f:
    v_content = f.read()

# پیدا کردن فرم افزودن تنوع و جایگزینی فیلدهای نام و رنگ با منوی کشویی
# ما باید رنگ‌ها رو به صورت یک لیست از سمت پایتون به این قالب بفرستیم
# پس فعلاً فرم رو تغییر می‌دیم تا کاربر از بین رنگ‌ها انتخاب کنه (به جای تایپ دستی)
# اما برای اینکه کد پایتون رو هم تغییر بدیم، باید روت admin_product_variants رو هم آپدیت کنیم
# (این کار رو در قدم بعدی انجام می‌دیم)

print("\n🎉 تمام! حالا سرور رو ریستارت کن.")
