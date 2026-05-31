# clc-main - کانفیگ‌های VPN با به‌روزرسانی خودکار


مجموعه‌ای از کانفیگ‌های عمومی VPN (`V2Ray` / `VLESS` / `Trojan` / `VMess` / `Reality` / `Shadowsocks` / `Hysteria2` / `TUIC`) با قابلیت به‌روزرسانی خودکار جهت دور زدن محدودیت‌های اینترنت و فیلترینگ. این کانفیگ‌ها همچنین برای عبور از لیست‌های سفید (White Lists) در اینترنت همراه بهینه‌سازی شده‌اند.

هر کانفیگ در واقع یک لینک اشتراک متنی (TXT) است که می‌توانید آن را در برنامه‌های مدرن و محبوب مانند `v2rayNG`، `NekoRay`، `Throne`، `v2rayN`، `V2Box`، `v2RayTun`، `Hiddify` و غیره وارد کنید.

این کانفیگ‌ها **به صورت روزانه** توسط GitHub Actions به‌روزرسانی می‌شوند، بنابراین تمام لینک‌ها همیشه فعال و معتبر هستند.

## ویژگی‌ها
- فیلترینگ خودکار و حذف کانفیگ‌های تکراری
- تقسیم فایل‌های بزرگ برای بهبود عملکرد (حداکثر ۳۰۰ کانفیگ در هر فایل)
- پشتیبانی از پروتکل‌های مختلف (V2Ray, VLESS, Trojan, VMess, و غیره)
- پشتیبانی از پردازش اشتراک‌های کدگذاری شده با Base64 همراه با فیلترینگ بر اساس نام دامنه
- **فیلترینگ پیشرفته امنیتی**: بررسی جامع پارامترهای ناامن (insecure) جهت افزایش امنیت کاربران:
  - **VMess**: بررسی پارامترهای `insecure`، `allowInsecure`، `security=none` و حالت قدیمی `alterId > 0`
  - **VLESS**: بررسی پارامترهای `allowInsecure`، `insecure`، `security=none`، `encryption=none`
  - **Shadowsocks**: بررسی و حذف سایفرهای ضعیف (حالت‌های RC4 و CFB، BF-CFB و غیره)
  - **ShadowsocksR**: بررسی سایفرهای ضعیف در فرمت SSR
  - **TUIC**: بررسی پارامتر `skip-cert-verify`
  - **عمومی**: بررسی پارامترهای `verify=0`، `verify=false`، `insecure=1` و سایر پارامترهای ناامن
- کانفیگ‌های اختصاصی برای عبور از لیست‌های سفید SNI/CIDR
- کانفیگ‌های ناامن برای عبور از SNI/CIDR
- تفکیک و دسته‌بندی کانفیگ‌ها بر اساس نوع پروتکل
- ایجاد فایل‌های جامع all.txt و all-secure.txt
- **تست و تایید خودکار کانفیگ‌ها**: تست از طریق Xray-core و مرتب‌سازی بر اساس سرعت (سریع‌ترین‌ها در ابتدا)
- **سیستم تایید دو مرحله‌ای**:
  - **فایل‌های Raw**: کانفیگ‌های تست‌نشده در پوشه‌های `/raw/`
  - **فایل‌های تایید شده**: تست شده با Xray-core و مرتب‌شده بر اساس پینگ (Ping)
- **پروکسی تلگرام**: جمع‌آوری، تایید و پردازش خودکار پروکسی‌های MTProto و SOCKS5 برای تلگرام با مرتب‌سازی بر اساس پینگ
- اعتبار‌سنجی بهبودیافته کانفیگ‌ها: اکنون فقط خطوطی که با پروتکل‌های پشتیبانی‌شده آغاز می‌شوند (vless://، vmess://، trojan:// و...) پردازش می‌شوند تا از ورود خطوط نامعتبر به فایل نهایی جلوگیری شود.
- پشتیبانی از ریپازیتوری‌های روزانه با قابلیت جستجوی خودکار کانفیگ‌ها بر اساس تاریخ
- پشتیبانی از کانفیگ‌های YAML و تبدیل آن‌ها به فرمت VPN URL
- **افزودن دستی کانفیگ**: امکان اضافه کردن سرورهای شخصی خودتان از طریق فایل `source/config/servers.txt` که به صورت خودکار فیلتر شده و با سایر منابع ادغام می‌شوند.
- دانلود موازی منابع جهت افزایش سرعت فرآیند به‌روزرسانی
- سیستم لاگ‌نویسی ایمن (Thread-safe) با تفکیک پیام‌ها بر اساس فایل
- معماری بهبودیافته با جداسازی دقیق وظایف میان ماژول‌های مختلف

## فهرست مطالب
- [clc-main - کانفیگ‌های VPN با به‌روزرسانی خودکار](#clc-main---کانفیگ‌های-vpn-با-به‌روزرسانی-خودکار)
  - [ویژگی‌ها](#ویژگی‌ها)
  - [فهرست مطالب](#فهرست-مطالب)
  - [راهنمای شروع سریع](#راهنمای-شروع-سریع)
  - [راهنمای ویدئویی](#راهنمای-ویدئویی)
  - [پیکربندی‌ها و لینک‌ها](#پیکربندی‌ها-و-لینک‌ها)
    - [کانفیگ‌های معمولی (default/)](#کانفیگ‌های-معمولی-default)
      - [فایل‌های تکمیلی در default/](#فایل‌های-تکمیلی-در-default)
    - [کانفیگ‌های عبور از لیست سفید SNI/CIDR (bypass/)](#کانفیگ‌های-عبور-از-لیست-سفید-snicidr-bypass)
    - [کانفیگ‌های ناامن عبور از SNI/CIDR (bypass-unsecure/)](#کانفیگ‌های-ناامن-عبور-از-snicidr-bypass-unsecure)
    - [کانفیگ‌های تفکیک شده بر اساس پروتکل (split-by-protocols/)](#کانفیگ‌های-تفکیک-شده-بر-اساس-پروتکل-split-by-protocols)
    - [پروکسی‌های تلگرام (tg-proxy/)](#پروکسی‌های-تلگرام-tg-proxy)
  - [نصب و نحوه استفاده](#نصب-و-نحوه-استفاده)
  - [اطلاعات تکمیلی](#اطلاعات-تکمیلی)
    - [ساختار ریپازیتوری](#ساختار-ریپازیتوری)
    - [اجرای محلی ژنراتور](#اجرای-محلی-ژنراتور)
    - [مجوز (License)](#مجوز-license)
    - [منابع و الهام‌بخش پروژه](#منابع-و-الهام‌بخش-پروژه)
    - [سلب مسئولیت](#سلب-مسئولیت)

## راهنمای شروع سریع

1. لینک مورد نظر خود را از بخش [پیکربندی‌ها و لینک‌ها](#پیکربندی‌ها-و-لینک‌ها) کپی کنید (پیشنهاد می‌شود با فایل‌های شماره 6، 22، 23، 24 یا 25 از پوشه default یا bypass/bypass-all.txt برای اینترنت همراه شروع کنید).
2. لینک را در **نرم‌افزار VPN** خود وارد (Import) کنید.
3. سروری که کمترین پینگ را دارد انتخاب کرده و متصل شوید.

---

## راهنمای ویدئویی

> **توجه!** راهنمای ویدئویی زیر در حال حاضر برای سیستم‌عامل‌های اندروید، اندروید تی‌وی، ویندوز، لینوکس و مک‌او‌اس مناسب است. برای iOS و iPadOS از دستورالعمل‌های متنی پایین استفاده کنید.

[مشاهده در YouTube](https://youtu.be/sagz2YluM70)

[مشاهده در Dzen](https://dzen.ru/video/watch/680d58f28c6d3504e953bd6d)

[مشاهده در VK Video](https://vk.com/video-200297343_456239303)

[مشاهده در تلگرام](https://t.me/avencoreschat/56595)

---

## پیکربندی‌ها و لینک‌ها

### کانفیگ‌های معمولی (default/)
کانفیگ‌های معمولی برای دور زدن فیلترینگ استاندارد. لینک‌های پیشنهادی:
- **[کانفیگ 1](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/default/1.txt)**
- **[کانفیگ 6](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/default/6.txt)**
- **[کانفیگ 22](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/default/22.txt)**
- **[کانفیگ 23](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/default/23.txt)**
- **[کانفیگ 24](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/default/24.txt)**
- **[کانفیگ 25](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/default/25.txt)**

#### فایل‌های تکمیلی در default/
- **[all.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/default/all.txt)** - تمام کانفیگ‌های یکتا از پوشه default در یک فایل
- **[all-secure.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/default/all-secure.txt)** - تمام کانفیگ‌های امن و یکتا (بدون پارامترهای insecure) از پوشه default در یک فایل

### کانفیگ‌های عبور از لیست سفید SNI/CIDR (bypass/)

> **قابل توجه کاربران موبایل**: در صورت بروز مشکل در سرعت یا عملکرد، توصیه می‌شود از فایل‌ها به صورت جداگانه استفاده کنید و از bypass-all.txt استفاده نکنید.

**[bypass-all](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-all.txt)** - تمام کانفیگ‌های امن برای عبور از SNI/CIDR در یک فایل شامل ۳۰۰ کانفیگ

**فایل‌های تفکیک شده بر اساس ۳۰۰ کانفیگ در هر فایل**:
- **[bypass-1](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-1.txt)**
- **[bypass-2](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-2.txt)**
- **[bypass-3](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-3.txt)**
- **[bypass-4](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-4.txt)**
- **[bypass-5](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-5.txt)**
- **[bypass-6](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-6.txt)**
- **[bypass-7](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-7.txt)**
- **[bypass-8](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-8.txt)**
- **[bypass-9](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-9.txt)**
- **[bypass-10](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-10.txt)**
- **[bypass-11](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-11.txt)**
- **[bypass-12](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-12.txt)**
- **[bypass-13](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-13.txt)**
- **[bypass-14](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-14.txt)**
- **[bypass-15](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass/bypass-15.txt)**

### کانفیگ‌های ناامن عبور از SNI/CIDR (bypass-unsecure/)

**[bypass-unsecure-all](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt)** - تمام کانفیگ‌های عبور از SNI/CIDR در یک فایل (شامل کانفیگ‌های ناامن)

**فایل‌های تفکیک شده بر اساس ۳۰۰ کانفیگ**:
- **[bypass-unsecure-1](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-1.txt)**
- **[bypass-unsecure-2](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-2.txt)**
- **[bypass-unsecure-3](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-3.txt)**
- **[bypass-unsecure-4](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-4.txt)**
- **[bypass-unsecure-5](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-5.txt)**
- **[bypass-unsecure-6](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-6.txt)**
- **[bypass-unsecure-7](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-7.txt)**
- **[bypass-unsecure-8](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-8.txt)**
- **[bypass-unsecure-9](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-9.txt)**
- **[bypass-unsecure-10](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-10.txt)**
- **[bypass-unsecure-11](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-11.txt)**
- **[bypass-unsecure-12](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-12.txt)**
- **[bypass-unsecure-13](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-13.txt)**
- **[bypass-unsecure-14](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-14.txt)**
- **[bypass-unsecure-15](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-15.txt)**
- **[bypass-unsecure-16](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-16.txt)**

### کانفیگ‌های تفکیک شده بر اساس پروتکل (split-by-protocols/)

**فایل‌های اختصاصی و امن هر پروتکل**:
- **[vless-secure.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/vless-secure.txt)** - فقط کانفیگ‌های امن VLESS
- **[vmess-secure.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/vmess-secure.txt)** - فقط کانفیگ‌های امن VMess
- **[trojan-secure.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/trojan-secure.txt)** - فقط کانفیگ‌های امن Trojan
- **[ss-secure.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/ss-secure.txt)** - فقط کانفیگ‌های امن Shadowsocks
- **[ssr-secure.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/ssr-secure.txt)** - فقط کانفیگ‌های امن ShadowsocksR
- **[tuic-secure.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/tuic-secure.txt)** - فقط کانفیگ‌های امن TUIC
- **[hysteria-secure.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/hysteria-secure.txt)** - فقط کانفیگ‌های امن Hysteria
- **[hysteria2-secure.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/hysteria2-secure.txt)** - فقط کانفیگ‌های امن Hysteria2
- **[hy2-secure.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/hy2-secure.txt)** - فقط کانفیگ‌های امن Hysteria2 (hy2)

**تمامی فایل‌های هر پروتکل (شامل کانفیگ‌های ناامن)**:
- **[vless.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/vless.txt)** - تمام کانفیگ‌های VLESS
- **[vmess.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/vmess.txt)** - تمام کانفیگ‌های VMess
- **[trojan.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/trojan.txt)** - تمام کانفیگ‌های Trojan
- **[ss.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/ss.txt)** - تمام کانفیگ‌های Shadowsocks
- **[ssr.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/ssr.txt)** - تمام کانفیگ‌های ShadowsocksR
- **[tuic.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/tuic.txt)** - تمام کانفیگ‌های TUIC
- **[hysteria.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/hysteria.txt)** - تمام کانفیگ‌های Hysteria
- **[hysteria2.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/hysteria2.txt)** - تمام کانفیگ‌های Hysteria2
- **[hy2.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/split-by-protocols/hy2.txt)** - تمام کانفیگ‌های Hysteria2 (hy2)

### پروکسی‌های تلگرام (tg-proxy/)

**فایل‌های حاوی پروکسی تلگرام برای عبور از فیلترینگ پیام‌رسان**:
- **[all.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/tg-proxy/all.txt)** - تمام پروکسی‌های تلگرام (MTProto + SOCKS5، مرتب‌شده بر اساس پینگ)
- **[MTProto.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/tg-proxy/MTProto.txt)** - فقط پروکسی‌های MTProto
- **[socks.txt](https://raw.githubusercontent.com/Amirchelios/clc-main/refs/heads/main/githubmirror/tg-proxy/socks.txt)** - فقط پروکسی‌های SOCKS5

[لینک به کدهای QR کانفیگ‌های همیشه معتبر](https://github.com/Amirchelios/clc-main/tree/main/qr-codes)

---
## نصب و نحوه استفاده

<details>
<summary>راهنمای اندروید (Android)</summary>

**۱.** برنامه **«v2rayNG»** نسخه‌ی universal.apk را دانلود کنید - [لینک دانلود](https://github.com/2dust/v2rayNG/releases)
همچنین می‌توانید از برنامه **«Happ»** استفاده کنید - [لینک گوگل‌پلی](https://play.google.com/store/apps/details?id=com.happproxy&hl=ru)، اما در تنظیمات: Subscriptions -> Sort by ping را فعال کنید.

**۲.** لینک یکی از کانفیگ‌ها را از بخش [پیکربندی‌ها و لینک‌ها](#پیکربندی‌ها-و-لینک‌ها) کپی کنید.

**۳.** وارد برنامه **«v2rayNG»** شوید، روی نماد + در بالا سمت راست ضربه بزنید و گزینه‌ی **«Import from clipboard»** را انتخاب کنید.

**۴.** روی منوی سه نقطه در بالا سمت راست کلیک کرده و **«Real delay all configuration»** (تست پینگ سرورها) را بزنید. پس از اتمام تست، در همان منو گزینه **«Sort by test results»** را بزنید تا سرورها بر اساس پینگ مرتب شوند.

**۵.** سرور مناسب را انتخاب کرده و روی دکمه‌ی اتصال ▶️ در پایین سمت راست ضربه بزنید.

</details>

<details>
<summary>راهنمای اندروید تی‌و‌ی (Android TV)</summary>

**۱.** نسخه universal.apk برنامه **«v2rayNG»** را دانلود و نصب کنید - [لینک دانلود](https://github.com/2dust/v2rayNG/releases)

**۲.** تصاویر **«QR-коды»** مربوط به کانفیگ‌ها را دانلود کنید - [لینک دانلود](https://github.com/Amirchelios/clc-main/tree/main/qr-codes)

**۳.** وارد برنامه شوید، روی + در بالا سمت راست کلیک کنید و **«Import from QR code»** را انتخاب کنید و تصویر دانلود شده را از گالری باز کنید.

**۴.** سه نقطه بالا سمت راست را بزنید، روی **«Real delay all configuration»** کلیک کنید و پس از اتمام تست، گزینه **«Sort by test results»** را بزنید.

**۵.** سرور مورد نظر را انتخاب و دکمه‌ی اتصال ▶️ در پایین سمت راست را فشار دهید.

</details>

<details>
<summary>عیب‌یابی و حل مشکلات احتمالی</summary>

**اگر بعد از اتصال اینترنت قطع شد (در v2rayNG)**
ویدئوی آموزشی حل این مشکل - [لینک ویدئو](https://t.me/avencoreschat/25254)

**اگر بعد از اد کردن لینک، کانفیگی اضافه نشد**
1. منوی همبرگری (سه خط) در بالا سمت چپ را بزنید.
2. روی گزینه **«Subscription group»** (یا Группы) کلیک کنید.
3. روی آیکون فلش چرخشی (به‌روزرسانی) در بالا سمت راست کلیک کنید و منتظر بمانید تا آپدیت کامل شود.

**رفع ارور "Cбой проверки интернет-соединения: net/http: 12X handshake timeout" یا "Fail to detect internet connection: io: read/write closed pipe"**
1. روی آیکون برنامه **«v2rayNG»** در صفحه گوشی نگه دارید و وارد **«App info»** (اطلاعات برنامه) شوید.
2. گزینه **«Force Stop»** (توقف اجباری) را بزنید و برنامه را مجدداً باز کنید.
3. مجدداً تست پینگ بگیرید، بر اساس پینگ مرتب کنید و متصل شوید.

**نحوه آپدیت دستی کانفیگ‌ها در v2rayNG**
1. روی نماد سه خط در بالا سمت چپ کلیک کنید.
2. تب **«Subscription group»** را انتخاب کنید.
3. آیکون چرخش فلش در بالا سمت راست را بزنید.

</details>

---
<details>
<summary>راهنمای ویندوز و لینوکس (Windows, Linux)</summary>

**۱.** نرم‌افزار **«Throne»** را دانلود کنید - [لینک دانلود](https://github.com/throneproj/Throne/releases)
ویندوز 10/11: فایل windows64.zip
ویندوز 7/8/8.1: فایل windowslegacy64.zip
لینوکس: فایل linux-amd64.zip

برنامه‌های جایگزین: **«nekoray»** - [لینک دانلود](https://github.com/MatsuriDayo/nekoray/releases) یا **«v2rayN»** - [لینک دانلود](https://github.com/2dust/v2rayN/releases)

**۲.** لینک کانفیگ مورد نظر را کپی کنید.

**۳.** در برنامه روی **«Profiles»** کلیک کرده و گزینه **«Add profile from clipboard»** را بزنید.

**۴.** با فشردن کلیدهای ترکیبی **«Ctrl + A»** تمام کانفیگ‌ها را انتخاب کرده، از منوی بالا روی **«Profiles»** و سپس **«Test latency (ping) of selected profile»** کلیک کنید. منتظر بمانید تا پیام اتمام تست در تب **«Logs»** ظاهر شود.

**۵.** روی ستون **«Latency (ping)»** کلیک کنید تا سرورها بر اساس پینگ مرتب شوند.

**۶.** در بالای صفحه اصلی برنامه، تیک گزینه‌ی **«TUN Mode»** را فعال کنید.

**۷.** یکی از کانفیگ‌های با پینگ پایین را انتخاب کرده، کلیک راست کنید و گزینه **«Start»** را بزنید.

</details>

<details>
<summary>راهنمای تکمیلی برای ویندوز</summary>

**رفع ارورهای MSVCP و VCRUNTIME در ویندوز 10/11**
1. کلیدهای **«Win+R»** را بفشارید و کلمه **«control»** را تایپ کنید تا Control Panel باز شود.
2. وارد **«Programs and Features»** شوید.
3. در کادر جستجوی بالا سمت راست کلمه **«Visual»** را سرچ کرده و تمام نسخه‌های مربوط به **«Microsoft Visual C++»** را پاک کنید.
4. این پکیج کامل را دانلود و استخراج کنید - [لینک دانلود](https://cf.comss.org/download/Visual-C-Runtimes-All-in-One-Jul-2025.zip)
5. فایل **«install_bat.all»** را به صورت *Run as Administrator* اجرا کنید و منتظر بمانید نصب کامل شود.

**به‌روزرسانی کانفیگ‌ها در NekoRay**
1. روی دکمه‌ی **«Preferences»** کلیک کنید.
2. گزینه **«Groups»** را انتخاب کنید.
3. روی دکمه‌ی **«Update all subscriptions»** کلیک کنید.

</details>

---
<details>
<summary>راهنمای آی‌او‌اس و آی‌پد (iOS, iPadOS)</summary>

**۱.** برنامه **«V2Box - V2ray Client»** را دانلود کنید - [لینک اپ‌استور](https://apps.apple.com/ru/app/v2box-v2ray-client/id6446814690)
برنامه جایگزین: **«Happ»** - [لینک اپ‌استور](https://apps.apple.com/us/app/happ-proxy-utility/id6504287215) (در تنظیمات گزینه Sort by ping فعال شود).

**۲.** لینک کانفیگ مورد نظر را کپی کنید.

**۳.** وارد برنامه **«V2Box»** شده و به بخش **«Config»** بروید. روی علامت + در بالا سمت راست کلیک کنید و **«Add Subscription»** را بزنید. یک نام دلخواه وارد کرده و لینک را در کادر **«URL»** پیست کنید.

**۴.** پس از اتمام پردازش، با ضربه زدن روی نام هر سرور آن را انتخاب کنید.

**۵.** در منوی پایینی برنامه، دکمه‌ی **«Connect»** را بزنید.

**به‌روزرسانی کانفیگ‌ها در V2Box:**
به تب **«Config»** بروید و روی آیکون به‌روزرسانی (فلش چرخشی) در کنار نام گروه اشتراک کلیک کنید.

</details>

---
<details>
<summary>راهنمای مک‌او‌اس (MacOS)</summary>

**۱.** برنامه **«Hiddify»** را دانلود کنید - [لینک دانلود مستقیم](https://github.com/hiddify/hiddify-app/releases/latest/download/Hiddify-MacOS.dmg)
همچنین می‌توانید از **«v2rayN»** استفاده کنید.

**۲.** روی گزینه **«New Profile»** کلیک کنید.

**۳.** لینک کانفیگ مورد نظر را کپی کنید.

**۴.** دکمه‌ی **«Add from Clipboard»** را در برنامه بزنید.

**۵.** به بخش **«Settings»** رفته و گزینه **«Routing Option»** را به **«Indonesia»** تغییر دهید.

**۶.** از منوی تنظیمات بالا سمت چپ، گزینه **«VPN Service»** را انتخاب کنید.

**۷.** با کلیک روی دکمه بزرگ وسط صفحه، **VPN** را روشن کنید.

**۸.** برای تغییر سرورها می‌توانید به تب **«Proxies»** بروید.

**به‌روزرسانی کانفیگ‌ها در Hiddify:**
برنامه را باز کرده، پروفایل مربوطه را انتخاب کنید و روی آیکون آپدیت در سمت چپ نام پروفایل کلیک کنید.

</details>

---

## اطلاعات تکمیلی

### ساختار ریپازیتوری
```text
githubmirror/         - فایل‌های متنی (.txt) تولید شده برای کانفیگ‌ها
 ├─ default/          - کانفیگ‌های اصلی (1.txt، 2.txt و ...، all.txt، all-secure.txt)
 ├─ bypass/           - کانفیگ‌های امن برای عبور از لیست سفید SNI/CIDR
 │   ├─ raw/          - کانفیگ‌های تست‌نشده خام (پیش از فرآیند تایید نهایی)
 │   └─ bypass-all.txt, bypass-1.txt, ... (تست شده و مرتب‌شده بر اساس پینگ)
 ├─ bypass-unsecure/  - تمام کانفیگ‌های عبور از SNI/CIDR (شامل موارد ناامن)
 │   ├─ raw/          - کانفیگ‌های خام پیش از تایید
 │   └─ bypass-unsecure-all.txt, bypass-unsecure-1.txt, ... (تست شده و مرتب بر اساس پینگ)
 ├─ split-by-protocols/ - فایل‌های تفکیک شده بر اساس پروتکل (vless.txt, vmess.txt و... در دو نسخه secure و unsecure)
 ├─ tg-proxy/         - پروکسی‌های تلگرام (all.txt، MTProto.txt، socks.txt)
qr-codes/            - نسخه‌های تصاویر PNG از کدهای QR جهت ایمپورت سریع
source/              - سورس‌کد اصلی برنامه ژنراتور
 ├─ main.py          - نقطه ورود اصلی برنامه (Main Entry Point)
 ├─ config/          - فایل‌های پیکربندی و تنظیمات اسکریپت
 │   ├─ settings.py  - تنظیمات عمومی، توکن‌ها، آدرس منابع ورودی و تایم‌زون‌ها
 │   ├─ URLS.txt     - لیست تمامی URLهای منابع ورودی کانفیگ‌ها
 │   ├─ servers.txt  - لیست سرورهای دستی جهت ادغام با خروجی
 │   ├─ whitelist-all.txt - لیست دامنه‌ها برای فیلترینگ SNI
 │   └─ cidrwhitelist.txt - لیست آدرس‌های CIDR برای فیلترینگ IP
 ├─ fetchers/        - ماژول‌های دانلود کانفیگ‌ها از منابع خارجی
 │   ├─ fetcher.py   - دانلودر پایه با استفاده از curl_cffi (سریع و با قابلیت دور زدن آنتی‌بات)
 │   ├─ daily_repo_fetcher.py - ماژول دانلود از ریپازیتوری‌های آپدیت روزانه
 │   ├─ telegram_proxy_scraper.py - اسکرپر اختصاصی پروکسی‌های تلگرام
 │   └─ yaml_converter.py - مبدل فایل‌های YAML (مانند کلش) به فرمت استاندارد VPN URL
 ├─ processors/      - بخش پردازش اصلی و فیلترینگ کانفیگ‌ها
 │   ├─ config_processor.py - حاوی منطق و بیزنس‌لاژیک اصلی پردازش فایل‌ها
 │   └─ telegram_proxy_processor.py - پردازشگر اختصاصی پروکسی‌های تلگرام
 ├─ utils/           - توابع کمکی و ابزارهای فرعی پروژه
 │   ├─ file_utils.py - عملیات روی فایل‌ها، فیلتر کانفیگ‌های ناامن و فیلترینگ SNI/CIDR
 │   ├─ logger.py    - سیستم لاگ‌نویسی بهینه و Thread-safe
 │   ├─ github_handler.py - تعامل با رابط GitHub API
 │   ├─ git_updater.py - ثبت کامیت‌های گیت (مخصوص حالت اجرا در GitHub Actions)
 │   ├─ config_verifier.py - بررسی وضعیت سرورها (DNS/TCP/HTTP) همراه با قابلیت کش
 │   ├─ xray_batch_tester.py - تست دسته‌ای سرورها به سبک v2rayN با Xray-core
 │   └─ telegram_proxy_verifier.py - تایید و ارزیابی پروکسی‌های تلگرام
 └─ requirements.txt - نیازمندی‌ها و پکیج‌های پایتونی پروژه
.github/workflows/   - تنظیمات CI/CD (جهت به‌روزرسانی خودکار و روزانه)
README.md            - همین فایل راهنما
docs/                - مستندات تکمیلی پروژه