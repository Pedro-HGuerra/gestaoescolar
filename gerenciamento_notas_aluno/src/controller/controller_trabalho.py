from model.trabalho import Trabalho
from conexion.oracle_queries import OracleQueries
from reports.relatorios import Relatorio
from datetime import datetime, date, timedelta

relatorio=Relatorio()

class controller_trabalho:
    def __init__(self):
        pass
        
    def inserir_trabalho(self) -> Trabalho:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        relatorio=Relatorio()

        qtdCriteriosAvaliados = input("Digite a quantidade de critérios avaliados que o trabalho terá: ")
        date_entrega = datetime.today()+timedelta(int(input(f"Quantos dias à frente da data {datetime.today().strftime('%d-%m-%Y')} a trabalho deverá ser entregue? ")))

        cursor = oracle.connect()
        output_value = cursor.var(int)
        data = dict(codigo=output_value, qtdCriteriosAvaliados=qtdCriteriosAvaliados, date_entrega=date_entrega)

        cursor.execute("""

        begin

            :codigo := TRABALHO_ID_TRABALHO_SEQ.NEXTVAL;

            insert into trabalho values(:codigo, :qtdCriteriosAvaliados, :date_entrega);

        end;

        """, data)

        codigo_trabalho = output_value.getvalue()

        oracle.conn.commit()

        df_trabalho = oracle.sqlToDataFrame(f"select id_trabalho, qtdcriteriosavaliados, to_char(date_entrega, 'dd-mm-yyyy') as date_entrega from trabalho where id_trabalho = {codigo_trabalho}")
        novo_trabalho = Trabalho(df_trabalho.id_trabalho.values[0], df_trabalho.qtdcriteriosavaliados.values[0], df_trabalho.date_entrega.values[0])
        print(novo_trabalho.to_string())
        return novo_trabalho

    def atualizar_trabalho(self) -> Trabalho:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_trabalho = int(input("Digite o código que deseja alterar: "))

        if not self.verifica_existencia_trabalho(oracle, id_trabalho):
            novo_qtdCriteriosAvaliados = input("Digite a quantidade de novos critérios avaliados: ")
            
            oracle.write(f"update trabalho set qtdCriteriosAvaliados = '{novo_qtdCriteriosAvaliados}' where id_trabalho = {id_trabalho}")

            df_trabalho = oracle.sqlToDataFrame(f"select id_trabalho, qtdCriteriosAvaliados, to_char(date_entrega, 'dd-mm-yyyy') as date_entrega from trabalho where id_trabalho = {id_trabalho}")
            trabalho_atualizado = Trabalho(df_trabalho.id_trabalho.values[0], df_trabalho.qtdcriteriosavaliados.values[0], df_trabalho.date_entrega.values[0])
            print(trabalho_atualizado.to_string())
            return trabalho_atualizado
        else:
            print(f"O trabalho {id_trabalho} não existe.")
            return None

    def excluir_trabalho(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_trabalho = int(input("Digite o código do trabalho que deseja excluir:"))        

        if not self.verifica_existencia_trabalho(oracle, id_trabalho):
            if self.verificar_avaliacao_aluno(oracle, need_connect=True, id_trabalho=id_trabalho):            
                df_trabalho = oracle.sqlToDataFrame(f"select id_trabalho, qtdCriteriosAvaliados, to_char(date_entrega, 'dd-mm-yyyy') as date_entrega from trabalho where id_trabalho = {id_trabalho}")
                oracle.write(f"delete from trabalho where id_trabalho = {id_trabalho}")            
                trabalho_excluido = Trabalho(df_trabalho.id_trabalho.values[0], df_trabalho.qtdcriteriosavaliados.values[0], df_trabalho.date_entrega.values[0])
                print("Trabalho removido com sucesso!")
                print(trabalho_excluido.to_string())
            else:
                print("Não é possível excluir esse trabalho! Já foram registradas notas para o mesmo")
        else:
            print(f"Trabalho {id_trabalho} não existe.")

    def verifica_existencia_trabalho(self, oracle:OracleQueries, id_trabalho:str=None) -> bool:
        df_trabalho = oracle.sqlToDataFrame(f"select id_trabalho, qtdCriteriosAvaliados, to_char(date_entrega, 'dd-mm-yyyy') as date_entrega from trabalho where id_trabalho = {id_trabalho}")
        return df_trabalho.empty
    
    def verificar_avaliacao_aluno(self, oracle:OracleQueries, need_connect:bool=False, id_trabalho=0):
        query = f"""
                select id_trabalho 
                    from avaliacao_aluno
                    where id_trabalho = {id_trabalho}
        """ 
        if need_connect: 
            oracle.connect()
        
        return oracle.sqlToDataFrame(query).empty