from datetime import date

class Trabalho:
    def __init__(self, 
                 id_trabalho:int=None, 
                 qtdCriteriosAvaliados:int=None, 
                 date_entrega:date=None 
                ):
        self.set_id_trabalho(id_trabalho)
        self.set_qtdCriteriosAvaliados(qtdCriteriosAvaliados)
        self.set_date_entrega(date_entrega)

    def set_id_trabalho(self, id_trabalho:int):
        self.id_trabalho = id_trabalho
    
    def set_qtdCriteriosAvaliados(self, qtdCriteriosAvaliados:int):
        self.qtdCriteriosAvaliados = qtdCriteriosAvaliados
    
    def set_date_entrega(self, date_entrega:date):
        self.date_entrega = date_entrega 
    
    def get_id_trabalho(self) -> int:
        return self.id_trabalho
    
    def get_qtdCriteriosAvaliados(self) -> int:
        return self.qtdCriteriosAvaliados
    
    def get_date_entrega(self) -> date:
        return self.date_entrega
    
    def to_string(self) -> str:
        return f"Código: {self.get_id_trabalho()} | Quantidade de Critérios Avaliados: {self.get_qtdCriteriosAvaliados()} | Data de Entrega: {self.get_date_entrega()}"
