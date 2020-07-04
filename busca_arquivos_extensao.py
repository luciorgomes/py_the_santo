#! /usr/bin/python3
# busca_arquivos_extensao.py - busca arquivos por determinada extensão e os relaciona ou copia para um destino dado.

import os
import janela_texto as jt
import shutil
from tkinter import filedialog

def define_diretorio():
    '''chama o filedialog do Tkinter para definir o diretório'''
    folder = filedialog.askdirectory()
    return folder

def define_diretorio_destino(event=None):
    '''chama o filedialog do Tkinter para definir o diretório'''
    folder_destino = filedialog.askdirectory()
    return folder_destino

def testa_diretorios(folder, folder_destino, event=None):
    '''verifica a validade dos parâmetros e chama o método de busca de arquivos'''
    erro_folder = 'n'
    erro_destino = 'n'
    try:
        # altera o diretório de trabalho para a pasta 'folder'
        os.chdir(folder)
    except FileNotFoundError:
        print("Diretório inválido!")
        erro_folder = 's'
    try:
        # altera o diretório de trabalho para a pasta 'folder'
        os.chdir(folder_destino)
    except FileNotFoundError:
        print("Diretório inválido!")
        erro_destino = 's'
    return erro_folder == 'n' and erro_destino == 'n'

def run(folder, folder_destino, extension, full_content, new_folder, copia_arquivos):
    if not testa_diretorios(folder, folder_destino):
        return 'Erro! Verifique os diretórios informados.'
    if not os.path.exists(folder_destino):
        os.mkdir(folder_destino)
    finded = 0
    file_path = ''
    texto_saída = ''
    if full_content == 1:
        # Percorre toda árvore de diretório na procura de arquivos com a extensão dada
        with open(f'{folder_destino}/relacao_por_extensao_{extension}.txt', 'w') as file:
            for foldername, subfolders, filenames in os.walk(folder):
                try:
                    print('Percorrendo %s...' % (foldername))
                except UnicodeEncodeError:
                    print('Percorrendo %s...' % repr(foldername))
                # Copia os arquivos dessa pasta ao destino informado.
                for filename in filenames:
                    if filename.endswith('.' + extension) and foldername != folder_destino:
                        print('Encontrado ' + filename +
                              ', registrando em ' + file.name)
                        if copia_arquivos == 1:  # gera a relação e copia os arquivos
                            try:
                                shutil.copy(os.path.join(
                                    foldername, filename), folder_destino)
                            except shutil.SameFileError:
                                continue
                        file_path = os.path.join(
                            foldername, filename) + '\n'
                        try:
                            file.write(file_path)
                        except UnicodeEncodeError:
                            file.write('Unicode error\n')
                        texto_saída += file_path
                        finded += 1
            file.write('Finded ' + str(finded) + ' files.')
            texto_saída += 'Finded ' + str(finded) + ' files.'
        jt.janela_texto(
            'Busca arquivos por extensão - Resultado', 'Saída', texto_saída)
        print('Finded ' + str(finded) + ' files. \nDone.')

    else:
        # Apenas o diretório raiz é pesquisado
        with open(f'{folder_destino}/relacao_por_extensao_{extension}.txt', 'w') as file:
            for filename in os.listdir(folder):
                if filename.endswith('.' + extension) and folder != folder_destino:
                    print('Encontrado ' + filename +
                          ', registrando em ' + file.name)
                    if copia_arquivos == 1:  # gera a relação e copia os arquivos
                        try:
                            shutil.copy(os.path.join(
                                folder, filename), new_folder)
                        except shutil.SameFileError:
                            continue
                    file_path = os.path.join(folder, filename) + '\n'
                    try:
                        file.write(file_path)
                    except UnicodeEncodeError:
                        file.write('Unicode error\n')
                    texto_saída += file_path
                    finded += 1
            file.write('Finded ' + str(finded) + ' files.')
            texto_saída += 'Finded ' + str(finded) + ' files.'
        jt.janela_texto(
            'Busca arquivos por extensão - Resultado', 'Saída', texto_saída)
        print('Finded ' + str(finded) + ' files. \nDone.')
    return texto_saída


