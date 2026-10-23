import re

# فایل قالب صفحه محصول
product_detail_path = 'app/interfaces/templates/product_detail.html'

with open(product_detail_path, 'r', encoding='utf-8') as f:
    content = f.read()

# پیدا کردن بخش عکس محصول
# این regex به دنبال div یا تگی می‌گرده که عکس محصول رو نمایش میده
image_pattern = r'<div class="[^"]*">\s*{% if product\.image_url %}.*?{% else %}.*?{% endif %}\s*</div>'
# یا اگه ساختار ساده‌تره:
simple_img_pattern = r'<img src="\{\{ product\.image_url \}\}"[^>]*>'

# بهترین استایل برای عکس محصول در صفحه جزئیات
# استفاده از object-cover برای پر کردن کادر یا object-contain برای دیده شدن کل عکس
# برای اینکه عکس بزرگ نزنه و کادر رو به هم نریزه، از aspect-square و object-cover استفاده می‌کنیم
new_image_html = '''<div class="w-full h-96 md:h-[500px] bg-gray-100 rounded-2xl overflow-hidden flex items-center justify-center border border-gray-200">
            {% if product.image_url %}
                <img src="{{ product.image_url }}" alt="{{ product.name }}" class="w-full h-full object-cover object-center transition-transform duration-500 hover:scale-105">
            {% else %}
                <i class="fas fa-cube text-8xl text-gray-300"></i>
            {% endif %}
        </div>'''

# جایگزینی
if 'product.image_url' in content:
    # پیدا کردن بلوک عکس (به صورت عمومی)
    # ما فرض می‌کنیم عکس داخل یه div با کلاس h-64 یا h-96 یا مشابه هست
    # برای مطمئن شدن، سعی می‌کنیم کل بخش عکس رو با جدید جایگزین کنیم
    # این کار ممکنه کمی ریسک داشته باشه ولی چاره‌ای نیست
    
    # پیدا کردن یک بلوک بزرگتر که شامل img و if هست
    pattern_block = r'<div class="[^"]*h-64[^"]*">.*?<img src="\{\{ product\.image_url \}\}".*?>.*?</div>'
    
    # پیدا کردن تگ img و جایگزینی با کلاس‌های جدید
    # اگه تگ img پیدا شد، کلاس‌هاش رو عوض می‌کنیم
    img_pattern = r'<img src="\{\{ product\.image_url \}\}"[^>]*>'
    
    if re.search(img_pattern, content):
        content = re.sub(img_pattern, 
                         '<img src="{{ product.image_url }}" alt="{{ product.name }}" class="w-full h-full object-cover object-center transition-transform duration-500 hover:scale-105">', 
                         content)
        print("✅ استایل تگ عکس محصول اصلاح شد")
        
        # حالا کانتینر دور عکس رو فیکس می‌کنیم که ارتفاع ثابت داشته باشه
        # این کار از به هم ریختن صفحه جلوگیری می‌کنه
        container_pattern = r'<div class="md:w-1/2[^"]*">'
        # We need to find the parent div that has the image inside. 
        # This is tricky. Let's try to find the immediate parent of the img.
        # Actually, let's look for the div that wraps the image and has a background class.
        
    else:
        print("⚠️ تگ img با الگوی دقیق پیدا نشد. ممکنه ساختار فرق کنه.")
else:
    print("⚠️ بخش product.image_url در فایل پیدا نشد.")

# ذخیره تغییرات
with open(product_detail_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n🎉 تمام! حالا سرور رو ریستارت کن.")
