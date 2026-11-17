import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from regras import PRIORIDADES, STATUS, RegraError, ServicoSolicitacoes


class App(ttk.Frame):
    def __init__(self, raiz: tk.Tk, servico: ServicoSolicitacoes) -> None:
        super().__init__(raiz, padding=16)
        self.servico = servico
        self.pack(fill="both", expand=True)

        raiz.title("SupriDesk")
        raiz.geometry("950x560")
        raiz.minsize(800, 400)


        # Formulário
        formulario = ttk.LabelFrame(self, text="Nova Solicitação", padding=10)
        formulario.pack(fill="x")
        self.setor = ttk.Entry(formulario, width=20)
        self.material = ttk.Entry(formulario, width=24)
        self.quantidade = ttk.Entry(formulario, width=8)
        self.prioridade = ttk.Combobox(formulario, values=PRIORIDADES, state="readonly", width=8)
        self.prioridade.set("Normal")

        campos = [("Setor", self.setor), ("Material", self.material),
                  ("Quantidade", self.quantidade), ("Prioridade", self.prioridade)]
        for i, (texto, widget) in enumerate(campos):
            ttk.Label(formulario, text=texto + ":").grid(row=0, column=i * 2, padx=(0, 4))
            widget.grid(row=0, column=i * 2 + 1, padx=(0, 12))
        ttk.Button(formulario, text="Cadastrar", command=self.cadastrar).grid(row=0, column=8)


        # Busca
        busca = ttk.Frame(self)
        busca.pack(fill="x", pady=10)
        ttk.Label(busca, text="Buscar (setor/material):").pack(side="left")
        self.busca = ttk.Entry(busca, width=24)
        self.busca.pack(side="left", padx=8)
        self.busca.bind("<Return>", lambda _evento: self.atualizar_tabela())
        ttk.Label(busca, text="Status:").pack(side="left")
        self.filtro_status = ttk.Combobox(busca, values=["Todos"] + STATUS, state="readonly", width=15)
        self.filtro_status.set("Todos")
        self.filtro_status.pack(side="left", padx=8)
        ttk.Button(busca, text="Filtrar", command=self.atualizar_tabela).pack(side="left")
        ttk.Button(busca, text="Limpar", command=self.limpar_filtros).pack(side="left", padx=8)


        # Ações
        acoes = ttk.Frame(self)
        acoes.pack(fill="x", pady=(0, 10))
        ttk.Button(acoes, text="Iniciar Atendimento", command=self.iniciar_atendimento).pack(side="left", padx=(0, 8))
        ttk.Button(acoes, text="Concluir", command=self.concluir_atendimento).pack(side="left", padx=(0, 8))
        ttk.Button(acoes, text="Exportar CSV", command=self.exportar_csv).pack(side="left")

        # Tabela
        area = ttk.Frame(self)
        area.pack(fill="both", expand=True)
        colunas = ("id", "setor", "material", "quantidade", "prioridade", "status", "data_hora")
        self.tree = ttk.Treeview(area, columns=colunas, show="headings", selectmode="browse")
        for coluna, titulo, largura in (("id", "ID", 50), ("setor", "Setor", 130), ("material", "Material", 180),
                                        ("quantidade", "Quantidade", 80), ("prioridade", "Prioridade", 90),
                                        ("status", "Status", 120), ("data_hora", "Data/Hora", 150)):
            self.tree.heading(coluna, text=titulo)
            self.tree.column(coluna, width=largura, anchor="w")
        self.tree.column("id", stretch=False)
        self.tree.pack(side="left", fill="both", expand=True)
        barra = ttk.Scrollbar(area, orient="vertical", command=self.tree.yview)
        barra.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=barra.set)

        self.atualizar_tabela()
        self.setor.focus_set()


    # --- Tabela ---
    def atualizar_tabela(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            solicitacoes = self.servico.listar(self.busca.get(), self.filtro_status.get())
        except sqlite3.Error as erro:
            messagebox.showerror("Erro de banco", str(erro), parent=self)
            return

        for s in solicitacoes:
            self.tree.insert("", "end", iid=str(s.id), values=s.como_tupla())

    def limpar_filtros(self) -> None:
        self.busca.delete(0, "end")
        self.filtro_status.set("Todos")
        self.atualizar_tabela()

    def selecionado(self) -> int | None:
        itens = self.tree.selection()

        if not itens:
            messagebox.showwarning("Seleção", "Selecione uma solicitação na tabela.", parent=self)
            return None
        return int(itens[0])


    # --- Ações --- 
    def cadastrar(self) -> None:
        try:
            novo_id = self.servico.cadastrar(
                self.setor.get(), self.material.get(), self.quantidade.get(), self.prioridade.get()
            )

        except RegraError as erro:
            messagebox.showwarning("Cadastro recusado", str(erro), parent=self)
            return
        except sqlite3.Error as erro:
            messagebox.showerror("Erro de banco", str(erro), parent=self)
            return

        self.limpar_formulario()
        self.atualizar_tabela()
        messagebox.showinfo("Cadastro", f"Solicitação #{novo_id} cadastrada como Pendente.", parent=self)

    def limpar_formulario(self) -> None:
        for campo in (self.setor, self.material, self.quantidade):
            campo.delete(0, "end")
        self.prioridade.set("Normal")
        self.setor.focus_set()

    def _mudar_status(self, acao) -> None:
        solicitacao_id = self.selecionado()
        if solicitacao_id is None:
            return

        try:
            acao(solicitacao_id)
        except RegraError as erro:
            messagebox.showwarning("Ação bloqueada", str(erro), parent=self)
            return
        except sqlite3.Error as erro:
            messagebox.showerror("Erro de banco", str(erro), parent=self)
            return

        self.atualizar_tabela()
        if self.tree.exists(str(solicitacao_id)):
            self.tree.selection_set(str(solicitacao_id))

    def iniciar_atendimento(self) -> None:
        self._mudar_status(self.servico.iniciar_atendimento)

    def concluir_atendimento(self) -> None:
        self._mudar_status(self.servico.concluir_atendimento)

    def exportar_csv(self) -> None:
        caminho = filedialog.asksaveasfilename(
            parent=self, title="Exportar Histórico", defaultextension=".csv",
            initialfile="historico_solicitacoes.csv", filetypes=[("CSV", "*.csv")]
        )
        if not caminho:
            return

        try:
            total = self.servico.exportar_csv(caminho)
        except OSError as erro:
            messagebox.showerror("Erro ao exportar", str(erro), parent=self)
            return

        messagebox.showinfo("Exportação", f"{total} registro(s) exportado(s) para: \n{caminho}", parent=self)