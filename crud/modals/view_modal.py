from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Input, Select
from textual.containers import Horizontal

import entities
import operacoes


class View(ModalScreen):
    DEFAULT_CSS = """
    View { background: black; padding: 1; }
    #area-filtro { layout: horizontal; height: auto; margin-bottom: 1; }
    #select-coluna { width: 30%; margin-right: 1; }
    #input-filtro { width: 70%; }
    """

    TABELA_ENDERECO = "ENDERECO"
    TABELA_TELEFONE = "TELEFONE"

    def __init__(self, tabela: str, **kwargs):
        super().__init__(**kwargs)
        self.tabela = tabela.upper()
        self.dados_originais = []
        self.colunas = []

    def compose(self) -> ComposeResult:
        yield Button("Voltar", id="btn-voltar", variant="error")

        with Horizontal(id="area-filtro"):
            yield Select([], id="select-coluna", prompt="Filtrar por qual coluna?")
            yield Input(placeholder="Digite o valor para buscar...", id="input-filtro")

        yield DataTable(id="minha-lista")

    def on_mount(self) -> None:
        try:
            self._carregar_dados()
            self._montar_tabela()
            self._montar_select_filtro()

        except Exception as erro:
            self.app.notify(f"Erro ao carregar dados: {erro}", severity="error")

    def _carregar_dados(self) -> None:
        if self.tabela == self.TABELA_ENDERECO:
            self.colunas = list(entities.colunas("ENDERECO")) + [
                "Tipo Vínculo",
                "Proprietário"
            ]
            self.dados_originais = operacoes.select_enderecos_por_tipo("TODOS")

        elif self.tabela == self.TABELA_TELEFONE:
            self.colunas = [
                "Telefone",
                "Tipo Vínculo",
                "Proprietário"
            ]
            self.dados_originais = operacoes.select_telefones_geral()

        else:
            if not entities.existe_tabela(self.tabela):
                raise ValueError(f"Tabela não cadastrada em entities.py: {self.tabela}")

            self.colunas = list(entities.colunas(self.tabela))
            self.dados_originais = operacoes.select(
                self.tabela,
                order_by=entities.chave_primaria(self.tabela)
            )

    def _montar_tabela(self) -> None:
        tabela_widget = self.query_one("#minha-lista", DataTable)
        tabela_widget.clear(columns=True)
        tabela_widget.add_columns(*self.colunas)

        if self.dados_originais:
            tabela_widget.add_rows(self._formatar_linhas(self.dados_originais))

    def _montar_select_filtro(self) -> None:
        opcoes_select = [
            (coluna, str(indice))
            for indice, coluna in enumerate(self.colunas)
        ]

        select = self.query_one("#select-coluna", Select)
        select.set_options(opcoes_select)

    def _formatar_linhas(self, linhas):
        return [
            ["" if item is None else str(item) for item in linha]
            for linha in linhas
        ]

    @on(Input.Changed, "#input-filtro")
    @on(Select.Changed, "#select-coluna")
    def atualizar_filtro(self) -> None:
        input_widget = self.query_one("#input-filtro", Input)
        select_widget = self.query_one("#select-coluna", Select)
        tabela_widget = self.query_one("#minha-lista", DataTable)

        termo_busca = input_widget.value.strip().lower()
        indice_coluna = select_widget.value

        tabela_widget.clear()

        if not termo_busca or indice_coluna == Select.BLANK:
            tabela_widget.add_rows(self._formatar_linhas(self.dados_originais))
            return

        idx = int(indice_coluna)

        dados_filtrados = [
            linha for linha in self.dados_originais
            if termo_busca in str(linha[idx]).lower()
        ]

        tabela_widget.add_rows(self._formatar_linhas(dados_filtrados))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-voltar":
            self.app.pop_screen()