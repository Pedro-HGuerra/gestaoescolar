from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_aluno = config.QUERY_COUNT.format(tabela="aluno")
        self.qry_total_prova = config.QUERY_COUNT.format(tabela="prova")
        self.qry_total_trabalho = config.QUERY_COUNT.format(tabela="trabalho")
        self.qry_total_avaliacao_aluno = config.QUERY_COUNT.format(tabela="avaliacao_aluno")
        # Consultas de contagem de registros - fim

        # Nome(s) do(s) criador(es)
        self.created_by = """Bernardo N.                             #
        #              Erick C.                                #
        #              Henrique A.                             # 
        #              Mateus P.                               #
        #              Pedro B.                                #
        #              Pedro G.                                #"""
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_total_aluno(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_aluno)["total_aluno"].values[0]

    def get_total_prova(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_prova)["total_prova"].values[0]
    
    def get_total_trabalho(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_trabalho)["total_trabalho"].values[0]

    def get_total_avaliacao_aluno(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_avaliacao_aluno)["total_avaliacao_aluno"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                    GESTÃO ESCOLAR                    #  
        #                                                      #   
        #  TOTAL DE REGISTROS:                                 #   
        #      1 - ALUNOS:         {str(self.get_total_aluno()).rjust(5)}                       #
        #      2 - PROVAS:         {str(self.get_total_prova()).rjust(5)}                       #
        #      3 - TRABALHOS:      {str(self.get_total_trabalho()).rjust(5)}                       #
        #      4 - AVALIAÇÕES:     {str(self.get_total_avaliacao_aluno()).rjust(5)}                       #
        #                                                      #
        #  CRIADO POR: {self.created_by}                       
        #                                                      #
        #  PROFESSOR:  {self.professor}               # 
        #                                                      #
        #  DISCIPLINA: {self.disciplina}                          #
        #              {self.semestre}                                  #
        ########################################################
        """