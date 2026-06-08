def deletar_seguro(tabela: str, id_registro: int, coluna_id: str, id_default: int = 0, schema: str = 'hortifruti'):
    conn = conexao()
    try:
        with conn.cursor() as cur:
            enderecos_para_deletar = []
            
            if tabela == "VENDEDOR":
                cur.execute(f"SELECT IDEndereco FROM {schema}.ENDERECOVENDEDOR WHERE {coluna_id} = %s", (id_registro,))
                res = cur.fetchall()
                if res: enderecos_para_deletar.append(res[0][0])
                cur.execute(f"UPDATE {schema}.OPERACAOCAIXA SET {coluna_id} = %s WHERE {coluna_id} = %s", (id_default, id_registro))
                cur.execute(f"DELETE FROM {schema}.ENDERECOVENDEDOR WHERE {coluna_id} = %s", (id_registro,))
            
            elif tabela == "CLIENTE":
                cur.execute(f"SELECT IDEndereco FROM {schema}.ENDERECOCLIENTE WHERE {coluna_id} = %s", (id_registro,))
                res = cur.fetchall()
                if res: enderecos_para_deletar.append(res[0][0])
                cur.execute(f"UPDATE {schema}.PEDIDO SET {coluna_id} = %s WHERE {coluna_id} = %s", (id_default, id_registro))
                cur.execute(f"DELETE FROM {schema}.ENDERECOCLIENTE WHERE {coluna_id} = %s", (id_registro,))
                cur.execute(f"DELETE FROM {schema}.CLIENTE_CELCLIENTE WHERE {coluna_id} = %s", (id_registro,))


            cur.execute(f"DELETE FROM {schema}.{tabela} WHERE {coluna_id} = %s", (id_registro,))
            
            for id_end in enderecos_para_deletar:
                cur.execute(f"DELETE FROM {schema}.ENDERECO WHERE IDEndereco = %s", (id_end,))
            
        conn.commit()
        return cur.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()