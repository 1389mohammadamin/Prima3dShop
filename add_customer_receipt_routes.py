main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# =============================================
# ۱. اضافه کردن روت آپلود فیش برای مشتری
# =============================================
if 'def upload_receipt' not in content:
    upload_route = '''
# ===== آپلود فیش توسط مشتری =====
@app.route('/order/<int:order_id>/upload-receipt', methods=['POST'])
@login_required
def upload_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))

    receipt = request.files.get('receipt')
    if receipt and receipt.filename:
        receipts_dir = os.path.join('app', 'interfaces', 'static', 'receipts')
        os.makedirs(receipts_dir, exist_ok=True)

        import uuid
        ext = os.path.splitext(receipt.filename)[1]
        filename = f"receipt_{order.order_number}_{uuid.uuid4().hex[:8]}{ext}"
        filepath = os.path.join(receipts_dir, filename)
        receipt.save(filepath)
        order.receipt_image = f"/static/receipts/{filename}"
        db.session.commit()
        flash('✅ فیش با موفقیت آپلود شد!', 'success')
    else:
        flash('❌ لطفاً یک عکس انتخاب کنید!', 'error')

    return redirect(url_for('payment_page', order_id=order.id))

'''
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + upload_route + '\n' + content[create_app_pos:]
        print('✅ روت upload_receipt اضافه شد')

# =============================================
# ۲. اضافه کردن روت حذف فیش برای مشتری
# =============================================
if 'def customer_delete_receipt' not in content:
    delete_route = '''
# ===== حذف فیش توسط مشتری =====
@app.route('/order/<int:order_id>/receipt/delete', methods=['POST'])
@login_required
def customer_delete_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))

    if order.receipt_image:
        filepath = os.path.join('app', 'interfaces', order.receipt_image.lstrip('/'))
        if os.path.exists(filepath):
            os.remove(filepath)
        order.receipt_image = None
        db.session.commit()
        flash('✅ فیش با موفقیت حذف شد!', 'success')

    return redirect(url_for('payment_page', order_id=order.id))

'''
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + delete_route + '\n' + content[create_app_pos:]
        print('✅ روت customer_delete_receipt اضافه شد')

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('🎉 تمام!')
