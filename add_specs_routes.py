main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# بررسی اینکه آیا روت مشخصات فنی وجود داره یا نه
if 'def admin_product_specifications' not in content:
    print("⚠️ روت مشخصات فنی وجود ندارد. در حال اضافه کردن...")
    
    new_routes = '''
# ===== مدیریت مشخصات فنی =====
@app.route('/admin/products/<int:product_id>/specifications')
@login_required
def admin_product_specifications(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    specs = ProductSpecification.query.filter_by(product_id=product_id).order_by(ProductSpecification.display_order).all()
    return render_template('admin/specifications.html', product=product, specs=specs)

@app.route('/admin/products/<int:product_id>/specifications/create', methods=['POST'])
@login_required
def admin_specification_create(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    spec_key = request.form.get('spec_key')
    spec_value = request.form.get('spec_value')
    display_order = request.form.get('display_order', 0)
    
    if not spec_key or not spec_value:
        flash('عنوان و مقدار مشخصات الزامی است!', 'error')
        return redirect(url_for('admin_product_specifications', product_id=product_id))
    
    try:
        spec = ProductSpecification(
            product_id=product_id,
            spec_key=spec_key,
            spec_value=spec_value,
            display_order=int(display_order) if display_order else 0
        )
        db.session.add(spec)
        db.session.commit()
        flash('✅ مشخصات با موفقیت اضافه شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_product_specifications', product_id=product_id))

@app.route('/admin/specifications/<int:spec_id>/delete', methods=['POST'])
@login_required
def admin_specification_delete(spec_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    spec = ProductSpecification.query.get_or_404(spec_id)
    product_id = spec.product_id
    
    try:
        db.session.delete(spec)
        db.session.commit()
        flash('✅ مشخصات حذف شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_product_specifications', product_id=product_id))
'''

    # اضافه کردن روت‌ها قبل از def create_app
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + new_routes + '\n' + content[create_app_pos:]
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ روت‌های مشخصات فنی به main.py اضافه شدند")
    else:
        print("❌ def create_app پیدا نشد")
else:
    print("✅ روت مشخصات فنی از قبل وجود دارد")
