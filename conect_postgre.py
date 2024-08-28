import tkinter
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from psycopg2 import OperationalError, DatabaseError, InterfaceError, ProgrammingError

class connectBD:
    def __init__(self):
        print("Metodo construtor")
    # Função para conectar ao banco de dados PostgreSQL
    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname="OT-SUPRIMENTOS",  # substitua pelo nome do seu banco de dados
                user="postgres",  # substitua pelo seu usuário
                password="xxxxxxxx%",  # substitua pela sua senha
                host="localhost",  # substitua pelo seu host, se necessário
                port="5432"  # substitua pela sua porta, se necessário
            )
            return self.conn
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao banco de dados: {e}")
            return None
        
    ################################################################################################
    # Carrega todos os dados da tabela itens_estoque do banco.

    def carregaEstoque(self):
        try:
            self.connect_db()
            cursor = self.conn.cursor()
            postgres_select_query = """ SELECT  * FROM ot."itens_estoque" """
            cursor.execute(postgres_select_query)
            #self.conn.commit()
            item = cursor.fetchall()
            print (item, "Registro consultado com successo na tabela itens_estoque")
        except (Exception, psycopg2.Error) as error :
          if(self.conn):
             print("Erro: ", error)
        finally:
            #closing database connection.
            if(self.conn):
               cursor.close()
               self.conn.close()
               print("A conexão com o PostgreSQL foi fechada.")
        return item
    
    ############################################################################################    
    # Função para CONSULTAR UM ITEM na tabela itens_estoque no banco de dados.
    
    def consultarDados(self, codigo):
           try:
             self.connect_db()
             cursor = self.conn.cursor()
             postgres_select_query = """ SELECT  *
                                            FROM ot."itens_estoque"
                                         WHERE "itemid" = %s """
             record_to_select = (codigo)
             cursor.execute(postgres_select_query, (record_to_select,))
             #self.conn.commit()
             item = cursor.fetchall()
           except (Exception, psycopg2.Error) as error :
             if(self.conn):
                print("Falha ao consultar registro na tabela itens_estoque ->", error)
                return error
           finally:
               #closing database connection.
               if(self.conn):
                  cursor.close()
                  self.conn.close()
                  print("A conexão com o PostgreSQL foi fechada.")
           return item
    
    ################################################################################################
    # Função para LISTAR todos os ITENS da tabela itens_estoque do banco de dados.
    
    def listarCodigosItens(self):
           try:
             self.connect_db()
             cursor = self.conn.cursor()
             postgres_select_query = """ SELECT itemid FROM ot."itens_estoque" """
             cursor.execute(postgres_select_query)
             #self.conn.commit()
             item = cursor.fetchall()
             print (item, "Itens consultados com successo na tabela itens_estoque")
           except (Exception, psycopg2.Error) as error :
             if(self.conn):
                print("Falha ao consultar registro na tabela itens_estoque", error)
           finally:
               #closing database connection.
               if(self.conn):
                  cursor.close()
                  self.conn.close()
                  print("A conexão com o PostgreSQL foi fechada.")
           return item
    
    ################################################################################################
    # Função para LISTAR todos as BAIXAS da tabela baixa_itens do banco de dados.
    
    def listarBaixasItens(self):
           try:
             self.connect_db()
             cursor = self.conn.cursor()
             postgres_select_query = """ SELECT id_item, nome_item, quantidade_item, data_item
                                          FROM ot."itens_estoque", ot."baixa_itens"
                                         WHERE id_item = itemid """
             cursor.execute(postgres_select_query)
             #self.conn.commit()
             item = cursor.fetchall()
             print (item, "Itens consultados com successo na tabela baixa_estoque")
           except (Exception, psycopg2.Error) as error :
             if(self.conn):
                print("Falha ao consultar registro na tabela baixa_estoque", error)
           finally:
               #closing database connection.
               if(self.conn):
                  cursor.close()
                  self.conn.close()
                  print("A conexão com o PostgreSQL foi fechada.")
           return item
    
    ################################################################################################
    # Função para INSERIR código dos itens na tabela baixa_itens do banco de dados.

    def registrarItem(self, quantidade, data, codigo):
        try:
             self.connect_db()
             cursor = self.conn.cursor()
             postgres_insert_query = """ INSERT INTO ot."baixa_itens" (quantidade_item, data_item, id_item) 
                                           VALUES (%s,%s,%s) """
             dados_inserir =(quantidade, data, codigo)
             cursor.execute(postgres_insert_query, dados_inserir)
             self.conn.commit()
             count = cursor.rowcount
             print (count, "Registro inserido com successo na tabela baixa_itens")
             postgre_select_query = """ SELECT total_item
                                          FROM ot."itens_estoque"
                                          WHERE itemid = %s"""
             cursor.execute(postgre_select_query, (codigo,))
             total_item = cursor.fetchone()[0]
             print("Total item é: ", total_item)
             novo_total = (total_item - quantidade)
             print("Novo total antes do UPDATE: ", novo_total)
             postgre_update_query = """ UPDATE ot."itens_estoque" SET total_item = %s WHERE itemid = %s """
             #dado_update = (total_item, codigo)
             cursor.execute(postgre_update_query, (novo_total, codigo))
             self.conn.commit()
             count_up = cursor.rowcount
             print(count_up, "Saldo de itens atualizado com successo na tabela itens_estoque")
        except (Exception, psycopg2.Error) as error :
            if(self.conn):
              print("Falha ao inserir o registro na tabela baixa_itens", error)
        finally:
            #closing database connection.
            if(self.conn):
               cursor.close()
               self.conn.close()
               print("A conexão com o PostgreSQL foi fechada.")

################################################################################################
    # Função para GERAR RELATÓRIO das BAIXAS da tabela baixa_itens por período.
    
    def gerarRelatorioBaixas(self, datainicial, datafinal):
           try:
             self.connect_db()
             cursor = self.conn.cursor()
             postgres_select_query = """ SELECT id_item, nome_item, quantidade_item, data_item
                                          FROM ot."itens_estoque", ot."baixa_itens"
                                         WHERE data_item BETWEEN %s AND %s"""
             cursor.execute(postgres_select_query, (datainicial, datafinal))
             #self.conn.commit()
             dados = cursor.fetchall()
             print (dados, "Itens consultados com successo na tabela baixa_estoque")
           except (Exception, psycopg2.Error) as error :
             if(self.conn):
                print("Falha ao consultar registro na tabela baixa_estoque", error)
           finally:
               #closing database connection.
               if(self.conn):
                  cursor.close()
                  self.conn.close()
                  print("A conexão com o PostgreSQL foi fechada.")
           return dados

 ################################################################################################
    # Função para ATUALIZAR ITENS na tabela itens_estoque do banco de dados.

    def atualizarItem(self, nome, total, codigo):
        try:
             self.connect_db()
             cursor = self.conn.cursor()
             postgre_update_query = """ UPDATE ot."itens_estoque" SET nome_item = %s, total_item = %s WHERE itemid = %s """
             #dado_update = (total_item, codigo)
             cursor.execute(postgre_update_query, (nome, total, codigo))
             self.conn.commit()
             count_up = cursor.rowcount
             print(count_up, "Saldo de itens atualizado com successo na tabela itens_estoque")
        except (Exception, psycopg2.Error) as error :
            if(self.conn):
              print("Falha ao inserir o registro na tabela baixa_itens", error)
        finally:
            #closing database connection.
            if(self.conn):
               cursor.close()
               self.conn.close()
               print("A conexão com o PostgreSQL foi fechada.")

################################################################################################
    # Função para INSERIR ITENS na tabela itens_estoque do banco de dados.

    def inserirItem(self, nome, total):
        try:
             self.connect_db()
             cursor = self.conn.cursor()
             postgres_insert_query = """ INSERT INTO ot."itens_estoque" (nome_item, total_item) 
                                           VALUES (%s, %s) """
             dados_inserir =(nome, total)
             cursor.execute(postgres_insert_query, dados_inserir)
             self.conn.commit()
             count = cursor.rowcount
             print (count, "Registro inserido com successo na tabela itens_estoque")
        except (Exception, psycopg2.Error) as error :
            if(self.conn):
              print("Falha ao inserir o registro na tabela itens_estoque", error)
        finally:
            #closing database connection.
            if(self.conn):
               cursor.close()
               self.conn.close()
               print("A conexão com o PostgreSQL foi fechada.")

