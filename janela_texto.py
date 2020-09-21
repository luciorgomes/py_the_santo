import tkinter as tk
import pyperclip

def janela_texto(titulo='', label='', texto=''):
    root = tk.Tk()
    root.title(titulo)
        # Define caracterísicas da janela
    root.configure(bg='gray')
    #root.iconphoto(False, tk.PhotoImage(file='./image/Python-icon.png'))
    # dimensões da janela
    largura = 1150
    altura = 880
    # resolução da tela
    largura_screen = root.winfo_screenwidth()
    altura_screen = root.winfo_screenheight()
    # posição da janela
    posx = largura_screen / 2 - largura / 2  # meio da tela
    posy = altura_screen / 2 - altura / 2  # meio da primeira tela
    root.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))  # dimensões + posição inicial

    label_topo = tk.Label(root,text=label, width=140, bg='gray', fg='black', anchor='w')
    label_topo.pack()

    text = tk.Text(root, background='#125487',foreground='orange', font = 'Mono 10', wrap=tk.WORD)
    text.insert('insert', texto)
    text['width'] = 140
    text['height'] = 43
    text.pack()
    #
    text.tag_add("all", "1.0", 'end')
    conteudo = titulo +'\n\n' + label +'\n\n' + texto
    print(conteudo)
    pyperclip.copy(conteudo)

    def exit(event=None):
        root.destroy()

    root.bind('<Escape>', exit)  # com um Esc encera o programa

    root.mainloop()

if __name__ == '__main__': # executa se chamado diretamente
    janela_texto('1', '2', '3\n.......')