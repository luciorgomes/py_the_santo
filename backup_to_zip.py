#! /usr/bin/python3
# backup_to_zip.py - Copia uma pasta e seu conteúdo para um arquivo Zip com nome incrementado.

import os
import zipfile
import datetime
import tkinter as tk
import tkinter.ttk as ttk
import seleciona_diretório as sd



class Application(tk.Frame):
    '''instancia a janela'''

    def __init__(self, master=None):
        super().__init__(master)
        self.folder = ''
        self.master = master
        self.icon = tk.PhotoImage(file='./image/Folder-icon.png')
        self.pack()
        self.configure(bg='gray')

        '''cria os componentes da janela'''
        tk.Label(self, text='Diretório:', bg= 'gray', fg='black').grid(row=0, column=0, sticky='e')
        self.entry_dir = tk.Entry(self, bg='#33425c', fg= 'orange', width= 45)
        self.entry_dir.grid(row=0, column=1, columnspan=2)
        self.entry_dir.insert(0, os.getcwd())
        self.button_dir = tk.Button(self, text='>', image=self.icon, bg='#31363b', fg='white',
                                    command=self.define_diretorio)
        self.button_dir.grid(row=0, column=3, sticky='e')
        self.button_dir.bind('<Escape>', self.exit) # com um Esc encera o programa
        self.entry_dir.bind('<Escape>', self.exit)  # com um Esc encera o programa
        self.button_dir.focus()
        # fora do Frame
        tk.Button(self.master, text='Executar', anchor='n', bg='#31363b', fg='white',
                                    command=self.testa_e_executa).pack()
        self.separator = ttk.Separator(self.master, orient=tk.HORIZONTAL).pack(fill='x')
        self.saída = tk.Listbox(self.master, width= 140, height= 43, bg= '#33425c', fg='orange', font= 'Mono 8')
        self.saída.pack()
        ##33425c
        self.define_raiz()

    def define_diretorio(self, event=None):
        '''chama o filedialog do Tkinter para definir o diretório'''
        self.saída.delete(0, 'end')
        folder_diag = sd.seleciona_diretorio("Procurar arquivos grandes - selecione a pasta")
        if folder_diag is not None:  # Se não foi cancelado
            self.entry_dir.delete(0, 'end')
            self.entry_dir.insert(0, folder_diag)

    def define_raiz(self):
        '''Define caracterísicas da janela'''
        self.master.title('Backup to zip')
        self.master.configure(bg='gray')
        self.master.iconphoto(False, tk.PhotoImage(file='./image/Python-icon.png'))
        # dimensões da janela
        largura = 510
        altura = 300
        # resolução da tela
        largura_screen = self.master.winfo_screenwidth()
        altura_screen = self.master.winfo_screenheight()
        # posição da janela
        posx = largura_screen / 2 - largura / 2  # meio da tela
        posy = altura_screen / 2 - altura / 2  # meio da primeira tela
        self.master.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))  # dimensões + posição inicial

    def testa_e_executa(self,event=None):
        '''verifica a validade dos parâmetros e chama o método de busca de arquivos'''
        self.folder = self.entry_dir.get()
        try:
            os.chdir(self.folder)  # altera o diretório de trabalho para a pasta 'folder'
            self.executa_backup()
        except FileNotFoundError:
            print("Diretório inválido!")

    def exit(self,event=None):
        self.master.destroy()

    def executa_backup(self):
        '''Faz backup do conteúdo do 'folder' em um arquivo Zip.'''

        # Determina o nome de arquivo que esse código deverá usar conforme os arquivos já existentes
        number = 1
        while True:
            zipFilename = os.path.basename(self.folder) + '_' + str(datetime.date.today()) + '_' + str(
                number) + '.zip'  # basename = nome do arquivo sem o caminho da pasta
            if not os.path.exists(zipFilename):
                break
            number = number + 1

        # Cria o arquivo Zip
        nome_arquivo = "Creating %s..." % zipFilename
        print(nome_arquivo)
        self.saída.insert('end', nome_arquivo)
        self.saída.see(0)
        view = 2
        with zipfile.ZipFile(zipFilename, 'w') as backupZip:
            # Percorre toda árvore de diretório e compacta os arquivos de cada pasta.
            for foldername, subfolders, filenames in os.walk(self.folder):
                if 'venv' in foldername or '__pycache__' in foldername:  # evita pastas de ambiente do python
                    continue
                loop_text = 'Adding files in %s...' % foldername
                print(loop_text)
                self.saída.insert('end', loop_text)
                self.saída.see(view)
                view += 1
                # Acrescenta a pasta atual ao arquivo zip.
                backupZip.write(foldername)

                # Acrescenta os arquivos dessa pasta ao arquivo zip.
                for filename in filenames:
                    newBase = os.path.basename(self.folder) + '_'
                    if filename.startswith(newBase) and filename.endswith('.zip'):
                        continue  # não faz backup dos arquivos de backup anteriores.
                    backupZip.write(os.path.join(foldername, filename))

        # backupZip.close()
        self.saída.insert('end', 'Done.')
        print('Done.')


def backup_to_zip():
    '''busca arquivos de valor maior ou igual a um valor dado em um diretório'''
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':  # executa se chamado diretamente
    backup_to_zip()
