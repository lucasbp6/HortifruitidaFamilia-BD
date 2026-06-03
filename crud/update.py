from conexao import conexao
from dados import Cliente, Vendedor, Produto, Categoria, UnidadeMedida, Fornecedor, OperacaoCaixa, Pedido


def update(table_name, id, column_name, value, schema='public'):
    """
    Atualiza uma linha na tabela especificada com os valores fornecidos.

    Parâmetros:
    - table_name (str): nome da tabela onde a atualização será feita.
    - id: valor da chave primária para identificar a linha a ser atualizada.
    - column_name(str): Nome da coluna a ser editada
    - value: Novo valor a ser atribuído
    - schema (str): esquema do banco de dados, padrão é 'public'.
    """
    conn = conexao()
    colunas = get_columns(table_name=table_name)
    id_column_name = colunas[0]

    query = f"UPDATE {schema}.{table_name} SET {column_name} = %s WHERE {id_column_name} = %s;"
    valores = list(value) + [id]

    with conn.cursor() as cur:
        cur.execute(query, valores)
        conn.commit()
    conn.close()