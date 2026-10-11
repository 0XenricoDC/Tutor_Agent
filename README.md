# 🎓 Tutor Agent — AI Project Documentation

> A prompt system that turns Claude Code into an expert programming tutor: it analyzes any software project and writes structured documentation, then a Python script converts it into a professional PDF.

![Claude Code](https://img.shields.io/badge/Claude_Code-prompt-D97757?logo=anthropic&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![PDF](https://img.shields.io/badge/output-PDF-EC1C24)

🇮🇹 [Versione italiana](./README.it.md)

---

## What you get

The generated documentation covers:

- Project overview and tech stack
- Architecture and design patterns
- Module-by-module analysis
- Execution workflows
- Developer setup guide
- Assessment and improvement suggestions

## Usage

### 1. Analyze a project with Claude Code

```bash
cd /path/to/your/project
claude
```

Then ask it to act as the tutor (the full system prompt is in [`TUTOR_PROMPT.md`](./TUTOR_PROMPT.md)), for example:

```
Analyze this project completely as an expert tutor and produce Markdown documentation.
```

### 2. Save the output

Save Claude's answer as a Markdown file, e.g. `project_docs.md`.

### 3. Generate the PDF

```bash
pip install -r requirements.txt
python generate_pdf.py project_docs.md
python generate_pdf.py project_docs.md "API Documentation.pdf"   # custom output name
```

## PDF features

- A4 professional layout with automatic title page
- Header / footer with page numbers
- Code blocks, bulleted and numbered lists

## Files

```
TUTOR_PROMPT.md    full system prompt for the tutor agent
generate_pdf.py    Markdown → PDF converter
requirements.txt   Python dependencies
```
