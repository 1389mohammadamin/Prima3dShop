main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

# چک کن فیلدها وجود دارن یا نه
if 'shipping_cost' not in content.split('class Order(')[1].split('class ')[0]:
    print('❌ shipping_cost در مدل Order وجود ندارد')
else:
    print('✅ shipping_cost در مدل Order وجود دارد')

if 'province' not in content.split('class Order(')[1].split('class ')[0]:
    print('❌ province در مدل Order وجود ندارد')
else:
    print('✅ province در مدل Order وجود دارد')

# نمایش مدل Order
import re
match = re.search(r'class Order\(db\.Model\):(.*?)(?=\nclass |\Z)', content, re.DOTALL)
if match:
    print('\n📋 مدل Order فعلی:')
    print(match.group(0)[:800])
