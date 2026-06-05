import psycopg2
from conexao import conexao

def insert(list_table_name: list[str], list_values: list[dict], schema: str = 'hortifruti'):
    """Insere dados em múltiplas tabelas dentro da mesma transação."""
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
            
            # Confirmação da transação (Tudo ou Nada)
            conn.commit()
            
    except Exception as e:
        conn.rollback()
        print(f"Erro ao realizar inserções: {e}")
        raise e
    finally:
        conn.close()


def select(table_name, cols='*', where=None, schema='hortifruti'):
    """Busca dados no banco, aceitando filtros opcionais em formato de dicionário."""
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
        resultados = cursor.fetchall()
        return resultados
        
    except Exception as erro:
        print(f"Erro ao executar SELECT na tabela {table_name}: {erro}")
        return None
        
    finally:
        cursor.close()
        conn.close()


def delete(table_name, where, schema='hortifruti'):
    """Deleta registros com base em um dicionário de condições."""
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
        
        linhas_afetadas = cursor.rowcount
        return linhas_afetadas
        
    except Exception as erro:
        conn.rollback() 
        print(f"Erro ao deletar na tabela {table_name}: {erro}")
        raise erro
        
    finally:
        cursor.close()
        conn.close()


def update(table_name, data, where, schema='hortifruti'):
    """Atualiza registros com base em um dicionário de novos dados e condições WHERE."""
    conn = conexao()
    
    try:
        cursor = conn.cursor()
        
        if not data:
            print("Erro: Nenhum dado foi fornecido para atualização.")
            return 0
        if not where:
            print("Erro: A cláusula 'where' é obrigatória.")
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
        
        linhas_afetadas = cursor.rowcount
        return linhas_afetadas
        
    except Exception as erro:
        conn.rollback() 
        print(f"Erro ao atualizar na tabela {table_name}: {erro}")
        raise erro
        
    finally:
        cursor.close()
        conn.close()


def registrar_movimentacao_estoque(tabela_movimento: str, dados: dict, schema: str = 'hortifruti'):
    """Registra Entrada ou Perda e atualiza o saldo e preço de custo do Produto na mesma transação."""
    conn = conexao()
    try:
        with conn.cursor() as cur:
            # 1. Insere o log (Entrada ou Perda)
            campos = list(dados.keys())
            valores = list(dados.values())
            placeholders = ', '.join(['%s'] * len(campos))
            query_in = f"INSERT INTO {schema}.{tabela_movimento} ({', '.join(campos)}) VALUES ({placeholders});"
            cur.execute(query_in, valores)

            # 2. Atualiza o Produto correspondente
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
    """Transfere as dependências para um ID Padrão (Default) antes de apagar o registro original."""
    conn = conexao()
    try:
        with conn.cursor() as cur:
            if tabela == "PRODUTO":
                cur.execute(f"UPDATE {schema}.ITEMPEDIDO SET {coluna_id} = %s WHERE {coluna_id} = %s", (id_default, id_registro))
                cur.execute(f"UPDATE {schema}.ENTRADAESTOQUE SET {coluna_id} = %s WHERE {coluna_id} = %s", (id_default, id_registro))
                cur.execute(f"UPDATE {schema}.PERDAESTOQUE SET {coluna_id} = %s WHERE {coluna_id} = %s", (id_default, id_registro))
            
            elif tabela == "VENDEDOR":
                cur.execute(f"UPDATE {schema}.OPERACAOCAIXA SET {coluna_id} = %s WHERE {coluna_id} = %s", (id_default, id_registro))
                cur.execute(f"DELETE FROM {schema}.ENDERECOVENDEDOR WHERE {coluna_id} = %s", (id_registro,))
            
            elif tabela == "CLIENTE":
                cur.execute(f"UPDATE {schema}.PEDIDO SET {coluna_id} = %s WHERE {coluna_id} = %s", (id_default, id_registro))
                cur.execute(f"DELETE FROM {schema}.ENDERECOCLIENTE WHERE {coluna_id} = %s", (id_registro,))
                cur.execute(f"DELETE FROM {schema}.CLIENTE_CELCLIENTE WHERE {coluna_id} = %s", (id_registro,))

            # Após transferir e limpar relações N:M, deleta o registro principal
            cur.execute(f"DELETE FROM {schema}.{tabela} WHERE {coluna_id} = %s", (id_registro,))
            
        conn.commit()
        return cur.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()