


# 📚 LocalBookTranslatorOllama

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Ollama-Compatible-black?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Offline-100%25-success?style=for-the-badge" alt="Offline Ready">
</p>

<p align="center">
  <strong>An enterprise-grade, completely offline AI pipeline to extract, sanitize, and translate scanned technical books using DeepSeek-OCR and local LLMs via Ollama.</strong>
</p>

---

## 🌐 Documentation / مستندات
* [English Documentation](#english-documentation)
* [راهنمای جامع فارسی](#مستندات-فارسی)

---

## English Documentation

### 🚀 Overview
**BookTranslatorAI** is a robust, production-ready document processing pipeline engineered for researchers, engineers, and archivists who need to translate scanned textbooks, scientific papers, and technical manuals without exposing data to external cloud APIs. 

By wrapping local state-of-the-art vision-language and translation models inside a context-preserving architecture, it guarantees fluid, professional-grade Persian translations while operating completely on consumer-grade local hardware.

### 💡 Key Capabilities
* **Privacy-First Architecture:** Zero network requests. Your books never leave your local machine.
* **Layout-Agnostic DeepSeek-OCR:** Leverages the raw semantic extraction power of `deepseek-ocr` using the optimized `Free OCR.` structural trigger. It captures complex inline and block mathematical formulas without cluttering your text with complex absolute layout coordinates.
* **Contextual Continuum (Page-Aware):** Injects the last paragraph of the previous page into the prompt window of the next translation cycle. This eliminates disjointed sentences at page breaks and maintains consistent technical terminology.
* **Self-Healing Checkpoint Engine:** Progress is securely committed to disk page-by-page. If your hardware encounters a power loss or crash, the system resumes immediately from the exact paragraph it left off.
* **Hallucination & Infinite-Loop Defense:** Monitors generation behavior for sequential line repetitions and abnormal string lengths, automatically engaging safety mitigation layers.
* **Multi-Avenue Aligned Export:** Compiles separate markdown documents for raw OCR text, smooth Persian translation, and a perfectly aligned column-by-column bilingual master document alongside step-by-step granular JSON snapshots.

---

### 📦 Recommended Model Matrix

| Pipeline Role | Target Model | Parameter Size | Memory (VRAM) | Primary Objective |
| :--- | :--- | :--- | :--- | :--- |
| **Vision / OCR** | `deepseek-ocr:latest` | ~7B | ~6.5 GB | Layout-free structural LaTeX & raw text extraction. |
| **Primary Translator**| `translategemma:4b` | 4B | ~4.0 GB | High-fidelity technical English-to-Persian translation. |
| **Fallback / Shield** | `Gemma4:latest` | 4B / 9B | ~6.0 GB | Disengages repetitive loops and resolves anomalies. |

---

### 🔄 Architectural Pipeline Data Flow

```

[Scanned Input Images] (.png, .jpg, .tiff)

│

▼

[DeepSeek-OCR Engine] ◄── Triggered by "Free OCR." structure

│

▼

[Regex Cleaning Matrix] ◄── Converts structural

$$ $$

to $$, purges BBox noises

│

▼

[Context Injector Layer] ◄── Merges previous page's final paragraph

│

▼

[Ollama Translation Core] ◄── Translates page content smoothly

│

▼

[Loop & Anomaly Defense] ───► [Anomaly Detected?]

│ │

┌───────┴───────┐ ├─► YES ──► [Deploy Fallback Model]

▼ ▼ │

[No Loop] [Resolved] ◄───────────┘

│

▼

[Structured Publisher] ───► Outputs: .md (Raw), .md (Persian), .md (Bilingual), .json

````

---

### 🛠️ Step-by-Step Production Setup

#### 1. Repository Setup
Clone the codebase and initialize the environment footprint:
```bash
git clone git clone https://github.com/salehmohaghegh-glitch/LocalBookTranslatorOllama
cd BookTranslatorAI
````

#### 2. Install Core Dependencies

Deploy the internal pipeline communication frameworks:

Bash

```
pip install -r requirements.txt
```

#### 3. Establish Local LLM Infrastructure

Install the Ollama environment from [ollama.com](https://ollama.com/). Once the Ollama service daemon is active in your background system tray, fetch the target execution models:

Bash

```
# Pull the optimized vision-text extraction model
ollama pull deepseek-ocr:latest

# Pull the dedicated dictionary-aligned translation model
ollama pull translategemma:4b

# Pull the auxiliary backup model
ollama pull Gemma4:latest
```

#### 4. Configure Translation Terminology

Open `config.py` in your development environment to define global book behaviors. Supplying a clear topic helps the model map domain-specific terminology precisely:

Python

```
BOOK_TITLE = "Quantum Mechanics and Electrodynamics"
BOOK_TOPIC = "Theoretical physics, wave functions, Maxwell equations, and matrix mechanics"
```

#### 5. Execute Processing Pipeline

Feed your raw book pages into the `input/` directory (ensure alphanumeric order, e.g., `0001.jpg`, `0002.jpg`), then spin up the processor:

Bash

```
python main.py
```

### 📁 Pipeline File Mapping

```
BookTranslatorAI/
│
├── main.py                 # Core processing orchestrator and state engine
├── config.py               # Hyperparameters, model allocations, and global variables
├── prompts.py              # System prompt blueprints for OCR and Translation layers
├── requirements.txt        # Downstream library versions (requests, etc.)
│
├── input/                  # Feed source directory for scanned page images
└── output/                 # Publisher target directory for generated artifacts
    ├── logs/               # Live telemetry and pipeline debugging file output
    ├── json/               # Page-by-page immutable data snapshots
    └── temp/               # Active runtime cache and state preservation layers
```

## مستندات فارسی

### 🚀 مرور اجمالی پروژه

پروژه **BookTranslatorAI** یک پایپ‌لاین پیشرفته و صنعتی جهت استخراج متون، فرمول‌زدایی و ترجمه تخصصی کتاب‌های مصور، دانشگاهی و اسناد فنی اسکن‌شده است. این سیستم به گونه‌ای مهندسی شده تا پژوهشگران، مترجمان و توسعه‌دهندگان بتوانند بدون ارسال صفحات کتاب به سرویس‌های ابری تجاری و حفظ ۱۰۰٪ حریم خصوصی، متون پیچیده علمی را به فارسی روان ترجمه کنند.

این ابزار با متصل کردن مدل‌های زبانی بینایی (VLM) محلی به هسته ترجمه متصل به کانتکست، بر روی سخت‌افزارهای استاندارد خانگی بالاترین بازدهی را ارائه می‌دهد.

### 💡 ویژگی‌های کلیدی و برجسته

- **امنیت کامل داده‌ها (Zero-Cloud):** فرآیند پردازش تصویر و ترجمه کاملاً درون سیستم شما اتفاق می‌افتد و نیازی به اتصال به اینترنت وجود ندارد.
    
- **استخراج بدون اعوجاج با DeepSeek-OCR:** استفاده از مدل بینایی قدرتمند `deepseek-ocr` به همراه کلیدواژه ساختاریافته‌ی `Free OCR.` جهت استخراج فوق‌العاده دقیق فرمول‌های ریاضی پیچیده لیتک ($ و $$) و کدهای برنامه‌نویسی بدون درگیر شدن با کدهای لایوت اضافه و مختصات پیکسلی مزاحم.
    
- **پیوستگی معنایی مرز صفحات (Context-Aware):** سیستم به طور هوشمند آخرین پاراگراف ترجمه‌شده از صفحه قبل را به پنجره پردازش صفحه جدید تزریق می‌کند تا شکستگی لحن در خطوط مرزی صفحات کاملاً از بین برود.
    
- **چک‌پوینت مقاوم در برابر خطا (Self-Healing):** ثبت گام‌به‌گام وضعیت پیشرفت هر صفحه روی دیسک؛ در صورت بروز قطعی برق یا کرش سیستم، پردازش دقیقاً از خط اول آخرین صفحه ناتمام از سر گرفته می‌شود.
    
- **لایه دفاعی ضد لوپ (Anti-Loop Layer):** پایش مداوم فرآیند تولید متن جهت شناسایی الگوهای هذیان یا تکرار بی‌انتهای خطوط توسط هوش مصنوعی و تصحیح آنی مسیر پردازش.
    
- **خروجی‌های هم‌تراز همزمان:** تولید موازی نسخه خام متون استخراج شده، نسخه ترجمه شده فارسی، فایل یکپارچه دوزبانه (Bilingual ستون به ستون) به همراه پایگاه داده ساختاریافته‌ی JSON برای هر صفحه به طور مجزا.
    

### 📦 ماتریس فنی مدل‌های هوش مصنوعی

|**نقش در پایپ‌لاین**|**مدل عملیاتی**|**حجم پارامتر**|**حافظه گرافیکی مورد نیاز (VRAM)**|**هدف اصلی پردازش**|
|---|---|---|---|---|
|**بینایی / استخراج متن**|`deepseek-ocr:latest`|~7B|حدود ۶.۵ گیگابایت|استخراج متن خام و فرمول‌های لیتک بدون لایوت مزاحم.|
|**مترجم اصلی سیستم**|`translategemma:4b`|4B|حدود ۴.۰ گیگابایت|ترجمه تخصصی و اصطلاح‌شناسی دقیق انگلیسی به فارسی.|
|**مدل پشتیبان و ایمنی**|`Gemma4:latest`|4B / 9B|حدود ۶.۰ گیگابایت|شکستن لوپ‌های تکرار متن و مدیریت خطاهای ساختاری.|

### 🔄 راهنمای گام‌به‌گام راه‌اندازی و اجرای صفر تا صد

#### گام اول: دریافت مخزن پروژه

خط فرمان یا ترمینال سیستم خود را باز کرده و دستورات زیر را برای دریافت سورس‌کد وارد کنید:

Bash

```
git clone https://github.com/salehmohaghegh-glitch/LocalBookTranslatorOllama
cd BookTranslatorAI
```

#### گام دوم: نصب پکیج‌های پیش‌نیاز

نیازمندی‌های ارتباطی پایپ‌لاین پایتون را با دستور زیر به طور خودکار نصب کنید (توصیه می‌شود از Python 3.10 یا بالاتر استفاده کنید):

Bash

```
pip install -r requirements.txt
```

#### گام سوم: راه‌اندازی زیرساخت محلی Ollama

1. ابزار اولاما را متناسب با سیستم‌عامل خود از [ollama.com](https://ollama.com/) دانلود و نصب کنید.
    
2. پس از اطمینان از فعال بودن سرویس اولاما در پس‌زمینه سیستم، مدل‌های بهینه‌سازی شده زیر را در ترمینال فراخوانی کنید تا به صورت لوکال دانلود شوند:
    

Bash

```
# دریافت مدل تخصصی پردازش تصویر و فرمول
ollama pull deepseek-ocr:latest

# دریافت مدل بهینه شده برای واژگان تخصصی ترجمه
ollama pull translategemma:4b

# دریافت مدل لایه ایمنی و پشتیبان
ollama pull Gemma4:latest
```

#### گام چهارم: بومی‌سازی واژگان کتاب (پیکربندی)

فایل تنظیمات مرکزی پروژه یعنی `config.py` را باز کرده و مشخصات کتاب خود را وارد کنید. تعریف کلمات کلیدی به مترجم هوشمند کمک می‌کند تا معادل‌های تخصصی را متناسب با گرایش علمی کتاب انتخاب کند:

Python

```
BOOK_TITLE = "Quantum Mechanics and Electrodynamics"
BOOK_TOPIC = "فیزیک نظری، تابع موج، معادلات ماکسول و مکانیک ماتریسی"
```

#### گام پنجم: بارگذاری صفحات و استارت نهایی

تصاویر صفحات اسکن‌شده خود را به ترتیب حروف یا اعداد (مانند `page_01.jpg`, `page_02.png`) در پوشه `input/` قرار داده و با دستور زیر موتور پردازش را روشن کنید:

Bash

```
python main.py
```

### 📄 License / مجوز

This project is licensed under the MIT License - see the LICENSE file for details.

این پروژه تحت مجوز بین‌المللی MIT منتشر شده است؛ توسعه، تجاری‌سازی و استفاده از آن با حفظ حق مالکیت معنوی اثر کاملاً آزاد است.

```
