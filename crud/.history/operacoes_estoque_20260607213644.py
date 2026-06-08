def registrar_movimentacao_estoque(tabela_movimento: str, dados: dict, schema: str = 'hortifruti'):
    conn = conexao()
    try:
        with conn.cursor() as cur:
            campos = list(dados.keys())
            valores = list(dados.values())
            placeholders = ', '.join(['%s'] * len(campos))
            query_in = f"INSERT INTO {schema}.{tabela_movimento} ({', '.join(campos)}) VALUES ({placeholders});"
            cur.execute(query_in, valores)

            id_prod = dados['IDProd']
            if tabela_movimento == "ENTRADAESTOQUE":
                qtd = float(dados['EntradaQtd'])
                novo_custo = float(dados['EntradaPreco'])
                query_up = f"UPDATE {schema}.PRODUTO SET EstoqueAtualProd = EstoqueAtualProd + %s, PrecoCustoProd = %s WHERE IDProd = %s;"
                cur.execute(query_up, (qtd, novo_custo, id_prod))
            elif tabela_movimento == "PERDAESTOQUE":
                qtd = float(dados['QtdPerda'])
                query_up = f"UPDATE {schema}.PRODUTO SET EstoqueAtualProd = EstoqueAtualProd - %s WHERE IDProd = %s;"
                cur.execute(query_up, (qtd, id_prod))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def baixar_estoque(id_prod: int, qtd: float, schema: str = 'hortifruti'):
    conn = conexao()
    try:
        with conn.cursor() as cur:
            query = f"""
                UPDATE {schema}.PRODUTO
                SET EstoqueAtualProd = EstoqueAtualProd - %s
                WHERE IDProd = %s
            """
            cur.execute(query, (qtd, id_prod))

        conn.commit()
        return cur.rowcount

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()