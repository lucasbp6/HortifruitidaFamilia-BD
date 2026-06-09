BEGIN;

SET search_path TO hortifruti;

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

COMMIT;
