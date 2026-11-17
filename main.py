import tkinter as tk
from pathlib import Path
from tkinter import ttk

from database import Database
from interface import App
from regras import ServicoSolicitacoes

CAMINHO_BANCO = Path(__file__).with_name("solicitacoes.db")

def main() -> None:
    banco = Database(CAMINHO_BANCO)
    try:
        janela = tk.Tk()
        ttk.Style(janela).configure("Treeview", rowheight=26)
        App(janela, ServicoSolicitacoes(banco))
        janela.mainloop()
    finally:
        banco.fechar()


if __name__ == "__main__":
    main()