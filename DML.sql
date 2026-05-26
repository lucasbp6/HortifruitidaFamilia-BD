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

-- Inserir dados na tabela Fornecedor
INSERT INTO Fornecedor VALUES
(IDForn,'CEASA - CEAGESP - São José do Rio Preto','43.123.456/0001-12'),
(IDForn,'Coca-Cola FEMSA Brasil','55.987.654/0001-99'),
(IDForn, 'Roça do Eduardinho','12.345.678/0001-56'),
(IDForn, 'Sítio Santo Antônio (Família Souza)','11.222.333/0001-45'),
(IDForn, 'Sítio do Vovô Kaká','22.333.444/0001-56'),
(IDForn, 'Fazenda Vale Verde (Produção Orgânica)','33.444.555/0001-67'),
(IDForn, 'Cooperativa Agrícola Regional','44.555.666/0001-78'),
(IDForn, 'Hortaliças Dona Maria','55.666.777/0001-89'),
(IDForn, 'Hortifruti da Família Produções','66.777.888/0001-33'),
(IDForn, 'Seu Jair das aguas termais','77.888.999/0001-01');

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

