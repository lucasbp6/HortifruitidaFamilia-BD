TABELAS = {
    "CATEGORIA": (
        ("IDCat", "NomeCat", "IDCatPai"),
        ("int", "str(20)", "int | None")
    ),
    "UNIDADEMEDIDA": (          
        ("IDUnidade", "NomeUnidade", "SiglaUnidade"),
        ("int", "str(20)", "str(5)")
    ),
    "PRODUTO": (
        ("IDProd", "NomeProd", "DescricaoProd", "PrecoVendaProd", "EstoqueAtualProd", "PrecoCustoProd", "IDUnidade", "IDCat"),
        ("int", "str(20)", "str(100) | None", "float", "float", "float", "int", "int")
    ),
    "FORNECEDOR": (
        ("IDForn", "NomeForn", "CNPJForn"),
        ("int", "str(50)", "char(14)")
    ),
    "CLIENTE": (
        ("IDCliente", "NomeCliente", "DataNascCliente", "CPFCliente"),
        ("int", "str(50)", "date", "char(11)")
    ),
    "VENDEDOR": (
        ("IDVend", "NomeVend", "CPFVend", "DataNascVend", "CelVend", "SalarioVend"),
        ("int", "str(50)", "char(11)", "date", "str(15)", "float")
    ),
    "CAIXA": (
        ("IDCaixa", "TipoCaixa"),
        ("int", "str(20)")
    ),
    "OPERACAOCAIXA": (
        ("IDOperacao", "DataOpAber", "ValorOpAber", "DataOpFecham", "ValorOpFecham", "SaldoOp", "IDVend", "IDCaixa"),
        ("int", "datetime", "float", "datetime", "float", "float", "int", "int")
    ),
    "PEDIDO": (
        ("IDPedido", "ValorTotalPedido", "DataPedido", "TipoPedido", "IDCliente", "IDOperacao"),
        ("int", "float", "datetime", "str(20)", "int", "int")
    ),
    "PAGAMENTO": (
        ("IDPag", "MetodoPag", "ValorPag", "DataPag", "IDPedido"),
        ("int", "str(20)", "float", "datetime", "int")
    ),
    "ITEMPEDIDO": (
        ("IDProd", "IDPedido", "QtdItem", "DescItem", "PrecoUn"),
        ("int", "int", "float", "float | None", "float")
    ),
    "PERDAESTOQUE": (
        ("IDPerda", "DataPerda", "QtdPerda", "MotivoPerda", "ValorUnPerda", "IDProd"),
        ("int", "datetime", "float", "str(100)", "float", "int")
    ),
    "ENTRADAESTOQUE": (
        ("IDEntrada", "IDForn", "IDProd", "EntradaData", "EntradaQtd", "EntradaPreco"),
        ("int", "int", "int", "datetime", "float", "float")
    ),
    "ENDERECO": (
        ("IDEndereco", "RuaEnd", "NumeroEnd", "ComplemEnd", "CEPEnd", "BairroEnd", "CidadeEnd", "EstadoEnd", "PaisEnd"),
        ("int", "str(35)", "int", "str(20) | None", "char(8)", "str(20)", "str(25)", "char(2)", "str(20)")
    ),
    "ENDERECOCLIENTE": (
        ("IDCliente", "IDEndereco"),
        ("int", "int")
    ),
    "ENDERECOVENDEDOR": (
        ("IDVend", "IDEndereco"),
        ("int", "int")
    ),
    "ENDERECOFORNEC": (
        ("IDForn", "IDEndereco"),
        ("int", "int")
    ),
    "FORNECEDOR_CELFORN": (
        ("CelForn", "IDForn"),
        ("str(15)", "int")
    ),
    "CLIENTE_CELCLIENTE": (
        ("CelCliente", "IDCliente"),
        ("str(15)", "int")
    )
}