from datetime import date

class Prova:
    def __init__(self, 
                 id_prova:int=None, 
                 quant_Questao:int=None, 
                 date_Aplicacao:date=None 
                ):
        self.set_id_prova(id_prova)
        self.set_quant_Questao(quant_Questao)
        self.set_date_Aplicacao(date_Aplicacao)

    def set_id_prova(self, id_prova:int):
        self.id_prova = id_prova
        
    def set_quant_Questao(self, quant_Questao:int):
        self.quant_Questao = quant_Questao
    
    def set_date_Aplicacao(self, date_Aplicacao:date):
        self.date_Aplicacao = date_Aplicacao 
    
    def get_id_prova(self) -> int:
        return self.id_prova
    
    def get_quant_Questao(self) -> int:
        return self.quant_Questao
    
    def get_date_Aplicacao(self) -> date:
        return self.date_Aplicacao
    
    def to_string(self) -> str:
        return f"Código: {self.get_id_prova()} | Quantidade de Questões: {self.get_quant_Questao()} | Data da prova: {self.get_date_Aplicacao()}"
