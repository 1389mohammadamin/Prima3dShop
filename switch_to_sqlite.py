import re

main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن خط فعلی دیتابیس
old_uri = None
for line in content.split('\n'):
    if 'SQLALCHEMY_DATABASE_URI' in line and 'mysql' in line.lower():
        old_uri = line.strip()
        print(f'❌ خط قدیمی: {old_uri}')
        break

if old_uri:
    # ساخت آدرس SQLite
    new_uri = "app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), '3dshop.db')"
    
    # جایگزینی
    content = content.replace(old_uri, new_uri)
    
    # مطمئن شو os ایمپورت شده
    if 'import os' not in content:
        content = content.replace('import sys', 'import sys\nimport os')
    
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'✅ آدرس جدید: {new_uri}')
else:
    # اگه پیدا نشد، همه خطوط DATABASE_URI رو نشون بده
    print('🔍 همه خطوط DATABASE_URI:')
    for line in content.split('\n'):
        if 'DATABASE_URI' in line:
            print(f'   {line.strip()}')
