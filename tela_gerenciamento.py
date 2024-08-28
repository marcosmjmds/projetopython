############################################################################################################################
# TELA PARA CONSULTAR ITENS DO ESTOQUE:
#   1 - INFORMANDO O CODIGO PARA OBTER O VALOR DE UM ITEM. 
#   2 - CLICANDO EM CONSULTAR PARA VER TODOS OS ITENS.
############################################################################################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import conect_postgre as postgreBD


# Tela 1 do App.
class GerenciarItemApp(ttk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.objBD = postgreBD.connectBD()
        # Criação dos widgets
        self.create_widgets()
        # Create Treeview
        self.create_treeview()
        self.carregar_item()

##############################################################################################################
# Cria widgets.

    def create_widgets(self):
        #Label título tela
        self.label_nome = tk.Label(self, text="ATUALIZA / CADASTRAR / CONSULTAR ITEM DO ESTOQUE", font=("helvetica",15, "bold"))
        self.label_nome.place(x=10, y=9)
        
        # Label e Entry para Código do Item
        self.label_codigo = tk.Label(self, text="Código do Item", font=("helvetica",11, "bold") )
        self.label_codigo.place(x=80, y=87)
        self.entry_codigo = tk.Entry(self)
        self.entry_codigo.place(x=210, y=90)

        # Label e Entry para Nome do Item
        self.label_nome = tk.Label(self, text="Nome do Item", font=("helvetica",11, "bold") )
        self.label_nome.place(x=80, y=127)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.place(x=210, y=130)

        # Label e Entry para Total
        self.label_total = tk.Label(self, text="Total", font=("helvetica",11, "bold") )
        self.label_total.place(x=80, y=167)
        self.entry_total = tk.Entry(self)
        self.entry_total.place(x=210, y=170)

        ## Botão de Atualizar
        self.button_atualizar = tk.Button(self, text="Atualizar", command=self.atualizar_item)
        self.button_atualizar.place(x=140, y=216)

        ## Botão de Cadastrar
        self.button_cadastrar = tk.Button(self, text="Cadastrar", command=self.inserir_item)
        self.button_cadastrar.place(x=250, y=216)

        ## Botão de Registrar
        self.button_consultar = tk.Button(self, text="Consultar", command=self.carregar_item)
        self.button_consultar.place(x=360, y=216)

#################################################################################################################   
# Create Treeview.

    def create_treeview(self):
        self.tree = ttk.Treeview(self, columns=("codigo", "nome", "total"), show="headings", xscrollcommand="", yscrollcommand="")
        self.tree.heading("codigo", text="Código do Item")
        self.tree.heading("nome", text="Nome do Item")
        self.tree.heading("total", text="Total")
        self.tree.place(x=10, y=310)

        # Criação das barras de rolagem
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)

        # Associar as barras de rolagem ao Treeview
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Posicionar o Treeview e as barras de rolagem na janela
        self.tree.place(x=10, y=270, width=800, height=210)
        vsb.place(x=828, y=276, height=200, anchor="ne")
        hsb.place(x=10, y=496, width=800, anchor="sw")
        
        self.tree.bind("<<TreeviewSelect>>", self.apresentarRegistrosSelecionados)

##############################################################################################################
# Limpa campos.
   
    def limpa_campos(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_nome.delete(0, tk.END)
        self.entry_total.delete(0, tk.END)    

##############################################################################################################
# Carrega dados na tela do Treeview.

    def carregar_item(self):
            self.tree.delete(*self.tree.get_children()) #Limpa tela Treeview para manter somente uma linha de dados
            codigo = self.entry_codigo.get()
            #numero = codigo.isnumeric()
            if not codigo:
                try:
                    registro = self.objBD.carregaEstoque()
                    for itens in registro:
                        self.tree.insert("", "end", values=(itens))
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao efetuar a consulta dos itens do estoque! {e}")
                    return 
            else:
                try:
                    valor = int(codigo)
                    registro = self.objBD.consultarDados(codigo)
                    if not registro:
                        messagebox.showerror("Erro", "Item não localizado no estoque!")
                        return
                    for dado in registro:
                        self.tree.insert("", "end", values=(dado)) # Add item to the Treeview
                except Exception as e:
                    messagebox.showerror("Erro", "O código precisa conter somente números!")
            
################################################################################################
# Atualizar item pelo Botão Atualizar.

    def atualizar_item(self):
            #self.tree.delete(*self.tree.get_children()) #Limpa tela Treeview para manter somente uma linha de dados
            nome = self.entry_nome.get()
            total = self.entry_total.get()
            codigo = self.entry_codigo.get()
            if not nome or not total or not codigo:
                messagebox.showerror("Erro", "Todos os campos precisam ser preenchidos !")
                return
            try:
                self.objBD.atualizarItem(nome, total, codigo)
                self.limpa_campos()
                self.tree.delete(*self.tree.get_children())
                self.carregar_item()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar item no estoque! {e}")
                return

################################################################################################
# iNSERIR item pelo Botão Atualizar.

    def inserir_item(self):
            nome = self.entry_nome.get()
            total = self.entry_total.get()
            if not nome or not total:
                messagebox.showerror("Erro", "Os campos Nome do Item e Total precisam ser preenchidos !")
                return
            try:
                self.objBD.inserirItem(nome, total)
                self.limpa_campos()
                self.tree.delete(*self.tree.get_children())
                self.carregar_item()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar o itens no estoque! {e}")
                return
            
##################################################################################################
# Selecionar itens.

    def apresentarRegistrosSelecionados(self, event):  
            self.limpa_campos()  
            for selection in self.tree.selection():  
                item = self.tree.item(selection)  
                codigo,nome,total = item["values"][0:3]  
                self.entry_codigo.insert(0, codigo)  
                self.entry_nome.insert(0, nome)  
                self.entry_total.insert(0, total) 