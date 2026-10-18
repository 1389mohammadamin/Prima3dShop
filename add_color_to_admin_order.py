import os
import re

admin_order_path = 'app/interfaces/templates/admin/order_detail.html'

if not os.path.exists(admin_order_path):
    print(f"❌ {admin_order_path} پیدا نشد")
else:
    with open(admin_order_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # پیدا کردن بخشی که اسم محصول رو نمایش میده
    # الگوهای احتمالی در قالب‌های مختلف
    product_name_patterns = [
        r'{{ item\.product\.name }}',
        r'{{ item\.product_name }}',
        r'{{ order_item\.product\.name }}',
        r'{{ order_item\.product_name }}'
    ]
    
    changed = False
    for pattern in product_name_patterns:
        if pattern in content:
            # اضافه کردن رنگ بعد از اسم محصول
            color_html = pattern + '''
                                    {% if item.variant %}
                                    <div class="flex items-center gap-1 mt-1">
                                        <span class="inline-block w-3 h-3 rounded-full border border-gray-300" style="background-color: {{ item.variant.color_code or '#ccc' }};"></span>
                                        <span class="text-xs text-gray-500">رنگ: {{ item.variant.value }}</span>
                                    </div>
                                    {% endif %}'''
            
            content = content.replace(pattern, color_html, 1)
            changed = True
            print(f"✅ رنگ به الگوی {pattern} اضافه شد")
            break
    
    if not changed:
        print("⚠️ الگوی اسم محصول پیدا نشد. ساختار فایل رو بررسی کن.")
        # نمایش بخش محصولات برای بررسی
        match = re.search(r'محصولات.*?(?=<h2|<div)', content, re.DOTALL)
        if match:
            print(match.group(0)[:500])

    with open(admin_order_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("🎉 تمام!")
