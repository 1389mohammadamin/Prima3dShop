main_path = r'app\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# پیدا کردن خط try: اضافی
for i, line in enumerate(lines):
    if i >= 1015 and i <= 1035:
        print(f"{i+1}: {line.rstrip()}")
