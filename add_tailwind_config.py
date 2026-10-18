base_path = 'app/interfaces/templates/base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# اضافه کردن کانفیگ Tailwind بعد از اسکریپت لود
tailwind_config = '''
    <script>
        if (typeof tailwind !== 'undefined') {
            tailwind.config = {
                theme: {
                    extend: {
                        colors: {
                            emerald: {
                                50: '#ecfdf5', 100: '#d1fae5', 200: '#a7f3d0',
                                300: '#6ee7b7', 400: '#34d399', 500: '#10b981',
                                600: '#059669', 700: '#047857', 800: '#065f46', 900: '#064e3b',
                            }
                        },
                        fontFamily: {
                            sans: ['Vazirmatn', 'sans-serif'],
                        }
                    }
                }
            }
        }
    </script>
'''

# پیدا کردن تگ اسکریپت Tailwind و اضافه کردن کانفیگ بعد از اون
if 'tailwind.config' not in content:
    if 'js/tailwind.js' in content:
        content = content.replace(
            '<script src="{{ url_for(\'static\', filename=\'js/tailwind.js\') }}"></script>',
            '<script src="{{ url_for(\'static\', filename=\'js/tailwind.js\') }}"></script>\n' + tailwind_config
        )
        print("✅ کانفیگ Tailwind (رنگ‌ها و فونت) اضافه شد")

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎉 تمام!")
