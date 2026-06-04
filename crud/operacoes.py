import psycopg2
from conexao import conexao

def insert(list_table_name: list[str], list_values: list[dict], schema: str = 'hortifruti'):
    
    if len(list_table_name) != len(list_values):
        raise ValueError("A lista de tabelas e a lista de valores precisam ter o mesmo tamanho.")

    conn = conexao()

    try:
        with conn.cursor() as cur:
            
            for table_name, values in zip(list_table_name, list_values):
                
                # Prepara os campos (chaves do dict) e valores (valores do dict)
                campos = list(values.keys())
                valores = list(values.values())
                
                placeholders = ', '.join(['%s'] * len(campos))
                campos_str = ', '.join(campos)
                
                # Monta a query dinamicamente
                query = f"INSERT INTO {schema}.{table_name} ({campos_str}) VALUES ({placeholders});"
                
                # Executa a inserção desta tabela
                cur.execute(query, valores)
            
            # Se todas as inserções deram certo, faz o commit de tudo (Transação)
            conn.commit()
            
    except Exception as e:
        # Se der erro em qualquer inserção, desfaz tudo para não deixar dados pela metade
        conn.rollback()
        print(f"Erro ao realizar inserções: {e}")
        raise e
        

    conn.close()



def select(table_name, cols='*', where=None, schema='hortifruti'):
    conn = conexao()
    
    try:
        cursor = conn.cursor()
        
        # 1. Base da query
        query = f"SELECT {cols} FROM {schema}.{table_name}"
        valores = []
        
        # 2. Construção dinâmica do WHERE
        if where is not None:
            condicoes = []
            
            # Itera sobre o dicionário para montar "coluna = %s"
            for coluna, valor in where.items():
                condicoes.append(f"{coluna} = %s")
                valores.append(valor)
            
            # Junta tudo com AND (ex: "id_cat = %s AND preco = %s")
            query += " WHERE " + " AND ".join(condicoes)
            
        # 3. Execução segura
        # Se 'valores' estiver vazio, o psycopg2 ignora. Se tiver dados, ele substitui os %s.
        cursor.execute(query, tuple(valores))
        
        # 4. Retorno dos dados
        resultados = cursor.fetchall()
        return resultados
        
    except Exception as erro:
        print(f"Erro ao executar SELECT na tabela {table_name}: {erro}")
        return None
        
    finally:
        cursor.close()
        conn.close()


def delete(table_name, where, schema='hortifruti'):
    conn = conexao()
    
    try:
        cursor = conn.cursor()
        
        # 1. Base da query
        query = f"DELETE FROM {schema}.{table_name} WHERE "
        
        condicoes = []
        valores = []
        
        # 2. O for que você começou: extraindo as colunas e os valores
        for coluna, valor in where.items():
            condicoes.append(f"{coluna} = %s")
            valores.append(valor)
            
        # Junta tudo (Ex: "id_cat = %s AND status = %s")
        query += " AND ".join(condicoes)
        
        # 3. Executa a query com segurança
        cursor.execute(query, tuple(valores))
        
        # 4. SALVA A ALTERAÇÃO NO BANCO (Crucial para o DELETE)
        conn.commit()
        
        # 5. Retorna quantas linhas foram deletadas para você saber se deu certo
        linhas_afetadas = cursor.rowcount
        return linhas_afetadas
        
    except Exception as erro:
        # Se der erro, cancela a transação para não corromper o banco
        conn.rollback() 
        print(f"Erro ao deletar na tabela {table_name}: {erro}")
        return 0
        
    finally:
        cursor.close()
        conn.close()


def update(table_name, data, where, schema='hortifruti'):
    conn = conexao()
    
    try:
        cursor = conn.cursor()
        
        # Travas de segurança essenciais
        if not data:
            print("Erro: Nenhum dado foi fornecido para atualização.")
            return 0
        if not where:
            print("Erro: A cláusula 'where' é obrigatória para evitar atualizar a tabela inteira.")
            return 0
            
        valores = []
        
        # 1. Construção da parte SET (Os novos valores)
        set_condicoes = []
        for coluna, valor in data.items():
            set_condicoes.append(f"{coluna} = %s")
            valores.append(valor) # Adiciona os valores novos na lista
            
        # Base da query com o SET (Ex: UPDATE hortifruti.Produto SET preco_venda_prod = %s, estoque = %s)
        query = f"UPDATE {schema}.{table_name} SET " + ", ".join(set_condicoes)
        
        # 2. Construção da parte WHERE (O filtro de quem será alterado)
        where_condicoes = []
        for coluna, valor in where.items():
            where_condicoes.append(f"{coluna} = %s")
            valores.append(valor) # Adiciona os valores do filtro na MESMA lista
            
        # Junta o WHERE na query (Ex: ... WHERE id_prod = %s)
        query += " WHERE " + " AND ".join(where_condicoes)
        
        # 3. Execução segura
        cursor.execute(query, tuple(valores))
        
        # 4. SALVA A ALTERAÇÃO NO BANCO
        conn.commit()
        
        # 5. Retorna quantas linhas foram atualizadas
        linhas_afetadas = cursor.rowcount
        return linhas_afetadas
        
    except Exception as erro:
        # Desfaz em caso de erro
        conn.rollback() 
        print(f"Erro ao atualizar na tabela {table_name}: {erro}")
        return 0
        
    finally:
        cursor.close()
        conn.close()


