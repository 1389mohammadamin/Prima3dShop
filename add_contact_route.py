main_path = 'app/main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# بررسی اینکه آیا روت contact وجود داره یا نه
if "@app.route('/contact')" not in content:
    print("⚠️ روت تماس با ما وجود ندارد. در حال اضافه کردن...")
    
    contact_routes = '''
# ===== صفحه تماس با ما =====
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        contact_info = request.form.get('contact')
        message = request.form.get('message')
        
        # اینجا می‌تونید پیام رو توی دیتابیس ذخیره کنید یا ایمیل بفرستید
        # فعلاً فقط یه پیام موفقیت نشون می‌دیم
        flash(f'✅ پیام شما با موفقیت دریافت شد. {name} عزیز، به زودی با شما تماس می‌گیریم.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

'''

    # اضافه کردن روت قبل از def create_app
    create_app_pos = content.find('def create_app():')
    if create_app_pos > 0:
        content = content[:create_app_pos] + contact_routes + '\n' + content[create_app_pos:]
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ روت تماس با ما به main.py اضافه شد")
    else:
        print("❌ def create_app پیدا نشد")
else:
    print("✅ روت تماس با ما از قبل وجود دارد")
