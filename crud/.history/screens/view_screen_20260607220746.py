from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Button, Static

from modals.view_modal import View


class ViewScreen(Screen):
    MODO_INICIAL = "inicial"

    OPCOES_VISUALIZACAO = [
        ("Clientes", "CLIENTE"),
        ("Fornecedores", "FORNECEDOR"),
        ("Vendedores", "VENDEDOR"),
        ("Endereços", "ENDERECO"),
        ("Telefones", "TELEFONE"),
        ("Unidades", "UNIDADEMEDIDA"),
        ("Produtos", "PRODUTO"),
        ("Categorias", "CATEGORIA"),
        ("Entradas de estoque", "ENTRADAESTOQUE"),
        ("Perdas de estoque", "PERDAESTOQUE"),
        ("Vendas", "PEDIDO"),
        ("Operações de caixa", "OPERACAOCAIXA"),
        ("Caixas", "CAIXA"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("=== VISUALIZAR DADOS ===")
        yield Button("Tela Inicial", id="btn-inicial", variant="primary")

        for rotulo, tabela in self.OPCOES_VISUALIZACAO:
            yield Button(rotulo, id=f"btn-vw-{tabela}")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        botao_id = event.button.id

        if botao_id == "btn-inicial":
            self.app.switch_mode(self.MODO_INICIAL)
            return

        if botao_id and botao_id.startswith("btn-vw-"):
            tabela = botao_id.replace("btn-vw-", "", 1)
            self.app.push_screen(View(tabela))