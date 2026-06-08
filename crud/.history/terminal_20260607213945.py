from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Footer, Button, Static, DataTable, Input, Label, ContentSwitcher, Select
from textual.containers import Vertical, Horizontal
from textual import on
import entities
import operacoes
from datetime import datetime

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

class Vendasmodal(ModalScreen):
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

class FormularioPessoaComposto(ModalScreen):
    DEFAULT_CSS = """
    FormularioPessoaComposto { background: black; padding: 1; }
    #caixa-formulario { width: 80%; height: auto; border: solid green; padding: 1; }
    """

    def __init__(self, tipo_pessoa: str, **kwargs):
        super().__init__(**kwargs)
        self.tipo_pessoa = tipo_pessoa.upper()
        
    def compose(self) -> ComposeResult:
        with Vertical(id="caixa-formulario"):
            yield Label(f"Cadastro Completo: {self.tipo_pessoa}", id="titulo-form")
            
            yield Static("--- Dados Básicos ---")
            yield Input(placeholder="ID (Ex: 10)", id="pes_id")
            yield Input(placeholder="Nome Completo", id="pes_nome")
            yield Input(placeholder="Documento (CPF/CNPJ)", id="pes_doc")
            
            if self.tipo_pessoa in ["CLIENTE", "VENDEDOR"]:
                yield Input(placeholder="Data de Nascimento (AAAA-MM-DD)", id="pes_nasc")
            if self.tipo_pessoa == "VENDEDOR":
                yield Input(placeholder="Salário Base", id="pes_salario")
            
            yield Input(placeholder="Celular (Apenas números)", id="pes_celular")
            
            yield Static("--- Endereço ---")
            yield Input(placeholder="ID do Endereço a criar", id="end_id")
            yield Input(placeholder="CEP", id="end_cep")
            yield Input(placeholder="Rua", id="end_rua")
            yield Input(placeholder="Número", id="end_num")
            yield Input(placeholder="Bairro", id="end_bairro")
            yield Input(placeholder="Cidade", id="end_cid")
            yield Input(placeholder="Estado (Ex: SP)", id="end_est")
            yield Input(placeholder="País", id="end_pais")
            
            with Horizontal(id="botoes-form"):
                yield Button("Salvar Tudo", id="btn-salvar-comp", variant="success")
                yield Button("Cancelar", id="btn-cancelar-comp", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancelar-comp":
            self.dismiss()
            return
            
        if event.button.id == "btn-salvar-comp":
            try:
                d_end = {
                    "IDEndereco": self.query_one("#end_id", Input).value,
                    "RuaEnd": self.query_one("#end_rua", Input).value,
                    "NumeroEnd": self.query_one("#end_num", Input).value,
                    "ComplemEnd": None, 
                    "CEPEnd": self.query_one("#end_cep", Input).value,
                    "BairroEnd": self.query_one("#end_bairro", Input).value,
                    "CidadeEnd": self.query_one("#end_cid", Input).value,
                    "EstadoEnd": self.query_one("#end_est", Input).value,
                    "PaisEnd": self.query_one("#end_pais", Input).value,
                }
                
                id_pes = self.query_one("#pes_id", Input).value
                doc = self.query_one("#pes_doc", Input).value
                nome = self.query_one("#pes_nome", Input).value
                cel = self.query_one("#pes_celular", Input).value
                
                tabelas = ["ENDERECO"]
                valores = [d_end]

                if self.tipo_pessoa == "CLIENTE":
                    tabelas.extend(["CLIENTE", "ENDERECOCLIENTE", "CLIENTE_CELCLIENTE"])
                    valores.append({"IDCliente": id_pes, "NomeCliente": nome, "CPFCliente": doc, "DataNascCliente": self.query_one("#pes_nasc", Input).value})
                    valores.append({"IDCliente": id_pes, "IDEndereco": d_end["IDEndereco"]})
                    valores.append({"CelCliente": cel, "IDCliente": id_pes})
                    
                elif self.tipo_pessoa == "FORNECEDOR":
                    tabelas.extend(["FORNECEDOR", "ENDERECOFORNEC", "FORNECEDOR_CELFORN"])
                    valores.append({"IDForn": id_pes, "NomeForn": nome, "CNPJForn": doc})
                    valores.append({"IDForn": id_pes, "IDEndereco": d_end["IDEndereco"]})
                    valores.append({"CelForn": cel, "IDForn": id_pes})
                    
                elif self.tipo_pessoa == "VENDEDOR":
                    tabelas.extend(["VENDEDOR", "ENDERECOVENDEDOR"])
                    valores.append({"IDVend": id_pes, "NomeVend": nome, "CPFVend": doc, "DataNascVend": self.query_one("#pes_nasc", Input).value, "SalarioVend": self.query_one("#pes_salario", Input).value, "CelVend": cel})
                    valores.append({"IDVend": id_pes, "IDEndereco": d_end["IDEndereco"]})

                operacoes.insert(tabelas, valores)
                self.app.notify(f"{self.tipo_pessoa} salvo com sucesso!", severity="success")
                self.dismiss()
                
            except Exception as e:
                self.app.notify(f"Falha no cadastro (Rollback efetuado): {e}", severity="error")

class InitialScreen(Screen):
    def compose(self) -> ComposeResult:
        LOGO_HORTIFRUTI = r"""
         _   _               _   _  __               _     _ 
        | | | | ___  _ __  _| |_(_)/ _| _ __  _   _ | |_  (_)
        | |_| |/ _ \| '__||_   _| | |_ | '__|| | | ||  _| | |
        |  _  | (_) | |     | | | |  _|| |   | |_| || |_  | |
        |_| |_|\___/|_|     |_| |_|_|  |_|    \__,_| \__| |_|
                                                crud v26.6
        """
        yield Static(LOGO_HORTIFRUTI, classes="titulo-tela")
        yield Button("Operar", id="btn-operar", variant="primary")
        yield Button("Visualizar dados", id="btn-vizualizar", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-operar":
            self.app.switch_mode("operation")
        elif event.button.id == "btn-vizualizar":
            self.app.switch_mode("view")

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

class OperationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ident = None
        self.inicial = 0.0
        self.carrinho_itens = [] 
        self.total_venda = 0.0
        self.total = 0.0

    def compose(self) -> ComposeResult:
        with ContentSwitcher(initial="menu-opcoes", id="meu-switcher"):
            with Vertical(id="menu-opcoes"):
                yield Static("=== ESCOLHA UMA OPERAÇÃO ===")
                yield Button("Cadastros", id="btn-cadastro")
                yield Button("Iniciar Venda", id="btn-vender")
                yield Button("Deletar", id="btn-deletar")
                yield Button("Atualizar", id="btn-update")

            with Vertical(id="tela-cadastro"):
                yield Static("Escolha o que deseja cadastrar:")
                yield Button("Voltar para o Menu", id="btn-voltar", variant="error")
                yield Button("Add Produto", id="btn-ad-PRODUTO")
                yield Button("Add Categoria", id="btn-ad-CATEGORIA")
                yield Button("Add entrada de estoque", id="btn-ad-ENTRADAESTOQUE")
                yield Button("Add Perda estoque", id="btn-ad-PERDAESTOQUE")
                yield Button("Add Cliente", id="btn-ad-CLIENTE")
                yield Button("Add Fornecedor", id="btn-ad-FORNECEDOR")
                yield Button("Add Vendedor", id="btn-ad-VENDEDOR")
                yield Button("Add Unidade", id="btn-ad-UNIDADEMEDIDA")
                yield Button("Add Caixa", id="btn-ad-CAIXA")
                yield Button("Add Endereco", id="btn-ad-ENDERECO")

            with Vertical(id="tela-identificar"):
                yield Static("Identifique o Vendedor e o Caixa:")
                yield Select([], prompt="Selecione o Vendedor", id="vendedor-select")
                yield Select([], prompt="Selecione o Caixa", id="caixa-select")
                yield Input(placeholder="Valor Inicial de Abertura (Ex: 150.00)", id="valor-abertura")
                yield Button("Abrir Caixa e Prosseguir", id="btn-prosseg", variant="success")
                yield Button("Voltar para o Menu", id="btn-voltar-3", variant="error")

            with Vertical(id="tela-venda"):
                yield Static("=== FRENTE DE CAIXA ===")
                yield Input(placeholder="Código Produto (ID)", id="venda-input-id")
                yield Input(placeholder="Qtd", id="venda-input-qtd") 
                yield Button("Adicionar Produto", id="btn-addprod", variant="success")
                yield DataTable(id="carrinho-lista")
                yield Button("Finalizar Pagamento", id="btn-finalizar", variant="success")
                yield Button("Fechar operação", id="btn-fecharcx", variant="error")
                yield DataTable(id="produtos-lista")

            with Vertical(id="tela-fin"):
                yield Static("=== FINALIZAR PAGAMENTO ===")
                yield Select([], prompt="Selecione o cliente", id="fin-cliente")
                yield Select([("Dinheiro", "Dinheiro"), ("Débito", "Débito"), ("Crédito", "Crédito"), ("Pix", "Pix")], prompt="Selecione Forma de pagamento", id="fin-pagto")
                yield Select([("Venda", "Venda"), ("Delivery", "Delivery")], prompt="Selecione O tipo do pedido", id="fin-tipo")

                yield Button("Finalizar Venda", id="btn-final", variant="error")
                yield Button("Cancelar Venda", id="btn-voltar-4", variant="error")


            with Vertical(id="tela-deletar"):
                yield Static("Escolha o que deseja deletar:")
                yield Button("Voltar para o Menu", id="btn-voltar", variant="error")
                yield Button("Del Produto", id="btn-dl-PRODUTO")
                yield Button("Del Categoria", id="btn-dl-CATEGORIA")
                yield Button("Del Cliente", id="btn-dl-CLIENTE")
                yield Button("Del Vendedor", id="btn-dl-VENDEDOR")
                yield Button("Del Unidade", id="btn-dl-UNIDADEMEDIDA")
                yield Button("Del Caixa", id="btn-dl-CAIXA")
                
            with Vertical(id="tela-update"):
                yield Static("Escolha o que deseja atualizar:")
                yield Button("Voltar para o Menu", id="btn-voltar", variant="error")
                yield Button("Att Produto", id="btn-up-PRODUTO")
                yield Button("Att Categoria", id="btn-up-CATEGORIA")
                yield Button("Att estoque", id="btn-up-ENTRADAESTOQUE")
                yield Button("Att Perda", id="btn-up-PERDAESTOQUE")
                yield Button("Att Cliente", id="btn-up-CLIENTE")
                yield Button("Att Fornecedor", id="btn-up-FORNECEDOR")
                yield Button("Att Vendedor", id="btn-up-VENDEDOR")
                yield Button("Att Unidade", id="btn-up-UNIDADEMEDIDA")
                yield Button("Att Caixa", id="btn-up-CAIXA")
                yield Button("Att Endereco", id="btn-up-ENDERECO")

                
        yield Footer()

    def on_mount(self) -> None:
        carrinho = self.query_one("#carrinho-lista", DataTable)
        carrinho.add_columns("ID", "Produto", "Qtd", "Total (R$)")
        carrinho.styles.height = 10 

        prods = self.query_one("#produtos-lista", DataTable)
        prods.styles.height = 15 
        
        cols = entities.TABELAS["PRODUTO"][0]
        prods.add_columns(*cols)
        
        values = operacoes.select("PRODUTO")
        if values:
            prods.add_rows(values)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        switcher = self.query_one("#meu-switcher", ContentSwitcher)
        
        if event.button.id == "btn-cadastro":
            switcher.current = "tela-cadastro"
            
        elif event.button.id == "btn-vender":
            try:
                vendedores = operacoes.select("VENDEDOR", cols="IDVend, NomeVend")
                if vendedores:
                    self.query_one("#vendedor-select", Select).set_options([(r[1], str(r[0])) for r in vendedores])
                
                caixas = operacoes.select("CAIXA", cols="IDCaixa, TipoCaixa")
                if caixas:
                    self.query_one("#caixa-select", Select).set_options([(r[1], str(r[0])) for r in caixas])
            except Exception as e:
                self.app.notify(f"Erro ao carregar selects: {e}", severity="error")
            
            switcher.current = "tela-identificar"
            
        elif event.button.id == "btn-prosseg":
            id_vend = self.query_one("#vendedor-select", Select).value
            id_caixa = self.query_one("#caixa-select", Select).value
            valor_aber = self.query_one("#valor-abertura", Input).value.strip()

            if id_vend == Select.BLANK or id_caixa == Select.BLANK or not valor_aber:
                self.app.notify("Preencha Vendedor, Caixa e Valor Inicial!", severity="error")
                return
            
            try:
                valor_formatado = float(valor_aber.replace(",", "."))
                id_operacao = operacoes.abrir_operacao_caixa(int(id_vend), int(id_caixa), valor_formatado)
                self.ident = id_operacao
                self.inicial = valor_formatado
                self.app.notify(f"Caixa aberto com sucesso! Operação #{id_operacao}", severity="success")
                switcher.current = "tela-venda"
            except ValueError:
                self.app.notify("Valor de abertura inválido!", severity="error")
            except Exception as e:
                self.app.notify(f"Erro ao abrir caixa: {e}", severity="error")

        elif event.button.id in ["btn-voltar", "btn-voltar-3"]:
            switcher.current = "menu-opcoes"
            self.ident = None 

        elif event.button.id == "btn-inicial":
            self.app.switch_mode("inicial")

        elif event.button.id == "btn-deletar":
            switcher.current = "tela-deletar"

        elif event.button.id == "btn-update":
            switcher.current = "tela-update"

        elif event.button.id == "btn-addprod":
            id_prod = self.query_one("#venda-input-id", Input).value.strip()
            qtd_str = self.query_one("#venda-input-qtd", Input).value.strip()

            if not id_prod or not qtd_str:
                self.app.notify("Preencha ID e Quantidade!", severity="error")
                return

            try:
                qtd = float(qtd_str.replace(",", "."))
                
                prod = operacoes.select("PRODUTO", where={"IDProd": int(id_prod)}) 
                
                nome_prod = prod[0][1]
                preco = float(prod[0][3])
                
                
                subtotal = preco*qtd
                
                # Atualiza o estado da classe
                self.carrinho_itens.append({
                    "id": id_prod,
                    "nome": nome_prod,
                    "qtd": qtd,
                    "preco": preco
                })
                self.total_venda += subtotal

                # Atualiza a interface gráfica do carrinho
                carrinho = self.query_one("#carrinho-lista", DataTable)
                carrinho.add_row(id_prod, nome_prod, str(qtd), f"R$ {subtotal:.2f}")
                
                # Limpa os inputs para o próximo item
                self.query_one("#venda-input-id", Input).value = ""
                self.query_one("#venda-input-qtd", Input).value = "1"
                self.query_one("#venda-input-id", Input).focus() # Devolve o foco pro ID
                
                self.app.notify(f"{nome_prod} adicionado!", severity="success")

            except ValueError:
                self.app.notify("Quantidade inválida!", severity="error")
            except Exception as e:
                self.app.notify(f"Erro ao adicionar: {e}", severity="error")

        elif event.button.id == "btn-finalizar":
            clientes = operacoes.select("CLIENTE", cols="IDCliente, NomeCliente")
            if clientes:
                self.query_one("#fin-cliente", Select).set_options([(r[1], str(r[0])) for r in clientes])

            # A aqui vai precisar salvar as coisas, escolher cliente e pagamento
            switcher.current = "tela-fin"
            

        elif event.button.id == "btn-final":
            if not self.carrinho_itens:
                self.app.notify("O carrinho está vazio!", severity="error")
                return

            id_cliente = self.query_one("#fin-cliente", Select).value
            forma_pgt = self.query_one("#fin-pagto", Select).value
            tipo = self.query_one("#fin-tipo", Select).value

            # Correção 1: Incluir validação do campo 'tipo'
            if id_cliente == Select.BLANK or forma_pgt == Select.BLANK or tipo == Select.BLANK:
                self.app.notify("Selecione o Cliente, Forma de Pagamento e Tipo de Pedido!", severity="error")
                return
            
            try:
                id_pedido, id_pag = operacoes.finalizar_venda_transacao(
                    valor_total=self.total_venda,
                    tipo_pedido=tipo,
                    id_cliente=int(id_cliente),
                    id_operacao=int(self.ident),
                    metodo_pagamento=forma_pgt,
                    itens=self.carrinho_itens
                )

                self.app.notify("Venda finalizada com sucesso!", severity="success")
                
                # Correção 3: Limpeza de estado total e correta
                self.total += self.total_venda
                self.total_venda = 0.0
                self.carrinho_itens = []
                
                self.query_one("#carrinho-lista", DataTable).clear()
                self.query_one("#fin-cliente", Select).clear()
                self.query_one("#fin-pagto", Select).clear()
                self.query_one("#fin-tipo", Select).clear()
                
                # 4. Retorno para a tela de PDV
                switcher.current = "tela-venda"

            except Exception as e:
                self.app.notify(f"Erro ao finalizar venda: {e}", severity="error")

        elif event.button.id == "btn-fecharcx":
            # 1. Validação
            if not self.ident:
                self.app.notify("Não há nenhum caixa aberto!", severity="error")
                return
                
            if self.carrinho_itens:
                self.app.notify("Finalize ou cancele a venda atual antes de fechar o caixa!", severity="warning")
                return

            # 2. Persistência de fechamento
            try:
                agora = datetime.now() 
                
                operacoes.update(
                    "OPERACAOCAIXA",
                    data={
                        "DataOpFecham": agora, 
                        "ValorOpFecham": self.total + self.inicial, 
                        "SaldoOp": self.total
                    }, 
                    where={"IDOperacao": self.ident}
                )
                
                self.app.notify(f"Caixa (Operação #{self.ident}) fechado com sucesso!", severity="success")
                
                # 3. Limpeza do estado para a próxima abertura
                self.ident = None
                self.total_venda = 0.0
                self.total = 0.0
                self.inicial = 0.0
                self.carrinho_itens = []
                self.query_one("#carrinho-lista", DataTable).clear()
                
                # Correção 4: Limpar os campos da tela de identificação para evitar dados velhos ao abrir um novo caixa
                self.query_one("#vendedor-select", Select).clear()
                self.query_one("#caixa-select", Select).clear()
                self.query_one("#valor-abertura", Input).clear()
                
                switcher.current = "menu-opcoes"
                
            except Exception as e:
                self.app.notify(f"Erro ao fechar o caixa: {e}", severity="error")
        
        elif event.button.id == "btn-voltar-4":
            self.carrinho_itens = []
            switcher.current = "tela-venda"


        elif event.button.id.startswith("btn-ad-"):
            tabela_nome = event.button.id[7:] 
            if tabela_nome in ["CLIENTE", "VENDEDOR", "FORNECEDOR"]:
                self.app.push_screen(FormularioPessoaComposto(tabela_nome))
            else:
                self.app.push_screen(FormularioModal(tabela_nome, "inserir", entities.TABELAS[tabela_nome]))

        elif event.button.id.startswith("btn-up-"):
            tabela_nome = event.button.id[7:]
            # self.app.push_screen(FormularioModal(tabela_nome, "atualizar", entities.TABELAS[tabela_nome]))
            self.app.push_screen(UpdateSelectView(tabela_nome))
        elif event.button.id.startswith("btn-dl-"):
            tabela_nome = event.button.id[7:] 
            self.app.push_screen(DeleteByIdView(tabela_nome))


if __name__ == "__main__":
    app = ModesApp()
    app.run()
