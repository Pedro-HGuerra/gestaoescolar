from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):

    #------------------------------------------------------------------------------------
        #Abrir o arquivo com consulta e associa a um atributo da classe (Gestão de notas)
        
        with open("sql/relatorio_aluno.sql") as f:
            self.query_relatorio_aluno=f.read()

        with open("sql/relatorio_prova.sql") as f:
            self.query_relatorio_prova=f.read()
        
        with open("sql/relatorio_trabalho.sql") as f:
            self.query_relatorio_trabalho=f.read()
        
        with open("sql/relatorio_avaliacaoAluno.sql") as f:
            self.query_relatorio_avaliacaoAluno = f.read()

        with open("sql/relatorio_notaAluno_trabalho.sql") as f:
            self.query_relatorio_notaAluno_trabalho = f.read()
    #-------------------------------------------------------------------------------
    #Relatorio Aluno (Gestão de notas)
    def get_relatorio_aluno(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_aluno))
        input("Pressione ENTER para sair do Relatório de Aluno.")

    def get_relatorio_prova(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_prova))
        input("Pressione ENTER para sair do Relatório de Prova.") 

    def get_relatorio_trabalho(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_trabalho))
        input("Pressione ENTER para sair do Relatório de Trabalho.")

    def get_relatorio_avaliacaoAluno(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_avaliacaoAluno))
        input("Pressione ENTER para sair do Relatório de Média por prova.")
    
    def get_relatorio_notaAlunoTrabalho(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorio_notaAluno_trabalho))
        input("Pressione ENTER para sair do Relatório de Notas de Aluno por Trabalho.") 

    #---------------------------------------------------------------------------------