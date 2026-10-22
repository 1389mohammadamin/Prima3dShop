register_path = 'app/interfaces/templates/register.html'

html_content = '''{% extends "base.html" %}

{% block title %}ثبتنام - پریما استور{% endblock %}

{% block content %}
<div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
        
        <div class="text-center">
            <div class="mx-auto h-16 w-16 bg-emerald-100 rounded-full flex items-center justify-center mb-4">
                <i class="fas fa-user-plus text-3xl text-emerald-600"></i>
            </div>
            <h2 class="text-2xl font-bold text-gray-900">ایجاد حساب کاربری</h2>
            <p class="mt-2 text-sm text-gray-500">برای خرید و پیگیری سفارشات ثبتنام کنید</p>
        </div>

        <!-- پیامهای خطا -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="p-3 rounded-lg text-sm text-center {% if category == 'error' %}bg-red-50 text-red-600 border border-red-200{% else %}bg-emerald-50 text-emerald-600 border border-emerald-200{% endif %}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form class="mt-8 space-y-5" action="/auth/register" method="POST">
            <div>
                <label for="username" class="block text-sm font-semibold text-gray-700 mb-1">نام کاربری</label>
                <div class="relative">
                    <span class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400">
                        <i class="fas fa-user"></i>
                    </span>
                    <input id="username" name="username" type="text" required 
                           class="w-full pr-10 pl-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition"
                           placeholder="نام کاربری خود را وارد کنید">
                </div>
            </div>

            <div>
                <label for="email" class="block text-sm font-semibold text-gray-700 mb-1">ایمیل</label>
                <div class="relative">
                    <span class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400">
                        <i class="fas fa-envelope"></i>
                    </span>
                    <input id="email" name="email" type="email" required dir="ltr"
                           class="w-full pr-10 pl-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition text-left"
                           placeholder="example@email.com">
                </div>
            </div>

            <div>
                <label for="password" class="block text-sm font-semibold text-gray-700 mb-1">رمز عبور</label>
                <div class="relative">
                    <span class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400">
                        <i class="fas fa-lock"></i>
                    </span>
                    <input id="password" name="password" type="password" required 
                           class="w-full pr-10 pl-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition"
                           placeholder="رمز عبور خود را وارد کنید">
                </div>
            </div>

            <div>
                <label for="confirm_password" class="block text-sm font-semibold text-gray-700 mb-1">تکرار رمز عبور</label>
                <div class="relative">
                    <span class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400">
                        <i class="fas fa-lock"></i>
                    </span>
                    <input id="confirm_password" name="confirm_password" type="password" required 
                           class="w-full pr-10 pl-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition"
                           placeholder="رمز عبور را دوباره وارد کنید">
                </div>
            </div>

            <button type="submit" class="w-full bg-emerald-600 text-white py-3 px-4 rounded-xl hover:bg-emerald-700 transition font-bold text-lg shadow-md flex items-center justify-center gap-2">
                <i class="fas fa-check-circle"></i>
                ثبتنام
            </button>
        </form>

        <div class="text-center mt-6 border-t pt-6">
            <p class="text-sm text-gray-500">
                قبلا ثبتنام کردهاید 
                <a href="/auth/login" class="font-semibold text-emerald-600 hover:text-emerald-500 transition">
                    وارد شوید
                </a>
            </p>
        </div>
    </div>
</div>
{% endblock %}
'''

with open(register_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ صفحه ثبتنام (register.html) با استایل جدید و تمیز بازنویسی شد!")
