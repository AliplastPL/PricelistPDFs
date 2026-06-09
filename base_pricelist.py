import os
import html
from datetime import date
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

# 1 punkt = 1 jednostka w ReportLab
pt = 1.5

_FONT_DIR = 'C:/Windows/Fonts'
_fonts_registered = False


def _register_fonts():
    global _fonts_registered
    if _fonts_registered:
        return
    try:
        pdfmetrics.registerFont(TTFont('Arial', os.path.join(_FONT_DIR, 'arial.ttf')))
        pdfmetrics.registerFont(TTFont('Arial-Bold', os.path.join(_FONT_DIR, 'arialbd.ttf')))
        pdfmetrics.registerFont(TTFont('Arial-Italic', os.path.join(_FONT_DIR, 'ariali.ttf')))
        pdfmetrics.registerFont(TTFont('Arial-BoldItalic', os.path.join(_FONT_DIR, 'arialbi.ttf')))
        from reportlab.pdfbase.pdfmetrics import registerFontFamily
        registerFontFamily('Arial', normal='Arial', bold='Arial-Bold',
                           italic='Arial-Italic', boldItalic='Arial-BoldItalic')
        _fonts_registered = True
    except Exception as e:
        print(f'Uwaga: nie można zarejestrować czcionki Arial: {e}')

_register_fonts()

_FONT = 'Arial' if _fonts_registered else 'Helvetica'
_FONT_BOLD = 'Arial-Bold' if _fonts_registered else 'Helvetica-Bold'
_FONT_BOLD_ITALIC = 'Arial-BoldItalic' if _fonts_registered else 'Helvetica-BoldOblique'

_COLOR_HEADER_BG = colors.Color(0.753, 0.753, 0.753)
_COLOR_BORDER = colors.black
_COLOR_ROW_BG = colors.white
_COLOR_TEXT = colors.black
_COLOR_TITLE = colors.black


# ---------------------------------------------------------------------------
def fmt_price(val):
    if val == '' or val is None:
        return ''
    try:
        f = float(val)
        if f == 0:
            return ''
        # Format z separatorem tysięcy (spacja) i przecinkiem dziesiętnym
        formatted = '{:,.2f}'.format(f)          # '1,234.56'
        formatted = formatted.replace(',', '\u2019').replace('.', ',').replace('\u2019', '\u202f')
        return formatted
    except (ValueError, TypeError):
        return str(val)

class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        self._header_month = kwargs.pop('header_month', '')
        self._creation_date = kwargs.pop('creation_date', '')
        self._valid_from_date = kwargs.pop('valid_from_date', '')
        self._page_offset = kwargs.pop('page_offset', 0)
        self._logo_path = kwargs.pop('logo_path', None)
        self._currency = kwargs.pop('currency', 'PLN')
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _draw_header_footer(self, num_pages):
        page_w, page_h = self._pagesize
        page_num = self._pageNumber + self._page_offset

        self.saveState()

        self.setFont(_FONT, 10)
        self.setFillColor(_COLOR_TEXT)
        self.drawString(55 * pt, page_h - 22 * pt, self._header_month)

        if self._logo_path and os.path.exists(self._logo_path):
            try:
                logo_w = 120 * pt
                logo_h = logo_w * (1506 / 6842)   # ~85 pt
                logo_x = page_w - 20 * pt - logo_w
                logo_y = page_h - 30.0 * pt - logo_h
                self.drawImage(
                    self._logo_path,
                    logo_x, logo_y,
                    width=logo_w, height=logo_h,
                    preserveAspectRatio=True,
                    anchor='ne',
                    mask='auto'
                )
            except Exception as e:
                pass

        self.setFont(_FONT, 8)
        self.setFillColor(colors.Color(0.4, 0.4, 0.4))

        self.drawString(14 * pt, 14 * pt, f"V{self._creation_date}")

        if self._valid_from_date:
            if self._currency == 'EUR':
                text_center = f"Price list is valid from {self._valid_from_date}"
            else:
                text_center = f"Cennik obowiązuje od dnia {self._valid_from_date}"
            self.drawCentredString(page_w / 2, 14 * pt, text_center)

        if self._currency == 'EUR':
            text_right = f"Page - {page_num} -"
        else:
            text_right = f"STR. - {page_num} -"
        self.drawRightString(page_w - 14 * pt, 14 * pt, text_right)

        self.restoreState()


class BasePricelist:
    LOGO_FILENAME = 'logo.png'
    VALID_FROM_DATE = ''

    def generate(self):
        raise NotImplementedError("Podklasy muszą implementować generate()")

    # -----------------------------------------------------------------------
    def _build_pdf(self, sections):
        today = date.today()
        creation_date = getattr(self, 'version_date', today.strftime('%d.%m.%Y'))
        valid_from = getattr(self, 'VALID_FROM_DATE', '2026-05-18')

        margin = 14 * pt

        doc = SimpleDocTemplate(
            self.output_pdf,
            pagesize=A4,
            leftMargin=margin,
            rightMargin=margin,
            topMargin=45 * pt,    # miejsce na nagłówek (data)
            bottomMargin=25 * pt, # miejsce na stopkę
        )

        story = []

        for idx, section in enumerate(sections):
            if idx > 0:
                story.append(PageBreak())

            # Tabela
            col_widths = section['col_widths']
            table_data = []

            title_row = [section.get('title', '')] + [''] * (len(col_widths) - 1)
            table_data.append(title_row)

            n_header_rows = len(section['col_headers'])
            header_style = ParagraphStyle(
                name='HeaderStyle',
                fontName=_FONT_BOLD,
                fontSize=7,
                leading=8,
                alignment=TA_CENTER
            )
            for hrow in section['col_headers']:
                new_hrow = []
                for cell in hrow:
                    if cell != '':
                        new_hrow.append(Paragraph(html.escape(str(cell)), header_style))
                    else:
                        new_hrow.append('')
                table_data.append(new_hrow)

            vat_col = section.get('vat_col', 4)
            vat_row = [''] * len(col_widths)
            vat_row[vat_col] = section.get('vat_label', '')
            table_data.append(vat_row)

            data_start = len(table_data)

            is_pln = (self.currency == 'PLN')
            grid_width = 0.5
            data_font = _FONT
            data_font_size = 6
            art_font_size = 4

            desc_style = ParagraphStyle(
                name='DescStyle',
                fontName=_FONT,
                fontSize=art_font_size,
                leading=art_font_size,
                alignment=TA_LEFT
            )
            name_style = ParagraphStyle(
                name='NameStyle',
                fontName=_FONT,
                fontSize=art_font_size,
                leading=art_font_size,
                alignment=TA_LEFT
            )

            price_style = ParagraphStyle(
                name='PriceStyle',
                fontName=_FONT,
                fontSize=art_font_size + 1,
                leading=art_font_size + 1,
                alignment=TA_CENTER
            )
            mid_style = ParagraphStyle(
                name='MidStyle',
                fontName=_FONT,
                fontSize=data_font_size,
                leading=data_font_size,
                alignment=TA_CENTER
            )

            for row in section['data']:
                new_row = list(row)
                for i, cell in enumerate(new_row):
                    val = str(cell) if cell != '' else ''
                    safe = html.escape(val)
                    if i == 0:
                        new_row[i] = Paragraph(safe, desc_style) if val else ''
                    elif i == 1:
                        new_row[i] = Paragraph(safe, name_style) if val else ''
                    elif i >= vat_col:
                        new_row[i] = Paragraph(safe, price_style) if val else ''
                    else:
                        new_row[i] = Paragraph(safe, mid_style) if val else ''
                table_data.append(new_row)

            ts = TableStyle([
                # Tytuł sekcji - Wiersz 0
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, 0), _COLOR_TEXT),
                ('FONTNAME', (0, 0), (-1, 0), _FONT_BOLD),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('LEFTPADDING', (0, 0), (0, 0), 60),
                ('SPAN', (0, 0), (-1, 0)),

                # Nagłówki kolumn (Wiersz 1 do 2)
                ('BACKGROUND', (0, 1), (-1, 2), _COLOR_HEADER_BG),
                ('FONTNAME', (0, 1), (-1, 2), _FONT_BOLD),
                ('FONTSIZE', (0, 1), (-1, 2), 7),
                ('ALIGN', (0, 1), (-1, 2), 'CENTER'),
                ('VALIGN', (0, 1), (-1, 2), 'MIDDLE'),
                ('TEXTCOLOR', (0, 1), (-1, 2), _COLOR_TEXT),

                # Wiersz VAT (Wiersz 3)
                ('BACKGROUND', (0, 3), (-1, 3), _COLOR_HEADER_BG),
                ('FONTNAME', (0, 3), (-1, 3), _FONT_BOLD),
                ('FONTSIZE', (0, 3), (-1, 3), 7),
                ('ALIGN', (0, 3), (-1, 3), 'CENTER'),
                ('VALIGN', (0, 3), (-1, 3), 'MIDDLE'),

                # Dane (Wiersz 4+) — domyślnie wg waluty
                ('BACKGROUND', (0, 4), (-1, -1), _COLOR_ROW_BG),
                ('FONTNAME', (0, 4), (-1, -1), data_font),
                ('FONTSIZE', (0, 4), (-1, -1), data_font_size),
                ('TEXTCOLOR', (0, 4), (-1, -1), _COLOR_TEXT),

                # Wyrównanie danych: kol 0-1 lewo, reszta środek
                ('ALIGN', (0, 4), (1, -1), 'LEFT'),
                ('ALIGN', (2, 4), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),

                # Ramki
                ('GRID', (0, 1), (-1, -1), grid_width, _COLOR_BORDER),

                # Padding — mniejszy dla PLN żeby zmniejszyć wysokość wierszy
                ('TOPPADDING', (0, 1), (-1, 3), 1.5),
                ('BOTTOMPADDING', (0, 1), (-1, 3), 1.5),
                ('TOPPADDING', (0, 4), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 4), (-1, -1), 0),
                ('LEFTPADDING', (0, 1), (-1, -1), 2),
                ('RIGHTPADDING', (0, 1), (-1, -1), 2),
            ])

            for c in range(vat_col):
                ts.add('SPAN', (c, 1), (c, 3))

            ts.add('SPAN', (vat_col, 1), (-1, 1))

            ts.add('SPAN', (vat_col, 3), (-1, 3))

            ts.add('FONTNAME', (vat_col, 4), (-1, -1), _FONT)
            ts.add('FONTSIZE', (vat_col, 4), (-1, -1), art_font_size + 1)
            ts.add('FONTNAME', (0, 4), (1, -1), _FONT)
            ts.add('FONTSIZE', (0, 4), (1, -1), art_font_size)

            row_heights = [None] * data_start + [8] * len(section['data'])

            table = Table(
                table_data,
                colWidths=col_widths,
                rowHeights=row_heights,
                repeatRows=data_start
            )
            table.setStyle(ts)
            story.append(table)

        def make_canvas(filename, *args, **kwargs):
            return NumberedCanvas(
                filename,
                *args,
                header_month=self.header_text,
                creation_date=creation_date,
                valid_from_date=valid_from,
                page_offset=self.first_page - 1,
                logo_path=self.logo_path,
                currency=self.currency,
                **kwargs
            )

        doc.build(story, canvasmaker=make_canvas)
        print(f'PDF zapisany: {self.output_pdf}')
