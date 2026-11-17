import sqlite3
from pathlib import Path

from solicitacao import Solicitacao

class Database:
    def __init__(self, caminho: str | Path) -> None:
        self.conexao = sqlite3.connect(caminho)
        self.cursor = self.conexao.cursor()
        self.criar_tabela()


    def criar_tabela(self) -> None:
        with self.conexao:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS solicitacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setor TEXT NOT NULL,
                    material TEXT NOT NULL,
                    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
                    prioridade TEXT NOT NULL,
                    status TEXT NOT NULL,
                    data_hora TEXT NOT NULL
                )
            """)
            self.conexao.commit()

    def inserir(self, setor: str, material: str, quantidade: str,
                prioridade: str, status: str, data_hora: str) -> int:
        with self.conexao:
            self.cursor.execute(
                "INSERT INTO solicitacoes (setor, material, quantidade, prioridade, status, data_hora) VALUES (?,?,?,?,?,?)",
                (setor, material, quantidade, prioridade, status, data_hora) 
            )   

            self.conexao.commit()
            return self.cursor.lastrowid

    def buscar_por_id(self, solicitacao_id: int) -> Solicitacao | None:
        with self.conexao:
            linha = self.cursor.execute("""
                SELECT id, setor, material, quantidade, prioridade, status, data_hora FROM solicitacoes WHERE id = ?
            """, (solicitacao_id,)).fetchone()

            return Solicitacao(*linha) if linha else None

    def atualizar_status(self, solicitacao_id: int, novo_status: str) -> None:
        with self.conexao:
            self.cursor.execute("""
                UPDATE solicitacoes SET status = ? WHERE id = ?
            """, (novo_status, solicitacao_id,))

            self.conexao.commit()

    def listar(self, texto: str = "", status: str = "") -> list[Solicitacao]:
        with self.conexao:
            sql = ("SELECT id, setor, material, quantidade, prioridade, status, data_hora FROM solicitacoes WHERE 1 = 1")

            parametros: list = []
            if texto:
                sql += " AND (setor LIKE ? OR material LIKE ?)"
                parametros += [f"%{texto}%", f"%{texto}%"]
            if status:
                sql += " AND status = ?"
                parametros.append(status)

            sql += " ORDER BY id"
            return [Solicitacao(*linha) for linha in self.cursor.execute(sql, parametros)]

    def fechar(self) -> None:
        self.conexao.close()