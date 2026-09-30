main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# فیکس: استفاده از list() برای جلوگیری از تغییر دیکشنری در حین iteration
content = content.replace(
    "for cart_key, quantity in cart.items():",
    "for cart_key, quantity in list(cart.items()):"
)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ روت cart فیکس شد')
