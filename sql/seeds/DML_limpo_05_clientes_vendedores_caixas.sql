BEGIN;

SET search_path TO hortifruti;

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

COMMIT;
