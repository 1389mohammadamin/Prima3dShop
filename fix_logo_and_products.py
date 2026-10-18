import os

# =============================================
# ۱. برگرداندن پسوند لوگو به png در base.html
# =============================================
base_path = 'app/interfaces/templates/base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# برگردوندن لوگو به png (چون فایل واقعی png هست)
content = content.replace('images/logo.jpg', 'images/logo.png')

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ پسوند لوگو در base.html به png برگشت")

# =============================================
# ۲. اصلاح نمایش عکس در صفحه محصولات (products.html)
# =============================================
products_path = 'app/interfaces/templates/products.html'

if os.path.exists(products_path):
    with open(products_path, 'r', encoding='utf-8') as f:
        p_content = f.read()

    # پیدا کردن بخشی که عکس محصول رو نمایش میده
    import re
    
    # الگوی قدیمی عکس (اگه هست)
    old_img_pattern = r'<img src="[^"]*" alt="[^"]*" class="[^"]*">'
    
    # عکس جدید با استایل بهتر و آیکون فال‌بک
    new_img_html = '''<div class="h-48 bg-gray-100 rounded-t-xl flex items-center justify-center overflow-hidden">
                        {% if product.image_url %}
                            <img src="{{ product.image_url }}" alt="{{ product.name }}" class="w-full h-full object-cover transition-transform duration-500 hover:scale-110">
                        {% else %}
                            <i class="fas fa-cube text-6xl text-gray-300"></i>
                        {% endif %}
                    </div>'''

    # اگر تگ img پیدا شد، جایگزین کن (این بخش ممکنه بسته به کدت متفاوت باشه)
    if 'product.image_url' in p_content:
        # پیدا کردن بلوک عکس
        block_pattern = r'<div class="[^"]*">\s*{% if product\.image_url %}.*?{% endif %}\s*</div>'
        
        # سعی می‌کنیم فقط تگ img رو عوض کنیم اگه ساختار ساده‌تره
        p_content = re.sub(r'<img src="{{ product\.image_url }}".*?>', 
                          '<img src="{{ product.image_url }}" alt="{{ product.name }}" class="w-full h-full object-cover transition-transform duration-500 hover:scale-110">', 
                          p_content)
        
        # اضافه کردن آیکون به بخش else
        p_content = p_content.replace('<i class="fas fa-cube text-4xl text-gray-400"></i>', '<i class="fas fa-cube text-6xl text-gray-300"></i>')
        p_content = p_content.replace('<i class="fas fa-cube text-5xl text-gray-400"></i>', '<i class="fas fa-cube text-6xl text-gray-300"></i>')
        
        with open(products_path, 'w', encoding='utf-8') as f:
            f.write(p_content)
        print("✅ عکس‌های محصولات در products.html استایل‌دهی شدند")
    else:
        print("⚠️ بخش product.image_url در products.html پیدا نشد")
else:
    print("❌ فایل products.html پیدا نشد")

print("🎉 تمام!")
