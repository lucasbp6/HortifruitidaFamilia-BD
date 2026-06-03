import psycopg2

PGHOST="ep-green-pine-aclq723g-pooler.sa-east-1.aws.neon.tech"
PGDATABASE="neondb"
PGUSER="neondb_owner"
PGPASSWORD="npg_z3fIWdY9nHTp"
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
    print("Conexão com o Neon estabelecida com sucesso!")
    conn.close()