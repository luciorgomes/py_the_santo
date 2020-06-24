import os
import zipfile
import datetime
from tkinter import filedialog

def define_diretorio():
    '''chama o filedialog do Tkinter para definir o diretório'''
    folder = filedialog.askdirectory()
    return folder

def executa_backup(folder):
    '''Faz backup do conteúdo do 'folder' em um arquivo Zip.'''
    # Determina o nome de arquivo que esse código deverá usar conforme os arquivos já existentes
    number = 1
    while True:
        zipFilename = os.path.basename(folder) + '_' + str(datetime.date.today()) + '_' + str(
            number) + '.zip'  # basename = nome do arquivo sem o caminho da pasta
        if not os.path.exists(zipFilename):
            break
        number = number + 1
    # Cria o arquivo Zip
    nome_arquivo = "Criando %s..." % zipFilename
    print(nome_arquivo)
    saída = nome_arquivo + '\n'
    with zipfile.ZipFile(zipFilename, 'w') as backupZip:
        # Percorre toda árvore de diretório e compacta os arquivos de cada pasta.
        for foldername, subfolders, filenames in os.walk(folder):
            if 'venv' in foldername or '__pycache__' in foldername:  # evita pastas de ambiente do python
                continue
            loop_text = 'Adicionando arquivos em %s...' % foldername
            print(loop_text)
            saída += loop_text + '\n'
            # Acrescenta a pasta atual ao arquivo zip.
            backupZip.write(foldername)
            # Acrescenta os arquivos dessa pasta ao arquivo zip.
            for filename in filenames:
                newBase = os.path.basename(folder) + '_'
                if filename.startswith(newBase) and filename.endswith('.zip'):
                    continue  # não faz backup dos arquivos de backup anteriores.
                backupZip.write(os.path.join(foldername, filename))
    saída += 'Feito!\n'
    print(saída)
    return saída
    print('Feito!')

def testa_e_executa(folder):
    '''verifica a validade dos parâmetros e chama o método de busca de arquivos'''
    info = 'Comando cancelado'
    try:
        os.chdir(folder)  # altera o diretório de trabalho para a pasta 'folder'
        retorno = executa_backup(folder)
        return retorno
    except TypeError:
        return info
    except FileNotFoundError:
        return info

