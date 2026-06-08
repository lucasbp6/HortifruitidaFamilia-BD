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

def select(table_name, cols='*', where=None, schema='hortifruti', order_by=None):
    conn = conexao()
    cursor = None

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

        if order_by is not None:
            query += f" ORDER BY {order_by}"
            
        cursor.execute(query, tuple(valores))
        return cursor.fetchall()

    except Exception as erro:
        print(f"Erro no SELECT em {schema}.{table_name}: {erro}")
        raise erro

    finally:
        if cursor is not None:
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