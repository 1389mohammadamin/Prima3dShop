main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# چک کن روت admin_product_variants وجود داره یا نه
if 'def admin_product_variants' not in content:
    new_route = '''
@app.route('/admin/products/<int:product_id>/variants')
@login_required
def admin_product_variants(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    product = Product.query.get_or_404(product_id)
    variants = ProductVariant.query.filter_by(product_id=product_id).all()
    return render_template('admin/variants.html', product=product, variants=variants)

@app.route('/admin/products/<int:product_id>/variants/create', methods=['POST'])
@login_required
def admin_variant_create(product_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    
    name = request.form.get('name')
    value = request.form.get('value')
    color_code = request.form.get('color_code')
    price_adjustment = request.form.get('price_adjustment', 0)
    quantity = request.form.get('quantity', 0)
    sku = request.form.get('sku')
    
    if not name or not value or not sku:
        flash('نام مقدار و SKU الزامی است!', 'error')
        return redirect(url_for('admin_product_variants', product_id=product_id))
    
    try:
        variant = ProductVariant(
            product_id=product_id,
            name=name,
            value=value,
            color_code=color_code if color_code else None,
            price_adjustment=Decimal(str(price_adjustment)) if price_adjustment else 0,
            quantity=int(quantity) if quantity else 0,
            sku=sku
        )
        db.session.add(variant)
        db.session.commit()
        flash('تنوع با موفقیت اضافه شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_product_variants', product_id=product_id))

@app.route('/admin/variants/<int:variant_id>/delete', methods=['POST'])
@login_required
def admin_variant_delete(variant_id):
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    variant = ProductVariant.query.get_or_404(variant_id)
    product_id = variant.product_id
    
    try:
        db.session.delete(variant)
        db.session.commit()
        flash('تنوع حذف شد!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطا: {str(e)}', 'error')
    
    return redirect(url_for('admin_product_variants', product_id=product_id))
'''

    # اضافه کردن قبل از def create_app
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + new_route + '\n' + content[create_app_pos:]
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('✅ روتهای مدیریت تنوع اضافه شدند')
    else:
        print('❌ create_app پیدا نشد')
else:
    print('✅ روتها قبلا وجود دارند')
