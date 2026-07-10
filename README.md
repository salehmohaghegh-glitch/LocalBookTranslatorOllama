# 📚 BookTranslatorAI

[English](#english-documentation) | [فارسی](#مستندات-فارسی)

---

## English Documentation

### Local AI-powered book translation pipeline using Ollama with DeepSeek-OCR, context-aware translation, checkpoint resume, and Markdown/JSON export.

**BookTranslatorAI** is an offline AI-powered pipeline for translating scanned books using local Large Language Models (LLMs) through Ollama. The project combines advanced lightweight OCR triggers, prompt engineering, context-aware translation, checkpoint recovery, and structured bilingual export to produce high-quality translations while running entirely on your local machine. No cloud services or external APIs are required, preserving complete privacy.

---

### ✨ Features
* **100% Offline Execution:** Powered entirely by local models via Ollama.
* **DeepSeek-OCR Integration:** High-efficiency structural and mathematical formula recognition without layout bloat via structural `Free OCR.` processing.
* **Context-Aware Engine:** Passes the last paragraph of the previous page to maintain translation continuity across page breaks.
* **Robust Checkpoint System:** Automatically saves current pages and contexts to safely resume after sudden interruptions.
* **Loop & Hallucination Defense:** Advanced sequential line analysis and string constraints to prevent repetitive model traps.
* **Bilingual & Multi-Format Export:** Generates structured raw OCR Markdown, Persian translation Markdown, aligned Bilingual Markdown, and detailed page-by-page JSON files.

---

### 🔄 Pipeline Workflow
```
   Scanned Images (.png, .jpg)
                │
                ▼
      DeepSeek-OCR (Free OCR)
                │
                ▼
    Post-Processing Regex Filter ──► (Converts \[ \] to $$, cleans BBox residues)
                │
                ▼
     Context-Aware Translation ───► (Injects last translated paragraph)
                │
                ▼
     Loop & Anomaly Detection
                │
        ┌───────┴───────┐
        ▼               ▼
    [Success]       [Failure]
        │               │
        ▼               ▼
  Export Files    Backup Model
 (MD, JSON, BI)  (Gemma Fallback)
```

---

### ⚙️ System Requirements
* Python 3.10 or newer
* Ollama Framework Installed
* At least 8GB to 16GB of VRAM/RAM depending on target models
* Operating System: Windows, Linux, or macOS

---

### 🛠️ Step-by-Step Installation & Setup Guide

#### Step 1: Clone the Repository
Open your terminal or command prompt and run:
```bash
git clone https://github.com/USERNAME/BookTranslatorAI.git
cd BookTranslatorAI
```

#### Step 2: Install Python Dependencies
Ensure you have Python 3.10+ installed, then run:
```bash
pip install -r requirements.txt
```

#### Step 3: Install and Start Ollama
1. Download Ollama from the official website: [ollama.com](https://ollama.com).
2. Install it on your system and make sure the application or daemon is active.

#### Step 4: Download the Required Models
Execute the following commands in your terminal to fetch the optimized OCR and translation models:
```bash
# Pull the optimized OCR model
ollama pull deepseek-ocr:latest

# Pull the primary translation model
ollama pull translategemma:4b

# Pull the backup/fallback translation model
ollama pull Gemma4:latest
```

#### Step 5: Configure Your Project
Open `config.py` in your text editor and specify your book's parameters:
```python
BOOK_TITLE = "Your Book Title Here"
BOOK_TOPIC = "Brief abstract or topic keywords to guide translation terminology..."
```

#### Step 6: Load Input Data & Run
1. Place all your scanned book page images (sorted numerically, e.g., `page_1.png`, `page_2.png`) into the `input/` directory.
2. Run the main processing execution script:
```bash
python main.py
```

---

### 📁 Project Structure
```
BookTranslatorAI/
│
├── main.py                 # Main execution workflow pipeline
├── config.py               # Central project parameters and model configurations
├── prompts.py              # Optimized OCR and Translation prompt files
├── requirements.txt        # Python external library dependencies
├── README.md               # Unified English and Persian documentation
│
├── input/                  # Put your raw scanned page images here (.png, .jpg)
└── output/                 # Generated translations, raw OCR logs, and JSON backups
    ├── logs/               # Detailed pipeline logging file output
    ├── json/               # Page-by-page data snapshots
    └── temp/               # Temporary runtime caching storage
```

---

## مستندات فارسی

### پایپ‌لاین آفلاین ترجمه هوشمند کتاب با استفاده از Ollama، مدل تخصصی DeepSeek-OCR، فرآیند ترجمه پیوسته مبتنی بر کانتکست و قابلیت بازیابی خودکار چک‌پوینت.

پروژه **BookTranslatorAI** یک پایپ‌لاین کاملاً آفلاین و قدرتمند برای استخراج متن و ترجمه تخصصی کتاب‌های اسکن‌شده یا مصور علمی است. این ابزار با ترکیب تکنیک‌های نوین فعال‌سازی حالت اختصاصی بینایی، مهندسی پرامپت دقیق، در نظر گرفتن بستر متنی صفحات متوالی و سیستم بازیابی وضعیت پیشرفت، فایل‌هایی باکیفیت و ساختاریافته تولید می‌کند. تمام این فرآیند بدون نیاز به اینترنت و سرویس‌های ابری تجاری بر روی رایانه شخصی شما اجرا می‌شود.

---

### ✨ ویژگی‌های کلیدی
* **اجرای ۱۰۰٪ محلی و آفلاین:** حفظ کامل حریم خصوصی بدون وابستگی به کلیدهای API خارجی یا اینترنت.
* **یکپارچه‌سازی با DeepSeek-OCR:** استفاده از تریگر ساختاریافته‌ی `Free OCR.` جهت استخراج فوق‌العاده سریع متون و فرمول‌های ریاضی لیتک ($ و $$) بدون تولید مختصات پیکسلی و لایوت‌های مزاحم.
* **موتور ترجمه متصل به متن (Context-Aware):** تزریق خودکار آخرین پاراگراف صفحه قبل به مدل مترجم جهت حفظ یکپارچگی لحن، ارجاعات متنی و اصطلاحات تخصصی در خطوط مرزی صفحات.
* **سیستم هوشمند چک‌پوینت (Checkpoint Recovery):** ذخیره آنی وضعیت پیشرفت در پایان هر صفحه؛ در صورت قطع ناگهانی فرآیند، برنامه به طور خودکار از ابتدای آخرین صفحه ناتمام به کار خود ادامه می‌دهد.
* **مکانیسم ضد لوپ و هذیان هوش مصنوعی:** مجهز به لایه شناسایی توالی تکراری خطوط خروجی و توقف خودکار پردازش جهت جلوگیری از هدر رفتن منابع سخت‌افزاری.
* **خروجی‌های هم‌تراز دوزبانه:** تولید همزمان فایل‌های متنی مستقل OCR، فایل ترجمه فارسی روان، نسخه دوزبانه ستون به ستون (Bilingual) و خروجی‌های ساختاریافته‌ی JSON برای هر صفحه.

---

### 🔄 روال پایپ‌لاین و پردازش داده‌ها
```
   تصاویر اسکن شده ورودی (.png, .jpg)
                │
                ▼
      استخراج متن با DeepSeek-OCR
                │
                ▼
    فیلتر و پایش ساختاری Regex ──► (اصلاح ساختار لیتک \[ \] به $$ و پاکسازی کدهای اضافه)
                │
                ▼
    ترجمه هوشمند با پیوستگی متن ───► (تزریق آخرین پاراگراف ترجمه شده قبلی)
                │
                ▼
     بررسی کیفیت و الگوریتم ضد لوپ
                │
        ┌───────┴───────┐
        ▼               ▼
     [موفق]          [ناموفق]
        │               │
        ▼               ▼
  ذخیره خروجی‌ها     فراخوانی مدل پشتیبان
 (MD, JSON, BI)     (Gemma Fallback)
```

---

### ⚙️ نیازمندی‌های سیستم
* پایتون نسخه 3.10 یا بالاتر
* ابزار مدیریت مدل لوکال Ollama
* حافظه گرافیکی (VRAM) یا حافظه موقت (RAM) متناسب با حجم مدل‌های انتخابی (حداقل ۸ الی ۱۶ گیگابایت)
* سیستم‌عامل: ویندوز، لینوکس یا مک

---

### 🛠️ راهنمای گام‌به‌گام راه‌اندازی و اجرای صفر تا صد

#### گام اول: شبیه‌سازی یا دریافت مخزن پروژه
ترمینال یا خط فرمان (Command Prompt) خود را باز کرده و دستورات زیر را وارد کنید:
```bash
git clone https://github.com/USERNAME/BookTranslatorAI.git
cd BookTranslatorAI
```

#### گام دوم: نصب پکیج‌ها و پیش‌نیازهای پایتون
مطمئن شوید پایتون نسخه 3.10+ در سیستم شما نصب و فعال است، سپس دستور زیر را اجرا کنید:
```bash
pip install -r requirements.txt
```

#### گام سوم: نصب و فعال‌سازی نرم‌افزار Ollama
1. به سایت رسمی اولاما مراجعه کرده و آن را متناسب با سیستم‌عامل خود دانلود کنید: [ollama.com](https://ollama.com).
2. نرم‌افزار را نصب کرده و مطمئن شوید که سرویس آن در پس‌زمینه در حال اجرا است.

#### گام چهارم: دانلود مدل‌های هوش مصنوعی مورد نیاز
برای دانلود مدل تخصصی پردازش تصویر و مدل‌های ترجمه، دستورات زیر را به ترتیب در ترمینال وارد کنید تا فرآیند دانلود محلی آغاز شود:
```bash
# دانلود مدل تخصصی استخراج متن و فرمول
ollama pull deepseek-ocr:latest

# دانلود مدل اصلی ترجمه تخصصی متون
ollama pull translategemma:4b

# دانلود مدل پشتیبان جهت استفاده در مواقع اضطراری یا لوپ
ollama pull Gemma4:latest
```

#### گام پنجم: تنظیم مشخصات کتاب جاری
فایل `config.py` را با یک ادیتور متنی باز کنید و عنوان و موضوع خلاصه کتاب خود را بنویسید (این اطلاعات به مترجم کمک می‌کند تا اصطلاحات علمی را متناسب با موضوع حدس بزند):
```python
BOOK_TITLE = "عنوان کتاب شما در این قسمت"
BOOK_TOPIC = "موضوع خلاصه، کلمات کلیدی یا چکیده کتاب جهت هماهنگ‌سازی واژگان تخصصی..."
```

#### گام ششم: بارگذاری تصاویر و شروع فرآیند پردازش
1. تصاویر صفحات کتاب اسکن‌شده را (که به ترتیب شماره‌گذاری شده‌اند، مانند `1.png` یا `page_001.jpg`) داخل پوشه `input/` کپی کنید.
2. اسکریپت اصلی برنامه را برای شروع عملیات فراخوانی کنید:
```bash
python main.py
```

---

### 📁 ساختار پرونده‌های پروژه
```
BookTranslatorAI/
│
├── main.py                 # هسته اصلی و مدیریت پایپ‌لاین اجرای برنامه
├── config.py               # فایل مرکزی تنظیمات متغیرها، مسیرها و مدل‌ها
├── prompts.py              # پرامپت‌ها و دستورات بهینه‌سازی شده سیستم برای مدل‌ها
├── requirements.txt        # پکیج‌ها و کتابخانه‌های خارجی پایتون مورد نیاز
├── README.md               # مستندات جامع و راهنمای دو زبانه فعلی پروژه
│
├── input/                  # پوشه مبدا؛ تصاویر صفحات اسکن شده را اینجا قرار دهید
└── output/                 # پوشه مقصد؛ فایل‌های ترجمه، خروجی خام متون و جی‌سان‌ها
    ├── logs/               # فایل لاگین دقیق سیستم جهت رهگیری خطاهای احتمالی
    ├── json/               # فایل‌های پشتیبان صفحه‌به‌صفحه برای دسترسی‌های آینده
    └── temp/               # ذخیره‌سازی موقت لایه‌های در حال پردازش سیستم
```

---

### 📄 License / مجوز
This project is licensed under the MIT License - see the LICENSE file for details.  
این پروژه تحت مجوز بین‌المللی MIT منتشر شده است؛ استفاده و توسعه آن با ذکر نام منبع کاملاً آزاد است.