##############################################################################################################
# TELA PARA GERAR RELATÓRIOS DE BAIXA DOS ITENS.
##############################################################################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext, filedialog
from datetime import datetime
import conect_postgre as postgreBD
from datetime import datetime 
import csv
import io


# Tela 1 do App.
class RelatorioApp(ttk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.objBD = postgreBD.connectBD()
        # Criação dos widgets
        self.create_widgets()

##############################################################################################################
# Cria widgets.

    def create_widgets(self):
        #Label título tela
        self.label_nome = tk.Label(self, text="RELATÓRIO POR PERÍODO", font=("helvetica",15, "bold"))
        self.label_nome.place(x=10, y=9)
        
        # Label e Entry para Data inicial
        self.label_datainicial = tk.Label(self, text="Data Inicial", font=("helvetica",11, "bold") )
        self.label_datainicial.place(x=80, y=87)
        self.entry_datainicial = tk.Entry(self)
        self.entry_datainicial.place(x=210, y=90)

        # Label e Entry para Data Final
        self.label_datafinal = tk.Label(self, text="Data Final", font=("helvetica",11, "bold") )
        self.label_datafinal.place(x=80, y=127)
        self.entry_datafinal = tk.Entry(self)
        self.entry_datafinal.place(x=210, y=130)

        ## Botão de Registrar
        self.button_registrar = tk.Button(self, text="Gerar Relatório", command=self.gerar_relatorio)
        self.button_registrar.place(x=210, y=180)

        self.result_text = scrolledtext.ScrolledText(self, width=90, height=25)
        self.result_text.place(x=45, y=230)

    
##############################################################################################################
# Carrega as baixas na tela.

    def carrega_baixas(self):
        try:
            self.tree.delete(*self.tree.get_children()) #Limpa tela Treeview para manter somente uma linha de dados
            registros = self.objBD.listarBaixasItens()
            print(registros)
            for item in registros:
                codigo=item[0]
                nome=item[1]
                quantidade=item[2]
                data= datetime.strftime(item[3], '%d/%m/%Y')
                print("Código = ", codigo)
                print("Nome = ", nome)
                print("Quantidade  = ", quantidade)
                print("Data = ", data, "\n")
                self.tree.insert("", "end", values=(codigo, nome, quantidade, data))
        except Exception:
            messagebox.showerror("Erro", "Erro ao lista as baixas na tela!")
            return

################################################################################################################
# Limpar campos após registrar item.
   
    def limpa_campos(self):
        self.entry_datainicial.delete(0, tk.END)
        self.entry_datafinal.delete(0, tk.END)


############################################################################################
# Registrar baixa diária de itens na tabela baixa_itens.

    def gerar_relatorio(self):
        datainicial = self.entry_datainicial.get()
        datafinal = self.entry_datafinal.get()
        if not self.validar_data(datainicial) or not self.validar_data(datafinal):
            messagebox.showerror("Erro", "A Data precisa ser informada no formato DD/MM/YYYY!")
            return
        try:
            dados = self.objBD.gerarRelatorioBaixas(datainicial, datafinal)
            if dados:
                arquivo_csv = self.exportar_para_csv(dados)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, arquivo_csv)
                self.salvar_arquivo(arquivo_csv)
            else:
                messagebox.showinfo("Informação", "Nenhum dado encontrado para o intervalo fornecido.")
        except ValueError:
            messagebox.showerror("Erro", "Código do Item de ser um número inteiro!")
           
################################################################################################
# Validr datas.

    def validar_data(self, data_str):
            formato = '%d/%m/%Y'
            try:
                datetime.strptime(data_str, formato)
                return True
            except ValueError:
                return False

################################################################################################
# Exporta dados para arquivo CSV.

    def exportar_para_csv(self, dados):
            output = io.StringIO()
            writer = csv.writer(output)

            # Escrever o cabeçalho (opcional)
            writer.writerow(['Codigo do item', 'Nome do item', 'Quantidade', 'Data'])

            # Escrever os dados
            writer.writerows(dados)

            return output.getvalue()            

    def salvar_arquivo(self, csv_data):
        # Mostrar o diálogo para salvar o arquivo
        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os Arquivos", "*.*")])

        if caminho_arquivo:
            try:
                with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as file:
                    file.write(csv_data)
                messagebox.showinfo("Sucesso", "Relatório salvo com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")


