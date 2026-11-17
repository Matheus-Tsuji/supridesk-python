import csv
from datetime import datetime
from pathlib import Path

from database import Database

PENDENTE = "Pendente"
EM_ATENDIMENTO = "Em atendimento"
ATENDIDA = "Atendida"
STATUS = [PENDENTE, EM_ATENDIMENTO, ATENDIDA]
PRIORIDADES = ["Normal", "Alta"]

TRANSICOES = {
    PENDENTE: EM_ATENDIMENTO,
    EM_ATENDIMENTO: ATENDIDA
}

CABECALHO_CSV = ["ID", "Setor", "Material", "Quantidade", "Prioridade", "Status", "Data/Hora"]

class RegraError(ValueError):
    """Erro de regra de negócio (mensagem pronta para mostrar ao usuário)."""

def validar_cadastro(setor: str, material: str, quantidade: str, prioridade: str) -> tuple[str, str, int, str]:
    setor = setor.strip()
    material = material.strip()
    quantidade = str(quantidade).strip()

    if not setor or not material or not quantidade:
        raise RegraError("Preencha Setor, Material e Quantidade.")
    if not quantidade.isdigit() or int(quantidade) <= 0:
        raise RegraError("A quantidade deve ser um número inteiro positivo.")
    if prioridade not in PRIORIDADES:
        raise RegraError("Prioridade deve ser Normal ou Alta.")

    return setor, material, int(quantidade), prioridade

def validar_transicao(status_atual: str, novo_status: str) -> None:
    if TRANSICOES.get(status_atual) != novo_status:
        raise RegraError(f"Transição inválida: '{status_atual}' -> '{novo_status}'.")

class ServicoSolicitacoes:
    def __init__(self, db: Database) -> None:
        self.db = db

    def cadastrar(self, setor: str, material: str, quantidade: str, prioridade: str) -> int:
        setor, material, quantidade, prioridade = validar_cadastro(setor, material, quantidade, prioridade)
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return self.db.inserir(setor, material, quantidade, prioridade, PENDENTE, data_hora)

    def mudar_status(self, solicitacao_id: int, novo_status: str) -> None:
        solicitacao = self.db.buscar_por_id(solicitacao_id)
        if solicitacao is None:
            raise RegraError("Solicitação não encontrada.")
        validar_transicao(solicitacao.status, novo_status)
        self.db.atualizar_status(solicitacao_id, novo_status)

    def iniciar_atendimento(self, solicitacao_id: int) -> None:
        self.mudar_status(solicitacao_id, EM_ATENDIMENTO)

    def concluir_atendimento(self, solicitacao_id: int) -> None:
        self.mudar_status(solicitacao_id, ATENDIDA)

    def listar(self, texto: str = "", status: str = "Todos"):
        return self.db.listar(texto.strip(), "" if status == "Todos" else status)

    def exportar_csv(self, caminho: str | Path) -> int:
        solicitacoes = self.db.listar()

        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(CABECALHO_CSV)

            for s in solicitacoes:
                escritor.writerow(s.como_tupla())

        return len(solicitacoes)