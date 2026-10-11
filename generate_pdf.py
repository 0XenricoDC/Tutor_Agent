"""
Project Tutor Agent - Generatore PDF
=====================================
Converte documentazione Markdown in PDF professionale.

Uso:
    python generate_pdf.py input.md output.pdf
    python generate_pdf.py input.md  # genera input.pdf
"""

import sys
import os
import re
from datetime import datetime

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm, mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Preformatted, ListFlowable, ListItem
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Errore: reportlab non installato.")
    print("Installa con: pip install reportlab")
    sys.exit(1)


class MarkdownToPDF:
    """Convertitore Markdown -> PDF"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configura stili personalizzati"""

        # Titolo documento
        self.styles.add(ParagraphStyle(
            name='DocTitle',
            parent=self.styles['Title'],
            fontSize=28,
            spaceAfter=30,
            textColor=colors.HexColor('#1a1a2e'),
            alignment=TA_CENTER
        ))

        # Titoli sezione
        self.styles.add(ParagraphStyle(
            name='Heading1Custom',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor('#16213e'),
            borderWidth=1,
            borderColor=colors.HexColor('#0f3460'),
            borderPadding=5
        ))

        self.styles.add(ParagraphStyle(
            name='Heading2Custom',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor('#0f3460')
        ))

        self.styles.add(ParagraphStyle(
            name='Heading3Custom',
            parent=self.styles['Heading3'],
            fontSize=13,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.HexColor('#533483')
        ))

        # Corpo testo
        self.styles.add(ParagraphStyle(
            name='BodyCustom',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            spaceBefore=6,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        ))

        # Blocco codice
        self.styles.add(ParagraphStyle(
            name='CodeBlock',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Courier',
            backColor=colors.HexColor('#f5f5f5'),
            borderWidth=1,
            borderColor=colors.HexColor('#e0e0e0'),
            borderPadding=8,
            spaceBefore=8,
            spaceAfter=8
        ))

        # Lista
        self.styles.add(ParagraphStyle(
            name='ListItem',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            leftIndent=20,
            bulletIndent=10
        ))

    def parse_markdown(self, md_content):
        """Converte Markdown in elementi PDF"""
        elements = []
        lines = md_content.split('\n')

        in_code_block = False
        code_buffer = []
        code_lang = ""

        i = 0
        while i < len(lines):
            line = lines[i]

            # Gestione blocchi codice
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_lang = line.strip()[3:]
                    code_buffer = []
                else:
                    in_code_block = False
                    code_text = '\n'.join(code_buffer)
                    if code_text.strip():
                        elements.append(Spacer(1, 6))
                        elements.append(Preformatted(code_text, self.styles['CodeBlock']))
                        elements.append(Spacer(1, 6))
                i += 1
                continue

            if in_code_block:
                code_buffer.append(line)
                i += 1
                continue

            # Linea vuota
            if not line.strip():
                elements.append(Spacer(1, 6))
                i += 1
                continue

            # Titoli
            if line.startswith('# '):
                text = self._clean_text(line[2:])
                elements.append(PageBreak())
                elements.append(Paragraph(text, self.styles['DocTitle']))
                i += 1
                continue

            if line.startswith('## '):
                text = self._clean_text(line[3:])
                elements.append(Spacer(1, 12))
                elements.append(Paragraph(text, self.styles['Heading1Custom']))
                i += 1
                continue

            if line.startswith('### '):
                text = self._clean_text(line[4:])
                elements.append(Paragraph(text, self.styles['Heading2Custom']))
                i += 1
                continue

            if line.startswith('#### '):
                text = self._clean_text(line[5:])
                elements.append(Paragraph(text, self.styles['Heading3Custom']))
                i += 1
                continue

            # Liste puntate
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                list_items = []
                while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ')):
                    item_text = self._clean_text(lines[i].strip()[2:])
                    list_items.append(ListItem(Paragraph(item_text, self.styles['ListItem'])))
                    i += 1
                elements.append(ListFlowable(list_items, bulletType='bullet', start='-'))
                continue

            # Liste numerate
            if re.match(r'^\d+\.\s', line.strip()):
                list_items = []
                while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                    item_text = re.sub(r'^\d+\.\s', '', lines[i].strip())
                    item_text = self._clean_text(item_text)
                    list_items.append(ListItem(Paragraph(item_text, self.styles['ListItem'])))
                    i += 1
                elements.append(ListFlowable(list_items, bulletType='1'))
                continue

            # Separatore
            if line.strip() in ['---', '***', '___']:
                elements.append(Spacer(1, 10))
                i += 1
                continue

            # Paragrafo normale
            text = self._clean_text(line)
            if text:
                elements.append(Paragraph(text, self.styles['BodyCustom']))

            i += 1

        return elements

    def _clean_text(self, text):
        """Pulisce e formatta il testo per PDF"""
        # Bold -> <b>
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)

        # Italic -> <i>
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)

        # Inline code -> <font>
        text = re.sub(r'`(.+?)`', r'<font name="Courier" size="9" color="#c0392b">\1</font>', text)

        # Links [text](url) -> text
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)

        # Escape caratteri speciali XML
        text = text.replace('&', '&amp;')
        # Ripristina i tag HTML
        text = text.replace('&amp;lt;', '<').replace('&amp;gt;', '>')

        return text

    def add_header_footer(self, canvas, doc):
        """Aggiunge header e footer alle pagine"""
        canvas.saveState()

        # Footer
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#666666'))

        # Numero pagina
        page_num = canvas.getPageNumber()
        canvas.drawCentredString(A4[0]/2, 20*mm, f"Pagina {page_num}")

        # Data generazione
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        canvas.drawRightString(A4[0] - 20*mm, 20*mm, f"Generato: {date_str}")

        # Linea separatore
        canvas.setStrokeColor(colors.HexColor('#cccccc'))
        canvas.line(20*mm, 25*mm, A4[0] - 20*mm, 25*mm)

        canvas.restoreState()

    def generate(self, md_content, output_path, title="Documentazione Progetto"):
        """Genera il PDF dal contenuto Markdown"""

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=3*cm
        )

        elements = []

        # Pagina titolo
        elements.append(Spacer(1, 100))
        elements.append(Paragraph(title, self.styles['DocTitle']))
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            f"Generato il {datetime.now().strftime('%d/%m/%Y alle %H:%M')}",
            ParagraphStyle('Subtitle', parent=self.styles['Normal'],
                          alignment=TA_CENTER, textColor=colors.grey)
        ))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(
            "Documentazione generata da Project Tutor Agent",
            ParagraphStyle('Credit', parent=self.styles['Normal'],
                          alignment=TA_CENTER, fontSize=10, textColor=colors.grey)
        ))

        # Contenuto
        elements.extend(self.parse_markdown(md_content))

        # Genera PDF
        doc.build(elements, onFirstPage=self.add_header_footer,
                 onLaterPages=self.add_header_footer)

        return output_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUso: python generate_pdf.py <file.md> [output.pdf]")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Errore: File '{input_file}' non trovato")
        sys.exit(1)

    # Output file
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = os.path.splitext(input_file)[0] + '.pdf'

    # Leggi markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Estrai titolo dal primo heading
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Documentazione Progetto"

    # Genera PDF
    converter = MarkdownToPDF()
    converter.generate(md_content, output_file, title)

    print(f"PDF generato: {output_file}")
    print(f"Dimensione: {os.path.getsize(output_file) / 1024:.1f} KB")


if __name__ == '__main__':
    main()
