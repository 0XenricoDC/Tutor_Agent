# Project Tutor Agent

Sistema di prompt per Claude che funziona come tutor esperto di programmazione e workflow.
Analizza progetti software e genera documentazione PDF professionale.

## Installazione

```bash
cd project_tutor_agent
pip install -r requirements.txt
```

## Uso Rapido

### 1. Analizza un progetto con Claude

Apri Claude Code nella cartella del progetto:
```bash
cd /percorso/del/progetto
claude
```

Poi scrivi:
```
Sei un tutor esperto di programmazione. Analizza questo progetto e genera una documentazione
completa in formato Markdown che includa:
- Panoramica generale
- Architettura e pattern usati
- Analisi di ogni modulo
- Workflow di esecuzione
- Guida per sviluppatori
- Valutazione e suggerimenti
```

### 2. Salva l'output

Copia la risposta di Claude in un file `.md`:
```
documentazione_progetto.md
```

### 3. Genera il PDF

```bash
python generate_pdf.py documentazione_progetto.md
```

Output: `documentazione_progetto.pdf`

## Struttura File

```
project_tutor_agent/
├── TUTOR_PROMPT.md    # Prompt completo per l'agente
├── generate_pdf.py     # Script conversione MD -> PDF
├── requirements.txt    # Dipendenze Python
└── README.md          # Questa guida
```

## Esempi di Comandi

### Analisi completa:
```
Analizza completamente questo progetto come un tutor esperto
```

### Focus architettura:
```
Spiega l'architettura di questo progetto con diagrammi
```

### Spiegazione didattica:
```
Spiega questo codice come se fossi un professore universitario
```

### Generazione con titolo custom:
```bash
python generate_pdf.py docs.md "Documentazione API REST.pdf"
```

## Caratteristiche PDF

- Formattazione professionale A4
- Pagina titolo automatica
- Header/Footer con numerazione
- Supporto code blocks
- Liste puntate e numerate
- Stili tipografici moderni
