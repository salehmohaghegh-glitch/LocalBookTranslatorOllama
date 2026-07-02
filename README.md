# LocalBookTranslatorOllama
Local AI-powered book translation pipeline using Ollama with OCR, context-aware translation, checkpoint resume and Markdown/JSON export.
# 📚 BookTranslatorAI

**BookTranslatorAI** is an offline AI-powered pipeline for translating scanned books using local Large Language Models (LLMs) through Ollama.

The project combines OCR, prompt engineering, context-aware translation, checkpoint recovery, and structured export to produce high-quality translations while running entirely on your own computer.

No cloud services or external APIs are required.

---
![Python](https://img.shields.io/badge/Python-3.10+-blue)

![License](https://img.shields.io/badge/License-MIT-green)

![Offline](https://img.shields.io/badge/Offline-Yes-success)

![Ollama](https://img.shields.io/badge/Ollama-Compatible-black)

![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-orange)
## ✨ Features

- Completely offline translation
- Local AI models powered by Ollama
- GLM OCR support for scanned pages
- Context-aware page-by-page translation
- Automatic resume after interruption
- Lightweight checkpoint system
- Simple loop detection to prevent repetitive AI outputs
- Handles empty or low-text pages
- Markdown export
- JSON export
- Backup translation model
- Easy configuration
- Designed for long books

---

# Workflow

```
Images
   │
   ▼
GLM OCR
   │
   ▼
OCR Validation
   │
   ▼
Context-aware Translation
   │
   ▼
Loop Detection
   │
   ▼
Quality Check
   │
   ├── OK ─────► Markdown + JSON
   │
   └── Retry
          │
          ▼
     Backup Model
```

---

# Why BookTranslatorAI?

Most OCR translation tools simply translate each page independently.

BookTranslatorAI keeps a small context from the previous page to improve translation continuity while avoiding the huge memory consumption of traditional translation memory systems.

The project is optimized for:

- scientific books
- engineering books
- historical books
- technical manuals
- educational documents

---

# Main Characteristics

Unlike many AI translation scripts, this project focuses on:

- Stable long-book translation
- Small memory footprint
- Simple architecture
- Easy debugging
- Local execution
- Human-editable prompts
- Reliable checkpoint recovery

---

# Requirements

- Python 3.10+
- Ollama
- GLM OCR model
- Translation model
- Windows / Linux

---

# Recommended Models

## OCR

```
glm-ocr:latest
```

## Translation

```
translategemma:4b
```

## Backup

```
Gemma4:e4b
```

Any Ollama-compatible model can be used.

---

# Installation

Clone repository

```bash
git clone https://github.com/USERNAME/BookTranslatorAI.git

cd BookTranslatorAI
```

Install Python packages

```bash
pip install -r requirements.txt
```

Install Ollama

https://ollama.com/

Download models

```bash
ollama pull glm-ocr

ollama pull translategemma:4b

ollama pull Gemma4:e4b
```

---

# Project Structure

```
BookTranslatorAI/

│
├── main.py
├── config.py
├── prompts.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── input/
│
├── output/
│
└── examples/
```

---

# Input

Copy scanned page images into

```
input/
```

Supported formats

- JPG
- PNG
- JPEG
- TIFF

---

# Run

```bash
python main.py
```

---

# Output

The translated book is generated as

```
output/

book.md
```

Each page is also exported as

```
0001.json

0002.json

...
```

---

# Checkpoint Recovery

The translator automatically saves

- last translated page
- last paragraph context

If the process stops unexpectedly, translation continues from the last completed page.

---

# Prompt Engineering

Instead of relying on complex translation memory systems, this project uses carefully designed prompts to improve translation quality.

The prompts are designed to:

- preserve formatting
- preserve paragraph order
- avoid AI hallucinations
- avoid endless repetition
- handle empty pages
- handle pages containing only page numbers
- keep terminology consistent
- improve translation continuity

Prompt customization is available through

```
prompts.py
```

---

# Configuration

Most settings can be modified in

```
config.py
```

including

- models
- directories
- retry count
- temperature
- checkpoint
- export options

---

# Roadmap

- [x] OCR
- [x] Local translation
- [x] Checkpoint resume
- [x] Loop detection
- [x] Markdown export
- [x] JSON export

Future plans

- [ ] GUI
- [ ] PDF input
- [ ] EPUB export
- [ ] DOCX export
- [ ] Multi-language interface
- [ ] Better OCR validation
- [ ] Translation quality scoring

---

# Contributing

Pull requests are welcome.

If you have ideas for improving translation quality, OCR accuracy, prompt engineering, or workflow optimization, feel free to open an issue or submit a pull request.

---

# License

This project is released under the MIT License.

See the LICENSE file for details.

---

# Acknowledgments

This project would not be possible without the following open-source projects:

- Ollama
- GLM OCR
- TranslateGemma
- Gemma
- Python

Special thanks to all contributors in the open-source AI community.

---

# Why this project was created

This project started from a simple idea:

> Translating a scanned book locally should be straightforward, reliable, and accessible to everyone.

Many existing AI translation workflows require cloud services, expensive APIs, or complex software stacks. While these solutions are powerful, they are not always practical for users who prefer offline processing, value privacy, or work with large collections of scanned books.

BookTranslatorAI was created to provide a lightweight alternative that combines OCR, prompt engineering, and local Large Language Models into a simple and transparent workflow.

The project is intentionally designed to be:

- Fully offline
- Easy to understand
- Easy to customize
- Easy to debug
- Efficient on consumer hardware

Rather than trying to replace professional translation software, BookTranslatorAI aims to be an open-source foundation that anyone can study, improve, and adapt to their own translation workflow.

Contributions, ideas, and feedback are always welcome.


# Disclaimer

BookTranslatorAI is intended as an AI-assisted translation tool.

Although the generated translations are often of high quality, human review is recommended before publication or commercial use.
