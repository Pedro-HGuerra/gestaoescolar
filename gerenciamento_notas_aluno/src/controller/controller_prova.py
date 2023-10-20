from model.prova import Prova
from conexion.oracle_queries import OracleQueries
from reports.relatorios import Relatorio
from datetime import datetime, date, timedelta

relatorio=Relatorio()

class controller_prova:
    def __init__(self):
        pass
        
    def inserir_prova(self) -> Prova:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        relatorio=Relatorio()
        quant_Questao = input("Digite a quantidade de questões que terá na prova: ")
        date_Aplicacao = datetime.today()+timedelta(int(input(f"Quantos dias à frente da data {datetime.today().strftime('%d-%m-%Y')} a prova será aplicada? ")))
        cursor = oracle.connect()
        output_value = cursor.var(int)
        data = dict(codigo=output_value, quant_Questao=quant_Questao, date_Aplicacao=date_Aplicacao)

        cursor.execute("""

        begin

            :codigo := PROVA_ID_PROVA_SEQ.NEXTVAL;

            insert into prova values(:codigo, :quant_Questao, :date_Aplicacao);

        end;

        """, data)

        codigo_prova = output_value.getvalue()
        oracle.conn.commit()
        df_prova = oracle.sqlToDataFrame(f"select id_prova, quant_questao, to_char(date_aplicacao, 'dd-mm-yyyy') as date_aplicacao from prova where id_prova = {codigo_prova}")
        novo_prova = Prova(df_prova.id_prova.values[0], df_prova.quant_questao.values[0], df_prova.date_aplicacao.values[0])
        print(novo_prova.to_string())
        return novo_prova

    def atualizar_prova(self) -> Prova:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_prova = int(input("Digite o código que deseja alterar: "))

        if not self.verifica_existencia_prova(oracle, id_prova):
            novo_quant_Questao = input("Digite a quantidade de novas questões: ")

            oracle.write(f"update prova set quant_Questao = '{novo_quant_Questao}' where id_prova = {id_prova}")

            df_prova = oracle.sqlToDataFrame(f"select id_prova, quant_Questao, to_char(date_aplicacao, 'dd-mm-yyyy') as date_aplicacao from prova where id_prova = {id_prova}")
            prova_atualizado = Prova(df_prova.id_prova.values[0], df_prova.quant_questao.values[0], df_prova.date_aplicacao.values[0])
            print(prova_atualizado.to_string())
            return prova_atualizado
        else:
            print(f"A prova {id_prova} não existe.")
            return None

    def excluir_prova(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_prova = int(input("Digite o código da prova que deseja excluir:"))        

        if not self.verifica_existencia_prova(oracle, id_prova): 
            if self.verificar_avaliacao_aluno(oracle, need_connect=True, id_prova=id_prova):           
                df_prova = oracle.sqlToDataFrame(f"select id_prova, quant_Questao, to_char(date_aplicacao, 'dd-mm-yyyy') as date_aplicacao from prova where id_prova = {id_prova}")
                oracle.write(f"delete from prova where id_prova = {id_prova}")            
                prova_excluido = Prova(df_prova.id_prova.values[0], df_prova.quant_questao.values[0], df_prova.date_aplicacao.values[0])
                print("Prova removida com sucesso!")
                print(prova_excluido.to_string())
            else:
                print("Não é possível excluir esta prova! Já foram registradas notas para a mesma")
        else:
            print(f"Prova {id_prova} não existe.")

    def verifica_existencia_prova(self, oracle:OracleQueries, id_prova:str=None) -> bool:
        df_prova = oracle.sqlToDataFrame(f"select id_prova, quant_questao, to_char(date_aplicacao, 'dd-mm-yyyy') as date_aplicacao from prova where id_prova = {id_prova}")
        return df_prova.empty
    
    def verificar_avaliacao_aluno(self, oracle:OracleQueries, need_connect:bool=False, id_prova=0):
        query = f"""
                select id_prova 
                    from avaliacao_aluno
                    where id_prova = {id_prova}
        """ 
        if need_connect: 
            oracle.connect()
        
        return oracle.sqlToDataFrame(query).empty