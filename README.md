# SupriDesk

Trabalho individual da disciplina de Desenvolvimento Rápido de Aplicações em Python (2026.2).

O SupriDesk é um sistema desktop simples para registrar pedidos internos de materiais (cabos, periféricos, papel etc.) e acompanhar o atendimento de cada um.

## Como rodar

Usei Python 3.13, mas deve funcionar a partir do 3.10. Não precisa instalar nada além do Python, porque só uso bibliotecas que já vêm com ele (tkinter, sqlite3 e csv).

```
python main.py
```

Na primeira vez o programa cria sozinho o arquivo `solicitacoes.db`, onde ficam salvos os pedidos.

## O que o sistema faz

- Cadastra pedidos com setor, material, quantidade e prioridade (Normal ou Alta). O ID e a data/hora são gerados automaticamente e todo pedido começa como Pendente.
- Não deixa cadastrar com campo vazio ou com quantidade que não seja um número inteiro maior que zero.
- O atendimento segue a ordem Pendente → Em atendimento → Atendida. Não dá para pular etapa nem concluir duas vezes.
- Dá para buscar por setor ou material, filtrar por status e limpar os filtros.
- Exporta o histórico para CSV.

## Organização do código

Separei o projeto em arquivos de acordo com a função de cada parte:

- `main.py`: abre o banco e inicia a janela
- `interface.py`: a tela em Tkinter (formulário, botões e tabela)
- `regras.py`: validações e controle de status, além da exportação CSV
- `database.py`: comandos SQL, todos com parâmetros `?`
- `solicitacao.py`: a classe que representa um pedido

## Testes que fiz

1. Cadastrei `TI / Mouse USB / 5 / Alta` e ele apareceu na tabela como Pendente.
2. Tentei cadastrar `Administrativo / Papel A4 / 0 / Normal` e o sistema recusou.
3. Passei um pedido de Pendente para Em atendimento e depois para Atendida. Quando tentei concluir de novo, apareceu a mensagem de bloqueio.
4. Fechei e abri o programa de novo e os pedidos continuavam lá.
5. Pesquisei por "Mouse" e por "TI", filtrei por Atendida e exportei o CSV.

## Referências

Documentação que consultei para fazer o projeto:

**Interface (Tkinter)**
- tkinter: https://docs.python.org/3/library/tkinter.html
- tkinter.ttk (Entry, Combobox, Treeview, Scrollbar): https://docs.python.org/3/library/tkinter.ttk.html
- tkinter.messagebox: https://docs.python.org/3/library/tkinter.messagebox.html
- tkinter.filedialog (janela de salvar o CSV): https://docs.python.org/3/library/dialog.html
- TkDocs, tutorial do Treeview: https://tkdocs.com/tutorial/tree.html

**Banco de dados (SQLite)**
- sqlite3: https://docs.python.org/3/library/sqlite3.html
- Consultas com `?` (placeholders): https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders
- CREATE TABLE no SQLite: https://www.sqlite.org/lang_createtable.html
- Operador LIKE (usado na busca): https://www.sqlite.org/lang_expr.html#like

**Outros módulos do Python**
- csv: https://docs.python.org/3/library/csv.html
- dataclasses: https://docs.python.org/3/library/dataclasses.html
- datetime (formato da data com strftime): https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
- pathlib: https://docs.python.org/3/library/pathlib.html

**Material da disciplina**
- Exemplos das aulas, principalmente a aula 13 (Treeview e cadastro com SQLite), que usei como base para a estrutura da tela e do banco.

## Vídeo do desenvolvimento
Timelapse de parte do desenvolvimento: https://youtu.be/QKuhGcaD_eY