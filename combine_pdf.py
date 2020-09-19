#! /usr/bin/python3
# combine_pdf.py - Combina os Pdf do diretório de trabalho em um único arquivo.

import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog


def combine_pdf():
    """
    Comcatena os arquivos pdf de uma pasta
    :return: str
    """
    # abre dialogbox para seleção do folder
    directory_root = tk.Tk()
    directory_root.withdraw()
    folder = filedialog.askdirectory(parent=directory_root, initialdir='/',
                                     title='Selecione a pasta com os arquivos pdf')
    if not len(folder):  # se clicou 'cancel'
        cancel = "comando cancelado"
        return cancel

    os.chdir(folder)  # altera o diretório de trabalho para a pasta 'folder'

    # Gera lista com a relação de arquivos pdf do diretório
    pdf_files = []
    for filename in os.listdir(folder):
        if filename.endswith('.pdf'):
            pdf_files.append(filename)
    print(pdf_files)

    pdf_files.sort(key=str.lower)

    pdf_writer = PyPDF2.PdfFileWriter()

    # Percorre os arquivos em um loop
    for filename in pdf_files:
        pdf_file_obj = open(filename, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

    # Percorre as páginas e as adiciona à saída
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        pdf_writer.addPage(page_obj)

    # Salva o Pdf resultante em um arquivo
    pdf_output = open('all_files.pdf', 'wb')
    pdf_writer.write(pdf_output)
    pdf_output.close()


if __name__ == '__main__':  # executa se chamado diretamente
    combine_pdf()
