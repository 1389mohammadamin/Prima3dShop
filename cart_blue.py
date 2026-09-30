cart_path = r'app\interfaces\templates\cart.html'
with open(cart_path, 'r', encoding='utf-8') as f:
    content = f.read()

# تغییر رنگ‌های سبد خرید به آبی (فقط توی این فایل)
content = content.replace('bg-emerald-600', 'bg-blue-600')
content = content.replace('hover:bg-emerald-700', 'hover:bg-blue-700')
content = content.replace('text-emerald-600', 'text-blue-600')
content = content.replace('hover:text-emerald-800', 'hover:text-blue-800')
content = content.replace('border-emerald-500', 'border-blue-500')
content = content.replace('focus:border-emerald-500', 'focus:border-blue-500')
content = content.replace('bg-emerald-50', 'bg-blue-50')
content = content.replace('text-emerald-700', 'text-blue-700')

with open(cart_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ رنگ‌های سبد خرید به آبی تغییر کرد')
