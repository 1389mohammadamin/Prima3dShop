detail_path = r'app\interfaces\templates\product_detail.html'
with open(detail_path, 'r', encoding='utf-8') as f:
    content = f.read()

# چک کن بخش variants وجود داره
if 'product.variants' not in content:
    print('❌ بخش variants در product_detail.html وجود نداره - باید اضافه بشه')
else:
    print('✅ بخش variants وجود داره')

# چک کن دایره رنگی درست هست
if 'color_code' in content:
    print('✅ color_code در product_detail.html هست')
else:
    print('❌ color_code نیست')
