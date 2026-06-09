BEGIN;

SET search_path TO hortifruti;

-- ============================================================
-- PRODUTOS
-- ============================================================
-- Produtos cadastrados com categorias e unidades coerentes.
-- IDs de categoria e unidade dependem dos inserts anteriores:
-- CATEGORIA e UNIDADEMEDIDA.

INSERT INTO PRODUTO
  (IDProd, NomeProd, DescricaoProd, PrecoVendaProd, EstoqueAtualProd, PrecoCustoProd, IDUnidade, IDCat)
VALUES
  -- Frutas
  (1,  'Banana Prata',     'Banana prata vendida por kg',                         6.99,  80.000, 3.80, 1, 2),
  (2,  'Maca Gala',        'Maca gala selecionada vendida por kg',                 9.99,  45.000, 5.60, 1, 2),
  (3,  'Laranja Pera',     'Laranja pera para mesa ou suco vendida por kg',        5.49,  70.000, 2.90, 1, 2),
  (4,  'Mamao Papaya',     'Mamao papaya vendido por unidade',                     8.50,  35.000, 4.20, 3, 2),
  (5,  'Abacaxi',          'Abacaxi perola vendido por unidade',                   9.90,  28.000, 5.10, 3, 2),
  (6,  'Manga Palmer',     'Manga palmer vendida por kg',                          7.99,  32.000, 4.30, 1, 2),
  (7,  'Uva Thompson',     'Uva thompson sem semente em bandeja',                 13.90,  24.000, 8.20, 5, 2),
  (8,  'Morango',          'Morango fresco em bandeja',                           11.90,  30.000, 6.70, 5, 2),
  (9,  'Melancia',         'Melancia vendida por kg',                              3.49, 120.000, 1.90, 1, 2),
  (10, 'Limao Tahiti',     'Limao tahiti vendido por kg',                          4.99,  40.000, 2.50, 1, 2),

  -- Verduras
  (11, 'Alface Crespa',    'Alface crespa vendida por unidade',                    4.50,  55.000, 2.10, 3, 3),
  (12, 'Couve Manteiga',   'Couve manteiga vendida por maco',                      4.00,  36.000, 1.80, 4, 3),
  (13, 'Espinafre',        'Espinafre fresco vendido por maco',                    5.50,  22.000, 2.70, 4, 3),
  (14, 'Rucula',           'Rucula fresca vendida por maco',                       4.80,  26.000, 2.20, 4, 3),

  -- Legumes
  (15, 'Tomate Italiano',  'Tomate italiano vendido por kg',                       8.99,  65.000, 4.90, 1, 4),
  (16, 'Pepino Japones',   'Pepino japones vendido por kg',                        6.49,  34.000, 3.30, 1, 4),
  (17, 'Abobrinha',        'Abobrinha italiana vendida por kg',                    5.99,  38.000, 2.90, 1, 4),
  (18, 'Pimentao Verde',   'Pimentao verde vendido por kg',                        9.49,  25.000, 5.00, 1, 4),
  (19, 'Brocolis',         'Brocolis vendido por unidade',                         7.50,  20.000, 3.80, 3, 4),

  -- Raizes
  (20, 'Batata Inglesa',   'Batata inglesa vendida por kg',                        5.99,  90.000, 2.80, 1, 5),
  (21, 'Batata Doce',      'Batata doce vendida por kg',                           6.49,  50.000, 3.10, 1, 5),
  (22, 'Cenoura',          'Cenoura vendida por kg',                               5.49,  60.000, 2.60, 1, 5),
  (23, 'Cebola',           'Cebola vendida por kg',                                5.99,  75.000, 2.90, 1, 5),
  (24, 'Alho',             'Alho vendido por pacote',                              8.90,  40.000, 4.70, 6, 5),
  (25, 'Mandioca',         'Mandioca vendida por kg',                              4.99,  45.000, 2.30, 1, 5),

  -- Temperos
  (26, 'Salsa',            'Salsa fresca vendida por maco',                        3.50,  30.000, 1.40, 4, 6),
  (27, 'Cebolinha',        'Cebolinha fresca vendida por maco',                    3.50,  30.000, 1.40, 4, 6),
  (28, 'Coentro',          'Coentro fresco vendido por maco',                      3.20,  20.000, 1.30, 4, 6),
  (29, 'Manjericao',       'Manjericao fresco vendido por maco',                   4.90,  18.000, 2.20, 4, 6),

  -- Organicos
  (30, 'Banana Organica',  'Banana organica vendida por kg',                       8.99,  25.000, 5.10, 1, 7),
  (31, 'Alface Organica',  'Alface organica vendida por unidade',                  6.50,  18.000, 3.20, 3, 7),

  -- Mercearia, bebidas, ovos e embalados
  (32, 'Arroz Integral',   'Arroz integral tipo 1 em pacote',                      24.90,  25.000, 16.50, 6, 9),
  (33, 'Feijao Carioca',   'Feijao carioca em pacote',                             8.90,  35.000, 5.20, 6, 9),
  (34, 'Suco Uva Integral','Suco de uva integral em garrafa',                      17.90,  20.000, 10.80, 7, 10),
  (35, 'Agua Mineral',     'Agua mineral sem gas',                                  3.00,  60.000, 1.20, 7, 10),
  (36, 'Ovos Brancos',     'Ovos brancos em duzia',                                13.90,  22.000, 8.00, 10, 11),
  (37, 'Ovos Caipiras',    'Ovos caipiras em duzia',                               18.90,  16.000, 11.00, 10, 11),
  (38, 'Castanha Caju',    'Castanha de caju em pacote',                           21.90,  14.000, 13.50, 6, 12),

  -- Apoio de loja
  (39, 'Detergente',       'Detergente neutro para limpeza',                        3.99,  30.000, 1.90, 3, 13),
  (40, 'Sabonete',         'Sabonete para higiene pessoal',                         2.99,  40.000, 1.30, 3, 14);

COMMIT;
