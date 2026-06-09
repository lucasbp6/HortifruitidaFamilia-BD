BEGIN;

SET search_path TO hortifruti;

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

COMMIT;
