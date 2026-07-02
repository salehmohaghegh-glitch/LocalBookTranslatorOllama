# =====================================================
# Book Translator AI v2
# Main Program
# =====================================================

import json
import logging
import re
import base64
from pathlib import Path

import requests

from config import *
from prompts import OCR_PROMPT, TRANSLATION_PROMPT


# =====================================================
# Session
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
# Checkpoint
# =====================================================

def load_checkpoint():
    """
    خواندن آخرین وضعیت برنامه
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

    data = {

        "page": page,

        "context": context

    }

    with open(

        CHECKPOINT_FILE,

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

    if image is not None:

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

            data = response.json()

            if "response" not in data:

                raise Exception("Invalid response")

            text = data["response"].strip()

            if not text:

                raise Exception("Empty response")

            return text

        except Exception as e:

            logger.warning(

                f"Retry {attempt+1}: {e}"

            )

    return ""


# =====================================================
# OCR
# =====================================================

def ocr_page(image_path):
    """
    OCR صفحه
    """

    return call_ollama(

        OCR_MODEL,

        OCR_PROMPT,

        image_path

    )


# =====================================================
# Translation
# =====================================================

def translate_page(text, context=""):
    """
    ترجمه صفحه
    """

    if text == EMPTY_PAGE_TEXT:

        return EMPTY_PAGE_TEXT

    prompt = TRANSLATION_PROMPT.format(

        BOOK_TITLE=BOOK_TITLE,

        BOOK_TOPIC=BOOK_TOPIC,

        CONTEXT=context,

        TEXT=text

    )

    return call_ollama(

        TRANSLATE_MODEL,

        prompt

    )

# =====================================================
# Utility Functions
# =====================================================

def detect_loop(text):
    """
    تشخیص ساده خروجی‌های تکراری یا خراب
    """

    text = text.strip()

    if not text:
        return True

    if text == EMPTY_PAGE_TEXT:
        return False

    # پاسخهای رایج خراب
    bad_patterns = [

        "i'm sorry",

        "as an ai",

        "i cannot",

        "translation:",

        "translated:",

        "```"

    ]

    lower = text.lower()

    for item in bad_patterns:

        if item in lower:

            return True

    # تکرار بیش از حد یک خط
    lines = [

        line.strip()

        for line in text.splitlines()

        if line.strip()

    ]

    if not lines:

        return True

    for line in set(lines):

        if len(line) > 10 and lines.count(line) >= 3:

            return True

    return False


# =====================================================

def extract_last_paragraph(text):
    """
    استخراج آخرین پاراگراف برای Context
    """

    if not text:

        return ""

    paragraphs = [

        p.strip()

        for p in re.split(r"\n\s*\n", text)

        if p.strip()

    ]

    if not paragraphs:

        return ""

    return paragraphs[-1]


# =====================================================

def save_json(page, ocr_text, translation):
    """
    ذخیره خروجی JSON
    """

    if not SAVE_JSON:

        return

    file = JSON_DIR / f"{page:04d}.json"

    data = {

        "page": page,

        "ocr": ocr_text,

        "translation": translation

    }

    with open(

        file,

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
    افزودن ترجمه به فایل Markdown
    """

    if not SAVE_MARKDOWN:

        return

    with open(

        MARKDOWN_FILE,

        "a",

        encoding="utf-8"

    ) as f:

        f.write("\n\n")

        f.write("----------------------------------------\n")

        f.write(f"## Page {page}\n\n")

        f.write(translation)

        f.write("\n")


# =====================================================

def translate_with_retry(ocr_text, context):
    """
    ترجمه با Retry و Backup Model
    """

    if not ocr_text.strip():

        return FAILED_TRANSLATION

    # صفحه خالی
    if ocr_text == EMPTY_PAGE_TEXT:

        return EMPTY_PAGE_TEXT

    # فقط شماره صفحه
    if ocr_text.strip().isdigit():

        return ocr_text

    # تلاش با مدل اصلی
    for _ in range(MAX_RETRY):

        translated = translate_page(

            ocr_text,

            context

        )

        if not detect_loop(translated):

            return translated

    logger.warning("Using Backup Model")

    prompt = TRANSLATION_PROMPT.format(

        BOOK_TITLE=BOOK_TITLE,

        BOOK_TOPIC=BOOK_TOPIC,

        CONTEXT=context,

        TEXT=ocr_text

    )

    translated = call_ollama(

        BACKUP_MODEL,

        prompt

    )

    if detect_loop(translated):

        return FAILED_TRANSLATION

    return translated

# =====================================================
# Main Pipeline
# =====================================================

def main():
    print("=" * 60)
    print(PROJECT_NAME)
    print(f"OCR Model       : {OCR_MODEL}")
    print(f"Translate Model : {TRANSLATE_MODEL}")
    print(f"Backup Model    : {BACKUP_MODEL}")
    print(f"Input Folder    : {INPUT_DIR}")
    print(f"Output Folder   : {OUTPUT_DIR}")
    print("=" * 60)
    logger.info("=" * 60)
    logger.info("Book Translation Started")
    logger.info("=" * 60)

    # -------------------------------------------------
    # Resume
    # -------------------------------------------------

    checkpoint = load_checkpoint()

    start_page = checkpoint["page"] + 1

    context = checkpoint["context"]

    # -------------------------------------------------
    # Images
    # -------------------------------------------------
    images = sorted(
        (
            file
            for file in INPUT_DIR.iterdir()
            if file.suffix.lower() in SUPPORTED_IMAGES
        ),
        key=lambda f: int(re.search(r"\d+", f.stem).group())
    )

    if not images:

        print("No images found.")

        logger.error("No images found.")

        return

    print(f"{len(images)} pages found.\n")

    # -------------------------------------------------
    # Process Pages
    # -------------------------------------------------

    for page, image in enumerate(images, start=1):

        if page < start_page:

            continue

        print(f"[{page}/{len(images)}] {image.name}")

        logger.info(f"Page {page}")

        # ---------------------------------------------
        # OCR
        # ---------------------------------------------

        ocr_text = ocr_page(image)

        if not ocr_text:

            logger.warning("OCR failed.")

            continue

        # ---------------------------------------------
        # Translation
        # ---------------------------------------------

        translated = translate_with_retry(

            ocr_text,

            context

        )

        # ---------------------------------------------
        # Save
        # ---------------------------------------------

        save_json(

            page,

            ocr_text,

            translated

        )

        save_markdown(

            page,

            translated

        )

        # ---------------------------------------------
        # Update Context
        # ---------------------------------------------

        context = extract_last_paragraph(

            ocr_text

        )

        # ---------------------------------------------
        # Checkpoint
        # ---------------------------------------------

        save_checkpoint(

            page,

            context

        )

        logger.info(f"Page {page} completed.")

    logger.info("=" * 60)
    logger.info("Translation Finished")
    logger.info("=" * 60)

    print("\nTranslation Completed Successfully.")


# =====================================================
# Program Entry
# =====================================================

if __name__ == "__main__":


    try:

        main()

    except KeyboardInterrupt:

        print("\nInterrupted by user.")

        logger.warning("Interrupted by user.")

    except Exception as e:

        logger.exception(e)

        print("\nUnexpected Error")

    finally:

        session.close()
