import os
from tkinter import filedialog
from tkinter import messagebox
import io
import re

def define_arquivo():
    '''chama o filedialog do Tkinter para definir o arquivo'''
    file = filedialog.askopenfilename(title="Selecione arquivo csv", filetypes=[("Csv files", ".csv")])
    return file

def processa_arquivo_csv(file, separador=','):
    '''processa o arquivo csv e gera um segundo com o resultado do processamento'''
    with io.open(file, encoding='latin-1', newline='') as csv_file_object:
        contents = csv_file_object.read()
        if separador == ';':
            # substitui vírgula separador de campos por ponto-e-vírgula...
            # ... duplo "CR LF com aspas no meio" por simples “CR LF com aspas antes"
            contents = contents.replace('","', '";"').replace(r'\r\n"\r\n', r'"\r\n')
        else:
            contents = contents.replace(r'\r\n"\r\n', r'"\r\n')
        # “LF sem CR prévio” por "nada" (LF perdidos no texto)
        re_contents = re.sub(r'(?<!\r)\n', '', contents)
        # substituir “LF CR” antes das aspas por nada (retira duplo salto de linha)
        re_contents = re.sub(r'(?<!")\r\n', '', re_contents)
        # substituir aspas dentro do texto por nada, desde que não seja no início e fim da linha:
        if separador == ';':
            re_contents = re.sub(r'(?<![;]|\n)["](?![;]|\r)', '', re_contents)
        else:
            re_contents = re.sub(r'(?<![,]|\n)["](?![,]|\r)', '', re_contents)
        # substituir nova linha não seguida de aspas:
        re_contents = re.sub(r'\r\n(?!")', '', re_contents)
        # a penúltima substituição retira as primeiras " do início do arquivo, a última \n do final.
        final_contents = '"' + re_contents + '\n'
        arquivo_saída = file[:-4] + '_tratado.csv'
        with open(arquivo_saída, 'w', encoding='latin-1', newline='\n') as saida:
            saida.write(final_contents)
    return None

def testa_e_executa(file, separador):
    '''verifica a validade dos parâmetros e chama o método de busca de arquivos'''
    info = 'Comando cancelado'
    erro = 'Arquivo Inválido'
    try:
        folder = os.path.dirname(file)
        os.chdir(folder)  # altera o diretório de trabalho para a pasta 'folder'
        processa_arquivo_csv(file, separador)
    except TypeError:
        return info
    except FileNotFoundError:
        return info
    except OSError:
        return erro


