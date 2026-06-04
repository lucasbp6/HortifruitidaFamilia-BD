import psycopg2

PGHOST="ep-green-pine-aclq723g-pooler.sa-east-1.aws.neon.tech"
PGDATABASE="neondb"
PGUSER="neondb_owner"
PGPASSWORD="npg_uzF52oPsSCdm"
PGSSLMODE="require"

def conexao():

    conexao = psycopg2.connect(
        host=PGHOST,
        database=PGDATABASE,
        user=PGUSER,
        password=PGPASSWORD,
        sslmode=PGSSLMODE
        )
        
    return conexao

if __name__ == "__main__":
    conn = conexao()
    
    try:
        # 1. Cria o mensageiro (cursor)
        cursor = conn.cursor()
        
        # 2. Manda o comando SQL
        cursor.execute("SELECT version();")
        
        # 3. Pega o resultado de volta
        resultado = cursor.fetchone() # fetchone() pega uma linha, fetchall() pega todas
        
        print("Comando executado! O banco respondeu:")

    except Exception as erro:
        # Se algo der errado (erro de sintaxe no SQL, tabela não existe, etc), cai aqui
        print("Erro ao executar o comando:", erro)

    finally:
        # 4. É importante fechar o cursor e a conexão no final
        cursor.close()
        conn.close()
        print("Conexão encerrada.")