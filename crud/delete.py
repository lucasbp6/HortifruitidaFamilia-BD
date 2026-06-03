# nao feito

def delete(table_name, id, schema='public'):
    conn = get_connection()
    colunas = get_columns(table_name=table_name)
    id_column_name = colunas[0]
    valores = [id]
    query = f"DELETE FROM {schema}.{table_name} WHERE {id_column_name} = %s;"

    with conn.cursor() as cur:
        cur.execute(query, valores)
        if cur.rowcount != 0:
            conn.commit()

        return cur.rowcount