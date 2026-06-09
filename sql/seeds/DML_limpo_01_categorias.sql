BEGIN;

SET search_path TO hortifruti;

-- ============================================================
-- LIMPEZA DO BANCO
-- ============================================================
-- Este TRUNCATE zera os dados das tabelas do schema hortifruti.
-- O CASCADE remove também dados dependentes por chave estrangeira.
-- Como usamos IDs manuais, o RESTART IDENTITY fica preparado caso
-- futuramente alguma tabela passe a usar SERIAL/IDENTITY.

TRUNCATE TABLE
  CLIENTE_CELCLIENTE,
  FORNECEDOR_CELFORN,
  ENDERECOFORNEC,
  ENDERECOVENDEDOR,
  ENDERECOCLIENTE,
  ENTRADAESTOQUE,
  PERDAESTOQUE,
  ITEMPEDIDO,
  PAGAMENTO,
  PEDIDO,
  OPERACAOCAIXA,
  CAIXA,
  VENDEDOR,
  CLIENTE,
  FORNECEDOR,
  PRODUTO,
  UNIDADEMEDIDA,
  ENDERECO,
  CATEGORIA
RESTART IDENTITY CASCADE;

-- ============================================================
-- CATEGORIAS
-- ============================================================
-- Estrutura hierárquica:
-- categorias principais têm IDCatPai = NULL;
-- subcategorias apontam para sua categoria principal.

INSERT INTO CATEGORIA (IDCat, NomeCat, IDCatPai) VALUES
  (1,  'Hortifruti',   NULL),
  (2,  'Frutas',       1),
  (3,  'Verduras',     1),
  (4,  'Legumes',      1),
  (5,  'Raizes',       1),
  (6,  'Temperos',     1),
  (7,  'Organicos',    1),

  (8,  'Mercearia',    NULL),
  (9,  'Graos',        8),
  (10, 'Bebidas',      8),
  (11, 'Ovos',         8),
  (12, 'Embalados',    8),

  (13, 'Limpeza',      NULL),
  (14, 'Higiene',      NULL);

COMMIT;
