TABELAS = {
    "Categoria": (
        ("id_cat", "nome_cat", "id_cat_pai"),
        ("int", "str(20)", "int | None")
    ),
    "UnidadeMedida": (          
        ("id_unidade", "nome_unidade", "sigla_unidade"),
        ("int", "str(20)", "str(5)")
    ),                                                                                                                                                                                                                                                        
    "Fornecedor": (
        ("id_forn", "nome_forn", "cnpj_forn"),
        ("int", "str(50)", "char(14)")
    ),
    "Cliente": (
        ("id_cliente", "nome_cliente", "data_nasc_cliente", "cpf_cliente"),
        ("int", "str(50)", "date", "char(11)")
    ),
    "Vendedor": (
        ("id_vend", "nome_vend", "data_nasc_vend", "cel_vend", "cpf_vend"),
        ("int", "str(50)", "date", "str(15)", "char(11)")
    ),
    "Produto": (
        ("id_prod", "nome_prod", "preco_venda_prod", "estoque_atual_prod", "preco_custo_prod", "id_unidade", "id_cat", "descricao_prod"),
        ("int", "str(20)", "float", "float", "float", "int", "int", "str(100) | None")
    ),
    "OperacaoCaixa": (
        ("id_operacao", "data_op_aber", "valor_op_aber", "data_op_fecham", "valor_op_fecham", "saldo_op", "id_vend", "id_caixa"),
        ("int", "datetime", "float", "datetime", "float", "float", "int", "int")
    ),
    "Pedido": (
        ("id_pedido", "valor_total_pedido", "data_pedido", "tipo_pedido", "id_cliente", "id_operacao"),
        ("int", "float", "datetime", "str(20)", "int", "int")
    ),
    "ItemPedido": (
        ("id_prod", "id_pedido", "qtd_item", "preco_un", "desc_item"),
        ("int", "int", "float", "float", "float")
    ),
    "Endereco": (
        ("id_endereco", "rua", "numero", "complemento", "bairro", "cidade", "estado", "cep", "pais"),
        ("int", "str(35)", "int", "str(20) | None", "str(20)", "str(25)", "char(2)", "char(8)", "str(20)")
    ),
    "Caixa": (
        ("id_caixa", "tipo_caixa"),
        ("int", "str(20)")
    ),
    "PerdaDeEstoque": (
        ("id_perda", "data_perda", "qtd_perda", "motivo_perda", "id_prod"),
        ("int", "datetime", "float", "str(100)", "int")
    ),
    "EntradaDeEstoque": (
        ("id_entrada", "data_entrada", "qtd_entrada", "id_prod", "id_forn", "preco_entrada"),
        ("int", "datetime", "float", "int", "int", "float")
    )
}