import psycopg2
from datetime import datetime
from conexao import conexao

def insert(list_table_name: list[str], list_values: list[dict], schema: str = 'hortifruti'):
    if len(list_table_name) != len(list_values):
        raise ValueError("A lista de tabelas e a lista de valores precisam ter o mesmo tamanho.")

    conn = conexao()
    try:
        with conn.cursor() as cur:
            for table_name, values in zip(list_table_name, list_values):
                campos = list(values.keys())
                valores = list(values.values())
                
                placeholders = ', '.join(['%s'] * len(campos))
                campos_str = ', '.join(campos)
                
                query = f"INSERT INTO {schema}.{table_name} ({campos_str}) VALUES ({placeholders});"
                cur.execute(query, valores)
            
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def select(table_name, cols='*', where=None, schema='hortifruti'):
    conn = conexao()
    try:
        cursor = conn.cursor()
        query = f"SELECT {cols} FROM {schema}.{table_name}"
        valores = []
        
        if where is not None:
            condicoes = []
            for coluna, valor in where.items():
                condicoes.append(f"{coluna} = %s")
                valores.append(valor)
            
            query += " WHERE " + " AND ".join(condicoes)
            
        cursor.execute(query, tuple(valores))
        return cursor.fetchall()
    except Exception as erro:
        return None
    finally:
        cursor.close()
        conn.close()

def delete(table_name, where, schema='hortifruti'):
    conn = conexao()
    try:
        cursor = conn.cursor()
        query = f"DELETE FROM {schema}.{table_name} WHERE "
        
        condicoes = []
        valores = []
        for coluna, valor in where.items():
            condicoes.append(f"{coluna} = %s")
            valores.append(valor)
            
        query += " AND ".join(condicoes)
        cursor.execute(query, tuple(valores))
        conn.commit()
        return cursor.rowcount
    except Exception as erro:
        conn.rollback() 
        raise erro
    finally:
        cursor.close()
        conn.close()

def update(table_name, data, where, schema='hortifruti'):
    conn = conexao()
    try:
        cursor = conn.cursor()
        if not data or not where:
            return 0
            
        valores = []
        set_condicoes = []
        for coluna, valor in data.items():
            set_condicoes.append(f"{coluna} = %s")
            valores.append(valor) 
            
        query = f"UPDATE {schema}.{table_name} SET " + ", ".join(set_condicoes)
        
        where_condicoes = []
        for coluna, valor in where.items():
            where_condicoes.append(f"{coluna} = %s")
            valores.append(valor) 
            
        query += " WHERE " + " AND ".join(where_condicoes)
        cursor.execute(query, tuple(valores))
        conn.commit()
        return cursor.rowcount
    except Exception as erro:
        conn.rollback() 
        raise erro
    finally:
        cursor.close()
        conn.close()

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

def deletar_seguro(tabela: str, id_registro: int, coluna_id: str, id_default: int = 0, schema: str = 'hortifruti'):
    conn = conexao()
    try:
        with conn.cursor() as cur:
            enderecos_para_deletar = []
            
            if tabela == "VENDEDOR":
                cur.execute(f"SELECT IDEndereco FROM {schema}.ENDERECOVENDEDOR WHERE {coluna_id} = %s", (id_registro,))
                res = cur.fetchall()
                if res: enderecos_para_deletar.append(res[0][0])
                cur.execute(f"UPDATE {schema}.OPERACAOCAIXA SET {coluna_id} = %s WHERE {coluna_id} = %s", (id_default, id_registro))
                cur.execute(f"DELETE FROM {schema}.ENDERECOVENDEDOR WHERE {coluna_id} = %s", (id_registro,))
            
            elif tabela == "CLIENTE":
                cur.execute(f"SELECT IDEndereco FROM {schema}.ENDERECOCLIENTE WHERE {coluna_id} = %s", (id_registro,))
                res = cur.fetchall()
                if res: enderecos_para_deletar.append(res[0][0])
                cur.execute(f"UPDATE {schema}.PEDIDO SET {coluna_id} = %s WHERE {coluna_id} = %s", (id_default, id_registro))
                cur.execute(f"DELETE FROM {schema}.ENDERECOCLIENTE WHERE {coluna_id} = %s", (id_registro,))
                cur.execute(f"DELETE FROM {schema}.CLIENTE_CELCLIENTE WHERE {coluna_id} = %s", (id_registro,))


            cur.execute(f"DELETE FROM {schema}.{tabela} WHERE {coluna_id} = %s", (id_registro,))
            
            for id_end in enderecos_para_deletar:
                cur.execute(f"DELETE FROM {schema}.ENDERECO WHERE IDEndereco = %s", (id_end,))
            
        conn.commit()
        return cur.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

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

def inserir_pedido(ValorTotalPedido, TipoPedido, IDCliente, IDOperacao, schema = 'Hortifruti'):
    conn = conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COALESCE(MAX(IDPedido), 0) + 1 FROM {schema}.PEDIDO")
            novo_id = cur.fetchone()[0]

            cur.execute(f"SELECT COALESCE(MAX(IDPag), 0) + 1 FROM {schema}.PAGAMENTO")
            novo_id_pag = cur.fetchone()[0]
            
            agora = datetime.now()
            insert(["PEDIDO"], [{"IDPedido": novo_id, "ValorTotalPedido": ValorTotalPedido, "DataPedido": agora, "TipoPedido":TipoPedido, "IDCliente": IDCliente, "IDOperacao":IDOperacao}])
            
            conn.commit()
            return novo_id, novo_id_pag
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()