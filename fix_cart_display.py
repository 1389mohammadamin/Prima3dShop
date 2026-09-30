cart_path = r'app\interfaces\templates\cart.html'
with open(cart_path, 'r', encoding='utf-8') as f:
    content = f.read()

# اضافه کردن نمایش رنگ بعد از نام محصول
old_name = '<h3 class="font-semibold">{{ item.product.name }}</h3>'
new_name = '''<h3 class="font-semibold">{{ item.product.name }}</h3>
                    {% if item.variant %}
                    <div class="flex items-center gap-2 mt-1">
                        <span class="inline-block w-4 h-4 rounded-full border border-gray-300" style="background-color: {{ item.variant.color_code or '#cccccc' }};"></span>
                        <span class="text-xs text-gray-500">رنگ: {{ item.variant.value }}</span>
                    </div>
                    {% endif %}'''

if old_name in content:
    content = content.replace(old_name, new_name)
    print('✅ نمایش رنگ به cart.html اضافه شد')
else:
    print('⚠️ ساختار نام محصول متفاوته - باید دستی بررسی کنی')
    # نمایش ۵ خط اول برای بررسی
    lines = content.split('\n')[:50]
    for i, l in enumerate(lines):
        if 'product.name' in l:
            print(f'خط {i+1}: {l}')

with open(cart_path, 'w', encoding='utf-8') as f:
    f.write(content)
