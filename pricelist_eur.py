import os
import pyodbc
from base_pricelist import BasePricelist, fmt_price
from sql_queries_eur import QUERY_PROFILE_EUR, QUERY_AKCESORIA_EUR, QUERY_BLACHY_EUR, QUERY_FORMATKI_EUR, QUERY_MOSKITIERY_EUR

# 1 punkt = 1 jednostka w ReportLab
pt = 1.0

_PROFILE_WIDTHS = [
    68.7 * pt,   # Article
    110.4 * pt,  # Description
    30.0 * pt,   # Sales Unit
    29.2 * pt,   # Price Unit
    53.6 * pt,   # MF
    40.3 * pt,   # T
    45.7 * pt,   # N
    36.2 * pt,   # AN
    36.3 * pt,   # WD
    30.7 * pt,   # LN1
    30.0 * pt,   # LN2
    27.6 * pt,   # LN3
    28.5 * pt,   # ANC
]

# Akcesoria: ta sama tabela kolumnowa + 1 kolumna ilości handlowej wstawiona na poz. 4
_AKCES_WIDTHS = [
    60.0 * pt,   # Article
    100.0 * pt,  # Description
    26.0 * pt,   # Sales Unit
    26.0 * pt,   # Price Unit
    24.0 * pt,   # Ilość handlowa
    50.0 * pt,   # MF
    37.0 * pt,   # T
    37.0 * pt,   # N
    37.0 * pt,   # WD / ANC
    37.0 * pt,   # AN / Anod.
    27.0 * pt,   # LN1
    27.0 * pt,   # LN2
    27.0 * pt,   # LN3
]

# Blachy: 12 kolumn
_BLACH_WIDTHS = [
    68.7 * pt,   # Article
    130.0 * pt,  # Description
    30.0 * pt,   # Unit
    48.0 * pt,   # MF
    40.0 * pt,   # T
    40.0 * pt,   # N
    40.0 * pt,   # AN
    40.0 * pt,   # WD
    30.0 * pt,   # LN1
    30.0 * pt,   # LN2
    27.0 * pt,   # LN3
    33.3 * pt,   # ANC
]

# Formatki: 10 kolumn
_FORMAT_WIDTHS = [
    68.7 * pt,   # Article
    160.0 * pt,  # Description
    30.0 * pt,   # Unit
    57.0 * pt,   # MF
    57.0 * pt,   # T
    45.0 * pt,   # N
    45.0 * pt,   # WD
    35.0 * pt,   # LN1
    35.0 * pt,   # LN2
    34.3 * pt,   # LN3
]

# Moskitiery: 9 kolumn
_MOSK_WIDTHS = [
    68.7 * pt,   # Article
    220.0 * pt,  # Description
    30.0 * pt,   # Unit
    55.0 * pt,   # T
    50.0 * pt,   # N
    50.0 * pt,   # WD
    35.0 * pt,   # LN1
    35.0 * pt,   # LN2
    33.3 * pt,   # LN3
]


class PricelistEUR(BasePricelist):

    def __init__(self, number, version_date, valid_from, header_text, page_start=1):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        parts = version_date.split('.')
        if len(parts) >= 3:
            day_month = f"{parts[0]}.{parts[1]}"
            month_year = f"{parts[1]}.{parts[2]}"
        else:
            day_month = version_date
            month_year = version_date

        self.output_pdf = os.path.join(base_dir, f'Cennik Aliplast EUR {month_year} v{day_month}.pdf')
        self.currency = 'EUR'
        self.PRICELIST_NUMBER = number
        
        self.header_text = header_text
        self.version_date = version_date
        self.VALID_FROM_DATE = valid_from
        
        self.first_page = page_start
        self.logo_path = os.path.join(base_dir, self.LOGO_FILENAME)
        
        self.db_conn = pyodbc.connect('DSN=Aliplast;UID=PLRAP;PWD=Ali18RAP')

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

    def _section_profile(self):
        col_headers = [
            [
                'Article', 'Description', 'Sales Unit', 'Price Unit',
                'Price [EUR per price unit]', '', '', '', '', '', '', '', '',
            ],
            [
                '', '', '', '',
                'Mill finished MF',
                'Typical T',
                'Untypical N',
                'Silver anode AN',
                'Wood WD',
                'LN1', 'LN2', 'LN3',
                'Color anode ANC',
            ],
        ]
        raw = self.fetch_data(QUERY_PROFILE_EUR)
        data = []
        for row in raw:
            padded_row = list(row) + [''] * max(0, 13 - len(row))
            data.append(self._row_profile(padded_row))
        return {
            'title': 'ALIPLAST PROFILES PRICE LIST',
            'col_headers': col_headers,
            'col_widths': _PROFILE_WIDTHS,
            'data': data,
            'vat_label': '0% VAT',
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
                'Article', 'Description', 'Sales Unit', 'Price Unit', 'Trade quantity',
                'Price [EUR per price unit]', '', '', '', '', '', '', '',
            ],
            [
                '', '', '', '', '',
                'Mill finished MF',
                'Typical T',
                'Untypical N',
                'Wood WD',
                'Anodized or anodelike coated',
                'LN1', 'LN2', 'LN3',
            ],
        ]
        raw = self.fetch_data(QUERY_AKCESORIA_EUR)
        data = []
        for row in raw:
            padded_row = list(row) + [''] * max(0, 13 - len(row))
            data.append(self._row_akces(padded_row))
        return {
            'title': 'ALIPLAST HARDWARE AND ACCESSORIES PRICE LIST',
            'col_headers': col_headers,
            'col_widths': _AKCES_WIDTHS,
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
                'Article', 'Description', 'Sales Unit', 'Price Unit',
                '', '', '', '', '', '', '', '',
            ],
            [
                '', '', '',
                'Mill finished MF',
                'Typical T',
                'Untypical N',
                'Wood WD',
                'Silver anode AN',
                'Color Anode ANC',
                'LN1', 'LN2', 'LN3',
            ],
        ]
        raw = self.fetch_data(QUERY_BLACHY_EUR)
        data = []
        for row in raw:
            if len(row) > 3:
                row = row[:3] + row[4:]
            padded_row = list(row) + [''] * max(0, 12 - len(row))
            data.append(self._row_blach(padded_row))
        return {
            'title': 'SHEETS PRICE LIST',
            'col_headers': col_headers,
            'col_widths': _BLACH_WIDTHS,
            'data': data,
            'vat_label': '0% VAT',
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

    def _section_formatek(self):
        col_headers = [
            [
                'Article', 'Description', 'Sales Unit', 'Price Unit',
                '', '', '', '', '', '',
            ],
            [
                '', '', '',
                'Mill finished MF',
                'Typical T',
                'Untypical N',
                'Wood WD',
                'LN1', 'LN2', 'LN3',
            ],
        ]
        raw = self.fetch_data(QUERY_FORMATKI_EUR)
        data = []
        for row in raw:
            if len(row) > 3:
                row = row[:3] + row[4:]
            padded_row = list(row) + [''] * max(0, 10 - len(row))
            data.append(self._row_format(padded_row))
        return {
            'title': 'SHEETS CUT TO SIZE PRICE LIST',
            'col_headers': col_headers,
            'col_widths': _FORMAT_WIDTHS,
            'data': data,
            'vat_label': '0% VAT',
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

    def _section_moskitier(self):
        col_headers = [
            [
                'Article', 'Description', 'Sales Unit', 'Price Unit',
                '', '', '', '', '',
            ],
            [
                '', '', '',
                'Typical T',
                'Untypical N',
                'Wood WD',
                'LN1', 'LN2', 'LN3',
            ],
        ]
        raw = self.fetch_data(QUERY_MOSKITIERY_EUR)
        data = []
        for row in raw:
            if len(row) > 3:
                row = row[:3] + row[4:]
            padded_row = list(row) + [''] * max(0, 9 - len(row))
            data.append(self._row_mosk(padded_row))
        return {
            'title': "FLYSCREEN'S PRICE LIST",
            'col_headers': col_headers,
            'col_widths': _MOSK_WIDTHS,
            'data': data,
            'vat_label': 'VAT 0%',
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
