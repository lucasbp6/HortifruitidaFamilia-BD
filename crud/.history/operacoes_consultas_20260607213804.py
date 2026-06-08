def select_enderecos_por_tipo(tipo_pessoa: str, schema='hortifruti'):
    conn = conexao()
    try:
        with conn.cursor() as cur:
            # Preparamos as 3 consultas padronizadas com a mesma quantidade de colunas
            query_cliente = f"""
                SELECT e.*, 'Cliente' AS TipoVinculo, c.NomeCliente AS Proprietario 
                FROM {schema}.ENDERECO e
                JOIN {schema}.ENDERECOCLIENTE ec ON e.IDEndereco = ec.IDEndereco
                JOIN {schema}.CLIENTE c ON ec.IDCliente = c.IDCliente
            """
            query_forn = f"""
                SELECT e.*, 'Fornecedor' AS TipoVinculo, f.NomeForn AS Proprietario 
                FROM {schema}.ENDERECO e
                JOIN {schema}.ENDERECOFORNEC ef ON e.IDEndereco = ef.IDEndereco
                JOIN {schema}.FORNECEDOR f ON ef.IDForn = f.IDForn
            """
            query_vend = f"""
                SELECT e.*, 'Vendedor' AS TipoVinculo, v.NomeVend AS Proprietario 
                FROM {schema}.ENDERECO e
                JOIN {schema}.ENDERECOVENDEDOR ev ON e.IDEndereco = ev.IDEndereco
                JOIN {schema}.VENDEDOR v ON ev.IDVend = v.IDVend
            """
            
            # Escolhemos qual executar, ou unimos todas se for "TODOS"
            if tipo_pessoa == "CLIENTE":
                query = query_cliente
            elif tipo_pessoa == "FORNECEDOR":
                query = query_forn
            elif tipo_pessoa == "VENDEDOR":
                query = query_vend
            else: 
                query = f"{query_cliente} UNION ALL {query_forn} UNION ALL {query_vend}"
                
            cur.execute(query)
            return cur.fetchall()
    except Exception as erro:
        print(f"Erro na query de endereços: {erro}")
        return []
    finally:
        conn.close()
        
def select_telefones_geral(schema='hortifruti'):
    conn = conexao()
    try:
        with conn.cursor() as cur:
            # Vendedor tem o celular na própria tabela
            query_vend = f"""
                SELECT CelVend AS Telefone, 'Vendedor' AS TipoVinculo, NomeVend AS Proprietario 
                FROM {schema}.VENDEDOR
            """
            # Cliente tem tabela associativa
            query_cliente = f"""
                SELECT cc.CelCliente AS Telefone, 'Cliente' AS TipoVinculo, c.NomeCliente AS Proprietario 
                FROM {schema}.CLIENTE_CELCLIENTE cc
                JOIN {schema}.CLIENTE c ON cc.IDCliente = c.IDCliente
            """
            # Fornecedor tem tabela associativa
            query_forn = f"""
                SELECT fc.CelForn AS Telefone, 'Fornecedor' AS TipoVinculo, f.NomeForn AS Proprietario 
                FROM {schema}.FORNECEDOR_CELFORN fc
                JOIN {schema}.FORNECEDOR f ON fc.IDForn = f.IDForn
            """
            
            # Une todos os resultados
            query = f"{query_cliente} UNION ALL {query_forn} UNION ALL {query_vend}"
            
            cur.execute(query)
            return cur.fetchall()
    except Exception as erro:
        print(f"Erro na query de telefones: {erro}")
        return []
    finally:
        conn.close()
