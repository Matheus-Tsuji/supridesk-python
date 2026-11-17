from dataclasses import dataclass

@dataclass
class Solicitacao:
    id: int
    setor: str
    material: str
    quantidade: int
    prioridade: str
    status: str
    data_hora: str

    def como_tupla(self) -> tuple:
        return (self.id, self.setor, self.material, self.quantidade, self.prioridade, self.status, self.data_hora)