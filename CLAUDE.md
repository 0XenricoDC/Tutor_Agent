# Tutor Agent - Project Documentation Tool

Tool per generare documentazione strutturata di progetti software.

## Build & Development

```bash
# Installazione dipendenze
pip install -r requirements.txt

# Generare PDF da markdown
python generate_pdf.py <file.md>
```

## Architecture

```
Tutor_Agent/
├── generate_pdf.py      # Script conversione MD -> PDF
├── TUTOR_PROMPT.md      # System prompt del tutor agent
├── requirements.txt     # Dipendenze (markdown, weasyprint)
└── README.md            # Documentazione progetto
```

## Workflow

1. Analizza un progetto con Claude usando il prompt in TUTOR_PROMPT.md
2. Salva l'output markdown generato
3. Converti in PDF con `python generate_pdf.py output.md`

## Output Structure

La documentazione generata include:
- Panoramica e stack tecnologico
- Architettura e pattern
- Analisi moduli principali
- Workflow di esecuzione
- Setup sviluppo
- Valutazione e suggerimenti
