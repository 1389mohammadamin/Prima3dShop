variants_path = 'app/interfaces/templates/admin/variants.html'
with open(variants_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ۱. اضافه کردن فیلد مخفی value (اگه وجود نداره)
if 'name="value"' not in content:
    content = content.replace(
        '<input type="hidden" name="name" value="رنگ">',
        '<input type="hidden" name="name" value="رنگ">\n            <input type="hidden" name="value" id="hiddenColorValue" value="">'
    )
    print("✅ فیلد مخفی value اضافه شد")

# ۲. اصلاح جاوااسکریپت برای پر کردن مقدار value و color_code همزمان
old_script = '''
    document.addEventListener('DOMContentLoaded', function() {
        var colorSelect = document.getElementById('colorSelect');
        var hiddenColorCode = document.getElementById('hiddenColorCode');
        
        if (colorSelect) {
            colorSelect.addEventListener('change', function() {
                var selectedOption = this.options[this.selectedIndex];
                if (selectedOption) {
                    hiddenColorCode.value = selectedOption.getAttribute('data-color-code');
                }
            });
        }
    });
'''

new_script = '''
    document.addEventListener('DOMContentLoaded', function() {
        var colorSelect = document.getElementById('colorSelect');
        var hiddenColorCode = document.getElementById('hiddenColorCode');
        var hiddenColorValue = document.getElementById('hiddenColorValue');
        
        if (colorSelect) {
            colorSelect.addEventListener('change', function() {
                var selectedOption = this.options[this.selectedIndex];
                if (selectedOption) {
                    // کد رنگ رو ست کن
                    hiddenColorCode.value = selectedOption.getAttribute('data-color-code');
                    // اسم رنگ رو هم ست کن
                    hiddenColorValue.value = selectedOption.value;
                }
            });
        }
    });
'''

if old_script in content:
    content = content.replace(old_script, new_script)
    print("✅ اسکریپت جاوااسکریپت برای مقداردهی value اصلاح شد")
else:
    print("⚠️ اسکریپت قدیمی پیدا نشد، شاید ساختارش تغییر کرده.")

with open(variants_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("🎉 تمام! حالا سرور رو ریستارت کن.")
