from datetime import datetime
from conexao import conexao


SCHEMA_PADRAO = "hortifruti"


def abrir_operacao_caixa(
    id_vend: int,
    id_caixa: int,
    valor_aber: float,
    schema: str = SCHEMA_PADRAO
) -> int:
    """Abre uma operação de caixa e retorna o ID gerado."""

    if valor_aber < 0:
        raise ValueError("O valor de abertura do caixa não pode ser negativo.")

    conn = conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COALESCE(MAX(IDOperacao), 0) + 1 FROM {schema}.OPERACAOCAIXA")
            novo_id = cur.fetchone()[0]

            agora = datetime.now()

            cur.execute(
                f"""
                INSERT INTO {schema}.OPERACAOCAIXA
                (IDOperacao, DataOpAber, ValorOpAber, IDVend, IDCaixa)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (novo_id, agora, valor_aber, id_vend, id_caixa)
            )

        conn.commit()
        return novo_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def finalizar_venda_transacao(
    valor_total: float,
    tipo_pedido: str,
    id_cliente: int,
    id_operacao: int,
    metodo_pagamento: str,
    itens: list[dict],
    schema: str = SCHEMA_PADRAO
):
    """
    Finaliza uma venda completa em uma única transação.

    A função:
    1. valida os itens;
    2. confere estoque suficiente;
    3. cria PEDIDO;
    4. cria ITEMPEDIDO;
    5. baixa estoque;
    6. cria PAGAMENTO.

    Se qualquer etapa falhar, toda a venda sofre rollback.
    """

    if not itens:
        raise ValueError("Não é possível finalizar uma venda sem itens.")

    if valor_total <= 0:
        raise ValueError("O valor total da venda deve ser positivo.")

    if id_operacao is None:
        raise ValueError("Não há operação de caixa aberta para finalizar a venda.")

    conn = conexao()
    try:
        with conn.cursor() as cur:
            # Agrupa quantidades por produto.
            # Isso evita erro quando o mesmo produto aparece mais de uma vez no carrinho.
            qtd_por_produto = {}
            for item in itens:
                id_prod = int(item["id"])
                qtd = float(item["qtd"])

                if qtd <= 0:
                    raise ValueError(f"Quantidade inválida para o produto de ID {id_prod}.")

                qtd_por_produto[id_prod] = qtd_por_produto.get(id_prod, 0.0) + qtd

            # Valida estoque antes de inserir pedido/pagamento.
            # FOR UPDATE trava as linhas dos produtos durante a transação.
            for id_prod, qtd_total in qtd_por_produto.items():
                cur.execute(
                    f"""
                    SELECT NomeProd, EstoqueAtualProd
                    FROM {schema}.PRODUTO
                    WHERE IDProd = %s
                    FOR UPDATE
                    """,
                    (id_prod,)
                )

                resultado = cur.fetchone()

                if resultado is None:
                    raise ValueError(f"Produto de ID {id_prod} não encontrado.")

                nome_prod, estoque_atual = resultado
                estoque_atual = float(estoque_atual)

                if estoque_atual < qtd_total:
                    raise ValueError(
                        f"Estoque insuficiente para '{nome_prod}'. "
                        f"Disponível: {estoque_atual}, solicitado: {qtd_total}."
                    )

            # Gera IDs depois das validações.
            cur.execute(f"SELECT COALESCE(MAX(IDPedido), 0) + 1 FROM {schema}.PEDIDO")
            novo_id_pedido = cur.fetchone()[0]

            cur.execute(f"SELECT COALESCE(MAX(IDPag), 0) + 1 FROM {schema}.PAGAMENTO")
            novo_id_pag = cur.fetchone()[0]

            agora = datetime.now()

            # Insere pedido.
            cur.execute(
                f"""
                INSERT INTO {schema}.PEDIDO
                (IDPedido, ValorTotalPedido, DataPedido, TipoPedido, IDCliente, IDOperacao)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    novo_id_pedido,
                    valor_total,
                    agora,
                    tipo_pedido,
                    id_cliente,
                    id_operacao
                )
            )

            # Insere itens e baixa estoque.
            for item in itens:
                id_prod = int(item["id"])
                qtd = float(item["qtd"])
                preco = float(item["preco"])
                desconto = float(item.get("desconto", 0) or 0)

                cur.execute(
                    f"""
                    INSERT INTO {schema}.ITEMPEDIDO
                    (IDProd, IDPedido, QtdItem, DescItem, PrecoUn)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        id_prod,
                        novo_id_pedido,
                        qtd,
                        desconto,
                        preco
                    )
                )

                cur.execute(
                    f"""
                    UPDATE {schema}.PRODUTO
                    SET EstoqueAtualProd = EstoqueAtualProd - %s
                    WHERE IDProd = %s
                    """,
                    (qtd, id_prod)
                )

            # Insere pagamento.
            cur.execute(
                f"""
                INSERT INTO {schema}.PAGAMENTO
                (IDPag, MetodoPag, ValorPag, DataPag, IDPedido)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    novo_id_pag,
                    metodo_pagamento,
                    valor_total,
                    agora,
                    novo_id_pedido
                )
            )

        conn.commit()
        return novo_id_pedido, novo_id_pag

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()