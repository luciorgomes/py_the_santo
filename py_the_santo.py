#! /usr/bin/python3
# py_the_santp.py - Funções relacionadas ao e-Processo e outros.

import pyperclip  # manipulação de arquivos binários, clipboard e leitura de linha de comando
import tkinter as tk
import tkinter.ttk as ttk
import ToolTip as tt
import webbrowser
import time
import re
import os
import limpa_csv
import backup_to_zip
import calcula_dv

class Application(tk.Frame):
    '''instancia a janela de parâmetros'''
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.valor_negrito = tk.IntVar()
        self.valor_italico = tk.IntVar()
        self.valor_sublinhado = tk.IntVar()
        self.radio_link_var = tk.IntVar()
        self.radio_csv_var = tk.IntVar()
        self.radio_google_var = tk.IntVar()
        self.radio_dv_var = tk.IntVar()
        self.radio_form_var = tk.IntVar()
        self.pack()
        self.google_chrome = self.busca_google_chrome()

        # cria os componentes da janela
        # estilos
        style = ttk.Style()
        style = ttk.Style()
        style.configure('TFrame', foreground="black", background='gray')
        style.configure('TNotebook', foreground="black", background='gray', font='Helvetica 11 bold', borderwidth=0)
        style.configure('TNotebook.Tab', background='gray', borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', 'gray'), ('active', '#606060')],
                  foreground=[('selected', 'black'), ('active', '#bababa')])
        style.configure('Title.TLabel', foreground="black", background="gray", padding=1, font='Helvetica 11 bold')
        style.configure('BG.TLabel', foreground="black", background="gray", padding=1)
        style.configure('BW.TButton', foreground='#bfbfbf', background='black', highlightbackground='black',
                       width=51, font='Helvetica 11')
        style.configure('BG.TCheckbutton', selectcolor='#818181', foreground="black", background="gray"
                        , bd=2, width=10, anchor='w')
        style.configure('Combo.TCombobox', foreground="black", background="gray", bordercolor='black')
        style_button = {'width': 45, 'bg': '#31363b', 'fg': 'white', 'font': 'Helvetica 10',
                        'highlightbackground': 'black', 'cursor': 'hand2'}
        style_entry = {'bg': '#33425c', 'fg': 'orange', 'width': 55, 'font': 'Arial 10'}
        style_radio ={'foreground': 'black', 'background': 'gray', 'indicatoron': 0, 'bd': 1, 'relief': tk.FLAT,
                      'font':'Arial 10'}

        self.configure(bg='gray')

        # tabs
        self.tab_frame = tk.Frame(self.master, bg='gray')
        self.tab_frame.pack()
        self.tabControl = ttk.Notebook(self.tab_frame, style='TNotebook')  # Create Tab Control
        self.tab1 = ttk.Frame(self.tabControl, style='TFrame')  # Create a tab
        self.tabControl.add(self.tab1, text='e-Processo')  # Add the tab
        self.tab1a = ttk.Frame(self.tabControl, style='TFrame')  # Create a tab
        self.tabControl.add(self.tab1a, text='Arquivos')  # Add the tab
        self.tab2 = ttk.Frame(self.tabControl, style='TFrame')  # Add a second tab
        self.tabControl.add(self.tab2, text='Outros')  # Make second tab visible
        self.tabControl.pack()  # Pack to make visible
        # self.tabControl.pack(expand=1, fill="both")  # Pack to make visible

        # widgets
        # tab 1
        # formata texto
        ttk.Label(self.tab1, text='Formata texto para nota', style='Title.TLabel').pack(pady=3)
        self.frame_formato = tk.Frame(self.tab1, width=45, bg='gray')
        self.frame_formato.pack()
        # ttk.Label(self.tab1, text='Estilo:', style='BG.TLabel').grid(row=1, column=0, sticky='w', padx=2)
        self.check_negrito = ttk.Checkbutton(self.frame_formato, text='Negrito', variable=self.valor_negrito, style='BG.TCheckbutton')
        self.check_negrito.grid(row=0, column=0)
        self.valor_negrito.set('1')
        self.check_italico = ttk.Checkbutton(self.frame_formato, text='Itálico', variable=self.valor_italico, style='BG.TCheckbutton')
        self.check_italico.grid(row=0, column=1)
        self.check_sublinhado = ttk.Checkbutton(self.frame_formato, text='Sublinhado', variable=self.valor_sublinhado,
                                                style='BG.TCheckbutton')
        self.check_sublinhado.grid(row=0, column=2)
        # ttk.Label(self.frame_formato, text='Cor:', style='BG.TLabel').grid(row=0, column=3, sticky='e')
        self.combo_color = ttk.Combobox(self.frame_formato, values=['Preto', 'Azul', 'Verde','Vermelho' ], style='Combo.TCombobox',
                                        exportselection=0, width=9)
        self.combo_color.grid(row=0, column=3, pady=3)
        self.combo_color.set('Preto')
        self.texto_nota = tk.Text(self.frame_formato, width=55, height=5, bg='#33425c', fg='orange', font='Arial 10',
                                  wrap=tk.WORD) #bg original ='#125487'
        self.texto_nota.grid(row=1, columnspan=4, padx=3)
        self.texto_nota.insert(
            tk.INSERT,'Solicitação formalizada indevidamente via e-Cac por meio de dossiê de Restituição de AFRMM.')
        self.texto_nota.bind('<Escape>', self.exit)  # com um Esc encera o programa
        self.bt_gera_nota = tk.Button(self.tab1, style_button, text='Gera nota formatada', command=self.formata_texto_nota)
        self.bt_gera_nota.pack()
        tt.ToolTip(self.bt_gera_nota, 'Gera nota com o texto acima formatado conforme as seleções de estilo e cor')
        ttk.Separator(self.tab1, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=3)

        # Inclui link
        ttk.Label(self.tab1, text='Inclui link em nota', style='Title.TLabel').pack(pady=3)
        self.frame_link = tk.Frame(self.tab1, width=45, bg='gray')
        self.frame_link.pack()
        self.radio_link_processo = tk.Radiobutton(self.frame_link, style_radio, text="Processo", variable=self.radio_link_var,
                                         value=1, width=23)
        self.radio_link_processo.grid(row=0, column=0, padx=3, pady=3, sticky='we')
        tt.ToolTip(self.radio_link_processo, 'Gera nota com link para processo.')
        self.radio_link_url = tk.Radiobutton(self.frame_link, style_radio, text='URL', variable=self.radio_link_var,
                                           value=2, width=23)
        self.radio_link_url.grid(row=0, column=1, padx=3, pady=3, sticky='we')
        self.radio_link_processo.select()
        tt.ToolTip(self.radio_link_url, 'Gera nota com link para url (http://...)')

        self.entry_link = tk.Entry(self.tab1, style_entry)
        self.entry_link.pack()
        # self.entry_link.insert(0, 'http://receita.economia.gov.br/')
        self.entry_link.bind('<Escape>', self.exit)  # com um Esc encera o programa
        self.bt_gera_link = tk.Button(self.tab1, style_button ,text='Gera link para nota', command=self.link)
        self.bt_gera_link.pack()
        tt.ToolTip(self.bt_gera_link, 'Gera nota com link para o processo ou a url indicado acima')
        ttk.Separator(self.tab1, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=3)

        # Transpõe processos
        ttk.Label(self.tab1, text='Transpõe relação de processos copiados na memória',
                                        style='Title.TLabel').pack(pady=3)
        self.bt_transp_procs = tk.Button(self.tab1, style_button , text='Gera relação transposta',
                                         command=self.transpoe_clipboard)
        self.bt_transp_procs.pack()
        tt.ToolTip(self.bt_transp_procs, f'Transpõe a relação de processos copiados na memória para ser colada'
                                         f' no e-Processo')
        ttk.Separator(self.tab1, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=3)

        # Abre funcionalidades
        ttk.Label(self.tab1, text='Abre funções / processos',style='Title.TLabel').pack(pady=3)
        self.bt_abre_cx_trab = tk.Button(self.tab1, style_button ,text='Abre e-Processo',
                                         command=self.abre_e_processo)
        self.bt_abre_cx_trab.pack()
        tt.ToolTip(self.bt_abre_cx_trab, 'Abre a tela de login para o e-Processo')

        self.bt_abre_cx_trab_antiga = tk.Button(self.tab1, style_button ,text='Abre Caixa de Trabalho',
                                         command=self.abre_caixa_trabalho)
        self.bt_abre_cx_trab_antiga.pack()
        tt.ToolTip(self.bt_abre_cx_trab_antiga, 'Abre a caixa de trabalho de equipe no e-Processo')

        self.bt_abre_ger = tk.Button(self.tab1, style_button, text='Abre Gerencial de Estoque',
                  command=self.abre_gerencial_estoque)
        self.bt_abre_ger.pack()
        tt.ToolTip(self.bt_abre_ger, 'Abre o gerencial de estoque de processos do e-Processo')

        self.bt_abre_consulta = tk.Button(self.tab1, style_button, text='Abre Consulta',
                  command=self.abre_consulta)
        self.bt_abre_consulta.pack()
        tt.ToolTip(self.bt_abre_consulta, 'Abre a consulta de processos do e-Processo')

        self.bt_abre_procs = tk.Button(self.tab1, style_button, text='Abre processos copiados na área de transferência',
                  command=self.abre_processos)
        self.bt_abre_procs.pack()
        tt.ToolTip(self.bt_abre_procs, 'Abre os processos os copiados na memória no e-Processo')


        self.bt_abre_procs = tk.Button(self.tab1, style_button, text='Abre palavras-chave dos processos copiados',
                  command=self.abre_palavras_chave)
        self.bt_abre_procs.pack()
        tt.ToolTip(self.bt_abre_procs, 'Abre palavras-chave dos processos copiados na memória')
        ttk.Separator(self.tab1, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=3)

        # Text de sáida
        self.texto_saida = tk.Text(self.master, width=55, height=8,  bg='#33425c', fg='orange', font='Courier 9',
                                   wrap=tk.WORD)
        self.texto_saida.pack(pady=5)
        # self.texto_saida.grid(row=26, columnspan=4, padx=10, pady=5, sticky=tk.EW)
        # self.texto_saida.bind('<Escape>', self.exit)  # com um Esc encera o programa
        self.texto_nota.focus()

        # tab1a
        # Limpa csv
        ttk.Label(self.tab1a, text='Limpa arquivo .csv', style='Title.TLabel').pack(pady=3)
        self.frame_csv = tk.Frame(self.tab1a, width=48, bg='gray')
        self.frame_csv.pack()
        self.radio_csv_virgula = tk.Radiobutton(self.frame_csv, style_radio, text='Separador = ","',
                                               variable=self.radio_csv_var,
                                               value=1, width=23)
        self.radio_csv_virgula.grid(row=1, column=0, padx=4, pady=3, sticky='we')
        tt.ToolTip(self.radio_csv_virgula, 'Usa vírgula como separador de colunas')
        self.radio_csv_pontovirgula = tk.Radiobutton(self.frame_csv, style_radio, text='Separador = ";"',
                                                     variable=self.radio_csv_var, value=2, width=23)
        self.radio_csv_pontovirgula.grid(row=1, column=1, padx=4, pady=3, sticky='we')
        tt.ToolTip(self.radio_csv_pontovirgula, 'Usa ponto e vírgula como separador de colunas')
        self.radio_csv_virgula.select()
        self.run_cvs = tk.Button(self.tab1a, style_button, text='Selecionar o arquivo e executar', command=self.roda_csv)
        self.run_cvs.pack()
        tt.ToolTip(self.run_cvs, 'Processa a remoção de caracteres inválidos no arquivo .csv selecionado')
        ttk.Separator(self.tab1a, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=3)

        # Backup
        ttk.Label(self.tab1a, text='Backup de dirétório para .zip', style='Title.TLabel').pack(pady=3)
        self.run_bk = tk.Button(self.tab1a, style_button, text='Selecionar o diretório e executar', command=self.roda_bk)
        self.run_bk.pack()
        tt.ToolTip(self.run_bk, 'Faz o backup de todo o conteúdo de um diretório para um arquivo .zip')
        ttk.Separator(self.tab1a, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=3)

        # tab2
        # Google
        ttk.Label(self.tab2, text='Google', style='Title.TLabel').pack(pady=3)
        self.frame_google = tk.Frame(self.tab2, width=48, bg='gray')
        self.frame_google.pack()
        self.radio_google_rfb = tk.Radiobutton(self.frame_google, style_radio, text="Google RFB", variable=self.radio_google_var,
                                               value=1, width=23)
        self.radio_google_rfb.grid(row=1, column=0,  padx=4, pady=3, sticky='we')
        tt.ToolTip(self.radio_google_rfb, 'Pesquisa termo no site da RFB usando o Google')
        self.radio_map_it = tk.Radiobutton(self.frame_google,  style_radio, text='Maps', variable=self.radio_google_var,
                                           value=2, width=23)
        self.radio_map_it.grid(row=1, column=1, padx=4, pady=3, sticky='we')
        tt.ToolTip(self.radio_map_it, 'Pesquisa enderenço no Google Maps')
        self.entry_gm = tk.Entry(self.tab2, style_entry)
        self.entry_gm.pack()
        self.entry_gm.bind('<Return>', self.roda_google)
        self.radio_google_rfb.select()
        self.run_gm = tk.Button(self.tab2, style_button, text='Pesquisa', command=self.roda_google)
        self.run_gm.pack()
        tt.ToolTip(self.run_gm, 'Aciona a consulta do termo ou endereço para a opção selecionada (Google RFB ou Maps)')
        ttk.Separator(self.tab2, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=3)

        # Calcula DV
        ttk.Label(self.tab2, text='Cálculo de dígitos verificadores',
                  style='Title.TLabel').pack(pady=3)
        self.frame_dv = tk.Frame(self.tab2, width=48, bg='gray')
        self.frame_dv.pack()
        self.radio_cpf = tk.Radiobutton(self.frame_dv, style_radio, text="Cpf", variable=self.radio_dv_var, value=1,
                                        width=10)
        self.radio_cpf.grid(row=0, column=0, padx=3, sticky='we', pady=2)
        self.radio_cnpj = tk.Radiobutton(self.frame_dv, style_radio, text="Cnpj", variable=self.radio_dv_var, value=2,
                                               width=10)
        self.radio_cnpj.grid(row=0, column=1, padx=3, sticky='we', pady=2)
        self.radio_proc_novo = tk.Radiobutton(self.frame_dv, style_radio, text="Proc. /0000", variable=self.radio_dv_var,
                                              value=3, width=10)
        self.radio_proc_novo.grid(row=0, column=2, padx=3, sticky='we', pady=2)
        self.radio_proc_antigo = tk.Radiobutton(self.frame_dv, style_radio, text="Proc. /00", variable=self.radio_dv_var,
                                                value=4, width=10)
        self.radio_proc_antigo.grid(row=0, column=3, padx=3, sticky='we', pady=2)
        self.radio_cpf.select()
        self.entry_dv = tk.Entry(self.tab2, style_entry)
        self.entry_dv.pack()
        self.entry_dv.bind('<Return>', self.calc_dv)
        self.entry_dv.bind('<KP_Enter>', self.calc_dv)
        self.run_dv = tk.Button(self.tab2, style_button, text='Calcula', command=self.calc_dv)
        self.run_dv.pack()
        tt.ToolTip(self.run_dv, 'Calcula ou valida os DV de CPF, CNPJ ou Processo (com ano de 4 e 2 dígitos).')
        ttk.Separator(self.tab2, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=3)

        # Formata Texto
        ttk.Label(self.tab2, text='Formata texto',
                  style='Title.TLabel').pack(pady=3)
        self.frame_form = tk.Frame(self.tab2, width=48, bg='gray')
        self.frame_form.pack()
        self.radio_maiusculo = tk.Radiobutton(self.frame_form, style_radio, text="XXXX", variable=self.radio_form_var,
                                              value=1, width=10)
        self.radio_maiusculo.grid(row=0, column=0, padx=3, sticky='we', pady=2)
        self.radio_minusculo = tk.Radiobutton(self.frame_form, style_radio, text="xxxx", variable=self.radio_form_var,
                                              value=2, width=10)
        self.radio_minusculo.grid(row=0, column=1, padx=3, sticky='we', pady=2)
        self.radio_title = tk.Radiobutton(self.frame_form, style_radio, text="Xxxx", variable=self.radio_form_var,
                                              value=3, width=10)
        self.radio_title.grid(row=0, column=2, padx=3, sticky='we', pady=2)
        self.radio_inverso = tk.Radiobutton(self.frame_form, style_radio, text="X<>x", variable=self.radio_form_var,
                                                value=4, width=10)
        self.radio_inverso.grid(row=0, column=3, padx=3, sticky='we', pady=2)
        self.radio_maiusculo.select()
        self.entry_form = tk.Entry(self.tab2, style_entry)
        self.entry_form.pack()
        self.entry_form.bind('<Return>', self.formata_txt)
        self.entry_form.bind('<KP_Enter>', self.formata_txt)
        self.run_dv = tk.Button(self.tab2, style_button, text='Formata', command=self.formata_txt)
        self.run_dv.pack()
        tt.ToolTip(self.run_dv, 'Formata o texto em maiúsculas, minúsculas, nome próprio ou caixa invertida.')
        ttk.Separator(self.tab2, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=3)

        self.define_raiz()

    def define_raiz(self):
        '''Define caracterísicas da janela'''
        self.master.title('Py de santo...')
        self.master.configure(bg='gray')
        # dimensões da janela
        largura = 420
        altura = 715
        # resolução da tela
        largura_screen = self.master.winfo_screenwidth()
        altura_screen = self.master.winfo_screenheight()
        # posição da janela
        posx = 6 * largura_screen / 7 - largura / 2  # direita da tela
        posy = altura_screen / 2 - altura / 2  # meio da primeira tela
        self.master.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))  # dimensões + posição inicial

    def exit(self, event=None):
        '''Fecha o aplicativo'''
        self.master.destroy()

    def imprime_saída(self, texto):
        '''Envia texto para o tk.Text de saída'''
        self.texto_saida.insert(tk.INSERT, texto)
        self.texto_saida.see(tk.END)

    def formata_texto_nota(self, event=None):
        '''Aplica formatação a Nota de processo'''
        prefixo = ''
        sufixo = ''

        if self.valor_negrito.get():
            prefixo += '<b>'
            sufixo += '</b>'
        if self.valor_italico.get():
            prefixo += '<i>'
            sufixo += '</i>'
        if self.valor_sublinhado.get():
            prefixo += '<u>'
            sufixo += '</u>'

        cor = self.combo_color.get()
        fonte_cor = ''

        if cor == 'Azul':
            fonte_cor = '<FONT COLOR="blue">'
            sufixo += '</FONT>'
        elif cor == 'Vermelho':
            fonte_cor = '<FONT COLOR="red">'
            sufixo += '</FONT>'
        elif cor == 'Verde':
            fonte_cor = '<FONT COLOR="green">'
            sufixo += '</FONT>'
        elif cor != 'Preto': # se for inserida uma cor manualmente
            fonte_cor = f'<FONT COLOR="{cor}">'
            sufixo += '</FONT>'

        texto = self.texto_nota.get(1.0, tk.END)
        if len(texto) == 0:
            print('Informe o texto da nota')
            self.imprime_saída('Informe o texto da nota\n\n')
        else:
            texto = texto[:-1] # remove a nova linha do final do texto
            saida = prefixo + fonte_cor + texto + sufixo
            pyperclip.copy(saida)  # manda para o clipboard
            print('Nota copiada para a memória (cole com Ctrl+v)')
            self.imprime_saída(saida + '\n\nNota copiada para a memória (cole com Ctrl+v)\n\n')

    def link(self, event=None):
        if self.radio_link_var.get() == 1:
            self.link_processo()
        else:
            self.link_url()

    def link_processo(self, event=None):
        '''Gera link para outro processo para ser inserido em Nota'''
        processo = self.entry_link.get()
        if len(processo) == 0:
            print('Informe o processo.')
            self.imprime_saída('Informe o processo\n\n')
        else:
            proc_filtered = ''.join(i for i in processo if i.isdigit())  # desconsidera tudo o que não for texto
            processo_link = f'<a href="https://eprocesso.suiterfb.receita.fazenda/ControleVisualizacaoProcesso.asp?psAcao=exibir&psNumeroProcesso={proc_filtered} " target = "_blank" title = "{proc_filtered} ">{proc_filtered} </a>'
            pyperclip.copy(processo_link)
            print('Texto do link copiado para a memória (cole com Ctrl+v)')
            self.imprime_saída(processo_link + '\n\nTexto do link copiado para a memória (cole com Ctrl+v)\n\n')

    def link_url(self, event=None):
        '''Gera link (url) para Nota de processo'''
        link = self.entry_link.get()
        if len(link) == 0:
            print('Informe o link')
            self.imprime_saída('Informe o endereço (url)\n\n', 1)
        else:
            tag_link = f'<a href="{link}" target = "_blank" title = "{link}">{link}</a>'
            pyperclip.copy(tag_link)
            print('Texto do link copiado para a memória (cole com Ctrl+v)')
            self.imprime_saída(tag_link + '\n\nTexto do link copiado para a memória (cole com Ctrl+v)\n\n')

    def transpoe_clipboard(self):
        '''Transpõe relação de processos em coluna para serem abertos na caixa de trabalho ou em consulta'''
        mem = pyperclip.paste()
        mem = mem.split()
        transposed = ','.join(mem)
        pyperclip.copy(transposed)
        print('Relação transposta copiada para a memória (cole com Ctrl+v)')
        self.imprime_saída(transposed + '\n\nRelação transposta copiada para a memória (cole com Ctrl+v)\n\n')

    def abre_e_processo(self, event=None):
        '''Faz login no e-Processo'''
        webbrowser.open('https://eprocesso.suiterfb.receita.fazenda/')

    def abre_caixa_trabalho(self, event=None):
        '''Abre caixa de trabalho de equipe no e-Processo'''
        webbrowser.open('https://eprocesso.suiterfb.receita.fazenda/eprocesso/index.html#/ngx/caixa-trabalho-equipe')

    def abre_gerencial_estoque(self, event=None):
        '''Abre gerencioal de estoque no e-Processo'''
        webbrowser.open("https://eprocesso.suiterfb.receita.fazenda/relatorios/ControleManterVisao.asp?psAcao=exibir")

    def abre_consulta(self, event=None):
        '''Abre consulta no e-Processo'''
        webbrowser.open("https://eprocesso.suiterfb.receita.fazenda/eprocesso/index.html#/consultaProcesso")

    def abre_processos(self, event=None):
        '''Abre processos copiados no cliuboard no e-Processo'''
        mem = pyperclip.paste()
        if ',' in mem: # se processos concatenados separados por vírgula
            mem = mem.split(',')
        else:
            mem = mem.split()
        mem = [re.sub('[-./]', '', item) for item in mem] # exclui traço, ponto e barra para passar pelo isnumeric
        saída = ''
        for processo in mem:
            if processo.isnumeric():
                webbrowser.open(f'https://eprocesso.suiterfb.receita.fazenda/ControleVisualizacaoProcesso.asp?psAcao=exibir&psNumeroProcesso={processo}')
                time.sleep(0.5)
                saída += processo + '\n'
        self.imprime_saída(f'Processo(s) aberto(s):\n{saída}\n')

    def abre_palavras_chave(self, event=None):
        '''Abre palavras-chave copiados no clipboard no e-Processo'''
        mem = pyperclip.paste()
        if ',' in mem: # se processos concatenados separados por vírgula
            mem = mem.split(',')
        else:
            mem = mem.split()
        mem = [re.sub('[-./]', '', item) for item in mem] # exclui traço, ponto e barra para passar pelo isnumeric
        saída = ''
        for processo in mem:
            if processo.isnumeric():
                webbrowser.open(f'https://eprocesso.suiterfb.receita.fazenda/ControleConsultarPalavrasChave.asp?psAcao=exibir&psNumeroDocumento=&pbResponsavelProcesso=Nao&psNumeroProcesso={processo}')
                time.sleep(0.5)
                saída += processo + '\n'
        self.imprime_saída(f'Palavras-chave aberta(s) para o(s) processo(s):\n{saída}\n')

    def roda_csv(self, event=None):
        '''Executa a limbeza de arquivos .csv'''
        file = limpa_csv.define_arquivo()
        if self.radio_csv_var.get() == 1:
            separador = ','
        else:
            separador = ';'
        retorno = limpa_csv.testa_e_executa(file, separador)
        if retorno is None:
            self.imprime_saída('Feito!\n')
        else:
            self.imprime_saída(retorno + '\n')

    def roda_bk(self, event=None):
        '''Executa o backup de um diretório'''
        folder = backup_to_zip.define_diretorio()
        try:
            self.imprime_saída('Processando backup em ' + folder + '\n')
        except TypeError:
            self.imprime_saída('Cancelado.\n')
            return
        retorno = backup_to_zip.testa_e_executa(folder)
        print(retorno)
        self.imprime_saída(retorno + '\n')

    def busca_google_chrome(self):
        '''Verifica a existência da instalação do Google Chrome no Windows'''
        path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        if os.path.exists(path):
            return path
        else:
            return None

    def roda_google(self, event=None):
        '''Executa consulta no site da RFB usando o Google a abre endereço no Google Maps'''
        pesquisa = self.entry_gm.get()
        if pesquisa == '':
            self.imprime_saída('Informe o termo ou endereço para busca.\n')
            return
        if self.google_chrome: # se localizado o google-chrome
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(self.google_chrome))
            if self.radio_google_var.get() == 1:
                webbrowser.get('chrome').open(f'https://www.google.com/search?q={pesquisa}+site:receita.economia.gov.br')
            else:
                webbrowser.get('chrome').open(f'https://google.com/maps/place/{pesquisa}')
        else:
            if self.radio_google_var.get() == 1:
                webbrowser.open(f'https://www.google.com/search?q={pesquisa}+site:receita.economia.gov.br')
            else:
                webbrowser.open(f'https://google.com/maps/place/{pesquisa}')

    def calc_dv(self, event=None):
        '''Efetua o cálculo de dígitos verificadores'''
        # self.texto_saida_2.insert(tk.INSERT, self.entry_dv.get())
        if self.radio_dv_var.get() == 1:
            saida = calcula_dv.calcula_cpf(self.entry_dv.get())
        elif self.radio_dv_var.get() == 2:
            saida = calcula_dv.calcula_cnpj(self.entry_dv.get())
        elif self.radio_dv_var.get() > 2:
            saida = calcula_dv.calcula_processo(self.entry_dv.get(), self.radio_dv_var.get() - 2)
        self.imprime_saída(saida + '\n\n')

    def formata_txt(self, event=None):
        '''Altera a formatação de um texto'''
        texto = self.entry_form.get()
        if texto == '':
            self.imprime_saída('Informe o texto a ser formatado.\n')
            return
        saida = ''
        if self.radio_form_var.get() == 1:
            saida = texto.upper()
        elif self.radio_form_var.get() == 2:
            saida = texto.lower()
        elif self.radio_form_var.get() == 3:
            saida = texto.title()
        else:
            saida = texto.swapcase()
        pyperclip.copy(saida)
        print('Texto formatado enviado para a memória (cole com Ctrl+v)')
        self.imprime_saída(f'Texto formatado = {saida} \n\nCopiado para a memória (cole com Ctrl+v)\n\n')

def py_the_santo():
    '''Roda o aplicativo'''
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':  # executa se chamado diretamente
    py_the_santo()
