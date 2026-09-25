# ============================================================
# 🚀 اعمال تمام تغییرات مورد نیاز
# ============================================================

Write-Host "🚀 شروع اعمال تغییرات..." -ForegroundColor Cyan

# ============================================================
# 1. رفع تم دارک و فاصله‌ها در style.css
# ============================================================

$cssPath = "app\interfaces\static\css\style.css"
$cssContent = @'
/* ============================================================
   🎨 3DShop - طراحی نهایی
   ============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --bg-primary: #f1f5f9;
    --bg-secondary: #ffffff;
    --bg-card: #ffffff;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #94a3b8;
    --border-color: #e2e8f0;
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --primary-light: #dbeafe;
    --primary-gradient: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
    --shadow: 0 4px 24px rgba(0,0,0,0.06);
    --shadow-lg: 0 12px 48px rgba(0,0,0,0.10);
    --shadow-xl: 0 20px 60px rgba(0,0,0,0.12);
    --shadow-primary: 0 4px 24px rgba(37,99,235,0.30);
    --radius: 16px;
    --radius-lg: 24px;
    --transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
}

[data-theme="dark"] {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a2332;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border-color: #2d3748;
    --shadow: 0 4px 24px rgba(0,0,0,0.3);
    --shadow-lg: 0 12px 48px rgba(0,0,0,0.4);
    --shadow-xl: 0 20px 60px rgba(0,0,0,0.5);
}

* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }

body {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, sans-serif;
    transition: all 0.4s ease !important;
    min-height: 100vh;
    line-height: 1.7;
}

.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

/* ===== هدر ===== */
.navbar {
    background: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border-color) !important;
    padding: 12px 0 !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 1000 !important;
    transition: all 0.4s ease !important;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand {
    font-size: 1.5rem;
    font-weight: 900;
    color: var(--primary);
    text-decoration: none;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 28px;
}

.nav-links a {
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    transition: var(--transition);
    font-size: 0.95rem;
    padding: 4px 0;
}

.nav-links a:hover { color: var(--primary); }

/* ===== منوی کشویی ===== */
.dropdown { position: relative; }

.dropdown-menu {
    display: none;
    position: absolute;
    top: calc(100% + 8px);
    right: 0;
    min-width: 220px;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    box-shadow: var(--shadow-lg);
    padding: 8px 0;
    z-index: 1001;
    opacity: 0;
    transform: translateY(-8px);
    transition: opacity 0.25s ease, transform 0.25s ease;
}

.dropdown:hover .dropdown-menu {
    display: block;
    opacity: 1;
    transform: translateY(0);
}

.dropdown-menu a {
    display: block;
    padding: 10px 20px;
    color: var(--text-secondary);
    text-decoration: none;
    transition: var(--transition);
    font-size: 0.9rem;
}

.dropdown-menu a:hover {
    background: var(--primary-light);
    color: var(--primary);
}

.dropdown-menu .divider {
    border-top: 1px solid var(--border-color);
    margin: 4px 12px;
}

/* ===== دکمه‌ها ===== */
.btn {
    display: inline-block;
    padding: 10px 28px;
    border: none;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: var(--transition);
    text-decoration: none;
    text-align: center;
}

.btn-primary {
    background: var(--primary-gradient);
    color: white;
    box-shadow: var(--shadow-primary);
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: var(--shadow-xl); }

/* ===== Hero ===== */
.hero {
    padding: 60px 0;
    background: var(--primary-gradient);
    border-radius: var(--radius-lg);
    margin: 16px 0 32px;
    position: relative;
    overflow: hidden;
}

.hero-content { position: relative; z-index: 1; text-align: center; color: white; padding: 0 20px; }
.hero h1 { font-size: 2.8rem; font-weight: 900; line-height: 1.2; margin-bottom: 12px; }
.hero p { font-size: 1.1rem; opacity: 0.9; max-width: 600px; margin: 0 auto 24px; }

/* ===== کارت‌ها ===== */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    transition: var(--transition);
    overflow: hidden;
}
.card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); border-color: var(--primary); }

.card-img { height: 180px; background: var(--primary-light); display: flex; align-items: center; justify-content: center; }
.card-body { padding: 16px; }
.card-title { font-size: 1rem; font-weight: 700; color: var(--text-primary); }
.card-price { font-size: 1.2rem; font-weight: 800; color: var(--primary); }

/* ===== تخفیف ===== */
.price-with-discount {
    display: flex;
    align-items: center;
    gap: 10px;
}
.old-price {
    text-decoration: line-through;
    color: var(--text-muted);
    font-size: 0.9rem;
}
.new-price {
    color: #ef4444;
    font-weight: 800;
    font-size: 1.2rem;
}
.discount-badge {
    background: #ef4444;
    color: white;
    padding: 2px 10px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
}

/* ===== آمار ===== */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}

.stat-item {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 20px;
    text-align: center;
    transition: var(--transition);
}
.stat-item:hover { transform: translateY(-3px); box-shadow: var(--shadow-lg); }

.stat-number {
    font-size: 1.8rem;
    font-weight: 800;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label { color: var(--text-secondary); font-size: 0.85rem; margin-top: 4px; }

/* ===== محصولات ===== */
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.section-title { font-size: 1.3rem; font-weight: 700; display: flex; align-items: center; gap: 8px; }

.products-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 32px;
}

/* ===== اسلایدر ===== */
.slider-wrapper { position: relative; padding: 0 40px; }
.slider-track { display: flex; gap: 16px; transition: transform 0.5s cubic-bezier(0.4,0,0.2,1); }
.slider-item { flex: 0 0 calc(20% - 13px); min-width: calc(20% - 13px); }

.slider-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    font-size: 16px;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow);
}
.slider-btn:hover { background: var(--primary); color: white; border-color: var(--primary); }
.slider-btn.prev { left: 0; }
.slider-btn.next { right: 0; }

/* ===== دکمه تغییر تم ===== */
.theme-toggle {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 9999;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: var(--primary-gradient);
    border: none;
    color: white;
    font-size: 22px;
    cursor: pointer;
    box-shadow: var(--shadow-primary);
    transition: var(--transition);
    display: flex;
    align-items: center;
    justify-content: center;
}
.theme-toggle:hover { transform: scale(1.1) rotate(20deg); }

/* ===== اعلان سراسری ===== */
.announcement-bar {
    background: var(--primary-gradient);
    color: white;
    padding: 10px 0;
    text-align: center;
    font-size: 0.9rem;
    font-weight: 500;
}
.announcement-bar a {
    color: white;
    text-decoration: underline;
    margin: 0 4px;
}

/* ===== فوتر ===== */
.footer {
    background: var(--bg-secondary);
    border-top: 1px solid var(--border-color);
    padding: 32px 0;
    margin-top: 32px;
}

/* ===== ریسپانسیو ===== */
@media (max-width: 1024px) {
    .products-grid { grid-template-columns: repeat(3, 1fr); }
    .slider-item { flex: 0 0 calc(33.33% - 11px); min-width: calc(33.33% - 11px); }
}
@media (max-width: 768px) {
    .products-grid { grid-template-columns: repeat(2, 1fr); }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    .slider-item { flex: 0 0 calc(50% - 8px); min-width: calc(50% - 8px); }
    .hero { padding: 30px 0; }
    .hero h1 { font-size: 1.8rem; }
    .nav-links { gap: 16px; }
}
@media (max-width: 480px) {
    .products-grid { grid-template-columns: 1fr; }
    .stats-grid { grid-template-columns: 1fr; }
    .slider-item { flex: 0 0 100%; min-width: 100%; }
    .hero { padding: 20px 0; }
    .hero h1 { font-size: 1.4rem; }
    .slider-wrapper { padding: 0 32px; }
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--primary-gradient); border-radius: 10px; }
'@

$cssContent | Out-File -FilePath $cssPath -Encoding UTF8
Write-Host "✅ CSS به‌روزرسانی شد" -ForegroundColor Green

# ============================================================
# 2. اصلاح base.html (منو و اعلان)
# ============================================================

$basePath = "app\interfaces\templates\base.html"
$baseContent = Get-Content $basePath -Raw -Encoding UTF8

# اضافه کردن اعلان سراسری
$announcement = @'
<!-- اعلان سراسری -->
{% if announcement %}
<div class="announcement-bar">
    <i class="fas fa-bullhorn ml-2"></i>
    {{ announcement }}
    {% if announcement_link %}
    <a href="{{ announcement_link }}">اطلاعات بیشتر</a>
    {% endif %}
</div>
{% endif %}
'@

$baseContent = $baseContent -replace '(<nav class="navbar")', $announcement + '$1'

# اصلاح منوی کشویی
$baseContent = $baseContent -replace 'class="dropdown-menu"', 'class="dropdown-menu" style="display:none;"'

$baseContent | Out-File -FilePath $basePath -Encoding UTF8
Write-Host "✅ base.html به‌روزرسانی شد" -ForegroundColor Green

# ============================================================
# 3. اضافه کردن روت اعلان به main.py
# ============================================================

$mainPath = "app\main.py"
$mainContent = Get-Content $mainPath -Raw -Encoding UTF8

if ($mainContent -notmatch 'announcement') {
    $announceRoute = @"

# ===== اعلان سراسری =====
announcement = None
announcement_link = None

@app.context_processor
def inject_announcement():
    return {
        'announcement': announcement,
        'announcement_link': announcement_link
    }

@app.route('/admin/announcement', methods=['GET', 'POST'])
@login_required
def admin_announcement():
    global announcement, announcement_link
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        announcement = request.form.get('announcement')
        announcement_link = request.form.get('announcement_link')
        flash('اعلان با موفقیت به‌روزرسانی شد!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/announcement.html', 
                          announcement=announcement, 
                          announcement_link=announcement_link)
"@
    $mainContent = $mainContent -replace '(def create_app\(\):)', $announceRoute + "`n`n`$1"
    $mainContent | Out-File -FilePath $mainPath -Encoding UTF8
    Write-Host "✅ روت اعلان اضافه شد" -ForegroundColor Green
}

# ============================================================
# 4. اضافه کردن بخش سفارشات و کدهای تخفیف به داشبورد ادمین
# ============================================================

$dashboardPath = "app\interfaces\templates\admin\dashboard.html"
$dashboardContent = @'
{% extends "base.html" %}

{% block title %}داشبورد مدیریت - 3DShop{% endblock %}

{% block content %}
<div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <h1 class="text-2xl font-bold mb-4">پنل مدیریت</h1>
    <p class="text-gray-600 dark:text-gray-400 mb-6">خوش آمدید {{ current_user.full_name }}!</p>
    
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-800">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm text-blue-600 dark:text-blue-400">تعداد محصولات</p>
                    <p class="text-2xl font-bold text-blue-800 dark:text-blue-300">{{ stats.total_products }}</p>
                </div>
                <i class="fas fa-boxes text-3xl text-blue-400"></i>
            </div>
            <a href="/admin/products" class="inline-block mt-2 text-blue-600 hover:text-blue-800 text-sm">مدیریت</a>
        </div>
        
        <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-800">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm text-green-600 dark:text-green-400">تعداد کاربران</p>
                    <p class="text-2xl font-bold text-green-800 dark:text-green-300">{{ stats.total_users }}</p>
                </div>
                <i class="fas fa-users text-3xl text-green-400"></i>
            </div>
            <a href="/admin/users" class="inline-block mt-2 text-green-600 hover:text-green-800 text-sm">مدیریت</a>
        </div>
        
        <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-200 dark:border-purple-800">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm text-purple-600 dark:text-purple-400">دسته‌بندی‌ها</p>
                    <p class="text-2xl font-bold text-purple-800 dark:text-purple-300">{{ stats.total_categories }}</p>
                </div>
                <i class="fas fa-tags text-3xl text-purple-400"></i>
            </div>
            <a href="/admin/categories" class="inline-block mt-2 text-purple-600 hover:text-purple-800 text-sm">مدیریت</a>
        </div>
        
        <div class="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg border border-yellow-200 dark:border-yellow-800">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-sm text-yellow-600 dark:text-yellow-400">سفارشات</p>
                    <p class="text-2xl font-bold text-yellow-800 dark:text-yellow-300">{{ stats.total_orders }}</p>
                </div>
                <i class="fas fa-shopping-cart text-3xl text-yellow-400"></i>
            </div>
            <a href="/admin/orders" class="inline-block mt-2 text-yellow-600 hover:text-yellow-800 text-sm">مدیریت</a>
        </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between mb-3">
                <h3 class="font-bold text-gray-700 dark:text-gray-300">کدهای تخفیف</h3>
                <i class="fas fa-ticket-alt text-2xl text-primary"></i>
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400">مدیریت کدهای تخفیف و کوپن‌ها</p>
            <a href="/admin/coupons" class="inline-block mt-3 text-primary hover:text-primary-dark text-sm font-medium">مدیریت کدها →</a>
        </div>
        
        <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between mb-3">
                <h3 class="font-bold text-gray-700 dark:text-gray-300">اعلان سراسری</h3>
                <i class="fas fa-bullhorn text-2xl text-primary"></i>
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400">مدیریت پیام‌های مهم سایت</p>
            <a href="/admin/announcement" class="inline-block mt-3 text-primary hover:text-primary-dark text-sm font-medium">مدیریت اعلان →</a>
        </div>
    </div>
</div>
{% endblock %}
'@

$dashboardContent | Out-File -FilePath $dashboardPath -Encoding UTF8
Write-Host "✅ داشبورد ادمین به‌روزرسانی شد" -ForegroundColor Green

# ============================================================
# 5. اضافه کردن صفحه مدیریت اعلان
# ============================================================

$announcementPage = @'
{% extends "base.html" %}

{% block title %}مدیریت اعلان - 3DShop{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h1 class="text-2xl font-bold mb-6">مدیریت اعلان سراسری</h1>
        
        <form method="POST">
            <div class="mb-4">
                <label class="block text-gray-700 dark:text-gray-300 mb-2">متن اعلان</label>
                <input type="text" name="announcement" value="{{ announcement or '' }}" 
                       placeholder="مثال: تخفیف ویژه تا پایان هفته..."
                       class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:border-primary dark:bg-gray-700 dark:text-white">
            </div>
            
            <div class="mb-4">
                <label class="block text-gray-700 dark:text-gray-300 mb-2">لینک (اختیاری)</label>
                <input type="text" name="announcement_link" value="{{ announcement_link or '' }}" 
                       placeholder="مثال: /products"
                       class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:border-primary dark:bg-gray-700 dark:text-white">
            </div>
            
            <div class="flex gap-4">
                <button type="submit" class="bg-primary text-white px-6 py-2 rounded-lg hover:bg-primary-dark transition">
                    <i class="fas fa-save ml-2"></i> ذخیره
                </button>
                <a href="/admin" class="bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-6 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition">
                    <i class="fas fa-times ml-2"></i> انصراف
                </a>
            </div>
            
            {% if announcement %}
            <div class="mt-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                <p class="text-sm text-green-800 dark:text-green-300">
                    <i class="fas fa-check-circle ml-2"></i>
                    اعلان فعلی: <strong>{{ announcement }}</strong>
                    {% if announcement_link %}
                    <br>لینک: <a href="{{ announcement_link }}" class="text-primary hover:underline">{{ announcement_link }}</a>
                    {% endif %}
                </p>
            </div>
            {% endif %}
        </form>
    </div>
</div>
{% endblock %}
'@

$announcementPage | Out-File -FilePath "app\interfaces\templates\admin\announcement.html" -Encoding UTF8
Write-Host "✅ صفحه مدیریت اعلان اضافه شد" -ForegroundColor Green

# ============================================================
# 6. به‌روزرسانی stats در admin_dashboard
# ============================================================

$mainContent = Get-Content $mainPath -Raw -Encoding UTF8

# اصلاح stats برای شامل سفارشات
$newStats = @'
stats = {
    'total_products': Product.query.count(),
    'total_users': User.query.count(),
    'total_categories': Category.query.count(),
    'total_orders': Order.query.count(),
}
'@

$mainContent = $mainContent -replace "(stats = \{.*?total_categories.*?\})", $newStats
$mainContent | Out-File -FilePath $mainPath -Encoding UTF8
Write-Host "✅ آمار داشبورد به‌روزرسانی شد" -ForegroundColor Green

# ============================================================
# 7. اضافه کردن قیمت با تخفیف به product_detail.html
# ============================================================

$detailPath = "app\interfaces\templates\product_detail.html"
$detailContent = Get-Content $detailPath -Raw -Encoding UTF8

# اضافه کردن نمایش تخفیف
$discountBlock = @'
                {% if product.discount_price %}
                <div class="price-with-discount mt-4">
                    <span class="old-price">{{ product.price|format_currency }}</span>
                    <span class="new-price">{{ product.discount_price|format_currency }}</span>
                    <span class="discount-badge">{{ ((product.price - product.discount_price) / product.price * 100)|round|int }}%</span>
                </div>
                {% else %}
                <div class="mt-4">
                    <span class="text-2xl font-bold text-primary-600">{{ product.price|format_currency }}</span>
                </div>
                {% endif %}
'@

$detailContent = $detailContent -replace '(<span class="text-2xl font-bold text-primary-600">{{ product.price\|format_currency }}</span>)', $discountBlock
$detailContent | Out-File -FilePath $detailPath -Encoding UTF8
Write-Host "✅ تخفیف به صفحه محصول اضافه شد" -ForegroundColor Green

# ============================================================
# 8. اضافه کردن فیلد discount_price به مدل Product
# ============================================================

if ($mainContent -notmatch 'discount_price') {
    $mainContent = $mainContent -replace "(status = db.Column\(db.String\(20\), default='published'\))", "status = db.Column(db.String(20), default='published')`n    discount_price = db.Column(db.Numeric(10, 2), nullable=True)"
    $mainContent | Out-File -FilePath $mainPath -Encoding UTF8
    Write-Host "✅ فیلد discount_price به مدل Product اضافه شد" -ForegroundColor Green
}

Write-Host "`n✅ همه تغییرات با موفقیت اعمال شد!" -ForegroundColor Green
Write-Host "🔄 برای اعمال تغییرات، دیتابیس را به‌روز کنید:" -ForegroundColor Yellow
Write-Host "   python -c \"from app.main import app, db; app.app_context().push(); db.create_all(); print('OK')\"" -ForegroundColor Cyan
Write-Host "   python run.py" -ForegroundColor Cyan