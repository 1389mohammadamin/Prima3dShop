import urllib.request
import os

url = "https://cdn.tailwindcss.com"
save_path = "app/interfaces/static/js/tailwind.js"

print("📥 در حال دانلود Tailwind...")

try:
    req = urllib.request.Request(
        url, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )
    
    with urllib.request.urlopen(req, timeout=15) as response:
        data = response.read()
        
    with open(save_path, 'wb') as f:
        f.write(data)
    
    size_kb = len(data) / 1024
    print(f"✅ دانلود شد! حجم: {size_kb:.1f} کیلوبایت")
    
    # چک کن فایل واقعاً JS هست یا نه (HTML صفحه خطا نباشه)
    with open(save_path, 'r', encoding='utf-8', errors='ignore') as f:
        first_line = f.read(200)
        if '<!DOCTYPE' in first_line or '<html' in first_line:
            print("❌ فایل دانلود شده HTML هست، نه JS! لطفاً دستی دانلود کن.")
        else:
            print("✅ فایل درست است.")
            
except Exception as e:
    print(f"❌ خطا: {e}")
