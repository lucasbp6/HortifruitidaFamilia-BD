class ViewScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Button("Tela Inicial", id="btn-inicial", variant="primary")
        yield Button("Clientes", id="btn-vw-CLIENTE")
        yield Button("Fornecedores", id="btn-vw-FORNECEDOR")
        yield Button("Vendedores", id="btn-vw-VENDEDOR")
        yield Button("Endereço", id="btn-vw-ENDERECO")
        yield Button("Telefones", id="btn-vw-TELEFONE")
        yield Button("Unidades", id="btn-vw-UNIDADEMEDIDA")
        yield Button("Produtos", id="btn-vw-PRODUTO")
        yield Button("Categorias", id="btn-vw-CATEGORIA")
        yield Button("Entrada estoque", id="btn-vw-ENTRADAESTOQUE")
        yield Button("Perda estoque", id="btn-vw-PERDAESTOQUE")
        yield Button("Vendas", id="btn-vw-PEDIDO")
        yield Button("Operações", id="btn-vw-OPERACAOCAIXA")
        yield Button("Caixas", id="btn-vw-CAIXA")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-inicial":
            self.app.switch_mode("inicial")
        elif event.button.id.startswith("btn-vw-"):
            self.app.push_screen(View(event.button.id[7:]))