SELECT (ID_PROVA) "Código da prova", avg(NOTA_AVALIACAO) AS media
    FROM AVALIACAO_ALUNO
    GROUP BY ID_PROVA
    ORDER BY media
 