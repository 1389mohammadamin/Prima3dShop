main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# روت جدید
new_route = '''
@app.route('/admin/products/create', methods=['GET', 'POST'])
@login_required
def admin_product_create():
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity', 0)
        category_id = request.form.get('category_id', type=int)
        material = request.form.get('material')
        discount_price = request.form.get('discount_price')
        
        if not name or not price:
            flash('نام و قیمت الزامی است!', 'error')
            return redirect(url_for('admin_product_create'))
        
        try:
            product = Product(
                name=name,
                description=description,
                price=Decimal(str(price)),
                quantity=int(quantity) if quantity else 0,
                category_id=category_id if category_id else None,
                material=material,
                discount_price=Decimal(str(discount_price)) if discount_price else None
            )
            db.session.add(product)
            db.session.commit()
            
            flash('محصول با موفقیت اضافه شد!', 'success')
            return redirect(url_for('admin_product_variants', product_id=product.id))
        except Exception as e:
            db.session.rollback()
            flash(f'خطا: {str(e)}', 'error')
    
    categories = Category.query.all()
    return render_template('admin/product_form.html', product=None, categories=categories)
'''

# اضافه کردن بعد از روت admin_products
old_route = "@app.route('/admin/products')\n@login_required\ndef admin_products():"
new_route_full = old_route + new_route

content = content.replace(old_route, new_route_full)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ روت /admin/products/create اضافه شد')
