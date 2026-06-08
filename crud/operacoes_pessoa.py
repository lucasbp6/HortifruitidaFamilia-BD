from conexao import conexao


SCHEMA_PADRAO = "hortifruti"

TABELAS_PERMITIDAS = {"CLIENTE", "VENDEDOR", "FORNECEDOR"}

COLUNA_ID_PADRAO = {
    "CLIENTE": "IDCliente",
    "VENDEDOR": "IDVend",
    "FORNECEDOR": "IDForn",
}

TABELA_ENDERECO = {
    "CLIENTE": "ENDERECOCLIENTE",
    "VENDEDOR": "ENDERECOVENDEDOR",
    "FORNECEDOR": "ENDERECOFORNEC",
}

TABELA_TELEFONE = {
    "CLIENTE": "CLIENTE_CELCLIENTE",
    "FORNECEDOR": "FORNECEDOR_CELFORN",
    # VENDEDOR tem CelVend direto na tabela VENDEDOR.
}

REFERENCIAS_HISTORICAS = {
    "CLIENTE": [("PEDIDO", "IDCliente")],
    "VENDEDOR": [("OPERACAOCAIXA", "IDVend")],
    "FORNECEDOR": [],
}


def _validar_tabela_pessoa(tabela: str) -> str:
    tabela = tabela.upper()

    if tabela not in TABELAS_PERMITIDAS:
        raise ValueError(
            "Deleção segura disponível apenas para CLIENTE, VENDEDOR ou FORNECEDOR."
        )

    return tabela


def _validar_coluna_id(tabela: str, coluna_id: str | None) -> str:
    coluna_esperada = COLUNA_ID_PADRAO[tabela]

    if coluna_id is None:
        return coluna_esperada

    if coluna_id != coluna_esperada:
        raise ValueError(
            f"Coluna de ID inválida para {tabela}. "
            f"Esperado: {coluna_esperada}, recebido: {coluna_id}."
        )

    return coluna_id


def _registro_existe(cur, tabela: str, coluna_id: str, id_registro: int, schema: str) -> bool:
    cur.execute(
        f"""
        SELECT 1
        FROM {schema}.{tabela}
        WHERE {coluna_id} = %s
        """,
        (id_registro,)
    )
    return cur.fetchone() is not None


def _buscar_enderecos_vinculados(cur, tabela: str, coluna_id: str, id_registro: int, schema: str) -> list[int]:
    tabela_vinculo = TABELA_ENDERECO[tabela]

    cur.execute(
        f"""
        SELECT IDEndereco
        FROM {schema}.{tabela_vinculo}
        WHERE {coluna_id} = %s
        """,
        (id_registro,)
    )

    return [linha[0] for linha in cur.fetchall()]


def _deletar_telefones_vinculados(cur, tabela: str, coluna_id: str, id_registro: int, schema: str) -> None:
    tabela_telefone = TABELA_TELEFONE.get(tabela)

    if tabela_telefone is None:
        return

    cur.execute(
        f"""
        DELETE FROM {schema}.{tabela_telefone}
        WHERE {coluna_id} = %s
        """,
        (id_registro,)
    )


def _deletar_vinculo_endereco(cur, tabela: str, coluna_id: str, id_registro: int, schema: str) -> None:
    tabela_vinculo = TABELA_ENDERECO[tabela]

    cur.execute(
        f"""
        DELETE FROM {schema}.{tabela_vinculo}
        WHERE {coluna_id} = %s
        """,
        (id_registro,)
    )


def _endereco_ainda_tem_vinculo(cur, id_endereco: int, schema: str) -> bool:
    consultas = [
        f"SELECT 1 FROM {schema}.ENDERECOCLIENTE WHERE IDEndereco = %s",
        f"SELECT 1 FROM {schema}.ENDERECOVENDEDOR WHERE IDEndereco = %s",
        f"SELECT 1 FROM {schema}.ENDERECOFORNEC WHERE IDEndereco = %s",
    ]

    for query in consultas:
        cur.execute(query, (id_endereco,))
        if cur.fetchone() is not None:
            return True

    return False


def _deletar_enderecos_orfaos(cur, enderecos: list[int], schema: str) -> int:
    deletados = 0

    for id_endereco in enderecos:
        if not _endereco_ainda_tem_vinculo(cur, id_endereco, schema):
            cur.execute(
                f"""
                DELETE FROM {schema}.ENDERECO
                WHERE IDEndereco = %s
                """,
                (id_endereco,)
            )
            deletados += cur.rowcount

    return deletados


def _validar_id_default(cur, tabela: str, coluna_id: str, id_default: int, schema: str) -> None:
    if id_default is None:
        raise ValueError(
            f"{tabela} possui referências históricas. "
            "Informe um id_default válido para preservar o histórico."
        )

    if not _registro_existe(cur, tabela, coluna_id, id_default, schema):
        raise ValueError(
            f"O ID padrão {id_default} não existe em {schema}.{tabela}. "
            "Crie um registro padrão antes de usar a deleção segura."
        )


def _reatribuir_referencias_historicas(
    cur,
    tabela: str,
    coluna_id: str,
    id_registro: int,
    id_default: int,
    schema: str
) -> int:
    referencias = REFERENCIAS_HISTORICAS.get(tabela, [])

    if not referencias:
        return 0

    _validar_id_default(cur, tabela, coluna_id, id_default, schema)

    total_afetado = 0

    for tabela_ref, coluna_ref in referencias:
        cur.execute(
            f"""
            UPDATE {schema}.{tabela_ref}
            SET {coluna_ref} = %s
            WHERE {coluna_ref} = %s
            """,
            (id_default, id_registro)
        )
        total_afetado += cur.rowcount

    return total_afetado


def _bloquear_fornecedor_com_historico(cur, id_forn: int, schema: str) -> None:
    cur.execute(
        f"""
        SELECT COUNT(*)
        FROM {schema}.ENTRADAESTOQUE
        WHERE IDForn = %s
        """,
        (id_forn,)
    )

    total_entradas = cur.fetchone()[0]

    if total_entradas > 0:
        raise ValueError(
            "Não é possível deletar este fornecedor porque existem entradas de estoque "
            "associadas a ele. Para preservar o histórico, mantenha o fornecedor cadastrado "
            "ou crie uma regra de reatribuição para um fornecedor padrão."
        )


def deletar_seguro(
    tabela: str,
    id_registro: int,
    coluna_id: str | None = None,
    id_default: int = 0,
    schema: str = SCHEMA_PADRAO
) -> dict:
    """
    Remove com segurança CLIENTE, VENDEDOR ou FORNECEDOR.

    A função:
    - valida se a tabela é permitida;
    - valida se o registro existe;
    - preserva histórico de CLIENTE e VENDEDOR reatribuindo para id_default;
    - remove telefones vinculados quando existirem em tabela separada;
    - remove vínculos de endereço;
    - remove endereços órfãos;
    - remove a pessoa.

    Retorna um resumo com as quantidades afetadas.
    """

    tabela = _validar_tabela_pessoa(tabela)
    coluna_id = _validar_coluna_id(tabela, coluna_id)
    id_registro = int(id_registro)

    if id_registro == id_default:
        raise ValueError("Não é permitido deletar o próprio registro padrão.")

    conn = conexao()
    try:
        with conn.cursor() as cur:
            if not _registro_existe(cur, tabela, coluna_id, id_registro, schema):
                raise ValueError(f"Registro não encontrado em {schema}.{tabela}: {coluna_id}={id_registro}.")

            if tabela == "FORNECEDOR":
                _bloquear_fornecedor_com_historico(cur, id_registro, schema)

            enderecos = _buscar_enderecos_vinculados(cur, tabela, coluna_id, id_registro, schema)

            referencias_reatribuidas = _reatribuir_referencias_historicas(
                cur,
                tabela,
                coluna_id,
                id_registro,
                id_default,
                schema
            )

            _deletar_telefones_vinculados(cur, tabela, coluna_id, id_registro, schema)
            _deletar_vinculo_endereco(cur, tabela, coluna_id, id_registro, schema)

            cur.execute(
                f"""
                DELETE FROM {schema}.{tabela}
                WHERE {coluna_id} = %s
                """,
                (id_registro,)
            )
            pessoas_deletadas = cur.rowcount

            enderecos_deletados = _deletar_enderecos_orfaos(cur, enderecos, schema)

        conn.commit()

        return {
            "tabela": tabela,
            "id_deletado": id_registro,
            "pessoas_deletadas": pessoas_deletadas,
            "enderecos_deletados": enderecos_deletados,
            "referencias_reatribuidas": referencias_reatribuidas,
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()