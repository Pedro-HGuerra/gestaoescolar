select (ID_TRABALHO) "Código do Trabalho"
       , (QTDCRITERIOSAVALIADOS) "Quantidade de Critérios Avaliados"
       , to_char(DATE_ENTREGA, 'dd-mm-yyyy') as "Data de Entrega"
from TRABALHO
where ID_TRABALHO != 0
order by QTDCRITERIOSAVALIADOS