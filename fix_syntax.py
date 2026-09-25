main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# فیکس primary_key
content = content.replace('3dshopry_key', 'primary_key')

# فیکس هر جای دیگه که خراب شده
content = content.replace('3dshopry', 'primary')
content = content.replace('3dshopnt', 'print')

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ primary_key فیکس شد')
