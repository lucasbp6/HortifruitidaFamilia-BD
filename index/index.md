# README - Índices e Otimização

Este documento descreve a proposta de índices de otimização para o banco de dados do projeto **Hortifruti da Família**.

O objetivo dos índices é melhorar o desempenho das consultas mais frequentes do sistema, especialmente nas operações de visualização, filtros, buscas por relacionamento e fluxo de venda.

## Ideia geral

No PostgreSQL, chaves primárias e restrições `UNIQUE` já criam índices automaticamente. Portanto, os campos usados como `PRIMARY KEY`, como `IDProd`, `IDCliente`, `IDPedido`, `IDForn` e outros, já possuem índices associados.

Mesmo assim, o banco pode se beneficiar de índices adicionais em colunas usadas com frequência em:

- filtros;
- buscas por nome;
- junções entre tabelas;
- relatórios;
- consultas por data;
- consultas relacionadas ao fluxo de caixa, estoque e vendas.

## Quando um índice é útil?

Um índice tende a ser útil quando a coluna aparece frequentemente em consultas com:

```sql
WHERE
JOIN
ORDER BY
GROUP BY
```

Por outro lado, índices em excesso podem prejudicar operações de escrita, como `INSERT`, `UPDATE` e `DELETE`, pois o banco precisa atualizar os índices a cada alteração.

Por isso, os índices abaixo foram pensados para consultas comuns do sistema, evitando criar índices desnecessários em todas as colunas.

## Índices para busca de produtos

Produtos são consultados frequentemente na aplicação, especialmente na visualização de dados, no cadastro e na frente de caixa.

```sql
CREATE INDEX idx_produto_nome
ON PRODUTO (NomeProd);
```

Esse índice ajuda em buscas e filtros por nome do produto.

```sql
CREATE INDEX idx_produto_categoria
ON PRODUTO (IDCat);
```

Esse índice ajuda em consultas que agrupam ou filtram produtos por categoria.

```sql
CREATE INDEX idx_produto_unidade
ON PRODUTO (IDUnidade);
```

Esse índice ajuda nas junções entre `PRODUTO` e `UNIDADEMEDIDA`.

## Índices para categorias

A tabela `CATEGORIA` possui uma autorreferência por meio de `IDCatPai`. Isso permite representar categorias principais e subcategorias.

```sql
CREATE INDEX idx_categoria_pai
ON CATEGORIA (IDCatPai);
```

Esse índice ajuda em consultas que buscam subcategorias de uma categoria principal.

## Índices para clientes, fornecedores e vendedores

Como a aplicação permite filtros e buscas por pessoas, os campos de nome são bons candidatos a índices.

```sql
CREATE INDEX idx_cliente_nome
ON CLIENTE (NomeCliente);
```

```sql
CREATE INDEX idx_fornecedor_nome
ON FORNECEDOR (NomeForn);
```

```sql
CREATE INDEX idx_vendedor_nome
ON VENDEDOR (NomeVend);
```

Esses índices ajudam na localização de clientes, fornecedores e vendedores pelo nome.

Os campos de CPF e CNPJ já são `UNIQUE`, portanto já possuem índices criados automaticamente pelo PostgreSQL.

## Índices para pedidos e vendas

Pedidos são uma parte central do sistema, pois conectam cliente, operação de caixa, itens e pagamentos.

```sql
CREATE INDEX idx_pedido_cliente
ON PEDIDO (IDCliente);
```

Esse índice ajuda a consultar pedidos de um determinado cliente.

```sql
CREATE INDEX idx_pedido_operacao
ON PEDIDO (IDOperacao);
```

Esse índice ajuda a consultar pedidos vinculados a uma operação de caixa.

```sql
CREATE INDEX idx_pedido_data
ON PEDIDO (DataPedido);
```

Esse índice ajuda em relatórios por período, como vendas do dia, da semana ou do mês.

Também é possível criar um índice composto para relatórios por cliente e data:

```sql
CREATE INDEX idx_pedido_cliente_data
ON PEDIDO (IDCliente, DataPedido);
```

Esse índice é útil quando a consulta filtra os pedidos de um cliente em um intervalo de datas.

## Índices para itens de pedido

A tabela `ITEMPEDIDO` liga produtos e pedidos. Como sua chave primária composta é formada por `IDProd` e `IDPedido`, já existe um índice composto nessa ordem.

Mesmo assim, se houver consultas frequentes que partem do pedido para buscar seus itens, pode ser útil criar um índice começando por `IDPedido`.

```sql
CREATE INDEX idx_itempedido_pedido
ON ITEMPEDIDO (IDPedido);
```

Esse índice ajuda em consultas como:

```sql
SELECT *
FROM ITEMPEDIDO
WHERE IDPedido = 10;
```

Também pode ajudar nas junções entre `PEDIDO` e `ITEMPEDIDO`.

## Índices para pagamentos

Pagamentos são consultados principalmente por pedido, método e data.

```sql
CREATE INDEX idx_pagamento_pedido
ON PAGAMENTO (IDPedido);
```

Esse índice ajuda a localizar pagamentos associados a um pedido.

```sql
CREATE INDEX idx_pagamento_data
ON PAGAMENTO (DataPag);
```

Esse índice ajuda em relatórios financeiros por período.

```sql
CREATE INDEX idx_pagamento_metodo
ON PAGAMENTO (MetodoPag);
```

Esse índice ajuda em consultas agregadas por forma de pagamento, como total recebido em dinheiro, débito, crédito ou Pix.

## Índices para operações de caixa

A tabela `OPERACAOCAIXA` registra abertura e fechamento de caixa.

```sql
CREATE INDEX idx_operacaocaixa_vendedor
ON OPERACAOCAIXA (IDVend);
```

Esse índice ajuda a consultar operações feitas por um vendedor específico.

```sql
CREATE INDEX idx_operacaocaixa_caixa
ON OPERACAOCAIXA (IDCaixa);
```

Esse índice ajuda a consultar operações associadas a um caixa específico.

```sql
CREATE INDEX idx_operacaocaixa_data_abertura
ON OPERACAOCAIXA (DataOpAber);
```

Esse índice ajuda em consultas por período de abertura de caixa.

## Índices para estoque

As tabelas `ENTRADAESTOQUE` e `PERDAESTOQUE` são importantes para rastrear movimentações de produtos.

```sql
CREATE INDEX idx_entradaestoque_produto
ON ENTRADAESTOQUE (IDProd);
```

```sql
CREATE INDEX idx_entradaestoque_fornecedor
ON ENTRADAESTOQUE (IDForn);
```

```sql
CREATE INDEX idx_entradaestoque_data
ON ENTRADAESTOQUE (EntradaData);
```

Esses índices ajudam a consultar entradas por produto, fornecedor ou período.

```sql
CREATE INDEX idx_perdaestoque_produto
ON PERDAESTOQUE (IDProd);
```

```sql
CREATE INDEX idx_perdaestoque_data
ON PERDAESTOQUE (DataPerda);
```

Esses índices ajudam a consultar perdas por produto ou por período.

## Índices para endereços

Endereços podem ser consultados por cidade, estado e CEP.

```sql
CREATE INDEX idx_endereco_cep
ON ENDERECO (CEPEnd);
```

```sql
CREATE INDEX idx_endereco_cidade_estado
ON ENDERECO (CidadeEnd, EstadoEnd);
```

O índice composto em cidade e estado ajuda em consultas que filtram endereços por localização.

## Índices para tabelas associativas de endereço

As tabelas associativas ligam clientes, fornecedores e vendedores aos seus endereços.

Como as chaves primárias compostas já criam índices, parte dessas consultas já fica otimizada. Ainda assim, quando a consulta parte do endereço para descobrir o dono, índices iniciados por `IDEndereco` podem ajudar.

```sql
CREATE INDEX idx_enderecocliente_endereco
ON ENDERECOCLIENTE (IDEndereco);
```

```sql
CREATE INDEX idx_enderecovendedor_endereco
ON ENDERECOVENDEDOR (IDEndereco);
```

```sql
CREATE INDEX idx_enderecofornec_endereco
ON ENDERECOFORNEC (IDEndereco);
```

## Índices para telefones

As tabelas de telefone são usadas para relacionar clientes e fornecedores aos seus números de contato.

```sql
CREATE INDEX idx_cliente_celcliente_idcliente
ON CLIENTE_CELCLIENTE (IDCliente);
```

```sql
CREATE INDEX idx_fornecedor_celforn_idforn
ON FORNECEDOR_CELFORN (IDForn);
```

Esses índices ajudam a recuperar telefones a partir do cliente ou fornecedor.

## Script sugerido de criação dos índices

Os índices podem ser reunidos em um arquivo separado, por exemplo:

```text
sql/indices.sql
```

Conteúdo sugerido:

```sql
-- Produtos
CREATE INDEX idx_produto_nome ON PRODUTO (NomeProd);
CREATE INDEX idx_produto_categoria ON PRODUTO (IDCat);
CREATE INDEX idx_produto_unidade ON PRODUTO (IDUnidade);

-- Categorias
CREATE INDEX idx_categoria_pai ON CATEGORIA (IDCatPai);

-- Pessoas
CREATE INDEX idx_cliente_nome ON CLIENTE (NomeCliente);
CREATE INDEX idx_fornecedor_nome ON FORNECEDOR (NomeForn);
CREATE INDEX idx_vendedor_nome ON VENDEDOR (NomeVend);

-- Pedidos
CREATE INDEX idx_pedido_cliente ON PEDIDO (IDCliente);
CREATE INDEX idx_pedido_operacao ON PEDIDO (IDOperacao);
CREATE INDEX idx_pedido_data ON PEDIDO (DataPedido);
CREATE INDEX idx_pedido_cliente_data ON PEDIDO (IDCliente, DataPedido);

-- Itens de pedido
CREATE INDEX idx_itempedido_pedido ON ITEMPEDIDO (IDPedido);

-- Pagamentos
CREATE INDEX idx_pagamento_pedido ON PAGAMENTO (IDPedido);
CREATE INDEX idx_pagamento_data ON PAGAMENTO (DataPag);
CREATE INDEX idx_pagamento_metodo ON PAGAMENTO (MetodoPag);

-- Operações de caixa
CREATE INDEX idx_operacaocaixa_vendedor ON OPERACAOCAIXA (IDVend);
CREATE INDEX idx_operacaocaixa_caixa ON OPERACAOCAIXA (IDCaixa);
CREATE INDEX idx_operacaocaixa_data_abertura ON OPERACAOCAIXA (DataOpAber);

-- Estoque
CREATE INDEX idx_entradaestoque_produto ON ENTRADAESTOQUE (IDProd);
CREATE INDEX idx_entradaestoque_fornecedor ON ENTRADAESTOQUE (IDForn);
CREATE INDEX idx_entradaestoque_data ON ENTRADAESTOQUE (EntradaData);
CREATE INDEX idx_perdaestoque_produto ON PERDAESTOQUE (IDProd);
CREATE INDEX idx_perdaestoque_data ON PERDAESTOQUE (DataPerda);

-- Endereços
CREATE INDEX idx_endereco_cep ON ENDERECO (CEPEnd);
CREATE INDEX idx_endereco_cidade_estado ON ENDERECO (CidadeEnd, EstadoEnd);

-- Associações de endereço
CREATE INDEX idx_enderecocliente_endereco ON ENDERECOCLIENTE (IDEndereco);
CREATE INDEX idx_enderecovendedor_endereco ON ENDERECOVENDEDOR (IDEndereco);
CREATE INDEX idx_enderecofornec_endereco ON ENDERECOFORNEC (IDEndereco);

-- Telefones
CREATE INDEX idx_cliente_celcliente_idcliente ON CLIENTE_CELCLIENTE (IDCliente);
CREATE INDEX idx_fornecedor_celforn_idforn ON FORNECEDOR_CELFORN (IDForn);
```

## Como testar se um índice está sendo usado

Para verificar se o PostgreSQL está usando um índice, pode-se utilizar o comando `EXPLAIN`.

Exemplo:

```sql
EXPLAIN
SELECT *
FROM PRODUTO
WHERE IDCat = 4;
```

Para obter uma análise com tempo real de execução:

```sql
EXPLAIN ANALYZE
SELECT *
FROM PRODUTO
WHERE IDCat = 4;
```

Se o índice estiver sendo usado, o plano pode indicar operações como `Index Scan` ou `Bitmap Index Scan`.

## Cuidados

Nem todo índice melhora o desempenho em todos os casos.

Em tabelas pequenas, o PostgreSQL pode preferir fazer uma varredura sequencial (`Seq Scan`), pois isso pode ser mais barato do que usar um índice.

Além disso, índices deixam operações de inserção, atualização e deleção um pouco mais custosas. Por isso, a escolha dos índices deve considerar as consultas mais importantes do sistema.

## Resumo dos índices mais importantes

Os índices prioritários para o projeto são:

```sql
CREATE INDEX idx_produto_nome ON PRODUTO (NomeProd);
CREATE INDEX idx_produto_categoria ON PRODUTO (IDCat);
CREATE INDEX idx_pedido_cliente ON PEDIDO (IDCliente);
CREATE INDEX idx_pedido_operacao ON PEDIDO (IDOperacao);
CREATE INDEX idx_pedido_data ON PEDIDO (DataPedido);
CREATE INDEX idx_itempedido_pedido ON ITEMPEDIDO (IDPedido);
CREATE INDEX idx_pagamento_pedido ON PAGAMENTO (IDPedido);
CREATE INDEX idx_operacaocaixa_vendedor ON OPERACAOCAIXA (IDVend);
CREATE INDEX idx_entradaestoque_produto ON ENTRADAESTOQUE (IDProd);
CREATE INDEX idx_perdaestoque_produto ON PERDAESTOQUE (IDProd);
```

Esses índices cobrem as principais consultas esperadas do sistema: busca de produtos, fluxo de vendas, relacionamento entre pedidos e pagamentos, controle de caixa e movimentações de estoque.
