import os
import re

admin_order_path = 'app/interfaces/templates/admin/order_detail.html'

if not os.path.exists(admin_order_path):
    print(f"❌ {admin_order_path} پیدا نشد")
else:
    with open(admin_order_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # پیدا کردن بخش محصولات (از کلمه محصولات تا قبل از آدرس)
    pattern = r'(<h3[^>]*>محصولات</h3>)(.*?)(<h3[^>]*>آدرس)'
    
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        print("✅ بخش محصولات پیدا شد:")
        print(match.group(2)[:800])
    else:
        print("❌ بخش محصولات پیدا نشد - ساختار متفاوته")
        
        # پیدا کردن همه جاهایی که product داره
        for line in content.split('\n'):
            if 'product' in line.lower() or 'item' in line.lower():
                print(line.strip())
