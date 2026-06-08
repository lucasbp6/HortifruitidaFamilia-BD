from operacoes_crud import insert, select, delete, update

from operacoes_estoque import (
    registrar_movimentacao_estoque,
    baixar_estoque,
)

from operacoes_venda import (
    abrir_operacao_caixa,
    finalizar_venda_transacao,
)

from operacoes_consultas import (
    select_enderecos_por_tipo,
    select_telefones_geral,
)

from operacoes_pessoa import deletar_seguro