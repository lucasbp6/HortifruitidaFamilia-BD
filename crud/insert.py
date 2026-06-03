# nao feito

import psycopg2
from conexao import conexao

def insert(table_name, dicio, schema='public'):
    """
    Insere um novo registro em uma tabela, com base nos dados fornecidos via dicionário.

    Args:
        nome_tabela (str): Nome da tabela de destino.
        dicio (dict): Dicionário contendo os dados a serem inseridos (chaves = colunas).
        schema (str): Nome do schema da tabela (padrão: 'public').
    """
    conn = get_connection()
    colunas = get_columns(table_name=table_name, schema=schema)

    # Prepara os campos e valores a inserir com base nas colunas existentes
    campos = []
    valores = []
    for coluna in colunas:
        if coluna in dicio:
            campos.append(coluna)
            valores.append(dicio[coluna])

    placeholders = ', '.join(['%s'] * len(campos))
    campos_str = ', '.join(campos)
    query = f"INSERT INTO {schema}.{table_name} ({campos_str}) VALUES ({placeholders});"

    # Executa a inserção
    with conn.cursor() as cur:
        cur.execute(query, valores)
        conn.commit()
    conn.close()
