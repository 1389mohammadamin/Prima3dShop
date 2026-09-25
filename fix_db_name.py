import re

main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# فیکس اسم دیتابیس - برگردوندن به 3dshop_db
content = re.sub(r'prima_db', '3dshop_db', content)
content = re.sub(r'prima', '3dshop', content)  # فقط توی آدرس دیتابیس

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ اسم دیتابیس به 3dshop_db برگشت')

# چک کردن خط دیتابیس
for line in content.split('\n'):
    if 'DATABASE_URI' in line or 'database' in line.lower():
        print(f'   📍 {line.strip()}')
