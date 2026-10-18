main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'def payment_page' not in content:
    new_route = '''
# ===== صفحه پرداخت =====
@app.route('/order/<int:order_id>/payment')
@login_required
def payment_page(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    return render_template('payment.html', order=order)

'''
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + new_route + '\n' + content[create_app_pos:]
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('✅ روت payment_page اضافه شد')
    else:
        print('❌ create_app پیدا نشد')
else:
    print('✅ روت payment_page از قبل وجود دارد')
