from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Input, Select
from textual.containers import Horizontal

import entities
import operacoes


class DeleteByIdView(ModalScreen):
    DEFAULT_CSS = """
    DeleteByIdView { background: black; padding: 1; }
    #area-filtro, #area-deletar { layout: horizontal; height: auto; margin-bottom: 1; }
    #select-coluna, #input-filtro, #input-deletar-id {
        margin-right: 1;
        background: #2a2a2a;
        color: #dcdcdc;
    }
    #select-coluna { width: 30%; }
    #input-filtro { width: 70%; }
    #input-deletar-id { width: 60%; }
    #btn-deletar-confirmar { width: 40%; }
    """

    TABELAS_DELECAO_SEGURA = {"CLIENTE", "VENDEDOR", "FORNECEDOR"}

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

        with Horizontal(id="area-deletar"):
            yield Input(placeholder="Digite o ID para DELETAR...", id="input-deletar-id")
            yield Button("Confirmar Deleção", id="btn-deletar-confirmar", variant="error")

        yield DataTable(id="minha-lista")

    def on_mount(self) -> None:
        try:
            if not entities.existe_tabela(self.tabela):
                raise ValueError(f"Tabela não cadastrada em entities.py: {self.tabela}")

            self.colunas = list(entities.colunas(self.tabela))
            self._montar_select_filtro()
            self._montar_tabela()
            self.carregar_dados()

        except Exception as erro:
            self.app.notify(f"Erro ao carregar tela de deleção: {erro}", severity="error")

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

    @on(Button.Pressed, "#btn-deletar-confirmar")
    def deletar_por_id(self, event: Button.Pressed) -> None:
        input_id = self.query_one("#input-deletar-id", Input)
        id_registro = input_id.value.strip()

        if not id_registro:
            self.app.notify("Informe um ID para deletar.", severity="error")
            return

        try:
            id_num = int(id_registro)
        except ValueError:
            input_id.value = ""
            self.app.notify("ID inválido. Digite apenas números.", severity="error")
            return

        nome_coluna_id = entities.chave_primaria(self.tabela)

        try:
            if self.tabela in self.TABELAS_DELECAO_SEGURA:
                resultado = operacoes.deletar_seguro(
                    self.tabela,
                    id_num,
                    nome_coluna_id
                )
                mensagem = self._formatar_resultado_delecao_segura(resultado)

            else:
                linhas = operacoes.delete(
                    self.tabela,
                    {nome_coluna_id: id_num}
                )
                mensagem = f"Deleção concluída. Registros afetados: {linhas}"

            self.app.notify(mensagem, severity="success")
            self.carregar_dados()
            input_id.value = ""

        except Exception as erro:
            self.app.notify(f"Erro ao deletar: {erro}", severity="error")

    def _formatar_resultado_delecao_segura(self, resultado: dict) -> str:
        return (
            f"Deleção segura concluída. "
            f"Registros deletados: {resultado.get('pessoas_deletadas', 0)}. "
            f"Endereços deletados: {resultado.get('enderecos_deletados', 0)}. "
            f"Referências reatribuídas: {resultado.get('referencias_reatribuidas', 0)}."
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-voltar":
            self.app.pop_screen()