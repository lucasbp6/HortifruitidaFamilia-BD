from conexao import conexao


SCHEMA_PADRAO = "hortifruti"


def _validar_identificador(nome: str, tipo: str = "identificador") -> str:
    """
    Valida nomes de schema, tabela e coluna usados diretamente no SQL.

    Observação:
    Valores continuam sendo enviados por placeholders (%s).
    Esta função protege apenas partes estruturais da query, como nomes de tabelas.
    """

    if not isinstance(nome, str) or not nome:
        raise ValueError(f"{tipo.capitalize()} inválido.")

    partes = nome.split(".")
    for parte in partes:
        if not parte.replace("_", "").isalnum():
            raise ValueError(f"{tipo.capitalize()} inválido: {nome}")

    return nome


def _montar_where(where: dict | None) -> tuple[str, list]:
    if not where:
        return "", []

    condicoes = []
    valores = []

    for coluna, valor in where.items():
        coluna = _validar_identificador(coluna, "coluna")
        condicoes.append(f"{coluna} = %s")
        valores.append(valor)

    return " WHERE " + " AND ".join(condicoes), valores


def insert(
    list_table_name: list[str],
    list_values: list[dict],
    schema: str = SCHEMA_PADRAO
) -> None:
    """
    Insere registros em uma ou mais tabelas dentro de uma única transação.
    """

    schema = _validar_identificador(schema, "schema")

    if len(list_table_name) != len(list_values):
        raise ValueError("A lista de tabelas e a lista de valores precisam ter o mesmo tamanho.")

    if not list_table_name:
        raise ValueError("Informe pelo menos uma tabela para inserção.")

    conn = conexao()
    try:
        with conn.cursor() as cur:
            for table_name, values in zip(list_table_name, list_values):
                table_name = _validar_identificador(table_name, "tabela")

                if not values:
                    raise ValueError(f"Não há valores para inserir em {table_name}.")

                campos = [_validar_identificador(campo, "coluna") for campo in values.keys()]
                valores = list(values.values())

                placeholders = ", ".join(["%s"] * len(campos))
                campos_str = ", ".join(campos)

                query = f"""
                    INSERT INTO {schema}.{table_name}
                    ({campos_str})
                    VALUES ({placeholders})
                """
                cur.execute(query, valores)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def select(
    table_name: str,
    cols: str | list[str] | tuple[str, ...] = "*",
    where: dict | None = None,
    schema: str = SCHEMA_PADRAO,
    order_by: str | None = None
):
    """
    Consulta registros de uma tabela.

    cols pode ser:
    - "*"
    - "IDProd, NomeProd"
    - ["IDProd", "NomeProd"]
    """

    schema = _validar_identificador(schema, "schema")
    table_name = _validar_identificador(table_name, "tabela")

    if isinstance(cols, (list, tuple)):
        cols_sql = ", ".join(_validar_identificador(col, "coluna") for col in cols)
    elif cols == "*":
        cols_sql = "*"
    else:
        cols_sql = cols

    where_sql, valores = _montar_where(where)

    query = f"SELECT {cols_sql} FROM {schema}.{table_name}{where_sql}"

    if order_by is not None:
        order_by = _validar_identificador(order_by, "coluna de ordenação")
        query += f" ORDER BY {order_by}"

    conn = conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(query, tuple(valores))
            return cur.fetchall()

    except Exception as erro:
        print(f"Erro no SELECT em {schema}.{table_name}: {erro}")
        raise

    finally:
        conn.close()


def delete(
    table_name: str,
    where: dict,
    schema: str = SCHEMA_PADRAO
) -> int:
    """
    Remove registros de uma tabela.

    Por segurança, where é obrigatório.
    """

    schema = _validar_identificador(schema, "schema")
    table_name = _validar_identificador(table_name, "tabela")

    if not where:
        raise ValueError("DELETE sem WHERE bloqueado por segurança.")

    where_sql, valores = _montar_where(where)
    query = f"DELETE FROM {schema}.{table_name}{where_sql}"

    conn = conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(query, tuple(valores))
            linhas_afetadas = cur.rowcount

        conn.commit()
        return linhas_afetadas

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def update(
    table_name: str,
    data: dict,
    where: dict,
    schema: str = SCHEMA_PADRAO
) -> int:
    """
    Atualiza registros de uma tabela.

    Por segurança, where é obrigatório.
    """

    schema = _validar_identificador(schema, "schema")
    table_name = _validar_identificador(table_name, "tabela")

    if not data:
        raise ValueError("UPDATE sem dados para atualizar.")

    if not where:
        raise ValueError("UPDATE sem WHERE bloqueado por segurança.")

    valores = []

    set_condicoes = []
    for coluna, valor in data.items():
        coluna = _validar_identificador(coluna, "coluna")
        set_condicoes.append(f"{coluna} = %s")
        valores.append(valor)

    where_sql, valores_where = _montar_where(where)
    valores.extend(valores_where)

    query = f"""
        UPDATE {schema}.{table_name}
        SET {", ".join(set_condicoes)}
        {where_sql}
    """

    conn = conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(query, tuple(valores))
            linhas_afetadas = cur.rowcount

        conn.commit()
        return linhas_afetadas

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()