import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


PGHOST = os.getenv("PGHOST")
PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGSSLMODE = os.getenv("PGSSLMODE", "require")


def conexao():
    """
    Cria e retorna uma conexão com o banco PostgreSQL.

    As credenciais são lidas de variáveis de ambiente ou do arquivo .env.
    """

    variaveis_obrigatorias = {
        "PGHOST": PGHOST,
        "PGDATABASE": PGDATABASE,
        "PGUSER": PGUSER,
        "PGPASSWORD": PGPASSWORD,
    }

    faltando = [
        nome for nome, valor in variaveis_obrigatorias.items()
        if not valor
    ]

    if faltando:
        raise EnvironmentError(
            "Variáveis de conexão ausentes: "
            + ", ".join(faltando)
        )

    return psycopg2.connect(
        host=PGHOST,
        database=PGDATABASE,
        user=PGUSER,
        password=PGPASSWORD,
        sslmode=PGSSLMODE
    )


if __name__ == "__main__":
    conn = None
    cursor = None

    try:
        conn = conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        resultado = cursor.fetchone()

        print("Comando executado! O banco respondeu:")
        print(resultado[0])

    except Exception as erro:
        print("Erro ao executar o comando:", erro)

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

        print("Conexão encerrada.")