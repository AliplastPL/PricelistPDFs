import os
import pyodbc
from base_pricelist import BasePricelist, fmt_price
from sql_queries_pln import QUERY_PROFILE, QUERY_AKCESORIA, QUERY_BLACHY, QUERY_FORMATKI, QUERY_MOSKITIERY

# 1 punkt = 1 jednostka w ReportLab
pt = 1.0

# Szerokości kolumn z analizy oryginału PLN (w punktach):
# Oryginał PLN kolumny x: 30.5, 80.2, 171.7, 196.9, 234.0, 266.3, 304.9,
#                         342.0, 380.6, 427.2, 458.0, 485.6, 513.2, 563.7
# Różnice: 49.7, 91.5, 25.2, 37.1, 32.3, 38.6, 37.1, 38.6, 46.6, 30.8, 27.6, 27.6, 50.5

_PROFILE_WIDTHS_PLN = [
    49.7 * pt,   # Numer Katalogowy
    135.5 * pt,  # Nazwa elementu (poszerzona do wyrównania szerokości)
    25.2 * pt,   # Jedn.
    37.1 * pt,   # Jedn. Sprzedaży
    32.3 * pt,   # MF Surowy
    38.6 * pt,   # Typowy T
    37.1 * pt,   # Nietypowy N
    38.6 * pt,   # Anoda AN
    46.6 * pt,   # Wood WD
    30.8 * pt,   # LN1
    27.6 * pt,   # LN2
    27.6 * pt,   # LN3
    50.5 * pt,   # Anoda kolor ANC
]

# Akcesoria PLN: 13 kolumn + ilość handlowa
_AKCES_WIDTHS_PLN = [
    45.0 * pt,   # Numer katalogowy
    168.0 * pt,  # Nazwa elementu (poszerzona do wyrównania szerokości)
    23.0 * pt,   # Jedn.
    23.0 * pt,   # Jedn. Sprzedaży
    22.0 * pt,   # Ilość handlowa
    47.0 * pt,   # MF Surowy
    35.0 * pt,   # Typowy T
    35.0 * pt,   # Nietypowy N
    35.0 * pt,   # Wood WD
    40.0 * pt,   # Anoda
    27.0 * pt,   # LN1
    27.0 * pt,   # LN2
    50.0 * pt,   # LN3
]

# Blachy PLN: 12 kolumn
_BLACH_WIDTHS_PLN = [
    55.0 * pt,   # Numer Katalogowy
    165.0 * pt,  # Nazwa elementu (poszerzona do wyrównania szerokości)
    30.0 * pt,   # Jedn.
    45.0 * pt,   # MF Surowy
    38.0 * pt,   # Typowy T
    38.0 * pt,   # Nietypowy N
    38.0 * pt,   # Anoda AN
    38.0 * pt,   # Anoda kolor ANC
    38.0 * pt,   # Wood WD
    30.0 * pt,   # LN1
    27.0 * pt,   # LN2
    35.0 * pt,   # LN3
]

# Formatki PLN: 10 kolumn
_FORMAT_WIDTHS_PLN = [
    55.0 * pt,   # Numer Katalogowy
    170.0 * pt,  # Nazwa elementu (poszerzona do wyrównania szerokości)
    30.0 * pt,   # Jedn.
    55.0 * pt,   # MF Surowy
    55.0 * pt,   # Typowy T
    45.0 * pt,   # Nietypowy N
    42.0 * pt,   # Wood WD
    35.0 * pt,   # LN1
    35.0 * pt,   # LN2
    55.0 * pt,   # LN3
]

# Moskitiery PLN: 9 kolumn
_MOSK_WIDTHS_PLN = [
    60.0 * pt,   # Numer Katalogowy
    230.0 * pt,  # Nazwa elementu
    30.0 * pt,   # Jedn.
    55.0 * pt,   # Typowy T
    48.0 * pt,   # Nietypowy N
    48.0 * pt,   # Wood WD
    35.0 * pt,   # LN1
    35.0 * pt,   # LN2
    36.0 * pt,   # LN3
]


class PricelistPLN(BasePricelist):
    """
    Cennik Aliplast PLN.
    """

    def __init__(self, number, version_date, valid_from, header_text, page_start=1):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Parsowanie daty "27.05.2026" -> miesiac.rok (05.2026) oraz dzien.miesiac (27.05)
        parts = version_date.split('.')
        if len(parts) >= 3:
            day_month = f"{parts[0]}.{parts[1]}"
            month_year = f"{parts[1]}.{parts[2]}"
        else:
            day_month = version_date
            month_year = version_date

        self.output_pdf = os.path.join(base_dir, f'Cennik Aliplast PLN {month_year} v{day_month}.pdf')
        self.currency = 'PLN'
        self.PRICELIST_NUMBER = number
        
        # Konfiguracja nagłówków i dat podawana wprost ze zmiennych
        self.header_text = header_text
        self.version_date = version_date
        self.VALID_FROM_DATE = valid_from
        self.first_page = page_start
        
        self.logo_path = os.path.join(base_dir, self.LOGO_FILENAME)
        from config import get_config_value
        db_string = get_config_value("DB_CONNECTION_STRING")
        self.db_conn = pyodbc.connect(db_string)

    def fetch_data(self, query_template):
        query = query_template.replace('{n}', str(self.PRICELIST_NUMBER))
        cursor = self.db_conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        
        cleaned_rows = []
        for row in rows:
            new_row = []
            for cell in row:
                if cell is None:
                    new_row.append('')
                elif isinstance(cell, (int, float)):
                    if cell == 0:
                        new_row.append('')
                    else:
                        new_row.append(f"{cell:g}")
                else:
                    new_row.append(str(cell).strip())
            cleaned_rows.append(new_row)
        return cleaned_rows

    def generate(self):
        sections = [
            self._section_profile(),
            self._section_akcesoria(),
            self._section_blach(),
            self._section_formatek(),
            self._section_moskitier(),
        ]
        self._build_pdf(sections)

    # ------------------------------------------------------------------
    def _section_profile(self):
        col_headers = [
            [
                'Numer Katalogowy', 'Nazwa elementu', 'Jedn.', 'Jedn. Sprzedaży',
                'Cena netto [PLN/jedn sprzedaży]', '', '', '', '', '', '', '', '',
            ],
            [
                '', '', '', '',
                'MF Surowy',
                'Lakier Typowy T',
                'Lakier Nietypowy N',
                'Anoda srebrna AN',
                'Lakier Wood WD',
                'Lakier LN1', 'Lakier LN2', 'Lakier LN3',
                'Lakier Anoda kolor ANC',
            ],
        ]

        raw = self.fetch_data(QUERY_PROFILE)
        
        data = []
        for row in raw:
            padded_row = list(row) + [''] * max(0, 13 - len(row))
            data.append(self._row_profile(padded_row))
            
        return {
            'title': 'CENNIK KSZTAŁTOWNIKÓW SYSTEMOWYCH ALIPLAST',
            'col_headers': col_headers,
            'col_widths': _PROFILE_WIDTHS_PLN,
            'data': data,
            'vat_label': '23% VAT',
            'vat_col': 4,
            'spans': [((4, 0), (12, 0))],
        }

    def _row_profile(self, row):
        return [
            str(row[0]) if row[0] != '' else '',
            str(row[1]) if row[1] != '' else '',
            str(row[2]) if row[2] != '' else '',
            str(row[3]) if row[3] != '' else '',
            fmt_price(row[4] if len(row) > 4 else ''),
            fmt_price(row[5] if len(row) > 5 else ''),
            fmt_price(row[6] if len(row) > 6 else ''),
            fmt_price(row[7] if len(row) > 7 else ''),
            fmt_price(row[8] if len(row) > 8 else ''),
            fmt_price(row[9] if len(row) > 9 else ''),
            fmt_price(row[10] if len(row) > 10 else ''),
            fmt_price(row[11] if len(row) > 11 else ''),
            fmt_price(row[12] if len(row) > 12 else ''),
        ]

    def _section_akcesoria(self):
        col_headers = [
            [
                'Numer katalogowy', 'Nazwa elementu', 'Jedn.', 'Jedn. Sprzedaży',
                'Ilość handlowa',
                'Cena za jedn. sprzedaży netto [PLN]', '', '', '', '', '', '', '',
            ],
            [
                '', '', '', '', '',
                'MF Surowy',
                'Lakier Typowy T',
                'Lakier Nietypowy N',
                'Lakier Wood WD',
                'Anoda / lak. Anodopodobny',
                'Lakier LN1', 'Lakier LN2', 'Lakier LN3',
            ],
        ]

        raw = self.fetch_data(QUERY_AKCESORIA)
        
        data = []
        for row in raw:
            padded_row = list(row) + [''] * max(0, 13 - len(row))
            data.append(self._row_akces(padded_row))
            
        return {
            'title': 'CENNIK AKCESORIÓW I OKUĆ DO SYSTEMÓW ALIPLAST',
            'col_headers': col_headers,
            'col_widths': _AKCES_WIDTHS_PLN,
            'data': data,
            'vat_label': '23% VAT',
            'vat_col': 5,
            'spans': [((5, 0), (12, 0))],
        }

    def _row_akces(self, row):
        qty = row[4] if len(row) > 4 else ''
        qty_str = ''
        if qty != '':
            try:
                v = float(qty)
                qty_str = str(int(v)) if v == int(v) else str(v)
            except (ValueError, TypeError):
                qty_str = str(qty)
        return [
            str(row[0]) if row[0] != '' else '',
            str(row[1]) if row[1] != '' else '',
            str(row[2]) if row[2] != '' else '',
            str(row[3]) if row[3] != '' else '',
            qty_str,
            fmt_price(row[5] if len(row) > 5 else ''),
            fmt_price(row[6] if len(row) > 6 else ''),
            fmt_price(row[7] if len(row) > 7 else ''),
            fmt_price(row[8] if len(row) > 8 else ''),
            fmt_price(row[9] if len(row) > 9 else ''),
            fmt_price(row[10] if len(row) > 10 else ''),
            fmt_price(row[11] if len(row) > 11 else ''),
            fmt_price(row[12] if len(row) > 12 else ''),
        ]

    def _section_blach(self):
        col_headers = [
            [
                'Numer Katalogowy', 'Nazwa elementu', 'Jedn.',
                'Cena netto [PLN/szt]',
                '', '', '', '', '', '', '', '',
            ],
            [
                '', '', '',
                'MF Surowy',
                'Lakier Typowy T',
                'Lakier Nietypowy N',
                'Anoda Srebrna AN',
                'Anoda Kolor ANC',
                'Lakier Wood WD',
                'Lakier LN1', 'Lakier LN2', 'Lakier LN3',
            ],
        ]
        
        # Pobranie danych bezpośrednio z bazy
        raw = self.fetch_data(QUERY_BLACHY)
        
        data = []
        for row in raw:
            if len(row) > 3:
                row = row[:3] + row[4:]
            padded_row = list(row) + [''] * max(0, 12 - len(row))
            data.append(self._row_blach(padded_row))
            
        return {
            'title': 'CENNIK BLACH',
            'col_headers': col_headers,
            'col_widths': _BLACH_WIDTHS_PLN,
            'data': data,
            'vat_label': '23% VAT',
            'vat_col': 3,
            'spans': [((3, 0), (11, 0))],
        }

    def _row_blach(self, row):
        return [
            str(row[0]) if row[0] != '' else '',
            str(row[1]) if row[1] != '' else '',
            str(row[2]) if row[2] != '' else '',
            fmt_price(row[3] if len(row) > 3 else ''),
            fmt_price(row[4] if len(row) > 4 else ''),
            fmt_price(row[5] if len(row) > 5 else ''),
            fmt_price(row[6] if len(row) > 6 else ''),
            fmt_price(row[7] if len(row) > 7 else ''),
            fmt_price(row[8] if len(row) > 8 else ''),
            fmt_price(row[9] if len(row) > 9 else ''),
            fmt_price(row[10] if len(row) > 10 else ''),
            fmt_price(row[11] if len(row) > 11 else ''),
        ]

    # ------------------------------------------------------------------
    def _section_formatek(self):
        col_headers = [
            [
                'Numer Katalogowy', 'Nazwa elementu', 'Jedn.',
                'Cena netto [PLN/m2] *',
                '', '', '', '', '', '',
            ],
            [
                '', '', '',
                'MF Surowy',
                'Lakier Typowy T',
                'Lakier Nietypowy N',
                'Lakier Wood WD',
                'Lakier LN1', 'Lakier LN2', 'Lakier LN3',
            ],
        ]
        
        # Pobranie danych bezpośrednio z bazy
        raw = self.fetch_data(QUERY_FORMATKI)
        
        data = []
        for row in raw:
            if len(row) > 3:
                row = row[:3] + row[4:]
            padded_row = list(row) + [''] * max(0, 10 - len(row))
            data.append(self._row_format(padded_row))
            
        return {
            'title': 'CENNIK FORMATEK',
            'col_headers': col_headers,
            'col_widths': _FORMAT_WIDTHS_PLN,
            'data': data,
            'vat_label': '23% VAT',
            'vat_col': 3,
            'spans': [((3, 0), (9, 0))],
        }

    def _row_format(self, row):
        return [
            str(row[0]) if row[0] != '' else '',
            str(row[1]) if row[1] != '' else '',
            str(row[2]) if row[2] != '' else '',
            fmt_price(row[3] if len(row) > 3 else ''),
            fmt_price(row[4] if len(row) > 4 else ''),
            fmt_price(row[5] if len(row) > 5 else ''),
            fmt_price(row[6] if len(row) > 6 else ''),
            fmt_price(row[7] if len(row) > 7 else ''),
            fmt_price(row[8] if len(row) > 8 else ''),
            fmt_price(row[9] if len(row) > 9 else ''),
        ]

    # ------------------------------------------------------------------
    def _section_moskitier(self):
        col_headers = [
            [
                'Numer Katalogowy', 'Nazwa elementu', 'Jedn.',
                'Cena netto [PLN/KPL]',
                '', '', '', '', '',
            ],
            [
                '', '', '',
                'Lakier Typowy T',
                'Lakier Nietypowy N',
                'Lakier Wood WD',
                'Lakier LN1', 'Lakier LN2', 'Lakier LN3',
            ],
        ]

        raw = self.fetch_data(QUERY_MOSKITIERY)
        
        data = []
        for row in raw:
            if len(row) > 3:
                row = row[:3] + row[4:]
            padded_row = list(row) + [''] * max(0, 9 - len(row))
            data.append(self._row_mosk(padded_row))
            
        return {
            'title': 'CENNIK MOSKITIER',
            'col_headers': col_headers,
            'col_widths': _MOSK_WIDTHS_PLN,
            'data': data,
            'vat_label': '23% VAT',
            'vat_col': 3,
            'spans': [((3, 0), (8, 0))],
        }

    def _row_mosk(self, row):
        return [
            str(row[0]) if row[0] != '' else '',
            str(row[1]) if row[1] != '' else '',
            str(row[2]) if row[2] != '' else '',
            fmt_price(row[3] if len(row) > 3 else ''),
            fmt_price(row[4] if len(row) > 4 else ''),
            fmt_price(row[5] if len(row) > 5 else ''),
            fmt_price(row[6] if len(row) > 6 else ''),
            fmt_price(row[7] if len(row) > 7 else ''),
            fmt_price(row[8] if len(row) > 8 else ''),
        ]
