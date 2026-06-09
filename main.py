"""
Użycie:
    python main.py            # generuje oba cenniki
    python main.py eur        # tylko EUR
    python main.py pln        # tylko PLN

Wszystkie zmienne konfiguracyjne są poniżej w funkcji main().
"""
import sys
import time
import os
try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    pass

def get_pdf_page_count(pdf_path):
    if not pdf_path or not os.path.exists(pdf_path):
        return 0
    try:
        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except Exception as e:
        print(f"Błąd odczytu {pdf_path}: {e}")
        return 0

def merge_pdfs(front_pdf, main_pdf, back_pdf, output_pdf):
    writer = PdfWriter()
    for pdf in [front_pdf, main_pdf, back_pdf]:
        if pdf and os.path.exists(pdf):
            try:
                reader = PdfReader(pdf)
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                print(f"Błąd łączenia {pdf}: {e}")
    with open(output_pdf, "wb") as f_out:
        writer.write(f_out)



def main():
    args = [a.lower() for a in sys.argv[1:]]
    generate_eur = ('eur' in args) or (len(args) == 0)
    generate_pln = ('pln' in args) or (len(args) == 0)

    if generate_eur:
        print('=' * 60)
        print('Generowanie cennika EUR...')
        print('=' * 60)
        t0 = time.time()
        from pricelist_eur import PricelistEUR
        
        # Zmienne dla cennika EUR (możesz je zmieniać)
        eur_number       = 47           # numer cennika w systemie ASW
        eur_version_date = "08.06.2026" # pojawi się jako V28.05.2026 w stopce
        eur_valid_from   = "18.05.2026" # "Price list is valid from ..."
        eur_header       = "May 2026"   # napis w lewym górnym rogu
        eur_front_pdf    = "Pierwsze.pdf" # plik PDF na początek (jeśli brak, wpisz "")
        eur_back_pdf     = "Ostatnia.pdf" # plik PDF na koniec (jeśli brak, wpisz "")
        
        eur_page_start   = get_pdf_page_count(eur_front_pdf) + 1
        
        eur = PricelistEUR(
            number=eur_number,
            version_date=eur_version_date,
            valid_from=eur_valid_from,
            header_text=eur_header,
            page_start=eur_page_start
        )
        print(f'  Wersja PDF:  V{eur_version_date}')
        print(f'  Obowiązuje:  {eur_valid_from}')
        print(f'  Numer:       {eur.PRICELIST_NUMBER}')
        print(f'  Nagłówek:    {eur.header_text}')
        print(f'  Str. od:     {eur_page_start}')
        print(f'  Wyjście PDF: {eur.output_pdf}')
        eur.generate()
        if (eur_front_pdf and os.path.exists(eur_front_pdf)) or (eur_back_pdf and os.path.exists(eur_back_pdf)):
            print("  Scalanie plików PDF...")
            temp_pdf = eur.output_pdf.replace(".pdf", "_temp.pdf")
            os.rename(eur.output_pdf, temp_pdf)
            merge_pdfs(eur_front_pdf, temp_pdf, eur_back_pdf, eur.output_pdf)
            os.remove(temp_pdf)
        print(f'  Czas: {time.time() - t0:.1f}s')
        print()

    if generate_pln:
        print('=' * 60)
        print('Generowanie cennika PLN...')
        print('=' * 60)
        t0 = time.time()
        from pricelist_pln import PricelistPLN
        
        # Zmienne dla cennika PLN (możesz je zmieniać)
        pln_number       = 48           # numer cennika w systemie ASW
        pln_version_date = "08.06.2026" # pojawi się jako V28.05.2026 w stopce
        pln_valid_from   = "2026-05-18" # "Cennik obowiązuje od dnia ..."
        pln_header       = "Maj 2026"   # napis w lewym górnym rogu
        pln_front_pdf    = "Pierwsze_PLN.pdf" # plik PDF na początek (jeśli brak, wpisz "")
        pln_back_pdf     = "Ostatnia_PLN.pdf" # plik PDF na koniec (jeśli brak, wpisz "")

        pln_page_start   = get_pdf_page_count(pln_front_pdf) + 1

        pln = PricelistPLN(
            number=pln_number,
            version_date=pln_version_date,
            valid_from=pln_valid_from,
            header_text=pln_header,
            page_start=pln_page_start
        )
        print(f'  Wersja PDF:  V{pln_version_date}')
        print(f'  Obowiązuje:  {pln_valid_from}')
        print(f'  Numer:       {pln.PRICELIST_NUMBER}')
        print(f'  Nagłówek:    {pln.header_text}')
        print(f'  Str. od:     {pln_page_start}')
        print(f'  Wyjście PDF: {pln.output_pdf}')
        pln.generate()
        if (pln_front_pdf and os.path.exists(pln_front_pdf)) or (pln_back_pdf and os.path.exists(pln_back_pdf)):
            print("  Scalanie plików PDF...")
            temp_pdf = pln.output_pdf.replace(".pdf", "_temp.pdf")
            os.rename(pln.output_pdf, temp_pdf)
            merge_pdfs(pln_front_pdf, temp_pdf, pln_back_pdf, pln.output_pdf)
            os.remove(temp_pdf)
        print(f'  Czas: {time.time() - t0:.1f}s')
        print()

    print('Gotowe!')


if __name__ == '__main__':
    main()
