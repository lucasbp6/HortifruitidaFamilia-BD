from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Button, Static, DataTable, Input, ContentSwitcher, Select
from textual.containers import Vertical

import entities
import operacoes
from datetime import datetime

from modals.delete_modal import DeleteByIdView
from modals.update_select_modal import UpdateSelectView
from modals.formulario_modal import FormularioModal
from modals.formulario_pessoa_composto import FormularioPessoaComposto


class OperationScreen(Screen):
    """Tela principal de operações do sistema.

    Esta tela concentra os fluxos de cadastro, atualização, deleção,
    abertura de caixa, venda e fechamento de caixa.
    """

    TABELAS_CADASTRO = [
        ("Add Produto", "PRODUTO"),
        ("Add Categoria", "CATEGORIA"),
        ("Add entrada de estoque", "ENTRADAESTOQUE"),
        ("Add Perda estoque", "PERDAESTOQUE"),
        ("Add Cliente", "CLIENTE"),
        ("Add Fornecedor", "FORNECEDOR"),
        ("Add Vendedor", "VENDEDOR"),
        ("Add Unidade", "UNIDADEMEDIDA"),
        ("Add Caixa", "CAIXA"),
        ("Add Endereco", "ENDERECO"),
    ]

    TABELAS_DELETE = [
        ("Del Produto", "PRODUTO"),
        ("Del Categoria", "CATEGORIA"),
        ("Del Cliente", "CLIENTE"),
        ("Del Vendedor", "VENDEDOR"),
        ("Del Unidade", "UNIDADEMEDIDA"),
        ("Del Caixa", "CAIXA"),
    ]

    TABELAS_UPDATE = [
        ("Att Produto", "PRODUTO"),
        ("Att Categoria", "CATEGORIA"),
        ("Att estoque", "ENTRADAESTOQUE"),
        ("Att Perda", "PERDAESTOQUE"),
        ("Att Cliente", "CLIENTE"),
        ("Att Fornecedor", "FORNECEDOR"),
        ("Att Vendedor", "VENDEDOR"),
        ("Att Unidade", "UNIDADEMEDIDA"),
        ("Att Caixa", "CAIXA"),
        ("Att Endereco", "ENDERECO"),
    ]

    PESSOAS_CADASTRO_COMPOSTO = {"CLIENTE", "VENDEDOR", "FORNECEDOR"}

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
                yield Button("Voltar para o Menu", id="btn-voltar-menu", variant="error")
                for texto, tabela in self.TABELAS_CADASTRO:
                    yield Button(texto, id=f"btn-ad-{tabela}")

            with Vertical(id="tela-identificar"):
                yield Static("Identifique o Vendedor e o Caixa:")
                yield Select([], prompt="Selecione o Vendedor", id="vendedor-select")
                yield Select([], prompt="Selecione o Caixa", id="caixa-select")
                yield Input(placeholder="Valor Inicial de Abertura (Ex: 150.00)", id="valor-abertura")
                yield Button("Abrir Caixa e Prosseguir", id="btn-prosseg", variant="success")
                yield Button("Voltar para o Menu", id="btn-voltar-menu", variant="error")

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
                yield Select(
                    [("Dinheiro", "Dinheiro"), ("Débito", "Débito"), ("Crédito", "Crédito"), ("Pix", "Pix")],
                    prompt="Selecione Forma de pagamento",
                    id="fin-pagto",
                )
                yield Select(
                    [("Venda", "Venda"), ("Delivery", "Delivery")],
                    prompt="Selecione o tipo do pedido",
                    id="fin-tipo",
                )
                yield Button("Finalizar Venda", id="btn-final", variant="success")
                yield Button("Cancelar Venda", id="btn-cancelar-venda", variant="error")

            with Vertical(id="tela-deletar"):
                yield Static("Escolha o que deseja deletar:")
                yield Button("Voltar para o Menu", id="btn-voltar-menu", variant="error")
                for texto, tabela in self.TABELAS_DELETE:
                    yield Button(texto, id=f"btn-dl-{tabela}")

            with Vertical(id="tela-update"):
                yield Static("Escolha o que deseja atualizar:")
                yield Button("Voltar para o Menu", id="btn-voltar-menu", variant="error")
                for texto, tabela in self.TABELAS_UPDATE:
                    yield Button(texto, id=f"btn-up-{tabela}")

        yield Footer()

    def on_mount(self) -> None:
        self._configurar_tabela_carrinho()
        self._configurar_tabela_produtos()
        self._carregar_produtos()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id or ""

        if button_id == "btn-cadastro":
            self._mostrar_tela("tela-cadastro")
        elif button_id == "btn-vender":
            self._preparar_abertura_caixa()
        elif button_id == "btn-deletar":
            self._mostrar_tela("tela-deletar")
        elif button_id == "btn-update":
            self._mostrar_tela("tela-update")
        elif button_id == "btn-voltar-menu":
            self._mostrar_tela("menu-opcoes")
        elif button_id == "btn-prosseg":
            self._abrir_caixa()
        elif button_id == "btn-addprod":
            self._adicionar_produto_ao_carrinho()
        elif button_id == "btn-finalizar":
            self._preparar_finalizacao_venda()
        elif button_id == "btn-final":
            self._finalizar_venda()
        elif button_id == "btn-fecharcx":
            self._fechar_caixa()
        elif button_id == "btn-cancelar-venda":
            self._cancelar_venda_atual()
        elif button_id.startswith("btn-ad-"):
            self._abrir_modal_cadastro(button_id[7:])
        elif button_id.startswith("btn-up-"):
            self._abrir_modal_update(button_id[7:])
        elif button_id.startswith("btn-dl-"):
            self._abrir_modal_delete(button_id[7:])

    def _mostrar_tela(self, tela: str) -> None:
        self.query_one("#meu-switcher", ContentSwitcher).current = tela

    def _configurar_tabela_carrinho(self) -> None:
        carrinho = self.query_one("#carrinho-lista", DataTable)
        carrinho.add_columns("ID", "Produto", "Qtd", "Total (R$)")
        carrinho.styles.height = 10

    def _configurar_tabela_produtos(self) -> None:
        produtos = self.query_one("#produtos-lista", DataTable)
        produtos.styles.height = 15
        produtos.add_columns(*entities.TABELAS["PRODUTO"][0])

    def _carregar_produtos(self) -> None:
        produtos = self.query_one("#produtos-lista", DataTable)
        produtos.clear()

        values = operacoes.select("PRODUTO", order_by="IDProd")
        if values:
            produtos.add_rows(values)

    def _carregar_select(self, select_id: str, tabela: str, cols: str) -> None:
        registros = operacoes.select(tabela, cols=cols, order_by=cols.split(",")[0].strip())
        select = self.query_one(select_id, Select)

        if registros:
            select.set_options([(str(r[1]), str(r[0])) for r in registros])
        else:
            select.set_options([])

    def _preparar_abertura_caixa(self) -> None:
        try:
            self._carregar_select("#vendedor-select", "VENDEDOR", "IDVend, NomeVend")
            self._carregar_select("#caixa-select", "CAIXA", "IDCaixa, TipoCaixa")
            self._mostrar_tela("tela-identificar")
        except Exception as erro:
            self.app.notify(f"Erro ao carregar dados de abertura: {erro}", severity="error")

    def _abrir_caixa(self) -> None:
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
            self.total = 0.0
            self.total_venda = 0.0
            self.carrinho_itens = []

            self.app.notify(f"Caixa aberto com sucesso! Operação #{id_operacao}", severity="success")
            self._mostrar_tela("tela-venda")

        except ValueError as erro:
            self.app.notify(str(erro), severity="error")
        except Exception as erro:
            self.app.notify(f"Erro ao abrir caixa: {erro}", severity="error")

    def _adicionar_produto_ao_carrinho(self) -> None:
        id_prod = self.query_one("#venda-input-id", Input).value.strip()
        qtd_str = self.query_one("#venda-input-qtd", Input).value.strip()

        if not id_prod or not qtd_str:
            self.app.notify("Preencha ID e Quantidade!", severity="error")
            return

        try:
            qtd = float(qtd_str.replace(",", "."))
            if qtd <= 0:
                raise ValueError("A quantidade deve ser positiva.")

            produto = operacoes.select("PRODUTO", where={"IDProd": int(id_prod)})
            if not produto:
                raise ValueError(f"Produto de ID {id_prod} não encontrado.")

            linha_produto = produto[0]
            nome_prod = linha_produto[1]
            preco = float(linha_produto[3])
            subtotal = preco * qtd

            self.carrinho_itens.append({
                "id": int(id_prod),
                "nome": nome_prod,
                "qtd": qtd,
                "preco": preco,
            })
            self.total_venda += subtotal

            carrinho = self.query_one("#carrinho-lista", DataTable)
            carrinho.add_row(str(id_prod), nome_prod, str(qtd), f"R$ {subtotal:.2f}")

            self.query_one("#venda-input-id", Input).value = ""
            self.query_one("#venda-input-qtd", Input).value = "1"
            self.query_one("#venda-input-id", Input).focus()

            self.app.notify(f"{nome_prod} adicionado!", severity="success")

        except ValueError as erro:
            self.app.notify(str(erro), severity="error")
        except Exception as erro:
            self.app.notify(f"Erro ao adicionar produto: {erro}", severity="error")

    def _preparar_finalizacao_venda(self) -> None:
        if not self.ident:
            self.app.notify("Abra uma operação de caixa antes de vender.", severity="error")
            return

        if not self.carrinho_itens:
            self.app.notify("O carrinho está vazio!", severity="error")
            return

        try:
            self._carregar_select("#fin-cliente", "CLIENTE", "IDCliente, NomeCliente")
            self._mostrar_tela("tela-fin")
        except Exception as erro:
            self.app.notify(f"Erro ao carregar clientes: {erro}", severity="error")

    def _finalizar_venda(self) -> None:
        if not self.carrinho_itens:
            self.app.notify("O carrinho está vazio!", severity="error")
            return

        id_cliente = self.query_one("#fin-cliente", Select).value
        forma_pgt = self.query_one("#fin-pagto", Select).value
        tipo = self.query_one("#fin-tipo", Select).value

        if id_cliente == Select.BLANK or forma_pgt == Select.BLANK or tipo == Select.BLANK:
            self.app.notify("Selecione o Cliente, Forma de Pagamento e Tipo de Pedido!", severity="error")
            return

        try:
            id_pedido, _ = operacoes.finalizar_venda_transacao(
                valor_total=self.total_venda,
                tipo_pedido=tipo,
                id_cliente=int(id_cliente),
                id_operacao=int(self.ident),
                metodo_pagamento=forma_pgt,
                itens=self.carrinho_itens,
            )

            self.total += self.total_venda
            self._limpar_venda_atual()
            self._limpar_select_finalizacao()
            self._carregar_produtos()

            self.app.notify(f"Venda finalizada com sucesso! Pedido #{id_pedido}", severity="success")
            self._mostrar_tela("tela-venda")

        except Exception as erro:
            self.app.notify(f"Erro ao finalizar venda: {erro}", severity="error")

    def _fechar_caixa(self) -> None:
        if not self.ident:
            self.app.notify("Não há nenhum caixa aberto!", severity="error")
            return

        if self.carrinho_itens:
            self.app.notify("Finalize ou cancele a venda atual antes de fechar o caixa!", severity="warning")
            return

        try:
            operacoes.update(
                "OPERACAOCAIXA",
                data={
                    "DataOpFecham": datetime.now(),
                    "ValorOpFecham": self.total + self.inicial,
                    "SaldoOp": self.total,
                },
                where={"IDOperacao": self.ident},
            )

            id_operacao = self.ident
            self._limpar_operacao_caixa()
            self.app.notify(f"Caixa (Operação #{id_operacao}) fechado com sucesso!", severity="success")
            self._mostrar_tela("menu-opcoes")

        except Exception as erro:
            self.app.notify(f"Erro ao fechar o caixa: {erro}", severity="error")

    def _cancelar_venda_atual(self) -> None:
        self._limpar_venda_atual()
        self._limpar_select_finalizacao()
        self.app.notify("Venda cancelada.", severity="warning")
        self._mostrar_tela("tela-venda")

    def _limpar_venda_atual(self) -> None:
        self.carrinho_itens = []
        self.total_venda = 0.0
        self.query_one("#carrinho-lista", DataTable).clear()

    def _limpar_select_finalizacao(self) -> None:
        self.query_one("#fin-cliente", Select).clear()
        self.query_one("#fin-pagto", Select).clear()
        self.query_one("#fin-tipo", Select).clear()

    def _limpar_operacao_caixa(self) -> None:
        self.ident = None
        self.inicial = 0.0
        self.total = 0.0
        self.total_venda = 0.0
        self.carrinho_itens = []

        self.query_one("#carrinho-lista", DataTable).clear()
        self.query_one("#vendedor-select", Select).clear()
        self.query_one("#caixa-select", Select).clear()
        self.query_one("#valor-abertura", Input).clear()

    def _abrir_modal_cadastro(self, tabela_nome: str) -> None:
        if tabela_nome in self.PESSOAS_CADASTRO_COMPOSTO:
            self.app.push_screen(FormularioPessoaComposto(tabela_nome))
        else:
            self.app.push_screen(FormularioModal(tabela_nome, "inserir", entities.TABELAS[tabela_nome]))

    def _abrir_modal_update(self, tabela_nome: str) -> None:
        self.app.push_screen(UpdateSelectView(tabela_nome))

    def _abrir_modal_delete(self, tabela_nome: str) -> None:
        self.app.push_screen(DeleteByIdView(tabela_nome))