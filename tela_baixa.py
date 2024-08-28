##############################################################################################################
# TELA PARA EFETUAR A BAIXA DOS ITENS UTILIZADOS NO DIA DIA.
##############################################################################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import conect_postgre as postgreBD
from datetime import datetime 

# Tela 1 do App.
class BaixaItemApp(ttk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.objBD = postgreBD.connectBD()
        # Criação dos widgets
        self.create_widgets()
        # Create Treeview
        self.create_treeview()


##############################################################################################################
# Cria widgets.

    def create_widgets(self):
        #Label título tela
        self.label_nome = tk.Label(self, text="REGISTRA ITENS UTILIZADOS NO DIA A DIA", font=("helvetica",15, "bold"))
        self.label_nome.place(x=10, y=9)
        
        # Label e Entry para Código do Item
        self.label_codigo = tk.Label(self, text="Código do Item", font=("helvetica",11, "bold") )
        self.label_codigo.place(x=80, y=87)
        self.entry_codigo = tk.Entry(self)
        self.entry_codigo.place(x=210, y=90)

        # Label e Entry para Quantidade
        self.label_quantidade = tk.Label(self, text="Quantidade", font=("helvetica",11, "bold") )
        self.label_quantidade.place(x=80, y=127)
        self.entry_quantidade = tk.Entry(self)
        self.entry_quantidade.place(x=210, y=130)

        # Label e Entry para Data
        self.label_data = tk.Label(self, text="Data (dd/mm/yyyy)", font=("helvetica",11, "bold") )
        self.label_data.place(x=80, y=167)
        self.entry_data = tk.Entry(self)
        self.entry_data.place(x=210, y=170)

        ## Botão de Registrar
        self.button_registrar = tk.Button(self, text="Registrar", command=self.registrar_item)
        self.button_registrar.place(x=240, y=210)


##############################################################################################################   
# Cria Treeview. 

    def create_treeview(self):
        self.tree = ttk.Treeview(self, columns=("codigo", "nome", "quantidade", "data"), show="headings", xscrollcommand="", yscrollcommand="")
        self.tree.heading("codigo", text="Código do Item")
        self.tree.heading("nome", text="Nome do Item")
        self.tree.heading("quantidade", text="Quantidade")
        self.tree.heading("data", text="Data")
        self.tree.place(x=10, y=210)
        
        # Carregar baixas na tela
        self.carrega_baixas()

        # Criação das barras de rolagem
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)

        # Associar as barras de rolagem ao Treeview
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Posicionar o Treeview e as barras de rolagem na janela
        self.tree.place(x=10, y=270, width=800, height=210)
        vsb.place(x=828, y=276, height=200, anchor="ne")
        hsb.place(x=10, y=496, width=800, anchor="sw")
    
##############################################################################################################
# Carrega as baixas na tela.

    def carrega_baixas(self):
        try:
            self.tree.delete(*self.tree.get_children()) #Limpa tela Treeview para manter somente uma linha de dados
            registros = self.objBD.listarBaixasItens()
            for item in registros:
                codigo=item[0]
                nome=item[1]
                quantidade=item[2]
                data= datetime.strftime(item[3], '%d/%m/%Y')
                #print("Código = ", codigo)
                #print("Nome = ", nome)
                #print("Quantidade  = ", quantidade)
                #print("Data = ", data, "\n")
                self.tree.insert("", "end", values=(codigo, nome, quantidade, data))
        except Exception:
            messagebox.showerror("Erro", "Erro ao lista as baixas na tela!")
            return

################################################################################################################
# Limpar campos após registrar item.
   
    def limpa_campos(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)


############################################################################################
# Registrar baixa diária de itens na tabela baixa_itens.

    def registrar_item(self):
        codigo = self.entry_codigo.get()
        quantidade = self.entry_quantidade.get()
        data = self.entry_data.get()
        if not self.validar_data(data):
            messagebox.showerror("Erro", "A Data precisa ser informada no formato DD/MM/YYYY!")
            return
        try:
            codigo = int(codigo)
            quantidade = int(quantidade)
            self.objBD.registrarItem(quantidade, data, codigo)
            self.limpa_campos()
            self.tree.delete(*self.tree.get_children()) #Limpa tela Treeview para manter somente uma linha de dados 
            # Atualizar Treeviewer
            registros = self.objBD.listarBaixasItens()
            for item in registros:
                codigo=item[0]
                nome=item[1]
                quantidade=item[2]
                data= datetime.strftime(item[3], '%d/%m/%Y')
                self.tree.insert("", "end", values=(codigo, nome, quantidade, data))
        except ValueError:
            messagebox.showerror("Erro", "Código do Item de ser um número inteiro!")
           
################################################################################################
# Validar datas.

    def validar_data(self, data_str):
            formato = '%d/%m/%Y'
            try:
                datetime.strptime(data_str, formato)
                return True
            except ValueError:
                return False
            

