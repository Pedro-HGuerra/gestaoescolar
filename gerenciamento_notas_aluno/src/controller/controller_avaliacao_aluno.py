from model.avaliacao_aluno import avaliacaoaluno
from model.aluno import Aluno
from controller.controller_aluno import controller_aluno
from model.prova import Prova
from controller.controller_prova import controller_prova
from model.trabalho import Trabalho
from controller.controller_trabalho import controller_trabalho
from conexion.oracle_queries import OracleQueries
from reports.relatorios import Relatorio
from utils import config

relatorio = Relatorio()

class controller_avaliacao_aluno:
    def __init__(self):
        self.ctrl_aluno = controller_aluno()
        self.ctrl_prova = controller_prova()
        self.ctrl_trabalho = controller_trabalho()

    def inserir_prova(self):
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        oracle = OracleQueries()

        self.listar_provas(oracle, need_connect=True, opc=1)
        id_prova = int(input("Digite o ID da Prova: "))
        prova = self.valida_prova(oracle, id_prova)
        if prova is None:
            return None

        turmas = self.listar_turmas(oracle, need_connect=True)
        if len(turmas.turma.values) == 0:
            return None
        
        turma = input("Informe a para a qual a avaliação foi aplicada: ")
        df_alunos_turma = self.recuperar_alunos_turma(oracle, need_connect=True, turma=turma)
        print(len(df_alunos_turma.id_aluno.values))
        for index in range(0, len(df_alunos_turma.id_aluno.values)):
            nota_aluno = int(input(f"Informe a nota do aluno {df_alunos_turma.nome.values[index]}: "))
            
            cursor = oracle.connect()
            output_value = cursor.var(int)
            data = dict(codigo=output_value, id_aluno=int(df_alunos_turma.id_aluno.values[index]), id_prova=id_prova, id_trabalho=0, nota_avaliacao=nota_aluno, nome_aluno= df_alunos_turma.nome.values[index])
            cursor.execute("""
            begin
                           
                :codigo := AVALIACAO_ALUNO_ID_AVALIACAO_ALUNO_SEQ.NEXTVAL;
                           
                INSERT INTO AVALIACAO_ALUNO VALUES(:codigo, :id_aluno, :id_prova, :id_trabalho, :nota_avaliacao, :nome_aluno);
                           
            end;
            """, data)
            oracle.conn.commit()

            config.clear_console()
            self.recuperar_av_alunoProva(oracle, need_connect=True, prova=id_prova)
            print("")
    
    def inserir_trabalho(self):
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        oracle = OracleQueries()

        self.listar_trabalhos(oracle, need_connect=True, opc=1)
        id_trabalho = int(input("Digite o ID do Trabalho: "))
        trabalho = self.valida_trabalho(oracle, id_trabalho)
        if trabalho is None:
            return None

        turmas = self.listar_turmas(oracle, need_connect=True)
        if len(turmas.turma.values) == 0:
            return None
        
        turma = input("Informe a turma para a qual o trabalho foi aplicado: ")
        df_alunos_turma = self.recuperar_alunos_turma(oracle, need_connect=True, turma=turma)
        for index in range(0, len(df_alunos_turma.id_aluno.values)):
            nota_aluno = float(input(f"Informe a nota do aluno {df_alunos_turma.nome.values[index]}: "))
            
            cursor = oracle.connect()
            output_value = cursor.var(int)

            data = dict(codigo=output_value, id_aluno=int(df_alunos_turma.id_aluno.values[index]), id_prova=0, id_trabalho=id_trabalho, nota_avaliacao=nota_aluno, nome_aluno=df_alunos_turma.nome.values[index])
            cursor.execute("""
            begin
                :codigo := AVALIACAO_ALUNO_ID_AVALIACAO_ALUNO_SEQ.NEXTVAL;
                insert into avaliacao_aluno values(:codigo, :id_aluno, :id_prova, :id_trabalho, :nota_avaliacao, :nome_aluno);
            end;
            """, data)
            oracle.conn.commit()

            config.clear_console()
            self.recuperar_av_alunoTrabalho(oracle, need_connect=True, trabalho=id_trabalho)
            print("")



    def alterar_prova(self):
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        oracle = OracleQueries(can_write=True)

        self.listar_provas(oracle, need_connect=True)
        id_prova = int(input("Digite o ID da Prova: "))
        prova = self.valida_prova(oracle, id_prova)
        if prova is None:
            print("Prova prova não existe!")
            return None
        
        config.clear_console(1)
        df_av_alunoProva = self.recuperar_av_alunoProva(oracle, need_connect=True, prova=id_prova)
        avAlunoAlterar = int(input("Digite o código da avliação(coluna Avaliacão) que deseja alterar: "))
        if avAlunoAlterar in df_av_alunoProva.avaliacao.values:
            nova_nota = float(input("Digite a nova nota: "))
            oracle.write(f'update avaliacao_aluno set nota_avaliacao = {nova_nota} where id_avaliacao_aluno = {avAlunoAlterar}')
            df_av_aluno = oracle.sqlToDataFrame(f'select id_avaliacao_aluno, id_aluno, id_prova, nota_avaliacao, nomealuno from avaliacao_aluno where id_avaliacao_aluno = {avAlunoAlterar}')
            editav_aluno = avaliacaoaluno(df_av_aluno.id_avaliacao_aluno.values[0], df_av_aluno.id_aluno.values[0],df_av_aluno.id_prova.values[0], 0, df_av_aluno.nota_avaliacao.values[0], df_av_aluno.nomealuno.values[0])
            print(editav_aluno.to_string_prova())
            return editav_aluno
        
        else:
            print("Esta avaliação de aluno não existe")


    def alterar_trabalho(self):
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''

        oracle = OracleQueries(can_write=True)

        self.listar_trabalhos(oracle, need_connect=True)
        id_trabalho = int(input("Digite o ID do Trabalho: "))
        trabalho = self.valida_trabalho(oracle, id_trabalho)
        if trabalho is None:
            print("Trabalho não Existe!")
            return None
        
        config.clear_console(1)
        df_av_alunoTrabalho = self.recuperar_av_alunoTrabalho(oracle, need_connect=True, trabalho=id_trabalho)
        avAlunoAlterar = int(input("Digite o código da avliação(coluna Avaliacão) que deseja alterar: "))
        if avAlunoAlterar in df_av_alunoTrabalho.avaliacao.values:
            nova_nota = float(input("Digite a nova nota: "))
            oracle.write(f'update avaliacao_aluno set nota_avaliacao = {nova_nota} where id_avaliacao_aluno = {avAlunoAlterar}')
            df_av_aluno = oracle.sqlToDataFrame(f'select id_avaliacao_aluno, id_aluno, id_trabalho, nota_avaliacao, nomealuno from avaliacao_aluno where id_avaliacao_aluno = {avAlunoAlterar}')
            editav_aluno = avaliacaoaluno(df_av_aluno.id_avaliacao_aluno.values[0], df_av_aluno.id_aluno.values[0], 0, df_av_aluno.id_trabalho.values[0], df_av_aluno.nota_avaliacao.values[0], df_av_aluno.nomealuno.values[0])
            print(editav_aluno.to_string_trabalho())
            return editav_aluno
        
        else:
            print("Esta avaliação de aluno não existe")



    def excluir_prova(self):
        oracle = OracleQueries(can_write=True)

        self.listar_provas(oracle, need_connect=True)
        id_prova = int(input("Digite o ID da Prova: "))
        prova = self.valida_prova(oracle, id_prova)
        if prova is None:
            print("Esta prova não não existe para ser excluida")
            return None
        
        oracle.write(f'delete from avaliacao_aluno where id_prova = {id_prova}')
        print(f'Avaliações de aluno removidas para a prova {id_prova}')
        return None

    def excluir_trabalho(self):
        oracle = OracleQueries(can_write=True)

        self.listar_trabalhos(oracle, need_connect=True)
        id_trabalho = int(input("Digite o ID do trabalho: "))
        trabalho = self.valida_trabalho(oracle, id_trabalho)
        if trabalho is None:
            print("Este não trabalho não existe para ser excluido")
            return None
        
        oracle.write(f'delete from avaliacao_aluno where id_trabalho = {id_trabalho}')
        print(f'Avaliações de aluno removidas para o trabalho {id_trabalho}')
        return None    




    def listar_provas(self, oracle:OracleQueries, need_connect:bool=False, opc=0):
        if opc == 1:
            query = """
                select id_prova as Prova,
                       to_char(date_aplicacao, 'DD-MM-YYYY') as data_aplicacao
                    from prova
                    where id_prova != 0
                    and not exists(select null
                                        from avaliacao_aluno
                                        where avaliacao_aluno.id_prova = prova.id_prova )
            """ 
        else:
            query = """
                select id_prova as Prova,
                       to_char(date_aplicacao, 'DD-MM-YYYY') as data_aplicacao
                    from prova
                    where id_prova != 0
                    and exists(select null
                                        from avaliacao_aluno
                                        where avaliacao_aluno.id_prova = prova.id_prova )
            """ 
        if need_connect: 
            oracle.connect()
        
        print(oracle.sqlToDataFrame(query))

    def listar_trabalhos(self, oracle:OracleQueries, need_connect:bool=False, opc=0):
        if opc == 1: 
            query = """
                select id_trabalho as Trabalho,
                       to_char(date_entrega, 'DD-MM-YYYY') as data_entrega
                    from trabalho
                    where id_trabalho != 0
                    and not exists(select null
                                        from avaliacao_aluno
                                        where avaliacao_aluno.id_trabalho = trabalho.id_trabalho )
            """
        else:
            query = """
                select id_trabalho as Trabalho,
                       to_char(date_entrega, 'DD-MM-YYYY') as data_entrega
                    from trabalho
                    where id_trabalho != 0
                    and exists(select null
                                        from avaliacao_aluno
                                        where avaliacao_aluno.id_trabalho = trabalho.id_trabalho )
            """ 
        if need_connect: 
            oracle.connect()
        
        print(oracle.sqlToDataFrame(query))



    def listar_turmas(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select turma
                    from aluno
                    group by turma
        """ 
        if need_connect: 
            oracle.connect()
        
        df_turmas = oracle.sqlToDataFrame(query)
        print(df_turmas)
        return df_turmas


    def recuperar_alunos_turma(self, oracle:OracleQueries, need_connect:bool=False, turma=""):
        query = f"""
                select id_aluno
                    , nome 
                    from aluno
                    where turma = '{turma}'
        """ 
        if need_connect: 
            oracle.connect()
        
        df_alunos = oracle.sqlToDataFrame(query)
        return df_alunos
    

    
    def recuperar_av_alunoProva(self, oracle:OracleQueries, need_connect:bool=False, prova=0):
        query = f"""
                select id_avaliacao_aluno as avaliacao,
                       id_prova as prova,
                       nomealuno as nome,
                       nota_avaliacao as nota
                    from avaliacao_aluno
                    where id_prova = '{prova}'
        """ 
        if need_connect: 
            oracle.connect()
        df_av_alunoProva = oracle.sqlToDataFrame(query)
        print(df_av_alunoProva)
        return df_av_alunoProva


    def recuperar_av_alunoTrabalho(self, oracle:OracleQueries, need_connect:bool=False, trabalho=0):
        query = f"""
                select id_avaliacao_aluno as avaliacao,
                       id_trabalho as trabalho,
                       nomealuno as nome,
                       nota_avaliacao as nota
                    from avaliacao_aluno
                    where id_trabalho = '{trabalho}'
        """ 
        if need_connect: 
            oracle.connect()
        df_av_alunoTrabalho = oracle.sqlToDataFrame(query)
        print(df_av_alunoTrabalho)
        return df_av_alunoTrabalho



    def valida_prova(self, oracle:OracleQueries, id_prova:int=None) -> Prova:
        if self.ctrl_prova.verifica_existencia_prova(oracle, id_prova):
            print(f"Não existe na base, prova cadastrada com o {id_prova}")
            return None
        else:
            oracle.connect()
            df_prova = oracle.sqlToDataFrame(f"select id_prova, quant_questao, to_char(date_aplicacao, 'dd-mm-yyyy') as date_aplicacao from prova where id_prova = {id_prova}")
            prova = Prova(df_prova.id_prova.values[0], df_prova.quant_questao.values[0], df_prova.date_aplicacao[0] )
            return prova
        
    def valida_trabalho(self, oracle:OracleQueries, id_trabalho:int=None) -> Trabalho:
        if self.ctrl_trabalho.verifica_existencia_trabalho(oracle, id_trabalho):
            print(f"Não existe na base, trabalho cadastrada com o {id_trabalho}")
            return None
        else:
            oracle.connect()
            df_trabalho = oracle.sqlToDataFrame(f"select id_trabalho, qtdcriteriosavaliados, to_char(date_entrega, 'DD-MM-YYYY') as data_entrega from trabalho where id_trabalho = {id_trabalho}")
            trabalho = Trabalho(df_trabalho.id_trabalho.values[0],df_trabalho.qtdcriteriosavaliados.values[0], df_trabalho.data_entrega.values[0] )
            return trabalho
        