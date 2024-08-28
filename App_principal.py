import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
#import conect_postgre
import psycopg2
import conect_postgre as postgreBD
from tela_baixa import BaixaItemApp
from tela_gerenciamento import GerenciarItemApp
from tela_relatorio import RelatorioApp
import csv
import io

################################################################################################

class MainApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("GESTÃO DE SUPRIMENTOS")
        self.root.geometry("850x700")
        self.centralizar_janela()

#############################################################################################################
# Cria o Notebook (aba). ####################################################################################
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, fill='both', expand=True)

        # Cria e adiciona as abas
        self.tela1_frame = BaixaItemApp(self.notebook)
        self.tela2_frame = GerenciarItemApp(self.notebook)
        self.tela3_frame = RelatorioApp(self.notebook)

        self.notebook.add(self.tela1_frame, text='  REGISTRAR USO DE ITENS  ')
        self.notebook.add(self.tela2_frame, text='  GERENCIAMENTO DE ITENS  ')
        self.notebook.add(self.tela3_frame, text='  RELATÓRIO POR PERÍODO  ')

##############################################################################################################
# Centralizar tela do App.####################################################################################

    def centralizar_janela(self):
        # Obtém a largura e a altura da tela
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        # Obtém a largura e a altura da janela
        largura_janela = 850
        altura_janela = 700
        # Calcula a posição x e y para centralizar a janela
        x = (largura_tela // 2) - (largura_janela // 2)
        y = (altura_tela // 2) - (altura_janela // 2)
        # Define a posição e o tamanho da janela
        self.root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()