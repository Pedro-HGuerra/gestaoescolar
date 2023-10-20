    select (ID_PROVA) "Código da Prova"
        , (QUANT_QUESTAO) "Quantidade de Questões"
        , to_char(DATE_APLICACAO, 'dd-mm-yyyy') as "Data de Aplicação"
    from PROVA
    where ID_PROVA != 0
    order by DATE_APLICACAO