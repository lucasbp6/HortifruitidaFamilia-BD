import psycopg2
from datetime import datetime
from conexao import conexao

from operacoes_crud import insert, select, delete, update
from operacoes_estoque import registrar_movimentacao_estoque, baixar_estoque
from operacoes_venda import abrir_operacao_caixa, finalizar_venda_transacao
from operacoes_consultas import select_enderecos_por_tipo, select_telefones_geral
from operacoes_pessoa import deletar_seguro



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


def inserir_pedido(ValorTotalPedido, TipoPedido, IDCliente, IDOperacao, schema ='hortifruti'):
    conn = conexao()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COALESCE(MAX(IDPedido), 0) + 1 FROM {schema}.PEDIDO")
            novo_id = cur.fetchone()[0]

            cur.execute(f"SELECT COALESCE(MAX(IDPag), 0) + 1 FROM {schema}.PAGAMENTO")
            novo_id_pag = cur.fetchone()[0]
            
            agora = datetime.now()
            insert(["PEDIDO"],
                [{
                    "IDPedido": novo_id,
                    "ValorTotalPedido": ValorTotalPedido,
                    "DataPedido": agora,
                    "TipoPedido": TipoPedido,
                    "IDCliente": IDCliente,
                    "IDOperacao": IDOperacao
                }],
                schema=schema
            )      
            conn.commit()
            return novo_id, novo_id_pag
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
        
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
