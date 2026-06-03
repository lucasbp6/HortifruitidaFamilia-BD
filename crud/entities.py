#define as classes de dados para facilitar a manipulação dos dados e a integração com o banco de dados

class Categoria:
    def __init__(self, id_cat, nome_cat, id_cat_pai=None):
        self.id_cat = id_cat
        self.nome_cat = nome_cat
        self.id_cat_pai = id_cat_pai

class UnidadeMedida:
    def __init__(self, id_unidade, nome_unidade, sigla_unidade):
        self.id_unidade = id_unidade
        self.nome_unidade = nome_unidade
        self.sigla_unidade = sigla_unidade

class Fornecedor:
    def __init__(self, id_forn, nome_forn, cnpj_forn):
        self.id_forn = id_forn
        self.nome_forn = nome_forn
        self.cnpj_forn = cnpj_forn

class Cliente:
    def __init__(self, id_cliente, nome_cliente, data_nasc_cliente, cpf_cliente):
        self.id_cliente = id_cliente
        self.nome_cliente = nome_cliente
        self.data_nasc_cliente = data_nasc_cliente
        self.cpf_cliente = cpf_cliente
        
class Vendedor:
    def __init__(self, id_vend, nome_vend,data_nasc_vend, cel_vend, cpf_vend):
        self.id_vend = id_vend
        self.nome_vend = nome_vend
        self.data_nasc_vend = data_nasc_vend
        self.cel_vend = cel_vend
        self.cpf_vend = cpf_vend

class Produto:
    def __init__(self, id_prod, nome_prod, preco_venda_prod, estoque_atual_prod, preco_custo_prod, id_unidade, id_cat, descricao_prod=None):
        self.id_prod = id_prod
        self.nome_prod = nome_prod
        self.preco_venda_prod = preco_venda_prod
        self.estoque_atual_prod = estoque_atual_prod
        self.preco_custo_prod = preco_custo_prod
        self.id_unidade = id_unidade
        self.id_cat = id_cat
        self.descricao_prod = descricao_prod

class OperacaoCaixa:
    def __init__(self, id_operacao, data_op_aber, valor_op_aber, data_op_fecham, valor_op_fecham, saldo_op, id_vend, id_caixa):
        self.id_operacao = id_operacao
        self.data_op_aber = data_op_aber
        self.valor_op_aber = valor_op_aber
        self.data_op_fecham = data_op_fecham
        self.valor_op_fecham = valor_op_fecham
        self.saldo_op = saldo_op
        self.id_vend = id_vend
        self.id_caixa = id_caixa

class Pedido:
    def __init__(self, id_pedido, valor_total_pedido, data_pedido, tipo_pedido, id_cliente, id_operacao):
        self.id_pedido = id_pedido
        self.valor_total_pedido = valor_total_pedido
        self.data_pedido = data_pedido
        self.tipo_pedido = tipo_pedido
        self.id_cliente = id_cliente
        self.id_operacao = id_operacao

class ItemPedido:
    def __init__(self, id_prod, id_pedido, qtd_item, preco_un, desc_item=0.0):
        self.id_prod = id_prod
        self.id_pedido = id_pedido
        self.qtd_item = qtd_item
        self.preco_un = preco_un
        self.desc_item = desc_item
        
class Endereço:
    def __init__(self, id_endereco, rua, numero, complemento, bairro, cidade, estado, cep):
        self.id_endereco = id_endereco
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        
class Caixa:
    def __init__(self, id_caixa, tipo_caixa):
        self.id_caixa = id_caixa
        self.tipo_caixa = tipo_caixa

class PerdaDeEstoque:
    def __init__(self, id_perda, data_perda, qtd_perda, motivo_perda, id_prod):
        self.id_perda = id_perda
        self.data_perda = data_perda
        self.qtd_perda = qtd_perda
        self.motivo_perda = motivo_perda
        self.id_prod = id_prod
        
class EntradaDeEstoque:
    def __init__(self, id_entrada, data_entrada, qtd_entrada, id_prod, id_forn, preco_entrada):
        self.id_entrada = id_entrada
        self.data_entrada = data_entrada
        self.qtd_entrada = qtd_entrada
        self.id_prod = id_prod
        self.preco_entrada = preco_entrada
        self.id_forn = id_forn

