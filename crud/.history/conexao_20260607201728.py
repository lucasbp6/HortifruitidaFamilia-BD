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
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        resultado = cursor.fetchone() 
        print("Comando executado! O banco respondeu:")

    except Exception as erro:
        print("Erro ao executar o comando:", erro)

    finally:
        cursor.close()
        conn.close()
        print("Conexão encerrada.")