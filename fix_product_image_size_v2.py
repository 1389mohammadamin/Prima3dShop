import re

product_detail_path = 'app/interfaces/templates/product_detail.html'

with open(product_detail_path, 'r', encoding='utf-8') as f:
    content = f.read()

# الگوی تگ img
img_pattern = r'<img src="\{\{ product\.image_url \}\}"[^>]*>'

# اگر تگ img پیدا شد، کلاس‌هایش را عوض کن
if re.search(img_pattern, content):
    # جایگزینی تگ img با کلاس‌های درست
    content = re.sub(
        img_pattern,
        '<img src="{{ product.image_url }}" alt="{{ product.name }}" class="w-full h-full object-cover object-center">',
        content
    )
    print("✅ کلاس‌های عکس تغییر کرد")

# پیدا کردن کانتینر والد عکس
# این regex به دنبال divی می‌گرده که کلاس h-64 داره (که معمولا کانتینر عکسه)
container_pattern = r'<div class="[^"]*bg-gray-200[^"]*h-64[^"]*">'

if re.search(container_pattern, content):
    # تغییر ارتفاع به h-96 یا h-[500px] و اضافه کردن استایل بهتر
    content = re.sub(
        container_pattern,
        '<div class="md:w-1/2 h-96 md:h-[500px] bg-gray-50 flex items-center justify-center overflow-hidden rounded-r-2xl border-r border-gray-100">',
        content
    )
    print("✅ کانتینر عکس اصلاح شد")

with open(product_detail_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n🎉 تمام! حالا سرور رو ریستارت کن.")
