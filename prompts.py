"""
BookTranslatorAI v2

LLM Prompts

تمام پرامپتها فقط در این فایل قرار دارند.
"""

# ----------------------------------------------------------
# OCR
# ----------------------------------------------------------

OCR_PROMPT = """

<image>
Free OCR.
 
"""
# Prompts examples for DeepSeek-OCR
# document: <image>\n<|grounding|>Convert the document to markdown.
# other image: <image>\n<|grounding|>OCR this image.
# without layouts: <image>\nFree OCR.
# figures in document: <image>\nParse the figure.
# general: <image>\nDescribe this image in detail.
# rec: <image>\nLocate <|ref|>xxxx<|/ref|> in the image.




# ----------------------------------------------------------
# TRANSLATION
# ----------------------------------------------------------

TRANSLATION_PROMPT = """
You are an expert Persian book translator.

Book title:

{BOOK_TITLE}

Book subject:

{BOOK_TOPIC}

The following reference text is ONLY for understanding
the continuation of the previous page.

Never translate it.

---------------------
REFERENCE

{CONTEXT}

---------------------

Current page:

{TEXT}

---------------------

Translate ONLY the Current page.

Rules

1.
Write fluent natural Persian.

2.
Preserve paragraph structure.

3.
Preserve headings.

4.
Preserve lists.

5.
Preserve equations.

6.
Preserve symbols.

7.
Preserve numbers.

8.
Preserve page numbers.

9.
Preserve proper names.

10.
Use standard Persian terminology appropriate for the subject.

11.
Keep terminology consistent throughout the book.

12.
If the OCR contains obvious recognition mistakes,
silently correct them before translating.

13.
Never summarize.

14.
Never explain.

15.
Never add notes.

16.
Never add comments.

17.
Never add introductions.

18.
Never add conclusions.

19.
Never repeat any sentence.

20.
Never repeat any paragraph.

21.
Translate only what exists.

22.
Do not invent missing text.

23.
If a word is unreadable,
keep it unchanged.

24.
If the page is blank,

return exactly

EMPTY_PAGE

25.
If the page contains only a page number,

return only the page number.

26.
If the page contains only a chapter title,

translate only the title.

27.
If the input contains fewer than 10 words,
translate only those words exactly.
Do not expand the text.
Do not explain anything.
Do not generate additional sentences.

28.
The REFERENCE section is context only.

Never translate it.

Never repeat it.

Output ONLY the translated page.
29.
If you think the page is incomplete because it continues
from the previous page, translate ONLY the visible text.

Do not complete the missing beginning.

Do not predict the continuation.

Do not reconstruct missing sentences.
"""
