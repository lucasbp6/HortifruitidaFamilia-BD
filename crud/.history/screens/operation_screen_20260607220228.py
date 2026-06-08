from datetime import datetime

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Button, Static, DataTable, Input, ContentSwitcher, Select
from textual.containers import Vertical

import entities
import operacoes

from modals.delete_modal import DeleteByIdView
from modals.update_select_modal import UpdateSelectView
from modals.formulario_modal import FormularioModal
from modals.formulario_pessoa_composto import FormularioPessoaComposto

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