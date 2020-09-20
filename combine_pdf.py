#! /usr/bin/python3
# combine_pdf.py - Combina os Pdf do diretório de trabalho em um único arquivo.

import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog
import glob


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
        cancel = "Comando cancelado."
        print(cancel)
        return cancel

    # altera o diretório de trabalho para a pasta 'folder'
    os.chdir(folder)

    # gera lista com os nomes dos arquivos do diretório
    files = [a for a in glob.glob('*.pdf') if a != 'arquivos_concatenados.pdf']

    # se lista vazia
    if not len(files):
        nenhum = 'Nenhum arquivo pdf encontrado'
        print(nenhum)
        return nenhum

    merger = PyPDF2.PdfFileMerger(strict=False)
    erros = []
    arquivos = 0
    if len(files) < 20:
        for pdf in files:
            try:
                merger.append(open(pdf, 'rb'))
            except (PyPDF2.utils.PdfReadError, AssertionError, ValueError):
                erros.append(pdf)
                print(pdf)
            except RecursionError:
                return 'Quantidade excessiva de páginas.'
        with open("arquivos_concatenados.pdf", "wb") as fout:
            merger.write(fout)
            merger.close()
    else:
        for pdf in files:
            try:
                merger.append(open(pdf, 'rb'))
                arquivos += 1
            except (PyPDF2.utils.PdfReadError, AssertionError, ValueError):
                erros.append(pdf)
                print(pdf)
            except RecursionError:
                return 'Quantidade excessiva de páginas.'
            if arquivos == 20:
                with open("arquivos_concatenados.pdf", "wb") as fout:
                    merger.write(fout)
                    merger.close()
                    merger = PyPDF2.PdfFileMerger(strict=False)
            elif arquivos % 20 == 0:
                with open("arquivos_concatenados.pdf", "ab") as fout:
                    merger.write(fout)
                    merger.close()
                    merger = PyPDF2.PdfFileMerger(strict=False)
            elif arquivos == len(files):
                with open("arquivos_concatenados.pdf", "ab") as fout:
                    merger.write(fout)
                    merger.close()


    saida = 'Feito! Arquivo resultante = "arquivos_concatenados.pdf". Arquivos não processados: ' + ', '.join(erros)
    # print(saida)
    return saida


if __name__ == '__main__':  # executa se chamado diretamente
    combine_pdf()
