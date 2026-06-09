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

-- ============================================================
-- UNIDADES DE MEDIDA
-- ============================================================
-- Unidades usadas no cadastro de produtos do hortifruti.

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


-- ============================================================
-- FORNECEDORES
-- ============================================================
-- Fornecedores ficticios para abastecimento do hortifruti.
-- CNPJs usam 14 digitos, sem pontuacao, para respeitar o tipo CHAR(14).

INSERT INTO FORNECEDOR
  (IDForn, NomeForn, CNPJForn)
VALUES
  (1, 'Sitio Boa Terra',            '11222333000101'),
  (2, 'Fazenda Sol Nascente',       '22333444000102'),
  (3, 'Cooperativa Verde Vale',     '33444555000103'),
  (4, 'Distribuidora Frutal',       '44555666000104'),
  (5, 'Organicos Serra Azul',       '55666777000105'),
  (6, 'Graos do Interior',          '66777888000106'),
  (7, 'Avicola Santa Clara',        '77888999000107'),
  (8, 'Bebidas Fonte Clara',        '88999000000108');


-- ============================================================
-- CLIENTES
-- ============================================================
-- CPFs usam 11 digitos, sem pontuacao, para respeitar o tipo CHAR(11).

INSERT INTO CLIENTE
  (IDCliente, NomeCliente, DataNascCliente, CPFCliente)
VALUES
  (1,  'Mariana Souza',       '1992-03-14', '12345678901'),
  (2,  'Carlos Henrique',     '1985-07-22', '23456789012'),
  (3,  'Ana Paula Martins',   '1998-11-05', '34567890123'),
  (4,  'Roberto Lima',        '1979-01-30', '45678901234'),
  (5,  'Fernanda Alves',      '1990-09-18', '56789012345'),
  (6,  'Juliana Castro',      '1995-12-02', '67890123456'),
  (7,  'Pedro Nascimento',    '1988-06-09', '78901234567'),
  (8,  'Camila Rocha',        '2001-04-25', '89012345678'),
  (9,  'Lucas Andrade',       '1993-08-17', '90123456789'),
  (10, 'Beatriz Oliveira',    '1986-10-11', '01234567890');

-- ============================================================
-- VENDEDORES
-- ============================================================
-- Vendedores ficticios para operacao de caixa e atendimento.

INSERT INTO VENDEDOR
  (IDVend, NomeVend, CPFVend, DataNascVend, CelVend, SalarioVend)
VALUES
  (0, 'Vendedor Padrao',      '00000000000', '1990-01-01', '11900000000', 0.00),
  (1, 'Joao Pereira',         '11122233344', '1994-05-12', '11981234567', 2200.00),
  (2, 'Larissa Gomes',        '22233344455', '1997-09-03', '11982345678', 2350.00),
  (3, 'Rafael Mendes',        '33344455566', '1989-02-19', '11983456789', 2500.00),
  (4, 'Patricia Nunes',       '44455566677', '1991-12-08', '11984567890', 2300.00);

-- ============================================================
-- CAIXAS
-- ============================================================
-- Caixas fisicos usados na frente de caixa.

INSERT INTO CAIXA
  (IDCaixa, TipoCaixa)
VALUES
  (1, 'Caixa 1'),
  (2, 'Caixa 2'),
  (3, 'Caixa Rapido'),
  (4, 'Delivery');


-- ============================================================
-- ENDERECOS
-- ============================================================
-- Enderecos ficticios para clientes, fornecedores e vendedores.
-- CEP usa 8 digitos, sem pontuacao, para respeitar o tipo CHAR(8).
-- Estado usa UF com 2 caracteres, para respeitar o tipo CHAR(2).

INSERT INTO ENDERECO
  (IDEndereco, RuaEnd, NumeroEnd, ComplemEnd, CEPEnd, BairroEnd, CidadeEnd, EstadoEnd, PaisEnd)
VALUES
  -- Enderecos de clientes
  (1,  'Rua das Laranjeiras',      120, 'Apto 31',     '01001000', 'Centro',          'Sao Paulo',     'SP', 'Brasil'),
  (2,  'Av Brasil',                450, NULL,          '01002000', 'Jardins',         'Sao Paulo',     'SP', 'Brasil'),
  (3,  'Rua do Mercado',            88, 'Casa 2',      '01003000', 'Vila Nova',       'Sao Paulo',     'SP', 'Brasil'),
  (4,  'Rua Primavera',            305, NULL,          '01004000', 'Bela Vista',      'Sao Paulo',     'SP', 'Brasil'),
  (5,  'Alameda das Flores',        77, 'Bloco B',     '01005000', 'Mooca',           'Sao Paulo',     'SP', 'Brasil'),
  (6,  'Rua das Palmeiras',        612, NULL,          '01006000', 'Perdizes',        'Sao Paulo',     'SP', 'Brasil'),
  (7,  'Rua Santa Clara',           44, 'Fundos',      '01007000', 'Santana',         'Sao Paulo',     'SP', 'Brasil'),
  (8,  'Av dos Bandeirantes',      900, NULL,          '01008000', 'Brooklin',        'Sao Paulo',     'SP', 'Brasil'),
  (9,  'Rua Monte Azul',           155, 'Apto 12',     '01009000', 'Ipiranga',        'Sao Paulo',     'SP', 'Brasil'),
  (10, 'Rua Boa Esperanca',        230, NULL,          '01010000', 'Tatuape',         'Sao Paulo',     'SP', 'Brasil'),

  -- Enderecos de fornecedores
  (11, 'Estrada Rural 1',           10, 'Galpao A',    '13001000', 'Zona Rural',      'Campinas',      'SP', 'Brasil'),
  (12, 'Rodovia dos Produtores',   250, NULL,          '13840000', 'Distrito Rural',  'Mogi Mirim',    'SP', 'Brasil'),
  (13, 'Av Cooperativa',           800, 'Unidade 3',   '12220000', 'Industrial',      'Sao Jose Campos','SP', 'Brasil'),
  (14, 'Rua das Frutas',           321, 'Deposito',    '05001000', 'Lapa',            'Sao Paulo',     'SP', 'Brasil'),
  (15, 'Estrada Serra Azul',        72, NULL,          '12460000', 'Serra Azul',      'Campos Jordao', 'SP', 'Brasil'),
  (16, 'Rua dos Graos',            190, 'Sala 4',      '14020000', 'Centro',          'Ribeirao Preto','SP', 'Brasil'),
  (17, 'Av das Granjas',           405, NULL,          '18010000', 'Granja Clara',    'Sorocaba',      'SP', 'Brasil'),
  (18, 'Rua Fonte Clara',          510, 'Galpao 2',    '13200000', 'Industrial',      'Jundiai',       'SP', 'Brasil'),

  -- Enderecos de vendedores
  (19, 'Rua do Caixa',              25, NULL,          '01111000', 'Centro',          'Sao Paulo',     'SP', 'Brasil'),
  (20, 'Rua Atendimento',          130, 'Apto 8',      '01112000', 'Liberdade',       'Sao Paulo',     'SP', 'Brasil'),
  (21, 'Av Hortifruti',            760, NULL,          '01113000', 'Vila Mariana',    'Sao Paulo',     'SP', 'Brasil'),
  (22, 'Rua das Bancas',            92, 'Casa 1',      '01114000', 'Saude',           'Sao Paulo',     'SP', 'Brasil');

-- ============================================================
-- VINCULOS ENTRE ENDERECOS E PESSOAS/EMPRESAS
-- ============================================================

INSERT INTO ENDERECOCLIENTE
  (IDCliente, IDEndereco)
VALUES
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 5),
  (6, 6),
  (7, 7),
  (8, 8),
  (9, 9),
  (10, 10);

INSERT INTO ENDERECOFORNEC
  (IDForn, IDEndereco)
VALUES
  (1, 11),
  (2, 12),
  (3, 13),
  (4, 14),
  (5, 15),
  (6, 16),
  (7, 17),
  (8, 18);

INSERT INTO ENDERECOVENDEDOR
  (IDVend, IDEndereco)
VALUES
  (1, 19),
  (2, 20),
  (3, 21),
  (4, 22);

-- ============================================================
-- TELEFONES DE CLIENTES E FORNECEDORES
-- ============================================================
-- Vendedores ja possuem telefone diretamente na tabela VENDEDOR.
-- Clientes e fornecedores possuem tabelas proprias para permitir multiplos telefones.

INSERT INTO CLIENTE_CELCLIENTE
  (CelCliente, IDCliente)
VALUES
  ('11970000001', 1),
  ('11970000002', 2),
  ('11970000003', 3),
  ('11970000004', 4),
  ('11970000005', 5),
  ('11970000006', 6),
  ('11970000007', 7),
  ('11970000008', 8),
  ('11970000009', 9),
  ('11970000010', 10),
  ('11971110001', 1),
  ('11971110005', 5);

INSERT INTO FORNECEDOR_CELFORN
  (CelForn, IDForn)
VALUES
  ('11960000001', 1),
  ('11960000002', 2),
  ('11960000003', 3),
  ('11960000004', 4),
  ('11960000005', 5),
  ('11960000006', 6),
  ('11960000007', 7),
  ('11960000008', 8),
  ('11961110004', 4),
  ('11961110008', 8);


-- ============================================================
-- ENTRADAS DE ESTOQUE
-- ============================================================
-- Registros historicos de abastecimento por fornecedor e produto.
-- O estoque atual dos produtos ja foi definido no cadastro de PRODUTO.
-- Estes registros servem para consultas e relatorios de movimentacao.

INSERT INTO ENTRADAESTOQUE
  (IDEntrada, IDForn, IDProd, EntradaData, EntradaQtd, EntradaPreco)
VALUES
  -- Frutas
  (1,  1,  1,  '2025-01-03 08:15:00', 100.000, 3.80),
  (2,  4,  2,  '2025-01-03 09:00:00',  60.000, 5.60),
  (3,  4,  3,  '2025-01-04 08:40:00',  90.000, 2.90),
  (4,  1,  4,  '2025-01-04 10:10:00',  40.000, 4.20),
  (5,  4,  5,  '2025-01-05 07:50:00',  35.000, 5.10),
  (6,  4,  6,  '2025-01-05 08:25:00',  45.000, 4.30),
  (7,  4,  7,  '2025-01-06 09:15:00',  30.000, 8.20),
  (8,  4,  8,  '2025-01-06 09:30:00',  38.000, 6.70),
  (9,  1,  9,  '2025-01-07 07:40:00', 150.000, 1.90),
  (10, 1,  10, '2025-01-07 08:05:00',  55.000, 2.50),

  -- Verduras e legumes
  (11, 2,  11, '2025-01-08 07:30:00',  70.000, 2.10),
  (12, 2,  12, '2025-01-08 07:45:00',  50.000, 1.80),
  (13, 2,  13, '2025-01-08 08:00:00',  35.000, 2.70),
  (14, 2,  14, '2025-01-08 08:20:00',  40.000, 2.20),
  (15, 3,  15, '2025-01-09 07:55:00',  85.000, 4.90),
  (16, 3,  16, '2025-01-09 08:10:00',  45.000, 3.30),
  (17, 3,  17, '2025-01-09 08:25:00',  50.000, 2.90),
  (18, 3,  18, '2025-01-10 09:00:00',  35.000, 5.00),
  (19, 3,  19, '2025-01-10 09:20:00',  30.000, 3.80),

  -- Raizes e temperos
  (20, 1,  20, '2025-01-11 07:30:00', 120.000, 2.80),
  (21, 1,  21, '2025-01-11 07:50:00',  70.000, 3.10),
  (22, 1,  22, '2025-01-11 08:15:00',  80.000, 2.60),
  (23, 1,  23, '2025-01-12 08:00:00', 100.000, 2.90),
  (24, 1,  24, '2025-01-12 08:30:00',  50.000, 4.70),
  (25, 1,  25, '2025-01-12 09:00:00',  60.000, 2.30),
  (26, 2,  26, '2025-01-13 07:30:00',  45.000, 1.40),
  (27, 2,  27, '2025-01-13 07:45:00',  45.000, 1.40),
  (28, 2,  28, '2025-01-13 08:00:00',  30.000, 1.30),
  (29, 2,  29, '2025-01-13 08:15:00',  25.000, 2.20),

  -- Organicos, mercearia, bebidas e apoio
  (30, 5,  30, '2025-01-14 08:10:00',  35.000, 5.10),
  (31, 5,  31, '2025-01-14 08:20:00',  25.000, 3.20),
  (32, 6,  32, '2025-01-15 10:00:00',  35.000, 16.50),
  (33, 6,  33, '2025-01-15 10:20:00',  45.000, 5.20),
  (34, 8,  34, '2025-01-16 11:00:00',  28.000, 10.80),
  (35, 8,  35, '2025-01-16 11:15:00',  80.000, 1.20),
  (36, 7,  36, '2025-01-17 09:30:00',  30.000, 8.00),
  (37, 7,  37, '2025-01-17 09:45:00',  22.000, 11.00),
  (38, 6,  38, '2025-01-18 10:10:00',  20.000, 13.50),
  (39, 3,  39, '2025-01-18 10:40:00',  40.000, 1.90),
  (40, 3,  40, '2025-01-18 10:55:00',  50.000, 1.30);

-- ============================================================
-- PERDAS DE ESTOQUE
-- ============================================================
-- Registros de perdas comuns em hortifruti: avaria, vencimento,
-- excesso de maturacao e quebra no manuseio.

INSERT INTO PERDAESTOQUE
  (IDPerda, DataPerda, QtdPerda, MotivoPerda, ValorUnPerda, IDProd)
VALUES
  (1,  '2025-01-06 17:30:00',  4.000, 'Frutas amassadas durante o transporte',       3.80,  1),
  (2,  '2025-01-07 18:10:00',  2.000, 'Bandejas danificadas na exposicao',            6.70,  8),
  (3,  '2025-01-08 18:00:00',  5.000, 'Folhas murchas ao fim do dia',                 2.10,  11),
  (4,  '2025-01-09 18:20:00',  3.000, 'Produto improprio para venda',                 1.80,  12),
  (5,  '2025-01-10 17:45:00',  4.500, 'Tomates muito maduros',                        4.90,  15),
  (6,  '2025-01-11 18:30:00',  6.000, 'Batatas com avarias',                          2.80,  20),
  (7,  '2025-01-12 18:10:00',  3.000, 'Cenouras quebradas no manuseio',               2.60,  22),
  (8,  '2025-01-13 17:50:00',  2.000, 'Macos de tempero ressecados',                  1.40,  26),
  (9,  '2025-01-14 18:15:00',  1.000, 'Alface organica murcha',                       3.20,  31),
  (10, '2025-01-15 18:40:00',  1.000, 'Pacote rasgado',                               16.50, 32),
  (11, '2025-01-16 19:00:00',  2.000, 'Garrafas com embalagem danificada',            10.80, 34),
  (12, '2025-01-17 18:30:00',  1.000, 'Duzia com ovos quebrados',                     8.00,  36),
  (13, '2025-01-18 18:10:00',  3.000, 'Melancia aberta para descarte parcial',        1.90,  9),
  (14, '2025-01-19 17:55:00',  2.000, 'Mandioca com partes escurecidas',              2.30,  25),
  (15, '2025-01-20 18:05:00',  1.500, 'Produto organico fora do padrao visual',       5.10,  30);


-- ============================================================
-- OPERACOES DE CAIXA
-- ============================================================
-- Operacoes fechadas, com saldo igual ao total vendido em cada operacao.
-- ValorOpFecham = ValorOpAber + SaldoOp.

INSERT INTO OPERACAOCAIXA
  (IDOperacao, DataOpAber, ValorOpAber, DataOpFecham, ValorOpFecham, SaldoOp, IDVend, IDCaixa)
VALUES
  (1, '2025-01-20 08:00:00', 200.00, '2025-01-20 18:00:00', 299.69, 99.69, 1, 1),
  (2, '2025-01-21 08:00:00', 180.00, '2025-01-21 18:10:00', 312.93, 132.93, 2, 2),
  (3, '2025-01-22 08:00:00', 220.00, '2025-01-22 18:05:00', 320.30, 100.30, 3, 3),
  (4, '2025-01-23 08:00:00', 200.00, '2025-01-23 18:20:00', 317.15, 117.15, 4, 1);

-- ============================================================
-- PEDIDOS
-- ============================================================
-- Pedidos vinculados a clientes e operacoes de caixa.
-- ValorTotalPedido corresponde a soma dos itens de cada pedido.

INSERT INTO PEDIDO
  (IDPedido, ValorTotalPedido, DataPedido, TipoPedido, IDCliente, IDOperacao)
VALUES
  (1, 26.72, '2025-01-20 09:35:00', 'Venda', 1, 1),
  (2, 26.27, '2025-01-20 10:20:00', 'Venda', 2, 1),
  (3, 46.70, '2025-01-20 11:05:00', 'Delivery', 3, 1),
  (4, 31.95, '2025-01-21 09:15:00', 'Venda', 4, 2),
  (5, 56.60, '2025-01-21 10:45:00', 'Venda', 5, 2),
  (6, 44.38, '2025-01-21 12:30:00', 'Delivery', 6, 2),
  (7, 34.98, '2025-01-22 08:55:00', 'Venda', 7, 3),
  (8, 35.35, '2025-01-22 10:10:00', 'Venda', 8, 3),
  (9, 29.97, '2025-01-22 13:40:00', 'Delivery', 9, 3),
  (10, 28.92, '2025-01-23 09:25:00', 'Venda', 10, 4),
  (11, 48.78, '2025-01-23 11:50:00', 'Venda', 1, 4),
  (12, 39.45, '2025-01-23 15:10:00', 'Delivery', 3, 4);

-- ============================================================
-- ITENS DOS PEDIDOS
-- ============================================================
-- Cada linha representa um produto vendido em um pedido.
-- PrecoUn foi mantido igual ao preco de venda cadastrado no produto.

INSERT INTO ITEMPEDIDO
  (IDProd, IDPedido, QtdItem, DescItem, PrecoUn)
VALUES
  (1, 1, 2.000, 0.00, 6.99),
  (11, 1, 1.000, 0.00, 4.50),
  (22, 1, 1.500, 0.00, 5.49),
  (15, 2, 1.200, 0.00, 8.99),
  (20, 2, 2.000, 0.00, 5.99),
  (27, 2, 1.000, 0.00, 3.50),
  (8, 3, 2.000, 0.00, 11.90),
  (7, 3, 1.000, 0.00, 13.90),
  (35, 3, 3.000, 0.00, 3.00),
  (3, 4, 3.000, 0.00, 5.49),
  (23, 4, 2.000, 0.00, 5.99),
  (26, 4, 1.000, 0.00, 3.50),
  (32, 5, 1.000, 0.00, 24.90),
  (33, 5, 2.000, 0.00, 8.90),
  (36, 5, 1.000, 0.00, 13.90),
  (30, 6, 1.500, 0.00, 8.99),
  (31, 6, 2.000, 0.00, 6.50),
  (34, 6, 1.000, 0.00, 17.90),
  (2, 7, 1.300, 0.00, 9.99),
  (4, 7, 2.000, 0.00, 8.50),
  (10, 7, 1.000, 0.00, 4.99),
  (5, 8, 1.000, 0.00, 9.90),
  (9, 8, 5.000, 0.00, 3.49),
  (12, 8, 2.000, 0.00, 4.00),
  (18, 9, 1.000, 0.00, 9.49),
  (19, 9, 1.000, 0.00, 7.50),
  (21, 9, 2.000, 0.00, 6.49),
  (6, 10, 2.000, 0.00, 7.99),
  (16, 10, 1.500, 0.00, 6.49),
  (28, 10, 1.000, 0.00, 3.20),
  (37, 11, 1.000, 0.00, 18.90),
  (38, 11, 1.000, 0.00, 21.90),
  (39, 11, 2.000, 0.00, 3.99),
  (14, 12, 2.000, 0.00, 4.80),
  (17, 12, 2.000, 0.00, 5.99),
  (24, 12, 1.000, 0.00, 8.90),
  (40, 12, 3.000, 0.00, 2.99);

-- ============================================================
-- PAGAMENTOS
-- ============================================================
-- Um pagamento para cada pedido, com valor igual ao total do pedido.

INSERT INTO PAGAMENTO
  (IDPag, MetodoPag, ValorPag, DataPag, IDPedido)
VALUES
  (1, 'Pix', 26.72, '2025-01-20 09:35:00', 1),
  (2, 'Débito', 26.27, '2025-01-20 10:20:00', 2),
  (3, 'Crédito', 46.70, '2025-01-20 11:05:00', 3),
  (4, 'Dinheiro', 31.95, '2025-01-21 09:15:00', 4),
  (5, 'Pix', 56.60, '2025-01-21 10:45:00', 5),
  (6, 'Débito', 44.38, '2025-01-21 12:30:00', 6),
  (7, 'Crédito', 34.98, '2025-01-22 08:55:00', 7),
  (8, 'Pix', 35.35, '2025-01-22 10:10:00', 8),
  (9, 'Débito', 29.97, '2025-01-22 13:40:00', 9),
  (10, 'Dinheiro', 28.92, '2025-01-23 09:25:00', 10),
  (11, 'Pix', 48.78, '2025-01-23 11:50:00', 11),
  (12, 'Crédito', 39.45, '2025-01-23 15:10:00', 12);


COMMIT;
