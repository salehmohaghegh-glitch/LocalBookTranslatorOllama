# =====================================================
# BookTranslatorAI
# Main Program
# Version 2.0
# =====================================================

import base64
import json
import logging
import re
from pathlib import Path

import requests

from config import (
    PROJECT_NAME,
    VERSION,
    OLLAMA_URL,
    OCR_MODEL,
    TRANSLATE_MODEL,
    BACKUP_MODEL,
    INPUT_DIR,
    OUTPUT_DIR,
    JSON_DIR,
    MARKDOWN_FILE,
    CHECKPOINT_FILE,
    LOG_FILE,
    BOOK_TITLE,
    BOOK_TOPIC,
    STREAM,
    TEMPERATURE,
    TOP_P,
    TOP_K,
    REPEAT_PENALTY,
    NUM_PREDICT,
    MAX_RETRY,
    TIMEOUT,
    SAVE_JSON,
    SAVE_MARKDOWN,
    SUPPORTED_IMAGES,
    EMPTY_PAGE_TEXT,
    FAILED_TRANSLATION,
)
from prompts import (
    OCR_PROMPT,
    TRANSLATION_PROMPT,
)

# =====================================================
# HTTP Session
# =====================================================

session = requests.Session()

# =====================================================
# Logger
# =====================================================

logging.basicConfig(

    filename=LOG_FILE,

    level=logging.INFO,

    encoding="utf-8",

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)

# =====================================================
# Startup
# =====================================================

def print_header():

    print("=" * 60)
    print(f"{PROJECT_NAME}   v{VERSION}")
    print("=" * 60)
    print()


def print_ok(text):

    print(f"✓ {text}")


def print_error(text):

    print(f"✗ {text}")


def check_ollama():
    """
    بررسی اجرای Ollama
    """

    try:

        requests.get(

            "http://127.0.0.1:11434",

            timeout=2

        )

        return True

    except:

        return False


def startup():
    """
    بررسی اولیه برنامه
    """

    print_header()

    print("Checking Ollama...")

    if not check_ollama():

        print_error("Ollama is not running.")
        print()
        print("Please start Ollama and run the program again.")
        print()

        input("Press Enter to exit...")

        return False

    print_ok("Ollama is running.")

    if not INPUT_DIR.exists():

        print_error("Input folder not found.")

        return False

    OUTPUT_DIR.mkdir(

        parents=True,

        exist_ok=True

    )

    images = sorted(

        [

            file

            for file in INPUT_DIR.iterdir()

            if file.suffix.lower() in SUPPORTED_IMAGES

        ],

        key=lambda f: int(

            re.search(

                r"\d+",

                f.stem

            ).group()

        )

    )

    if not images:

        print_error("No images found.")

        return False

    print_ok(f"Pages Found : {len(images)}")

    print()

    print("-" * 60)

    print("Configuration")

    print("-" * 60)

    print(f"OCR Model       : {OCR_MODEL}")
    print(f"Translate Model : {TRANSLATE_MODEL}")
    print(f"Backup Model    : {BACKUP_MODEL}")

    print()

    print(f"Book Title : {BOOK_TITLE}")

    print("-" * 60)

    print()

    return images
# =====================================================
# Checkpoint
# =====================================================

def load_checkpoint():
    """
    خواندن آخرین وضعیت ترجمه
    """

    if not CHECKPOINT_FILE.exists():

        return {
            "page": 0,
            "context": ""
        }

    try:

        with open(
            CHECKPOINT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception as e:

        logger.error(e)

        return {
            "page": 0,
            "context": ""
        }


def save_checkpoint(page, context):
    """
    ذخیره آخرین صفحه ترجمه شده
    """

    with open(
        CHECKPOINT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(

            {
                "page": page,
                "context": context
            },

            f,

            ensure_ascii=False,

            indent=4

        )


# =====================================================
# Ollama
# =====================================================

def call_ollama(model, prompt, image=None):
    """
    ارسال درخواست به Ollama
    """

    payload = {

        "model": model,

        "prompt": prompt,

        "stream": STREAM,

        "options": {

            "temperature": TEMPERATURE,

            "top_p": TOP_P,

            "top_k": TOP_K,

            "repeat_penalty": REPEAT_PENALTY,

            "num_predict": NUM_PREDICT

        }

    }

    if image:

        with open(image, "rb") as f:

            payload["images"] = [

                base64.b64encode(

                    f.read()

                ).decode()

            ]

    for attempt in range(MAX_RETRY):

        try:

            response = session.post(

                OLLAMA_URL,

                json=payload,

                timeout=TIMEOUT

            )

            response.raise_for_status()

            answer = response.json().get(

                "response",

                ""

            ).strip()

            if answer:

                return answer

        except Exception as e:

            logger.warning(

                f"{model} Retry {attempt+1}: {e}"

            )

    logger.error(

        f"{model} failed."

    )

    return ""


# =====================================================
# OCR
# =====================================================

def ocr_page(image_path):
    """
    OCR یک صفحه
    """

    text = call_ollama(

        OCR_MODEL,

        OCR_PROMPT,

        image_path

    )

    if not text:

        return EMPTY_PAGE_TEXT

    return text


# =====================================================
# Translation
# =====================================================

def translate_page(text, context=""):
    """
    ترجمه یک صفحه
    """

    if not text:

        return FAILED_TRANSLATION

    if text == EMPTY_PAGE_TEXT:

        return EMPTY_PAGE_TEXT

    prompt = TRANSLATION_PROMPT.format(

        BOOK_TITLE=BOOK_TITLE,

        BOOK_TOPIC=BOOK_TOPIC,

        CONTEXT=context,

        TEXT=text

    )

    translated = call_ollama(

        TRANSLATE_MODEL,

        prompt

    )

    if translated:

        return translated

    logger.warning(

        "Using backup model."

    )

    translated = call_ollama(

        BACKUP_MODEL,

        prompt

    )

    if translated:

        return translated

    return FAILED_TRANSLATION

# =====================================================
# Utility Functions
# =====================================================

def detect_loop(text):
    """
    تشخیص ساده خروجی خراب یا تکراری
    """

    if not text:

        return True

    text = text.strip()

    if text == EMPTY_PAGE_TEXT:

        return False

    lower = text.lower()

    bad_patterns = (

        "i'm sorry",

        "as an ai",

        "i cannot",

        "translation:",

        "translated:",

        "```"

    )

    for item in bad_patterns:

        if item in lower:

            return True

    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()

    ]

    if len(lines) >= 3:

        if len(set(lines)) == 1:

            return True

    return False


# =====================================================

def extract_last_paragraph(text):
    """
    استخراج آخرین پاراگراف
    """

    if not text:

        return ""

    paragraphs = [

        p.strip()

        for p in re.split(

            r"\n\s*\n",

            text

        )

        if p.strip()

    ]

    if not paragraphs:

        return ""

    return paragraphs[-1]


# =====================================================

def save_json(page, ocr_text, translation):
    """
    ذخیره JSON
    """

    if not SAVE_JSON:

        return

    filename = JSON_DIR / f"{page:04d}.json"

    data = {

        "page": page,

        "ocr": ocr_text,

        "translation": translation

    }

    with open(

        filename,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            ensure_ascii=False,

            indent=4

        )


# =====================================================

def save_markdown(page, translation):
    """
    افزودن صفحه به Markdown
    """

    if not SAVE_MARKDOWN:

        return

    with open(

        MARKDOWN_FILE,

        "a",

        encoding="utf-8"

    ) as f:

        f.write("\n\n")
        f.write("=" * 50)
        f.write("\n")
        f.write(f"## Page {page}")
        f.write("\n\n")
        f.write(translation)
        f.write("\n")


# =====================================================

def process_translation(ocr_text, context):
    """
    کنترل کیفیت ترجمه
    """

    translated = translate_page(

        ocr_text,

        context

    )

    if translated == FAILED_TRANSLATION:

        return translated

    if detect_loop(translated):

        logger.warning(

            "Loop detected."

        )

        return FAILED_TRANSLATION

    return translated

# =====================================================
# Main Pipeline
# =====================================================

def main():

    # بررسی اولیه
    images = startup()

    if not images:
        return

    # ایجاد پوشه‌های خروجی
    if SAVE_JSON:
        JSON_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    # بارگذاری آخرین وضعیت
    checkpoint = load_checkpoint()

    start_page = checkpoint["page"]

    context = checkpoint["context"]

    total_pages = len(images)

    print()
    print("=" * 60)
    print("Translation Started")
    print("=" * 60)
    print()

    # پردازش صفحات
    for index, image_path in enumerate(images, start=1):

        if index <= start_page:
            continue

        print(f"[{index}/{total_pages}] {image_path.name}")

        # ---------------- OCR ----------------

        ocr_text = ocr_page(image_path)

        # ---------------- Translation ----------------

        translation = process_translation(
            ocr_text,
            context
        )

        # ---------------- Save ----------------

        save_json(
            index,
            ocr_text,
            translation
        )

        save_markdown(
            index,
            translation
        )

        # ---------------- Context ----------------

        context = extract_last_paragraph(
            translation
        )

        save_checkpoint(
            index,
            context
        )

        logger.info(
            f"Page {index} completed."
        )

    print()
    print("=" * 60)
    print("Translation Finished")
    print("=" * 60)

# =====================================================
# Program Entry
# =====================================================

if __name__ == "__main__":

    main()
    
