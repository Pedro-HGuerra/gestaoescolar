from model.aluno import Aluno
from conexion.oracle_queries import OracleQueries
from reports.relatorios import Relatorio
relatorio=Relatorio()

class controller_aluno:
    def __init__(self):
        pass

    def inserir_aluno(self) -> Aluno:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
    
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        relatorio=Relatorio()
        
        nome=input("Digite o nome: ")
        idade=input("Digite a idade: ")
        turma=input("Digite a turma: ")

        cursor = oracle.connect()
        output_value = cursor.var(int)
        data = dict(codigo=output_value, nome=nome, idade=idade, turma=turma)
        #print(f'codigo={output_value}, nome={nome}, idade={idade}, turma={turma}')
        cursor.execute("""

        begin

            :codigo := ALUNO_ID_ALUNO_SEQ.NEXTVAL;

            insert into aluno values(:codigo, :nome, :idade, :turma);

        end;

        """, data)

        codigo_aluno = output_value.getvalue()
        oracle.conn.commit()
        df_aluno= oracle.sqlToDataFrame(f"select id_aluno, nome, idade, turma from aluno where id_aluno = {codigo_aluno}")
        novo_aluno=Aluno(df_aluno.id_aluno.values[0], df_aluno.nome.values[0], df_aluno.idade.values[0], df_aluno.turma.values[0])
        print(novo_aluno.to_string())
        return novo_aluno

    def atualizar_aluno(self) -> Aluno:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_aluno=int(input("Digite o código que deseja alterar: "))

        if not self.verifica_existencia_ID_Aluno(oracle,id_aluno):
            novo_nome=input("Digite o novo nome: ")
            novo_idade=input("Digite a nova idade: ")
            novo_turma=input("Digite a nova turma: ")
            oracle.write(f"update Aluno set nome = '{novo_nome}', idade = '{novo_idade}', turma = '{novo_turma}' where ID_Aluno = {id_aluno}")
            df_aluno=oracle.sqlToDataFrame(f"select id_aluno, nome, idade, turma from Aluno where id_aluno = {id_aluno}")
            aluno_atualizado=Aluno(df_aluno.id_aluno.values[0], df_aluno.nome.values[0], df_aluno.idade.values[0], df_aluno.turma.values[0])
            print(aluno_atualizado.to_string())
            return aluno_atualizado
        else:
            print(f"o ID_Aluno {id_aluno} não existe.")
            return None
        
    def excluir_Aluno(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        id_aluno = int(input("Digite o código do aluno que deseja excluir: ")) 

        if not self.verifica_existencia_ID_Aluno(oracle,id_aluno):
            if self.verificar_avaliacao_aluno(oracle=oracle, need_connect=True, id_aluno=id_aluno):
                df_aluno=oracle.sqlToDataFrame(f"select id_aluno,nome, idade, turma from Aluno where id_aluno = {id_aluno}")
                oracle.write(f"delete from aluno where id_aluno = {id_aluno}")
                aluno_excluido=Aluno(df_aluno.id_aluno.values[0],df_aluno.nome.values[0],df_aluno.idade.values[0],df_aluno.turma.values[0])
                print("Aluno Removido com sucesso!")
                print(aluno_excluido.to_string())
            else:
                print("Não é possível excluir aluno! Já foram registradas notas para o mesmo! ")
        else:
            print(f"O código {id_aluno} não existe.")
            
    def verifica_existencia_ID_Aluno(self, oracle:OracleQueries, id_aluno:str=None) -> bool:
        df_aluno = oracle.sqlToDataFrame(f"select id_aluno, nome, idade, turma from aluno where id_aluno = {id_aluno}")
        return df_aluno.empty
    
    def verificar_avaliacao_aluno(self, oracle:OracleQueries, need_connect:bool=False, id_aluno=0):
        query = f"""
                select id_aluno 
                    from avaliacao_aluno
                    where id_aluno = {id_aluno}
        """ 
        if need_connect: 
            oracle.connect()
        
        return oracle.sqlToDataFrame(query).empty