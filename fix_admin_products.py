main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# فیکس تابع admin_products - نسخه کامل
old_admin_products = """@app.route('/admin/products')
@login_required
def admin_products():
@app.route('/admin/products/create', methods=['GET', 'POST'])"""

new_admin_products = """@app.route('/admin/products')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/create', methods=['GET', 'POST'])"""

content = content.replace(old_admin_products, new_admin_products)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ تابع admin_products فیکس شد')
