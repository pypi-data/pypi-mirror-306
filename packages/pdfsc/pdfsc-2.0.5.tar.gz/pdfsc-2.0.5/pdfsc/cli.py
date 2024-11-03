import os
import subprocess
import sys

import click

from pdfsc.code_to_pdf import get_files_to_include, code_to_pdf

REQUIRED_MODULES = [
    "setuptools",
    "arabic_reshaper",  # Menggunakan underscore karena ini nama modul Python
    "asn1crypto",
    "certifi",
    "cffi",
    "chardet",
    "charset_normalizer",  # Menggunakan underscore karena ini nama modul Python
    "click",
    "cryptography",
    "cssselect2",
    "defusedxml",
    "fonttools",
    "fpdf2",
    "html5lib",
    "idna",
    "lxml",
    "oscrypto",
    "pillow",
    "pycparser",
    "pygments",  # Pygments untuk syntax highlighting
    "pyHanko",  # Nama modul sesuai dengan library pyHanko
    "pyhanko_certvalidator",  # Menggunakan underscore karena ini nama modul Python
    "pypdf",  # Modul pypdf (versi baru)
    "PyPDF2",  # Modul PyPDF2 (versi lama)
    "pypng",
    "bidi.algorithm",  # Modul 'python-bidi' diakses melalui 'bidi.algorithm'
    "yaml",  # Modul PyYAML diakses sebagai 'yaml'
    "qrcode",
    "reportlab",
    "requests",
    "six",
    "svglib",
    "tinycss2",
    "typing_extensions",
    "tzlocal",
    "uritools",
    "urllib3",
    "webencodings",
    "xhtml2pdf"
]


def check_and_install_modules():
    """Cek apakah modul sudah terinstall, jika tidak install otomatis."""

    for module in REQUIRED_MODULES:
        try:
            # Coba impor modul
            __import__(module)
        except ImportError:
            print(f"Module '{module}' tidak ditemukan. Menginstall...")
            try:
                # Install modul menggunakan pip
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except subprocess.CalledProcessError as e:
                print(f"Gagal menginstall module '{module}'. Error: {e}")
                sys.exit(1)  # Keluar jika gagal menginstall


@click.command()
@click.argument('input_file')
def main(input_file):
    check_and_install_modules()
    # Pastikan file .pdfignore ada, kalau nggak, generate otomatis
    pdfignore_path = '.pdfignore'
    if not os.path.exists(pdfignore_path):
        with open(pdfignore_path, 'w') as f:
            f.write('# Default ignore patterns\n*.tmp\n*.log\n')
        click.echo("File .pdfignore tidak ditemukan. File baru .pdfignore telah dibuat.")

    # Panggil fungsi utama (misal generate_pdf) setelah memastikan .pdfignore ada
    generate_pdf(input_file)


def generate_pdf(base_directory):
    # Fungsi utama untuk generate PDF dari base_directory
    click.echo(f"Generating PDFs from directory: {base_directory}...")

    try:
        # Ambil file-file yang akan di-include
        ignore_file = '.pdfignore'
        files_to_include = get_files_to_include(base_directory, ignore_file)
        output_page_path = 'output/page/'

        # Loop untuk generate PDF dari setiap file
        for file in files_to_include:
            name = file.replace('/', '{divider}')
            if not os.path.exists(output_page_path):
                os.makedirs(output_page_path)

            code_to_pdf(file, f'{output_page_path}{name}.pdf')

        click.echo("PDFs berhasil dibuat di folder output/page.")
    except Exception as e:
        click.echo(f"Terjadi kesalahan saat membuat PDF: {e}")


if __name__ == "__main__":
    main()