MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Remover Registros
0 - Sair
"""

MENU_RELATORIOS = """Relatórios
1 - Relatório de Alunos
2 - Relatório de Provas
3 - Relatório de Trabalhos
4 - Relatório de Média dos Alunos por Prova
5 - Relatório de Nota dos Alunos por Trabalho
0 - Voltar
"""

MENU_ENTIDADES = """Entidades
1 - Aluno
2 - Prova
3 - Trabalho
4 - Avaliação
0 - Voltar
"""

MENU_AVALIACAO_ALUNO = """
1 - Prova
2 - Trabalho
0 - Voltar
""" 

"""def continuaCadastroAvAluno(continuaCadAv):
     if continuaCadAv == '1':
         return True
     elif continuaCadAv =='N':
         return False
     else:
         print("Valor inválido. Digite um valor de [0-2]")
         return False"""

def continuaProcedimento(continua):
    if continua == 'S':
         return True
    elif continua =='N':
         return False
    else:
         print("Valor inválido. Digite S = SIM OU N = NÃO")
         return False

# Consulta de contagem de registros por tabela
QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'

def clear_console(wait_time:int=3):
    '''
       Esse método limpa a tela após alguns segundos
       wait_time: argumento de entrada que indica o tempo de espera
    '''
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")