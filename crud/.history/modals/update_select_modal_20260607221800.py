from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Input, Select
from textual.containers import Horizontal

import entities
import operacoes

from modals.formulario_modal import FormularioModal


class UpdateSelectView(ModalScreen):
    DEFAULT_CSS = """
    UpdateSelectView { background: black; padding: 1; }
    #area-filtro, #area-update { layout: horizontal; height: auto; margin-bottom: 1; }
    #select-coluna, #input-filtro, #input-update-id {
        margin-right: 1;
        background: #2a2a2a;
        color: #dcdcdc;
    }
    #select-coluna { width: 30%; }
    #input-filtro { width: 70%; }
    #input-update-id { width: 60%; }
    #btn-update-confirmar { width: 40%; }
    """

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

        with Horizontal(id="area-update"):
            yield Input(placeholder="Digite o ID para ATUALIZAR...", id="input-update-id")
            yield Button("Atualizar Selecionado", id="btn-update-confirmar", variant="primary")

        yield DataTable(id="minha-lista", cursor_type="row")

    def on_mount(self) -> None:
        try:
            if not entities.existe_tabela(self.tabela):
                raise ValueError(f"Tabela não cadastrada em entities.py: {self.tabela}")

            self.colunas = list(entities.colunas(self.tabela))
            self._montar_select_filtro()
            self._montar_tabela()
            self.carregar_dados()

        except Exception as erro:
            self.app.notify(f"Erro ao carregar tela de atualização: {erro}", severity="error")

    def _montar_select_filtro(self) -> None:
        opcoes_select = [
            (coluna, str(indice))
            for indice, coluna in enumerate(self.colunas)
        ]

        select = self.query_one("#select-coluna", Select)
        select.set_options(opcoes_select)

    def _montar_tabela(self) -> None:
        tabela_widget = self.query_one("#minha-lista", DataTable)
        tabela_widget.clear(columns=True)
        tabela_widget.add_columns(*self.colunas)

    def carregar_dados(self) -> None:
        tabela_widget = self.query_one("#minha-lista", DataTable)
        tabela_widget.clear()

        self.dados_originais = operacoes.select(
            self.tabela,
            order_by=entities.chave_primaria(self.tabela)
        )

        if self.dados_originais:
            tabela_widget.add_rows(self._formatar_linhas(self.dados_originais))

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

    @on(DataTable.RowSelected, "#minha-lista")
    def linha_selecionada(self, event: DataTable.RowSelected) -> None:
        tabela_widget = self.query_one("#minha-lista", DataTable)
        dados_linha = tabela_widget.get_row(event.row_key)

        try:
            id_selecionado = int(dados_linha[0])
            self.chamar_formulario(id_selecionado)

        except Exception as erro:
            self.app.notify(f"Erro ao selecionar registro: {erro}", severity="error")

    @on(Button.Pressed, "#btn-update-confirmar")
    def botao_confirmar(self, event: Button.Pressed) -> None:
        input_id = self.query_one("#input-update-id", Input)
        valor_id = input_id.value.strip()

        if not valor_id:
            self.app.notify("Informe um ID para atualizar.", severity="error")
            return

        if not valor_id.isdigit():
            input_id.value = ""
            self.app.notify("ID inválido. Digite apenas números.", severity="error")
            return

        self.chamar_formulario(int(valor_id))

    def chamar_formulario(self, id_registro: int) -> None:
        nome_coluna_pk = entities.chave_primaria(self.tabela)

        try:
            registros = operacoes.select(
                self.tabela,
                where={nome_coluna_pk: id_registro}
            )

            if not registros:
                self.app.notify("Registro não encontrado no banco!", severity="error")
                return

            linha_banco = registros[0]

            self.app.pop_screen()
            self.app.push_screen(
                FormularioModal(
                    self.tabela,
                    "atualizar",
                    entities.TABELAS[self.tabela],
                    preenchimento=linha_banco
                )
            )

        except Exception as erro:
            self.app.notify(f"Erro ao abrir formulário: {erro}", severity="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-voltar":
            self.app.pop_screen()