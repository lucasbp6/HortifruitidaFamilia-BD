from datetime import datetime

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select
from textual.containers import Horizontal, Vertical

import entities
import operacoes


class FormularioModal(ModalScreen):
    """
    Formulário genérico para inserir ou atualizar registros.

    Ele usa entities.TABELAS para descobrir colunas e tipos, e trata casos
    especiais como movimentação de estoque e cadastro de endereço vinculado.
    """

    DEFAULT_CSS = """
    FormularioModal { background: black; padding: 1; }
    #caixa-formulario { width: 80%; height: auto; border: solid green; padding: 1; }
    #botoes-form { height: auto; margin-top: 1; }
    """

    ACAO_INSERIR = "inserir"
    ACAO_ATUALIZAR = "atualizar"

    TABELAS_ESTOQUE = {"ENTRADAESTOQUE", "PERDAESTOQUE"}

    # Mapeia nomes de colunas de FK para a tabela consultada no Select.
    CHAVES_ESTRANGEIRAS = {
        "IDCatPai": "CATEGORIA",
        "IDCat": "CATEGORIA",
        "IDUnidade": "UNIDADEMEDIDA",
        "IDForn": "FORNECEDOR",
        "IDProd": "PRODUTO",
        "IDCliente": "CLIENTE",
        "IDVend": "VENDEDOR",
        "IDCaixa": "CAIXA",
        "IDOperacao": "OPERACAOCAIXA",
        "IDPedido": "PEDIDO",
        "IDEndereco": "ENDERECO",
    }

    # Coluna de texto usada para mostrar opções amigáveis no Select.
    COLUNAS_EXIBICAO = {
        "CATEGORIA": "NomeCat",
        "UNIDADEMEDIDA": "NomeUnidade",
        "PRODUTO": "NomeProd",
        "FORNECEDOR": "NomeForn",
        "CLIENTE": "NomeCliente",
        "VENDEDOR": "NomeVend",
        "CAIXA": "TipoCaixa",
        "OPERACAOCAIXA": "IDOperacao",
        "PEDIDO": "IDPedido",
        "ENDERECO": "RuaEnd",
    }

    # Coluna de ID real da tabela-alvo.
    COLUNAS_ID = {
        "CATEGORIA": "IDCat",
        "UNIDADEMEDIDA": "IDUnidade",
        "PRODUTO": "IDProd",
        "FORNECEDOR": "IDForn",
        "CLIENTE": "IDCliente",
        "VENDEDOR": "IDVend",
        "CAIXA": "IDCaixa",
        "OPERACAOCAIXA": "IDOperacao",
        "PEDIDO": "IDPedido",
        "ENDERECO": "IDEndereco",
    }

    def __init__(
        self,
        tabela_nome: str,
        acao: str,
        dados_iniciais: tuple,
        preenchimento: tuple | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.tabela_nome = tabela_nome.upper()
        self.acao = acao.lower()
        self.dados_iniciais = list(dados_iniciais[0])
        self.tipos = list(dados_iniciais[1])
        self.preenchimento = preenchimento

        if self.acao not in {self.ACAO_INSERIR, self.ACAO_ATUALIZAR}:
            raise ValueError("Ação inválida. Use 'inserir' ou 'atualizar'.")

    def compose(self) -> ComposeResult:
        with Vertical(id="caixa-formulario"):
            yield Label(f"{self.acao.capitalize()} - {self.tabela_nome}", id="titulo-form")

            for indice, coluna in enumerate(self.dados_iniciais):
                yield self._criar_widget_campo(indice, coluna)

            if self.tabela_nome == "ENDERECO" and self.acao == self.ACAO_INSERIR:
                yield Select(
                    [("Cliente", "CLIENTE"), ("Fornecedor", "FORNECEDOR")],
                    prompt="Para quem é este endereço?",
                    id="clienteouForn"
                )
                yield Select(
                    [],
                    prompt="Aguardando seleção acima...",
                    id="IDconexaoEnd",
                    disabled=True
                )

            with Horizontal(id="botoes-form"):
                yield Button("Confirmar", id="btn-salvar", variant="success")
                yield Button("Cancelar", id="btn-cancelar", variant="error")

    def _criar_widget_campo(self, indice: int, coluna: str):
        """
        Cria um Select para chaves estrangeiras e um Input para os demais campos.
        A chave primária da própria tabela permanece como Input.
        """

        if self._deve_usar_select_fk(indice, coluna):
            try:
                opcoes = self._opcoes_fk(coluna)
                return Select(opcoes, prompt=f"Selecione {coluna}", id=f"input-{indice}")
            except Exception:
                # Se houver problema ao montar FK, não quebra o formulário inteiro.
                return Input(placeholder=f"Digite o {coluna}...", id=f"input-{indice}")

        return Input(placeholder=f"Digite o {coluna}...", id=f"input-{indice}")

    def _deve_usar_select_fk(self, indice: int, coluna: str) -> bool:
        if indice == 0:
            return False

        return coluna in self.CHAVES_ESTRANGEIRAS

    def _opcoes_fk(self, coluna: str):
        tabela_alvo = self.CHAVES_ESTRANGEIRAS[coluna]
        coluna_id = self.COLUNAS_ID[tabela_alvo]
        coluna_exibicao = self.COLUNAS_EXIBICAO[tabela_alvo]

        registros = operacoes.select(
            tabela_alvo,
            cols=f"{coluna_id}, {coluna_exibicao}",
            order_by=coluna_id
        )

        if not registros:
            return [("Nenhum cadastrado", "")]

        return [
            (f"{registro[1]} (ID: {registro[0]})", str(registro[0]))
            for registro in registros
        ]

    def on_mount(self) -> None:
        if self.acao == self.ACAO_ATUALIZAR and self.preenchimento:
            self._preencher_campos()
            self._travar_chave_primaria()
            self.app.notify("Dados carregados! Altere os valores desejados.", severity="info")

    def _preencher_campos(self) -> None:
        for indice, valor in enumerate(self.preenchimento):
            try:
                widget = self.query_one(f"#input-{indice}")

                if isinstance(widget, Select):
                    widget.value = str(valor) if valor is not None else Select.BLANK
                else:
                    widget.value = "" if valor is None else str(valor)

            except Exception:
                pass

    def _travar_chave_primaria(self) -> None:
        try:
            self.query_one("#input-0").disabled = True
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancelar":
            self.dismiss(None)
            return

        if event.button.id == "btn-salvar":
            self._salvar_formulario()

    def _salvar_formulario(self) -> None:
        try:
            valores_validados = self._coletar_e_validar_campos()

            if self.acao == self.ACAO_INSERIR:
                self._executar_insercao(valores_validados)
                self.app.notify(f"Sucesso ao inserir em {self.tabela_nome}!", severity="success")

            elif self.acao == self.ACAO_ATUALIZAR:
                self._executar_atualizacao(valores_validados)
                self.app.notify(f"Sucesso ao atualizar {self.tabela_nome}!", severity="success")

            self.dismiss(valores_validados)

        except Exception as erro:
            self.app.notify(f"Erro no formulário/banco: {erro}", severity="error", timeout=7)

    def _coletar_e_validar_campos(self) -> dict:
        valores_validados = {}

        for indice, (coluna, tipo_esperado) in enumerate(zip(self.dados_iniciais, self.tipos)):
            widget = self.query_one(f"#input-{indice}")

            valor_texto = self._valor_do_widget(widget)
            valor_convertido = self._validar_e_converter_valor(coluna, valor_texto, tipo_esperado)

            valores_validados[coluna] = valor_convertido

        return valores_validados

    def _valor_do_widget(self, widget):
        if isinstance(widget, Select):
            return "" if widget.value == Select.BLANK else widget.value

        return widget.value.strip()

    def _validar_e_converter_valor(self, coluna: str, valor_texto, tipo_esperado: str):
        permite_none = "None" in tipo_esperado

        if valor_texto == "" or valor_texto is None:
            if permite_none:
                return None

            raise ValueError(f"O campo '{coluna}' é obrigatório.")

        tipo_base = self._tipo_base(tipo_esperado)

        if tipo_base == "int":
            try:
                return int(str(valor_texto))
            except ValueError:
                raise ValueError(f"O campo '{coluna}' aceita apenas números inteiros.")

        if tipo_base == "float":
            try:
                return float(str(valor_texto).replace(",", "."))
            except ValueError:
                raise ValueError(f"O campo '{coluna}' aceita apenas números.")

        if tipo_base in {"date", "datetime"}:
            # Mantemos string no formato esperado pelo PostgreSQL.
            # A validação mínima evita strings claramente vazias/inúteis.
            return str(valor_texto)

        return str(valor_texto)

    def _tipo_base(self, tipo_esperado: str) -> str:
        tipo_full = tipo_esperado.split(" | ")[0].strip()
        return tipo_full.split("(")[0] if "(" in tipo_full else tipo_full

    def _executar_insercao(self, valores_validados: dict) -> None:
        if self.tabela_nome in self.TABELAS_ESTOQUE:
            operacoes.registrar_movimentacao_estoque(self.tabela_nome, valores_validados)
            return

        if self.tabela_nome == "ENDERECO":
            self._inserir_endereco_com_vinculo(valores_validados)
            return

        operacoes.insert([self.tabela_nome], [valores_validados])

    def _executar_atualizacao(self, valores_validados: dict) -> None:
        chave_primaria = self.dados_iniciais[0]

        if chave_primaria not in valores_validados:
            raise ValueError(f"Chave primária '{chave_primaria}' não encontrada no formulário.")

        operacoes.update(
            self.tabela_nome,
            valores_validados,
            {chave_primaria: valores_validados[chave_primaria]}
        )

    def _inserir_endereco_com_vinculo(self, valores_validados: dict) -> None:
        tipo_pessoa = self.query_one("#clienteouForn", Select).value
        id_pessoa = self.query_one("#IDconexaoEnd", Select).value

        if tipo_pessoa == Select.BLANK or id_pessoa == Select.BLANK:
            raise ValueError("Selecione para quem é este endereço e a pessoa específica.")

        if tipo_pessoa == "FORNECEDOR":
            operacoes.insert(
                ["ENDERECO", "ENDERECOFORNEC"],
                [
                    valores_validados,
                    {
                        "IDEndereco": valores_validados["IDEndereco"],
                        "IDForn": int(id_pessoa),
                    }
                ]
            )

        elif tipo_pessoa == "CLIENTE":
            operacoes.insert(
                ["ENDERECO", "ENDERECOCLIENTE"],
                [
                    valores_validados,
                    {
                        "IDEndereco": valores_validados["IDEndereco"],
                        "IDCliente": int(id_pessoa),
                    }
                ]
            )

        else:
            raise ValueError("Tipo de pessoa inválido para endereço.")

    @on(Select.Changed, "#clienteouForn")
    def atualizar_select_pessoa(self, event: Select.Changed) -> None:
        select_conexao = self.query_one("#IDconexaoEnd", Select)

        if event.value == Select.BLANK:
            self._limpar_select_pessoa(select_conexao)
            return

        tipo_escolhido = event.value

        try:
            registros = self._buscar_pessoas_para_endereco(tipo_escolhido)
            self._atualizar_opcoes_pessoa(select_conexao, tipo_escolhido, registros)

        except Exception as erro:
            self._limpar_select_pessoa(select_conexao)
            self.app.notify(f"Erro ao buscar pessoas: {erro}", severity="error")

    def _limpar_select_pessoa(self, select_conexao: Select) -> None:
        select_conexao.set_options([])
        select_conexao.disabled = True
        select_conexao.prompt = "Aguardando seleção acima..."

    def _buscar_pessoas_para_endereco(self, tipo_escolhido: str):
        if tipo_escolhido == "FORNECEDOR":
            return operacoes.select(
                "FORNECEDOR",
                cols="IDForn, NomeForn",
                order_by="IDForn"
            )

        if tipo_escolhido == "CLIENTE":
            return operacoes.select(
                "CLIENTE",
                cols="IDCliente, NomeCliente",
                order_by="IDCliente"
            )

        raise ValueError("Tipo inválido. Use CLIENTE ou FORNECEDOR.")

    def _atualizar_opcoes_pessoa(self, select_conexao: Select, tipo_escolhido: str, registros) -> None:
        if registros:
            opcoes = [
                (f"{registro[1]} (ID: {registro[0]})", str(registro[0]))
                for registro in registros
            ]
            select_conexao.set_options(opcoes)
            select_conexao.disabled = False
            select_conexao.prompt = f"Selecione o {tipo_escolhido.capitalize()}"

        else:
            select_conexao.set_options([])
            select_conexao.disabled = True
            select_conexao.prompt = f"Nenhum {tipo_escolhido.capitalize()} cadastrado"