from conexao import conexao


SCHEMA_PADRAO = "hortifruti"
MOVIMENTOS_VALIDOS = {"ENTRADAESTOQUE", "PERDAESTOQUE"}


def _inserir_movimento(cur, tabela_movimento: str, dados: dict, schema: str) -> None:
    campos = list(dados.keys())
    valores = list(dados.values())
    placeholders = ", ".join(["%s"] * len(campos))
    campos_sql = ", ".join(campos)

    cur.execute(
        f"""
        INSERT INTO {schema}.{tabela_movimento}
        ({campos_sql})
        VALUES ({placeholders})
        """,
        valores
    )


def registrar_movimentacao_estoque(
    tabela_movimento: str,
    dados: dict,
    schema: str = SCHEMA_PADRAO
) -> None:
    """
    Registra uma entrada ou perda de estoque e atualiza o estoque do produto.

    A operação é transacional: se a inserção do movimento ou a atualização
    do produto falhar, tudo sofre rollback.
    """

    tabela_movimento = tabela_movimento.upper()

    if tabela_movimento not in MOVIMENTOS_VALIDOS:
        raise ValueError(
            "Movimentação de estoque inválida. "
            "Use 'ENTRADAESTOQUE' ou 'PERDAESTOQUE'."
        )

    if "IDProd" not in dados:
        raise ValueError("A movimentação precisa informar o campo IDProd.")

    conn = conexao()
    try:
        with conn.cursor() as cur:
            id_prod = int(dados["IDProd"])

            cur.execute(
                f"""
                SELECT NomeProd, EstoqueAtualProd
                FROM {schema}.PRODUTO
                WHERE IDProd = %s
                FOR UPDATE
                """,
                (id_prod,)
            )
            produto = cur.fetchone()

            if produto is None:
                raise ValueError(f"Produto de ID {id_prod} não encontrado.")

            nome_prod, estoque_atual = produto
            estoque_atual = float(estoque_atual)

            if tabela_movimento == "ENTRADAESTOQUE":
                qtd = float(dados.get("EntradaQtd", 0))
                novo_custo = float(dados.get("EntradaPreco", 0))

                if qtd <= 0:
                    raise ValueError("A quantidade de entrada deve ser positiva.")
                if novo_custo < 0:
                    raise ValueError("O preço de entrada não pode ser negativo.")

                _inserir_movimento(cur, tabela_movimento, dados, schema)

                cur.execute(
                    f"""
                    UPDATE {schema}.PRODUTO
                    SET EstoqueAtualProd = EstoqueAtualProd + %s,
                        PrecoCustoProd = %s
                    WHERE IDProd = %s
                    """,
                    (qtd, novo_custo, id_prod)
                )

            elif tabela_movimento == "PERDAESTOQUE":
                qtd = float(dados.get("QtdPerda", 0))

                if qtd <= 0:
                    raise ValueError("A quantidade de perda deve ser positiva.")

                if estoque_atual < qtd:
                    raise ValueError(
                        f"Perda maior que o estoque disponível para '{nome_prod}'. "
                        f"Disponível: {estoque_atual}, perda informada: {qtd}."
                    )

                _inserir_movimento(cur, tabela_movimento, dados, schema)

                cur.execute(
                    f"""
                    UPDATE {schema}.PRODUTO
                    SET EstoqueAtualProd = EstoqueAtualProd - %s
                    WHERE IDProd = %s
                    """,
                    (qtd, id_prod)
                )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def baixar_estoque(
    id_prod: int,
    qtd: float,
    schema: str = SCHEMA_PADRAO
) -> int:
    """
    Baixa estoque de um produto fora do fluxo de venda.

    Observação: a venda principal deve usar finalizar_venda_transacao,
    não esta função isolada.
    """

    if qtd <= 0:
        raise ValueError("A quantidade para baixa deve ser positiva.")

    conn = conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT NomeProd, EstoqueAtualProd
                FROM {schema}.PRODUTO
                WHERE IDProd = %s
                FOR UPDATE
                """,
                (id_prod,)
            )
            produto = cur.fetchone()

            if produto is None:
                raise ValueError(f"Produto de ID {id_prod} não encontrado.")

            nome_prod, estoque_atual = produto
            estoque_atual = float(estoque_atual)

            if estoque_atual < qtd:
                raise ValueError(
                    f"Estoque insuficiente para '{nome_prod}'. "
                    f"Disponível: {estoque_atual}, solicitado: {qtd}."
                )

            cur.execute(
                f"""
                UPDATE {schema}.PRODUTO
                SET EstoqueAtualProd = EstoqueAtualProd - %s
                WHERE IDProd = %s
                """,
                (qtd, id_prod)
            )

            linhas_afetadas = cur.rowcount

        conn.commit()
        return linhas_afetadas

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()