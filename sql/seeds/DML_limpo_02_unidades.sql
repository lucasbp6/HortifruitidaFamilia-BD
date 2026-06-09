BEGIN;

SET search_path TO hortifruti;

-- ============================================================
-- UNIDADES DE MEDIDA
-- ============================================================
-- Unidades usadas no cadastro de produtos do hortifruti.
-- Devem ser inseridas antes dos produtos, pois PRODUTO.IDUnidade
-- referencia UNIDADEMEDIDA.IDUnidade.

INSERT INTO UNIDADEMEDIDA (IDUnidade, NomeUnidade, SiglaUnidade) VALUES
  (1,  'Quilograma',  'kg'),
  (2,  'Grama',       'g'),
  (3,  'Unidade',     'un'),
  (4,  'Maco',        'mc'),
  (5,  'Bandeja',     'bdj'),
  (6,  'Pacote',      'pct'),
  (7,  'Litro',       'L'),
  (8,  'Mililitro',   'mL'),
  (9,  'Caixa',       'cx'),
  (10, 'Duzia',       'dz');

COMMIT;
