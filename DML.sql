-- Inserir dados na tabela Categoria
INSERT INTO Categoria  VALUES (1, 'Hortifruti');
INSERT INTO Categoria  VALUES (2, 'Mercearia');
INSERT INTO Categoria  VALUES (3, 'Legumes', 1);
INSERT INTO Categoria  VALUES (4, 'Frutas', 1);
INSERT INTO Categoria  VALUES (5, 'Bebidas', 2);
INSERT INTO Categoria  VALUES (6, 'Verduras', 1);
INSERT INTO Categoria  VALUES (7, 'Limpeza', 2);
INSERT INTO Categoria  VALUES (8, 'Temperos', 2);
INSERT INTO Categoria  VALUES (9, 'Alimentação', 2);

-- Inserir dados na tabela Produto
INSERT INTO Produto VALUES 
(IDProd, 'Cebolinha','Erva aromática de sabor suave, utilizada para finalização de pratos.',5.00, 8.00, 'Un', IDCat),
(IDProd, 'Tomate','Vermelhinho e saudavel.',11.99, 80.00, 'Kg', IDCat),
(IDProd, 'açucar','Branco e doce, utilizado para adoçar alimentos e bebidas.', 5.49, 15.00, 'Un', IDCat),
(IDProd, 'batata','Tubérculo versátil, utilizado em diversas receitas culinárias.',5.99, 60.00, 'Kg', IDCat),
(IDProd, 'cebola','Vegetal de sabor forte, utilizado como base para muitos pratos.',4.99, 60.00, 'Kg', IDCat),
(IDProd, 'couve manteiga','Folha verde escura, utilizada em saladas e refogados.',8.00, 7.00, 'Maço', IDCat),
(IDProd, 'rucula','Folha verde com sabor picante, utilizada em saladas e pratos gourmet.',8.00, 7.00, 'Maço', IDCat),
(IDProd, 'alho','Bulbo aromático, utilizado para temperar e dar sabor a diversos pratos.',36.99, 25.00, 'Kg', IDCat),
(IDProd, 'leite','Bebida nutritiva, utilizada para consumo direto e em receitas culinárias.',3.69, 36.00, 'Un', IDCat),
(IDProd, 'beterraba','Raiz de cor vermelha intensa, utilizada em saladas e sucos.',5.99, 20.00, 'Kg', IDCat);
(IDProd, 'cenoura','Raiz de cor laranja, utilizada em saladas, sopas e sucos.',6.49, 15.00, 'Kg', IDCat);
(IDProd, 'inhame','Tubérculo de sabor suave, utilizado em diversas receitas culinárias.',14.49, 10.00, 'Kg', IDCat);
(IDProd, 'laranja pera','Fruta cítrica de sabor doce e suculento, utilizada para consumo direto e em sucos.',3.99, 120.00, 'Kg', IDCat);
(IDProd, 'melancia','Fruta grande e refrescante, com polpa vermelha e sementes pretas, utilizada para consumo direto e em sucos.',3.79, 300.00, 'Kg', IDCat);
(IDProd, 'feijão carioquinha','Leguminosa de sabor suave, utilizada em pratos tradicionais da culinária brasileira.',5.99, 15.00, 'Un', IDCat);
(IDProd, 'sal','Condimento essencial, utilizado para realçar o sabor dos alimentos.',2.99, 20.00, 'Un', IDCat);
(IDProd, 'oleo de soja','Óleo vegetal versátil, utilizado para cozinhar e fritar alimentos.',9.99, 36.00, 'Un', IDCat);
(IDProd, 'polpa de frutas','Produto processado a partir de frutas, utilizado para sucos, smoothies e sobremesas.',10.00, 140.00, 'Un', IDCat);
(IDProd, 'mandioquinha','Tubérculo de sabor adocicado, utilizado em diversas receitas culinárias.',9.99, 12.00, 'Kg', IDCat);
(IDProd, 'milho verde','Grão de milho fresco, utilizado em saladas, sopas e pratos diversos.',8.00, 35.00, 'Un', IDCat);
(IDProd, 'mandioca','Tubérculo de sabor neutro, utilizado em diversas receitas culinárias, como farinhas e tapiocas.',10.00, 48.00, 'Un', IDCat);
(IDProd, 'pimentão verde','Vegetal de sabor suave, utilizado em saladas, refogados e pratos diversos.',16.99, 6.00, 'Kg', IDCat);
(IDProd, 'pimentão vermelho','Vegetal de sabor suave, utilizado em saladas, refogados e pratos diversos.',24.99, 3.00, 'Kg', IDCat);
(IDProd, 'pimentão amarelo','Vegetal de sabor suave, utilizado em saladas, refogados e pratos diversos.',24.99, 3.00, 'Kg', IDCat);
(IDProd, 'arroz branco','Cereal básico, utilizado como acompanhamento em diversas refeições.',26.59, 14.00, 'Un', IDCat);
(IDProd, 'coca-cola','Bebida carbonatada de sabor doce e refrescante, utilizada para consumo direto e em coquetéis.',11.99, 18.00, 'Un', IDCat);
(IDProd, 'suco de laranja','Bebida feita a partir do suco de laranjas frescas, utilizada para consumo direto e em coquetéis.',12.00, 8.00, 'Un', IDCat);
(IDProd, 'ovos','Alimento versátil, utilizado em diversas receitas culinárias, como bolos, omeletes e pratos principais.',18.00, 24.00, 'Un', IDCat);

-- Inserir dados na tabela Cliente
INSERT INTO Cliente VALUES
(IDCliente, 'Usuario', '24/11/2022',000.000.000-00),
(IDCliente, 'Samyra Mara Candido Silva', '08/10/2005', 145.236.789-01),
(IDCliente, 'Lucas Batista Perreira', '28/01/2006', 258.963.147-22),
(IDCliente, 'João Gabriel Carneiro Calbo', '09/07/2005', 369.852.147-33),
(IDCliente, 'Jean Domiguet', '26/07/2004', 456.789.123-44),
(IDCliente, 'Eliane Moreira', '15/03/2006', 568.124.963-55),
(IDCliente, 'Leonardo Verrisimo', '09/12/2005', 5654.321.987-66),
(IDCliente, 'Júlio César Chaves', '02/07/1986', 789.123.456-77),
(IDCliente, 'Mariana Kelly Lopes', '31/03/2006', 852.741.963-88),
(IDCliente, 'Geraldo Lima', '12/05/1942', 963.258.741-99),
(IDCliente, 'Benedito Sebastião Ferreira', '15/01/1951', 102.304.506-10),
(IDCliente, 'Claudio Neves', '11/11/1949', 203.405.607-21),
(IDCliente, 'Samuel Uchôa', '06/03/1955', 304.506.708-32);

INSERT INTO VENDEDOR VALUES
(IDGEN, 'Mariane Pereira', '40183561880', '2008-03-04', '17991112222', 1500),
(IDGEN, 'Maria José Batista Pereira', '57862209826', '1988-07-02', '17992223333', 1500),
(IDGEN, 'Agnaldo Pereira', '18295937812', '1987-05-09', '17993334444', 1500),
(IDGEN, 'Debora Rodrigues', '30427744814', '2000-08-29', '179944455551', 1500),
(IDGEN, 'Eduarda Costa', '35431346806', '2006-12-07', '17995556666', 1500),
(IDGEN, 'Carla Silva', '21134998973', '2004-11-09', '17996667777', 1500);

INSERT INTO CAIXA VALUES
(1, 'Normal'),
(2, 'Normal'),
(3, 'Rapido'),
(4, 'Rapido'),
(5, 'Preferencial');

INSERT INTO ENDERECOCLIENTE VALUES 
('E001', 'U000'),
('E002', 'U001'),
('E003', 'U001'),
('E004', 'U002'),
('E005', 'U002'),
('E006', 'U003'),
('E007', 'U003'),
('E008', 'U004'),
('E009', 'U004'),
('E010', 'U005'),
('E011', 'U005'),
('E012', 'U006'),
('E013', 'U006'),
('E014', 'U007'),
('E015', 'U007'),
('E016', 'U008'),
('E017', 'U008'),
('E018', 'U009'),
('E019', 'U009'),
('E020', 'U010'),
('E021', 'U010'),
('E022', 'U011'),
('E023', 'U011'),
('E024', 'U012'),
('E025', 'U012');

INSERT INTO CLIENTE_CELCLIENTE VALUES 
('(17) 99999-0000', 'U000'),
('(17) 98123-4567', 'U001'),
('(17) 3462-1111', 'U001'),
('(17) 99182-7364', 'U002'),
('(17) 99765-4321', 'U003'),
('(17) 98888-5555', 'U004'),
('(11) 97777-6666', 'U004'),
('(17) 99234-5678', 'U005'),
('(17) 99345-6789', 'U006'),
('(17) 99456-7890', 'U007'),
('(17) 3462-2222', 'U007'),
('(17) 99567-8901', 'U008'),
('(17) 3462-3333', 'U009'),
('(17) 99678-9012', 'U010'),
('(17) 3462-4444', 'U010'),
('(17) 99789-0123', 'U011'),
('(17) 99890-1234', 'U012');

INSERT INTO OPERACAOCAIXA VALUES 
('001', '2026-02-02 07:30:00', 230.00, '2026-02-02 13:20:00', 383.77, 153.77, 'V002', '001'),
('002', '2026-02-02 11:00:00', 250.00, '2026-02-02 18:00:00', 285.97, 35.97, 'V001', '003'),
('003', '2026-02-03 07:30:00', 230.00, '2026-02-03 01:20:00', 486.38, 256.38, 'V004', '001'),
('004', '2026-02-03 11:00:00', 250.00, '2026-02-03 18:00:00', 444.08, 194.08, 'V003', '003'),
('005', '2026-02-04 08:00:00', 250.00, '2026-02-04 13:00:00', 395.62, 145.62, 'V005', '002');

INSERT INTO ENDERECOFORNEC VALUES 
('E026', 'F001'),
('E027', 'F002'),
('E028', 'F001'),
('E029', 'F002'),
('E030', 'F003'),
('E031', 'F004'),
('E032', 'F005'),
('E033', 'F006'),
('E034', 'F007'),
('E035', 'F008'),
('E036', 'F009'),
('E037', 'F010'),
('E038', 'F003'),
('E039', 'F004'),
('E040', 'F005'),
('E041', 'F006'),
('E042', 'F007'),
('E043', 'F008'),
('E044', 'F009'),
('E045', 'F010');

INSERT INTO ENDERECO VALUES 
('E001', 'Tv. Pio XII', '10', 'Casa principal', '15603-504', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E002', 'Tv. Pio XII', '45', 'Apto 2', '15603-504', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E003', 'Rua São Paulo', '890', 'Fundos', '15600-020', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E004', 'Rua das Orquídeas', '112', 'Casa', '15603-510', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E005', 'Rua Paraná', '334', NULL, '15605-020', 'Jardim Paulista', 'Fernandópolis', 'SP', 'Brasil'),
('E006', 'Rua dos Ipês', '88', NULL, '15603-515', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E007', 'Av. Líbero de Almeida Silvares', '2050', 'Loja 3', '15606-000', 'Coester', 'Fernandópolis', 'SP', 'Brasil'),
('E008', 'Tv. Santa Rita', '12', 'Casa 1', '15603-520', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E009', 'Rua Rio de Janeiro', '455', NULL, '15608-050', 'Brasilândia', 'Fernandópolis', 'SP', 'Brasil'),
('E010', 'Rua Margarida', '300', 'Bloco B, Apto 101', '15603-530', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E011', 'Rua Minas Gerais', '760', 'Comercial', '15600-045', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E012', 'Tv. Pio XII', '110', 'Casa 2', '15603-504', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E013', 'Rua Espirito Santo', '99', NULL, '15608-080', 'Brasilândia', 'Fernandópolis', 'SP', 'Brasil'),
('E014', 'Rua das Camélias', '55', NULL, '15603-540', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E015', 'Rua Pernambuco', '812', NULL, '15610-010', 'Universitário', 'Fernandópolis', 'SP', 'Brasil'),
('E016', 'Tv. João de Barro', '25', 'Sobrado', '15603-550', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E017', 'Rua Bahia', '1005', 'Sala 2', '15600-060', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E018', 'Tv. Pio XII', '18', NULL, '15603-504', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E019', 'Rua Ceará', '210', 'Edícula', '15607-005', 'Santa Helena', 'Fernandópolis', 'SP', 'Brasil'),
('E020', 'Rua das Acácias', '400', NULL, '15603-560', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E021', 'Av. Afonso Pena', '670', 'Galpão', '15600-080', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E022', 'Tv. Canários', '15', 'Casa B', '15603-570', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E023', 'Rua Goiás', '320', NULL, '15612-000', 'Pôr do Sol', 'Fernandópolis', 'SP', 'Brasil'),
('E024', 'Rua das Rosas', '180', NULL, '15603-580', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil'),
('E025', 'Av. Expedicionários Brasileiros', '1500', 'Casa', '15600-001', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E026', 'Av. João Batista Vetorasso', '1600', 'Box 45 - Pavilhão Central', '15035-470', 'Distrito Industrial', 'São José do Rio Preto', 'SP', 'Brasil'),
('E027', 'Rodovia Washington Luís', '432', 'Km 432 - Galpão Logístico', '15025-999', 'Zona Rural', 'São José do Rio Preto', 'SP', 'Brasil'),
('E028', 'Av. Bady Bassitt', '3800', 'Escritório Administrativo', '15025-000', 'Boa Vista', 'São José do Rio Preto', 'SP', 'Brasil'),
('E029', 'Av. Expedicionários Brasileiros', '2150', 'Centro de Distribuição', '15600-002', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E030', 'Rua São Paulo', '1020', 'Box no Mercado Municipal', '15600-020', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E031', 'Rua Rio de Janeiro', '150', 'Unidade de Processamento', '15608-050', 'Brasilândia', 'Fernandópolis', 'SP', 'Brasil'),
('E032', 'Rua Minas Gerais', '980', 'Ponto de Entrega Urbana', '15600-045', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E033', 'Av. Líbero de Almeida Silvares', '1800', 'Loja de Produtos Orgânicos', '15606-000', 'Coester', 'Fernandópolis', 'SP', 'Brasil'),
('E034', 'Rodovia Péricles Belini', 'S/N', 'Km 122 - Armazém Regional', '15500-000', 'Zona Rural', 'Votuporanga', 'SP', 'Brasil'),
('E035', 'Rua Paraná', '455', 'Horta Comunitária', '15605-020', 'Jardim Paulista', 'Fernandópolis', 'SP', 'Brasil'),
('E036', 'Av. Francisco Jalles', '2200', 'Filial Regional', '15700-000', 'Centro', 'Jales', 'SP', 'Brasil'),
('E037', 'Av. Afonso Pena', '105', 'Escritório de Vendas', '15600-080', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E038', 'Estrada Municipal FND-150', 'S/N', 'Km 4 - Porteira Azul', '15614-899', 'Zona Rural', 'Fernandópolis', 'SP', 'Brasil'),
('E039', 'Estrada de Terra Seca', '12', 'Sítio Santo Antônio', '15615-000', 'Córrego do Jagora', 'Fernandópolis', 'SP', 'Brasil'),
('E040', 'Rodovia Euclides da Cunha', '552', 'Km 552 - Entrada de terra', '15614-000', 'Zona Rural', 'Fernandópolis', 'SP', 'Brasil'),
('E041', 'Estrada Municipal dos Coqueiros', 'S/N', 'Km 8 - Fazenda Vale Verde', '15614-500', 'Zona Rural', 'Fernandópolis', 'SP', 'Brasil'),
('E042', 'Av. dos Arnaldos', '1500', 'Armazém 2', '15607-100', 'Parque Universitário', 'Fernandópolis', 'SP', 'Brasil'),
('E043', 'Chácara das Flores', '5', 'Lote 2', '15613-200', 'Perímetro Urbano', 'Fernandópolis', 'SP', 'Brasil'),
('E044', 'Rua Amazonas', '850', 'Galpão de Distribuição', '15600-030', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E045', 'Rodovia João Carlos Alves Borges', 'S/N', 'Em frente ao Balneário', '15613-899', 'Águas Quentes', 'Fernandópolis', 'SP', 'Brasil'),
('E046', 'Rua Amazonas', '125', 'Casa', '15600-030', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E047', 'Av. dos Arnaldos', '450', 'Apto 34', '15607-100', 'Parque Universitário', 'Fernandópolis', 'SP', 'Brasil'),
('E048', 'Rua São Paulo', '815', 'Fundos', '15600-020', 'Centro', 'Fernandópolis', 'SP', 'Brasil'),
('E049', 'Rua Rio de Janeiro', '321', 'Casa 2', '15608-050', 'Brasilândia', 'Fernandópolis', 'SP', 'Brasil'),
('E050', 'Rua Paraná', '654', NULL, '15605-020', 'Jardim Paulista', 'Fernandópolis', 'SP', 'Brasil'),
('E051', 'Tv. Pio XII', '77', 'Edícula', '15603-504', 'Parque São Bernardo', 'Fernandópolis', 'SP', 'Brasil');


-- Estudar remoção, já que é 1 pra 1
INSERT INTO ENDERECOVENDEDOR VALUES 
('E046', 'V001'),
('E047', 'V002'),
('E048', 'V003'),
('E049', 'V004'),
('E050', 'V005'),
('E051', 'V006');

INSERT INTO ENTRADAESTOQUE VALUES 
('001', 'F002', '007', 12.00, 8.90, '2026-02-02'),
('002', 'F005', '039', 60.00, 1.70, '2026-02-03'),
('003', 'F001', '018', 10.00, 25.40, '2026-02-03'),
('004', 'F010', '003', 5.00, 3.00, '2026-02-05'),
('005', 'F006', '014', 3.00, 6.00, '2026-02-05');

INSERT INTO PERDAESTOQUE VALUES 
('001', '2026-02-27', 3.98, 'Apodreceu', 3.00, '006'),
('002', '2026-03-01', 2.00, 'Murchou', 6.00, '014'),
('003', '2026-03-01', 1.00, 'Caiu e explodiu', 8.90, '012'),
('004', '2026-03-07', 4.00, 'Azedou', 5.50, '108'),
('005', '2026-03-11', 12.00, 'Melância Passada', 2.94, '050');

INSERT INTO FORNECEDOR VALUES 
('F001', '43.123.456/0001-12', 'CEASA - CEAGESP - São José do Rio Preto'),
('F002', '55.987.654/0001-99', 'Coca-Cola FEMSA Brasil'),
('F003', '12.345.678/0001-00', 'Roça do Eduardinho, não ironicamente'),
('F004', '98.765.432/0001-11', 'Sítio Santo Antônio (Família Souza)'),
('F005', '11.222.333/0001-44', 'Sítio do Vovô Kaká'),
('F006', '44.555.666/0001-77', 'Fazenda Vale Verde (Produção Orgânica)'),
('F007', '77.888.999/0001-22', 'Cooperativa Agrícola Regional'),
('F008', '33.444.555/0001-88', 'Hortaliças Dona Maria'),
('F009', '66.777.888/0001-33', 'Hortifruti da Família Produções'),
('F010', '99.000.111/0001-55', 'Seu Jair das aguas termais');

INSERT INTO FORNECEDOR_CELFORN VALUES 
('(17) 3232-1000', 'F001'),
('(17) 99123-0001', 'F001'),
('(17) 3211-2000', 'F002'),
('(17) 99666-3333', 'F003'),
('(17) 99777-4444', 'F004'),
('(17) 99777-4445', 'F004'),
('(17) 99888-5555', 'F005'),
('(17) 3462-5050', 'F006'),
('(17) 99999-6666', 'F006'),
('(17) 3462-6060', 'F007'),
('(17) 99111-7777', 'F008'),
('(17) 3462-7070', 'F009'),
('(17) 99222-8888', 'F009'),
('(17) 99333-9999', 'F010');

INSERT INTO PAGAMENTO VALUES 
('001', 'Pix', 15.00, '2026-04-05', '001'),
('002', 'Cartão de Crédito', 35.97, '2026-04-09', '002'),
('003', 'Dinheiro', 5.00, '2026-04-04', '003'),
('004', 'Dinheiro', 50.00, '2026-04-07', '004'),
('005', 'Cartão de Débito', 83.77, '2026-04-07', '004'),
('006', 'Pix', 9.99, '2026-04-07', '005'),
('007', 'Cartão de Débito', 13.98, '2026-04-07', '006'),
('008', 'Cartão de Crédito', 46.34, '2026-04-07', '007'),
('009', 'Pix', 141.75, '2026-04-04', '008'),
('010', 'Dinheiro', 20.00, '2026-04-08', '009'),
('011', 'Vale Alimentação', 100.00, '2026-04-02', '010'),
('012', 'Cartão de Crédito', 66.41, '2026-04-02', '010'),
('013', 'Pix', 46.00, '2026-04-09', '011'),
('014', 'Dinheiro', 5.99, '2026-04-06', '012'),
('015', 'Cartão de Crédito', 76.57, '2026-04-11', '013'),
('016', 'Pix', 30.49, '2026-04-09', '014'),
('017', 'Cartão de Débito', 38.56, '2026-04-03', '015');

INSERT INTO ITEMPEDIDO VALUES 
('003', '001', 3.00, NULL, 5.00),
('004', '002', 3.00, NULL, 11.99),
('004', '003', 1.00, NULL, 5.00),
('005', '004', 3.00, NULL, 26.59),
('006', '004', 3.00, NULL, 18.00),
('013', '005', 1.00, NULL, 9.99),
('014', '006', 1.00, NULL, 9.99),
('018', '006', 1.00, NULL, 3.99),
('021', '007', 2.00, NULL, 3.69),
('022', '007', 3.00, NULL, 11.99),
('026', '007', 1.00, NULL, 2.99),
('036', '008', 1.00, NULL, 24.99),
('039', '008', 1.00, NULL, 36.99),
('050', '008', 3.00, NULL, 26.59),
('074', '009', 2.00, NULL, 10.00),
('086', '010', 3.00, NULL, 36.99),
('087', '010', 3.00, NULL, 11.99),
('100', '010', 3.00, NULL, 6.49),
('107', '011', 2.00, NULL, 8.00),
('108', '011', 3.00, NULL, 10.00),
('110', '012', 1.00, NULL, 5.99),
('117', '013', 2.00, NULL, 24.99),
('123', '013', 1.00, NULL, 26.59),
('124', '014', 1.00, NULL, 6.49),
('253', '014', 3.00, NULL, 8.00),
('300', '015', 2.00, NULL, 3.79),
('550', '015', 1.00, NULL, 5.99),
('900', '015', 1.00, NULL, 8.00),
('117', '015', 1.00, NULL, 16.99);


INSERT INTO PEDIDO VALUES 
('001', 15.00, '2026-04-05', 'Venda', '003', '001'),
('002', 35.97, '2026-04-09', 'Venda', '009', '002'),
('003', 5.00, '2026-04-04', 'Venda', '008', '001'),
('004', 133.77, '2026-04-07', 'Venda', '007', '001'),
('005', 9.99, '2026-04-07', 'Delivery', '004', '003'),
('006', 13.98, '2026-04-07', 'Venda', '005', '003'),
('007', 46.34, '2026-04-07', 'Venda', '008', '004'),
('008', 141.75, '2026-04-04', 'Delivery', '001', '004'),
('009', 20.00, '2026-04-08', 'Delivery', '002', '003'),
('010', 166.41, '2026-04-02', 'Venda', '008', '003'),
('011', 46.00, '2026-04-09', 'Venda', '010', '003'),
('012', 5.99, '2026-04-06', 'Delivery', '004', '004'),
('013', 76.57, '2026-04-11', 'Delivery', '006', '005'),
('014', 30.49, '2026-04-09', 'Delivery', '011', '005'),
('015', 38.56, '2026-04-03', 'Venda', '012', '005');