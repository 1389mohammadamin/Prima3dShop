main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# حذف خطوط خالی و try اضافی
new_lines = []
skip_next = False

for i, line in enumerate(lines):
    # اگه خط try: تنهاست و بعدش try دیگه‌ایه، حذفش کن
    if line.strip() == 'try:' and i + 1 < len(lines) and lines[i+1].strip() == 'try:':
        continue
    new_lines.append(line)

with open(main_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ خطوط اضافی حذف شدند')
