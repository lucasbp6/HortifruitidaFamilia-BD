def abrir_operacao_caixa(id_vend: int, id_caixa: int, valor_aber: float, schema: str = 'hortifruti') -> int:
    conn = conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COALESCE(MAX(IDOperacao), 0) + 1 FROM {schema}.OPERACAOCAIXA")
            novo_id = cur.fetchone()[0]
            
            agora = datetime.now()
            query = f"INSERT INTO {schema}.OPERACAOCAIXA (IDOperacao, DataOpAber, ValorOpAber, IDVend, IDCaixa) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query, (novo_id, agora, valor_aber, id_vend, id_caixa))
            
            conn.commit()
            return novo_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def finalizar_venda_transacao(
    valor_total: float,
    tipo_pedido: str,
    id_cliente: int,
    id_operacao: int,
    metodo_pagamento: str,
    itens: list[dict],
    schema: str = 'hortifruti'
):
    conn = conexao()
    try:
        with conn.cursor() as cur:
            # 1. Valida todos os itens antes de inserir qualquer coisa
            for item in itens:
                id_prod = int(item["id"])
                qtd = float(item["qtd"])

                if qtd <= 0:
                    raise ValueError(f"Quantidade inválida para o produto de ID {id_prod}.")

                cur.execute(
                    f"""
                    SELECT NomeProd, EstoqueAtualProd
                    FROM {schema}.PRODUTO
                    WHERE IDProd = %s
                    """,
                    (id_prod,)
                )

                resultado = cur.fetchone()

                if resultado is None:
                    raise ValueError(f"Produto de ID {id_prod} não encontrado.")

                nome_prod, estoque_atual = resultado
                estoque_atual = float(estoque_atual)

                if estoque_atual < qtd:
                    raise ValueError(
                        f"Estoque insuficiente para '{nome_prod}'. "
                        f"Disponível: {estoque_atual}, solicitado: {qtd}."
                    )

            # 2. Só depois de validar tudo, gera os IDs
            cur.execute(f"SELECT COALESCE(MAX(IDPedido), 0) + 1 FROM {schema}.PEDIDO")
            novo_id_pedido = cur.fetchone()[0]

            cur.execute(f"SELECT COALESCE(MAX(IDPag), 0) + 1 FROM {schema}.PAGAMENTO")
            novo_id_pag = cur.fetchone()[0]

            agora = datetime.now()

            # 3. Insere o pedido
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

            # 4. Insere os itens e baixa estoque
            for item in itens:
                id_prod = int(item["id"])
                qtd = float(item["qtd"])
                preco = float(item["preco"])

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
                        0,
                        preco
                    )
                )

                cur.execute(
                    f"""
                    UPDATE {schema}.PRODUTO
                    SET EstoqueAtualProd = EstoqueAtualProd - %s
                    WHERE IDProd = %s
                    """,
                    (
                        qtd,
                        id_prod
                    )
                )

            # 5. Insere pagamento
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

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()