# Define as funções geradoras de dicionários para facilitar a manipulação dos dados e a integração com o banco de dados

from typing import Any
from datetime import date, datetime

TABELAS = {
    "Categoria": (
        ("id_cat", "nome_cat", "id_cat_pai"),
        ("int", "str", "int | None")
    ),
    "UnidadeMedida": (          
        ("id_unidade", "nome_unidade", "sigla_unidade"),
        ("int", "str", "str")
    ),                                                                                                                                                                                                                                                        
    "Fornecedor": (
        ("id_forn", "nome_forn", "cnpj_forn"),
        ("int", "str", "str")
    ),
    "Cliente": (
        ("id_cliente", "nome_cliente", "data_nasc_cliente", "cpf_cliente"),
        ("int", "str", "date", "str")
    ),
    "Vendedor": (
        ("id_vend", "nome_vend", "data_nasc_vend", "cel_vend", "cpf_vend"),
        ("int", "str", "date", "str", "str")
    ),
    "Produto": (
        ("id_prod", "nome_prod", "preco_venda_prod", "estoque_atual_prod", "preco_custo_prod", "id_unidade", "id_cat", "descricao_prod"),
        ("int", "str", "float", "float", "float", "int", "int", "str | None")
    ),
    "OperacaoCaixa": (
        ("id_operacao", "data_op_aber", "valor_op_aber", "data_op_fecham", "valor_op_fecham", "saldo_op", "id_vend", "id_caixa"),
        ("int", "datetime", "float", "datetime", "float", "float", "int", "int")
    ),
    "Pedido": (
        ("id_pedido", "valor_total_pedido", "data_pedido", "tipo_pedido", "id_cliente", "id_operacao"),
        ("int", "float", "datetime", "str", "int", "int")
    ),
    "ItemPedido": (
        ("id_prod", "id_pedido", "qtd_item", "preco_un", "desc_item"),
        ("int", "int", "float", "float", "float")
    ),
    "Endereco": (
        ("id_endereco", "rua", "numero", "complemento", "bairro", "cidade", "estado", "cep"),
        ("int", "str", "int", "str | None", "str", "str", "str", "str")
    ),
    "Caixa": (
        ("id_caixa", "tipo_caixa"),
        ("int", "str")
    ),
    "PerdaDeEstoque": (
        ("id_perda", "data_perda", "qtd_perda", "motivo_perda", "id_prod"),
        ("int", "datetime", "float", "str", "int")
    ),
    "EntradaDeEstoque": (
        ("id_entrada", "data_entrada", "qtd_entrada", "id_prod", "id_forn", "preco_entrada"),
        ("int", "datetime", "float", "int", "int", "float")
    )
}

def criar_categoria(id_cat: int, nome_cat: str, id_cat_pai: int | None = None) -> dict[str, Any]:
    return {
        "id_cat": id_cat,
        "nome_cat": nome_cat,
        "id_cat_pai": id_cat_pai
    }

def criar_unidade_medida(id_unidade: int, nome_unidade: str, sigla_unidade: str) -> dict[str, Any]:
    return {
        "id_unidade": id_unidade,
        "nome_unidade": nome_unidade,
        "sigla_unidade": sigla_unidade
    }

def criar_fornecedor(id_forn: int, nome_forn: str, cnpj_forn: str) -> dict[str, Any]:
    return {
        "id_forn": id_forn,
        "nome_forn": nome_forn,
        "cnpj_forn": cnpj_forn
    }

def criar_cliente(id_cliente: int, nome_cliente: str, data_nasc_cliente: date | str, cpf_cliente: str) -> dict[str, Any]:
    return {
        "id_cliente": id_cliente,
        "nome_cliente": nome_cliente,
        "data_nasc_cliente": data_nasc_cliente,
        "cpf_cliente": cpf_cliente
    }
        
def criar_vendedor(id_vend: int, nome_vend: str, data_nasc_vend: date | str, cel_vend: str, cpf_vend: str) -> dict[str, Any]:
    return {
        "id_vend": id_vend,
        "nome_vend": nome_vend,
        "data_nasc_vend": data_nasc_vend,
        "cel_vend": cel_vend,
        "cpf_vend": cpf_vend
    }

def criar_produto(id_prod: int, nome_prod: str, preco_venda_prod: float, estoque_atual_prod: float, preco_custo_prod: float, id_unidade: int, id_cat: int, descricao_prod: str | None = None) -> dict[str, Any]:
    return {
        "id_prod": id_prod,
        "nome_prod": nome_prod,
        "preco_venda_prod": preco_venda_prod,
        "estoque_atual_prod": estoque_atual_prod,
        "preco_custo_prod": preco_custo_prod,
        "id_unidade": id_unidade,
        "id_cat": id_cat,
        "descricao_prod": descricao_prod
    }

def criar_operacao_caixa(id_operacao: int, data_op_aber: datetime | str, valor_op_aber: float, data_op_fecham: datetime | str | None, valor_op_fecham: float | None, saldo_op: float, id_vend: int, id_caixa: int) -> dict[str, Any]:
    return {
        "id_operacao": id_operacao,
        "data_op_aber": data_op_aber,
        "valor_op_aber": valor_op_aber,
        "data_op_fecham": data_op_fecham,
        "valor_op_fecham": valor_op_fecham,
        "saldo_op": saldo_op,
        "id_vend": id_vend,
        "id_caixa": id_caixa
    }

def criar_pedido(id_pedido: int, valor_total_pedido: float, data_pedido: datetime | str, tipo_pedido: str, id_cliente: int, id_operacao: int) -> dict[str, Any]:
    return {
        "id_pedido": id_pedido,
        "valor_total_pedido": valor_total_pedido,
        "data_pedido": data_pedido,
        "tipo_pedido": tipo_pedido,
        "id_cliente": id_cliente,
        "id_operacao": id_operacao
    }

def criar_item_pedido(id_prod: int, id_pedido: int, qtd_item: float, preco_un: float, desc_item: float = 0.0) -> dict[str, Any]:
    return {
        "id_prod": id_prod,
        "id_pedido": id_pedido,
        "qtd_item": qtd_item,
        "preco_un": preco_un,
        "desc_item": desc_item
    }
        
def criar_endereco(id_endereco: int, rua: str, numero: str, complemento: str | None, bairro: str, cidade: str, estado: str, cep: str) -> dict[str, Any]:
    return {
        "id_endereco": id_endereco,
        "rua": rua,
        # 'numero' como string, pois pode existir "S/N", "123B", etc.
        "numero": numero, 
        "complemento": complemento,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
        "cep": cep
    }
        
def criar_caixa(id_caixa: int, tipo_caixa: str) -> dict[str, Any]:
    return {
        "id_caixa": id_caixa,
        "tipo_caixa": tipo_caixa
    }

def criar_perda_estoque(id_perda: int, data_perda: date | str, qtd_perda: float, motivo_perda: str, id_prod: int) -> dict[str, Any]:
    return {
        "id_perda": id_perda,
        "data_perda": data_perda,
        "qtd_perda": qtd_perda,
        "motivo_perda": motivo_perda,
        "id_prod": id_prod
    }
        
def criar_entrada_estoque(id_entrada: int, data_entrada: date | str, qtd_entrada: float, id_prod: int, id_forn: int, preco_entrada: float) -> dict[str, Any]:
    return {
        "id_entrada": id_entrada,
        "data_entrada": data_entrada,
        "qtd_entrada": qtd_entrada,
        "id_prod": id_prod,
        "preco_entrada": preco_entrada,
        "id_forn": id_forn
    }

