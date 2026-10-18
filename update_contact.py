contact_path = 'app/interfaces/templates/contact.html'

html_content = '''{% extends "base.html" %}
{% block title %}تماس با ما - پریما استور{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto">
    <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">تماس با ما</h1>
        <p class="text-gray-500">ما همیشه آماده شنیدن نظرات و پاسخ به سوالات شما هستیم.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- اطلاعات تماس -->
        <div class="space-y-4">
            <!-- شماره تماس -->
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex items-center gap-4">
                <div class="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600">
                    <i class="fas fa-phone-alt text-2xl"></i>
                </div>
                <div class="flex-1">
                    <p class="text-sm text-gray-500 mb-1">شماره پشتیبانی</p>
                    <div class="flex items-center justify-between">
                        <span class="text-xl font-bold text-gray-800" dir="ltr">09945553206</span>
                        <button onclick="copyToClipboard('09945553206')" class="text-emerald-600 hover:text-emerald-700 bg-emerald-50 hover:bg-emerald-100 p-2 rounded-lg transition" title="کپی">
                            <i class="fas fa-copy"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- ایمیل -->
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex items-center gap-4">
                <div class="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600">
                    <i class="fas fa-envelope text-2xl"></i>
                </div>
                <div class="flex-1 overflow-hidden">
                    <p class="text-sm text-gray-500 mb-1">ایمیل</p>
                    <div class="flex items-center justify-between gap-2">
                        <span class="text-sm sm:text-base font-bold text-gray-800 truncate" dir="ltr">PrimaStore@vatanmail.ir</span>
                        <button onclick="copyToClipboard('PrimaStore@vatanmail.ir')" class="text-emerald-600 hover:text-emerald-700 bg-emerald-50 hover:bg-emerald-100 p-2 rounded-lg transition shrink-0" title="کپی">
                            <i class="fas fa-copy"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- آیدی تلگرام / بله -->
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex items-center gap-4">
                <div class="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600">
                    <i class="fab fa-telegram-plane text-2xl"></i>
                </div>
                <div class="flex-1">
                    <p class="text-sm text-gray-500 mb-1">آیدی پیام‌رسان (بله و تلگرام)</p>
                    <div class="flex items-center justify-between">
                        <span class="text-xl font-bold text-gray-800" dir="ltr">@prima3dstore</span>
                        <button onclick="copyToClipboard('prima3dstore')" class="text-emerald-600 hover:text-emerald-700 bg-emerald-50 hover:bg-emerald-100 p-2 rounded-lg transition" title="کپی">
                            <i class="fas fa-copy"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- فرم تماس -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h2 class="text-xl font-bold mb-4">ارسال پیام</h2>
            <form action="/contact" method="POST" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">نام و نام خانوادگی</label>
                    <input type="text" name="name" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">ایمیل یا شماره تماس</label>
                    <input type="text" name="contact" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">پیام شما</label>
                    <textarea name="message" rows="4" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"></textarea>
                </div>
                <button type="submit" class="w-full bg-emerald-600 text-white font-bold py-3 rounded-xl hover:bg-emerald-700 transition">
                    <i class="fas fa-paper-plane ml-2"></i> ارسال پیام
                </button>
            </form>
        </div>
    </div>
</div>

<script>
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            // ایجاد یک نوتیفیکیشن ساده
            const toast = document.createElement('div');
            toast.className = 'fixed bottom-5 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-opacity duration-300';
            toast.innerHTML = '<i class="fas fa-check-circle text-emerald-400 ml-2"></i> کپی شد!';
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 300);
            }, 2000);
        }).catch(err => {
            alert('خطا در کپی کردن: ' + err);
        });
    }
</script>
{% endblock %}
'''

with open(contact_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ صفحه تماس با ما (contact.html) به‌روزرسانی شد!")
print("✅ شماره تماس، ایمیل و آیدی به همراه دکمه کپی اضافه شدند.")
