"""
=====================================================
Book Translator AI
Configuration File
=====================================================
فقط تنظیمات پروژه
"""
import re

def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()

from pathlib import Path

# =====================================================
# Project
# =====================================================

PROJECT_NAME = "Book Translator AI"

VERSION = "2.0"

# =====================================================
# Book Information
# =====================================================

BOOK_TITLE = "Your Book Name "

BOOK_TOPIC = """
Your book Abstract for translation model attention

"""

SOURCE_LANGUAGE = "English"

TARGET_LANGUAGE = "Persian" 

# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).parent

INPUT_DIR = BASE_DIR / "input"

OUTPUT_DIR = BASE_DIR / "output"

LOG_DIR = OUTPUT_DIR / "logs"

JSON_DIR = OUTPUT_DIR / "json"

TEMP_DIR = OUTPUT_DIR / "temp"

INPUT_DIR.mkdir(exist_ok=True)

OUTPUT_DIR.mkdir(exist_ok=True)

LOG_DIR.mkdir(exist_ok=True)

JSON_DIR.mkdir(exist_ok=True)

TEMP_DIR.mkdir(exist_ok=True)

# =====================================================
# Output Files
# =====================================================

MARKDOWN_FILE = OUTPUT_DIR / f"{safe_filename(BOOK_TITLE)}.md"

OCR_MARKDOWN_FILE = OUTPUT_DIR / f"{safe_filename(BOOK_TITLE)}.ocr.md"

TRANSLATION_MARKDOWN_FILE = OUTPUT_DIR / f"{safe_filename(BOOK_TITLE)}.fa.md"

BILINGUAL_MARKDOWN_FILE = OUTPUT_DIR / f"{safe_filename(BOOK_TITLE)}.bilingual.md"

CHECKPOINT_FILE = OUTPUT_DIR / "checkpoint.json"

LOG_FILE = LOG_DIR / "translator.log"

# =====================================================
# Ollama
# =====================================================

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

TIMEOUT = 300

STREAM = False

# =====================================================
# Models
# =====================================================

OCR_MODEL ="deepseek-ocr:latest"  #"glm-ocr:latest"  "deepseek-ocr:latest" 

TRANSLATE_MODEL =  "translategemma:4b "   #"Gemma4:e4b" "translategemma:4b "

BACKUP_MODEL ="Gemma4:latest " #"translategemma:4b " 

# =====================================================
# Retry
# =====================================================

MAX_RETRY = 3

# =====================================================
# Generation
# =====================================================

TEMPERATURE = 0.1

TOP_P = 0.9

TOP_K = 40

REPEAT_PENALTY = 1.05

NUM_PREDICT = 8192

# =====================================================
# Context
# =====================================================

USE_CONTEXT = True

# فقط آخرین پاراگراف صفحه قبل
CONTEXT_PARAGRAPHS = 1

# =====================================================
# Validation
# =====================================================

EMPTY_PAGE_TEXT = "EMPTY_PAGE"

FAILED_TRANSLATION = "[TRANSLATION FAILED]"

# =====================================================
# Supported Images
# =====================================================

SUPPORTED_IMAGES = (
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp"
)

# =====================================================
# Logging
# =====================================================

LOG_LEVEL = "INFO"

# =====================================================
# Save Options
# =====================================================

SAVE_JSON = True

SAVE_MARKDOWN = True



