# nao  feito


def select(query: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)

            return cur.fetchall()