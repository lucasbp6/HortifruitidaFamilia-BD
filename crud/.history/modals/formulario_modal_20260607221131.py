class FormularioModal(ModalScreen):
    def __init__(self, tabela_nome: str, acao: str, dados_iniciais: tuple, preenchimento: tuple = None, **kwargs):
        super().__init__(**kwargs)
        self.tabela_nome = tabela_nome
        self.acao = acao
        self.dados_iniciais = dados_iniciais[0]
        self.tipos = dados_iniciais[1]
        self.preenchimento = preenchimento # Recebe a tupla do banco de dados
    
    def compose(self) -> ComposeResult:
        with Vertical(id="caixa-formulario"):
            yield Label(f"{self.acao.capitalize()} - {self.tabela_nome}", id="titulo-form")

            
            for i, coluna in enumerate(self.dados_iniciais):
                if coluna.startswith("ID") and i != 0:
                    tabela_alvo = coluna.replace("ID", "").upper()
                    if tabela_alvo == "CAT": tabela_alvo = "CATEGORIA"
                    if tabela_alvo == "CATPAI": tabela_alvo = "CATEGORIA"
                    if tabela_alvo == "UNIDADE": tabela_alvo = "UNIDADEMEDIDA"
                    if tabela_alvo == "FORN": tabela_alvo = "FORNECEDOR"
                    if tabela_alvo == "PROD": tabela_alvo = "PRODUTO"
                    
                    try:
                        # Em vez de adivinhar o nome da coluna, pegamos direto do entities.py
                        # A posição [1] é sempre o "Nome..." (ex: NomeUnidade, NomeCat)
                        nome_campo = entities.TABELAS[tabela_alvo][0][1]
                        
                        # Tratamento para o IDCatPai buscar no IDCat
                        coluna_id_real = coluna.replace('Pai', '')
                        
                        registros = operacoes.select(tabela_alvo, cols=f"{coluna_id_real}, {nome_campo}")
                        
                        if registros:
                            opcoes = [(f"{r[1]} (ID: {r[0]})", str(r[0])) for r in registros]
                        else:
                            opcoes = [("Nenhum cadastrado", "")]
                            
                        yield Select(opcoes, prompt=f"Selecione {coluna}", id=f"input-{i}")
                    except Exception as e:
                        # Se der qualquer problema (como a tabela não ter a mesma estrutura), cai pro Input normal
                        yield Input(placeholder=f"Digite o {coluna}...", id=f"input-{i}")
                else:
                    yield Input(placeholder=f"Digite o {coluna}...", id=f"input-{i}")

            if self.tabela_nome == "ENDERECO":
                # 1. Cria o primeiro Select
                yield Select(
                    [("Cliente", "CLIENTE"), ("Fornecedor", "FORNECEDOR")], 
                    prompt="Para quem é este endereço?", 
                    id="clienteouForn"
                )
                # 2. Cria o segundo Select vazio e desabilitado (até o usuário escolher a primeira opção)
                yield Select(
                    [], 
                    prompt="Aguardando seleção acima...", 
                    id="IDconexaoEnd",
                    disabled=True
                )

            with Horizontal(id="botoes-form"):
                yield Button("Confirmar", id="btn-salvar", variant="success")
                yield Button("Cancelar", id="btn-cancelar", variant="error")

    def on_mount(self) -> None:
        if self.acao == "atualizar" and hasattr(self, 'preenchimento') and self.preenchimento:
            for i, valor in enumerate(self.preenchimento):
                try:
                    widget = self.query_one(f"#input-{i}")
                    
                    if isinstance(widget, Select):
                        widget.value = str(valor) if valor is not None else Select.BLANK
                    else:
                        widget.value = str(valor) if valor is not None else ""
                except Exception:
                    pass # Ignora se o widget não for encontrado por algum motivo
            
            self.app.notify("Dados carregados! Altere os valores desejados.", severity="info")
            
            try:
                # Trava o campo da Chave Primária
                self.query_one("#input-0").disabled = True 
            except Exception:
                pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancelar":
            self.dismiss(None) 
            
        elif event.button.id == "btn-salvar":
            valores_validados = {}

            for i, (coluna, tipo_esperado) in enumerate(zip(self.dados_iniciais, self.tipos)):
                widget = self.query_one(f"#input-{i}")
                
                if isinstance(widget, Select):
                    valor_texto = widget.value if widget.value != Select.BLANK else ""
                else:
                    valor_texto = widget.value.strip()
                
                if not valor_texto and valor_texto != 0:
                    if "None" in tipo_esperado:
                        valores_validados[coluna] = None
                        continue 
                    else:
                        self.app.notify(f"O campo '{coluna}' é obrigatório!", severity="error")
                        return 

                tipo_full = tipo_esperado.split(" | ")[0].strip() 
                tipo_base = tipo_full.split("(")[0] if "(" in tipo_full else tipo_full

                if tipo_base == "int":
                    if not str(valor_texto).isdigit():
                        self.app.notify(f"O campo '{coluna}' aceita APENAS números inteiros.", severity="error")
                        return
                elif tipo_base == "float":
                    try:
                        float(str(valor_texto).replace(",", "."))
                    except ValueError:
                        self.app.notify(f"O campo '{coluna}' aceita APENAS números.", severity="error")
                        return
                    
                valores_validados[coluna] = valor_texto

            try:
                if self.acao == "inserir":
                    if self.tabela_nome in ["ENTRADAESTOQUE", "PERDAESTOQUE"]:
                        operacoes.registrar_movimentacao_estoque(self.tabela_nome, valores_validados)
                    elif self.tabela_nome == "ENDERECO":
                        CouF = self.query_one("#clienteouForn").value
                        val_pessoa = self.query_one("#IDconexaoEnd").value
                        if type(CouF).__name__ == "NoSelection" or type(val_pessoa).__name__ == "NoSelection":
                            self.app.notify("Por favor, selecione para quem é este endereço e a pessoa específica antes de salvar!", severity="error", timeout=5)
                            return
                        if CouF == "FORNECEDOR":
                            operacoes.insert([self.tabela_nome, "ENDERECOFORNEC"], [valores_validados, {'IDEndereco': valores_validados["IDEndereco"], "IDForn": val_pessoa }])
                        else:
                            operacoes.insert([self.tabela_nome, "ENDERECOCLIENTE"], [valores_validados, {'IDEndereco': valores_validados["IDEndereco"], "IDCliente": val_pessoa }])
                    else:
                        operacoes.insert([self.tabela_nome], [valores_validados])
                        

                    self.app.notify(f"Sucesso ao inserir em {self.tabela_nome}!", severity="success")

                elif self.acao == "atualizar":
                    chave_primaria = self.dados_iniciais[0]
                    operacoes.update(self.tabela_nome, valores_validados, {chave_primaria: valores_validados[chave_primaria]})
                    self.app.notify(f"Sucesso ao atualizar {self.tabela_nome}!", severity="success")

                self.dismiss(valores_validados) 

            except Exception as e:
                self.app.notify(f"Erro no banco: {e}", severity="error", timeout=6)
    
    @on(Select.Changed, "#clienteouForn")
    def atualizar_select_pessoa(self, event: Select.Changed) -> None:
        # Captura o segundo widget
        select_conexao = self.query_one("#IDconexaoEnd", Select)
        
        # Se o usuário limpou o campo, desabilita o de baixo e sai
        if event.value == Select.BLANK:
            select_conexao.set_options([])
            select_conexao.disabled = True
            select_conexao.prompt = "Aguardando seleção acima..."
            return
            
        tipo_escolhido = event.value # Será "CLIENTE" ou "FORNECEDOR"
        
        # Faz a busca no banco dependendo da escolha
        if tipo_escolhido == "FORNECEDOR":
            registros = operacoes.select("FORNECEDOR", cols="IDForn, NomeForn")
        else:
            registros = operacoes.select("CLIENTE", cols="IDCliente, NomeCliente")
            
        # Atualiza as opções do segundo Select e habilita ele
        if registros:
            opcoes = [(f"{r[1]} (ID: {r[0]})", str(r[0])) for r in registros]
            select_conexao.set_options(opcoes)
            select_conexao.disabled = False
            select_conexao.prompt = f"Selecione o {tipo_escolhido.capitalize()}"
        else:
            select_conexao.set_options([])
            select_conexao.disabled = True
            select_conexao.prompt = f"Nenhum {tipo_escolhido.capitalize()} cadastrado"
