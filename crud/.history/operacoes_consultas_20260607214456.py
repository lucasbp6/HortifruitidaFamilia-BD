from conexao import conexao


SCHEMA_PADRAO = "hortifruti"
TIPOS_PESSOA_VALIDOS = {"CLIENTE", "FORNECEDOR", "VENDEDOR", "TODOS"}


def select_enderecos_por_tipo(
    tipo_pessoa: str = "TODOS",
    schema: str = SCHEMA_PADRAO
):
    """
    Retorna endereços vinculados a clientes, fornecedores e/ou vendedores.

    tipo_pessoa pode ser:
    - CLIENTE
    - FORNECEDOR
    - VENDEDOR
    - TODOS
    """

    tipo_pessoa = (tipo_pessoa or "TODOS").upper()

    if tipo_pessoa not in TIPOS_PESSOA_VALIDOS:
        raise ValueError(
            "Tipo de pessoa inválido. Use CLIENTE, FORNECEDOR, VENDEDOR ou TODOS."
        )

    queries = {
        "CLIENTE": f"""
            SELECT
                e.*,
                'Cliente' AS TipoVinculo,
                c.NomeCliente AS Proprietario
            FROM {schema}.ENDERECO e
            JOIN {schema}.ENDERECOCLIENTE ec
                ON e.IDEndereco = ec.IDEndereco
            JOIN {schema}.CLIENTE c
                ON ec.IDCliente = c.IDCliente
        """,
        "FORNECEDOR": f"""
            SELECT
                e.*,
                'Fornecedor' AS TipoVinculo,
                f.NomeForn AS Proprietario
            FROM {schema}.ENDERECO e
            JOIN {schema}.ENDERECOFORNEC ef
                ON e.IDEndereco = ef.IDEndereco
            JOIN {schema}.FORNECEDOR f
                ON ef.IDForn = f.IDForn
        """,
        "VENDEDOR": f"""
            SELECT
                e.*,
                'Vendedor' AS TipoVinculo,
                v.NomeVend AS Proprietario
            FROM {schema}.ENDERECO e
            JOIN {schema}.ENDERECOVENDEDOR ev
                ON e.IDEndereco = ev.IDEndereco
            JOIN {schema}.VENDEDOR v
                ON ev.IDVend = v.IDVend
        """,
    }

    if tipo_pessoa == "TODOS":
        query = " UNION ALL ".join(queries.values())
    else:
        query = queries[tipo_pessoa]

    query += " ORDER BY TipoVinculo, Proprietario, IDEndereco"

    conn = conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    except Exception as erro:
        print(f"Erro na consulta de endereços ({tipo_pessoa}): {erro}")
        raise

    finally:
        conn.close()


def select_telefones_geral(schema: str = SCHEMA_PADRAO):
    """
    Retorna todos os telefones vinculados a clientes, fornecedores e vendedores.

    Cliente e fornecedor usam tabelas associativas.
    Vendedor possui telefone direto na tabela VENDEDOR.
    """

    query_cliente = f"""
        SELECT
            cc.CelCliente AS Telefone,
            'Cliente' AS TipoVinculo,
            c.NomeCliente AS Proprietario
        FROM {schema}.CLIENTE_CELCLIENTE cc
        JOIN {schema}.CLIENTE c
            ON cc.IDCliente = c.IDCliente
    """

    query_fornecedor = f"""
        SELECT
            fc.CelForn AS Telefone,
            'Fornecedor' AS TipoVinculo,
            f.NomeForn AS Proprietario
        FROM {schema}.FORNECEDOR_CELFORN fc
        JOIN {schema}.FORNECEDOR f
            ON fc.IDForn = f.IDForn
    """

    query_vendedor = f"""
        SELECT
            CelVend AS Telefone,
            'Vendedor' AS TipoVinculo,
            NomeVend AS Proprietario
        FROM {schema}.VENDEDOR
        WHERE CelVend IS NOT NULL
    """

    query = f"""
        {query_cliente}
        UNION ALL
        {query_fornecedor}
        UNION ALL
        {query_vendedor}
        ORDER BY TipoVinculo, Proprietario, Telefone
    """

    conn = conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    except Exception as erro:
        print(f"Erro na consulta de telefones: {erro}")
        raise

    finally:
        conn.close()