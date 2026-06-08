class View(ModalScreen):
    DEFAULT_CSS = """
    View { background: black; padding: 1; }
    #area-filtro { layout: horizontal; height: auto; margin-bottom: 1; }
    #select-coluna { width: 30%; margin-right: 1; }
    #input-filtro { width: 70%; }
    """

    def __init__(self, tabela: str, **kwargs):
        super().__init__(**kwargs)
        self.tabela = tabela
        self.dados_originais = []
        self.colunas = []
    
    def compose(self) -> ComposeResult:
        yield Button("Voltar", id="btn-voltar", variant="error")
        with Horizontal(id="area-filtro"):
            yield Select([], id="select-coluna", prompt="Filtrar por qual coluna?")
            yield Input(placeholder="Digite o valor para buscar...", id="input-filtro")
        yield DataTable(id="minha-lista")

    def on_mount(self) -> None:
            lista = self.query_one("#minha-lista", DataTable)
            
            # Interceptamos ENDERECO
            if self.tabela == "ENDERECO":
                self.colunas = list(entities.TABELAS[self.tabela][0]) + ["Tipo Vinculo", "Proprietário (Nome)"]
                self.dados_originais = operacoes.select_enderecos_por_tipo("TODOS")
                
            # Interceptamos TELEFONE (Tabela Virtual)
            elif self.tabela == "TELEFONE":
                self.colunas = ["Telefone", "Tipo Vinculo", "Proprietário (Nome)"]
                self.dados_originais = operacoes.select_telefones_geral()
                
            # Comportamento Padrão para as demais
            else:
                self.colunas = list(entities.TABELAS[self.tabela][0])
                self.dados_originais = operacoes.select(
                    self.tabela,
                    order_by=entities.TABELAS[self.tabela][0][0]
                )
                
            lista.add_columns(*self.colunas)
            
            opcoes_select = [(coluna, str(indice)) for indice, coluna in enumerate(self.colunas)]
            select = self.query_one("#select-coluna", Select)
            select.set_options(opcoes_select)
            
            if self.dados_originais:
                lista.add_rows(self.dados_originais)

    @on(Input.Changed, "#input-filtro")
    @on(Select.Changed, "#select-coluna")
    def atualizar_filtro(self) -> None:
        input_widget = self.query_one("#input-filtro", Input)
        select_widget = self.query_one("#select-coluna", Select)
        lista = self.query_one("#minha-lista", DataTable)
        
        termo_busca = input_widget.value.lower()
        indice_coluna = select_widget.value
        lista.clear()
        
        if not termo_busca or indice_coluna == Select.BLANK:
            lista.add_rows(self.dados_originais)
            return
        
        idx = int(indice_coluna)
        dados_filtrados = [linha for linha in self.dados_originais if termo_busca in str(linha[idx]).lower()]
        lista.add_rows(dados_filtrados)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-voltar":
            self.app.pop_screen()