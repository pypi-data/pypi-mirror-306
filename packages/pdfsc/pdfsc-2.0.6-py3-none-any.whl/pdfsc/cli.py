import os
import click

from pdfsc.code_to_pdf import get_files_to_include, code_to_pdf, create_pdfignore_if_not_exists


@click.command()
@click.argument('input_file')
def main(input_file):
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
    create_pdfignore_if_not_exists()

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