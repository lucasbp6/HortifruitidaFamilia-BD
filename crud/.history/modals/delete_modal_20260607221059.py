class DeleteByIdView(ModalScreen):
    DEFAULT_CSS = """
    DeleteByIdView { background: black; padding: 1; }
    #area-filtro, #area-deletar { layout: horizontal; height: auto; margin-bottom: 1; }
    #select-coluna, #input-filtro, #input-deletar-id { margin-right: 1; background: #2a2a2a; color: #dcdcdc; }
    #select-coluna { width: 30%; }
    #input-filtro { width: 70%; }
    #input-deletar-id { width: 60%; }
    #btn-deletar-confirmar { width: 40%; }
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
        with Horizontal(id="area-deletar"):
            yield Input(placeholder="Digite o ID para DELETAR...", id="input-deletar-id")
            yield Button("Confirmar Deleção", id="btn-deletar-confirmar", variant="error")
        yield DataTable(id="minha-lista")

    def on_mount(self) -> None:
        self.colunas = entities.TABELAS[self.tabela][0] 
        opcoes_select = [(coluna, str(indice)) for indice, coluna in enumerate(self.colunas)]
        select = self.query_one("#select-coluna", Select)
        select.set_options(opcoes_select)
        
        lista = self.query_one("#minha-lista", DataTable)
        lista.add_columns(*self.colunas)
        self.carregar_dados()

    def carregar_dados(self) -> None:
        lista = self.query_one("#minha-lista", DataTable)
        lista.clear() 
        self.dados_originais = operacoes.select(
            self.tabela,
            order_by=entities.TABELAS[self.tabela][0][0]
        )
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

    @on(Button.Pressed, "#btn-deletar-confirmar")
    def deletar_por_id(self, event: Button.Pressed) -> None:
        input_id = self.query_one("#input-deletar-id", Input)
        id_registro = input_id.value.strip()

        if not id_registro: return

        try:
            id_num = int(id_registro)
        except ValueError:
             input_id.value = "" 
             return

        nome_coluna_id = self.colunas[0]

        try:
            if self.tabela in ["CLIENTE", "VENDEDOR"]:
                linhas = operacoes.deletar_seguro(self.tabela, id_num, nome_coluna_id)
            else:
                linhas = operacoes.delete(self.tabela, {nome_coluna_id: id_num})
            
            self.app.notify(f"Deleção concluída. Registros afetados: {linhas}")
            self.carregar_dados()
            input_id.value = ""
        except Exception as e:
            self.app.notify(f"Erro ao deletar: {e}", severity="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-voltar":
            self.app.pop_screen()
