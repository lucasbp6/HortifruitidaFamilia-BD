class UpdateSelectView(ModalScreen):
    DEFAULT_CSS = """
    UpdateSelectView { background: black; padding: 1; }
    #area-filtro, #area-update { layout: horizontal; height: auto; margin-bottom: 1; }
    #select-coluna, #input-filtro, #input-update-id { margin-right: 1; background: #2a2a2a; color: #dcdcdc; }
    #select-coluna { width: 30%; }
    #input-filtro { width: 70%; }
    #input-update-id { width: 60%; }
    #btn-update-confirmar { width: 40%; }
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
        
        with Horizontal(id="area-update"):
            yield Input(placeholder="Digite o ID para ATUALIZAR...", id="input-update-id")
            yield Button("Atualizar Selecionado", id="btn-update-confirmar", variant="primary")
            
        yield DataTable(id="minha-lista", cursor_type="row") # cursor_type="row" permite selecionar a linha inteira

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
            # Converte os IDs para string para evitar problemas de formatação na DataTable
            linhas_formatadas = [[str(item) if item is not None else "" for item in linha] for linha in self.dados_originais]
            lista.add_rows(linhas_formatadas)

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
            linhas_formatadas = [[str(item) if item is not None else "" for item in linha] for linha in self.dados_originais]
            lista.add_rows(linhas_formatadas)
            return
        
        idx = int(indice_coluna)
        dados_filtrados = [linha for linha in self.dados_originais if termo_busca in str(linha[idx]).lower()]
        linhas_formatadas = [[str(item) if item is not None else "" for item in linha] for linha in dados_filtrados]
        lista.add_rows(linhas_formatadas)

    # Lógica 1: Usuário CLICOU na linha da tabela
    @on(DataTable.RowSelected, "#minha-lista")
    def linha_selecionada(self, event: DataTable.RowSelected) -> None:
        lista = self.query_one("#minha-lista", DataTable)
        dados_linha = lista.get_row(event.row_key)
        id_selecionado = int(dados_linha[0]) # Pega a primeira coluna (PK)
        self.chamar_formulario(id_selecionado)

    # Lógica 2: Usuário DIGITOU o ID e clicou no botão
    @on(Button.Pressed, "#btn-update-confirmar")
    def botao_confirmar(self, event: Button.Pressed) -> None:
        valor_id = self.query_one("#input-update-id", Input).value.strip()
        if valor_id.isdigit():
            self.chamar_formulario(int(valor_id))
        else:
            self.app.notify("ID inválido! Digite apenas números.", severity="error")

    def chamar_formulario(self, id_registro: int) -> None:
        nome_coluna_pk = self.colunas[0]
        registros = operacoes.select(self.tabela, where={nome_coluna_pk: id_registro})
        
        if registros:
            linha_banco = registros[0]
            self.app.pop_screen() # Fecha a tela de seleção
            # Abre o formulário passando a linha encontrada no banco
            self.app.push_screen(FormularioModal(self.tabela, "atualizar", entities.TABELAS[self.tabela], preenchimento=linha_banco))
        else:
            self.app.notify("Registro não encontrado no banco!", severity="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-voltar":
            self.app.pop_screen()