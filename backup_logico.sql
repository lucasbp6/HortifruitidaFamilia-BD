--
-- PostgreSQL database dump
--

\restrict fzQ23f2gFQiv5F3WpD8ID4euw6sqJz5KogbSSANWMn3PodT4me6VPo1qUedXGou

-- Dumped from database version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: hfamilia; Type: SCHEMA; Schema: -; Owner: lucas
--

CREATE SCHEMA hfamilia;


ALTER SCHEMA hfamilia OWNER TO lucas;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: caixa; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.caixa (
    idcaixa integer NOT NULL,
    tipocaixa character varying(20) NOT NULL
);


ALTER TABLE hfamilia.caixa OWNER TO lucas;

--
-- Name: categoria; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.categoria (
    idcat integer NOT NULL,
    nomecat character varying(20) NOT NULL,
    idcatpai integer
);


ALTER TABLE hfamilia.categoria OWNER TO lucas;

--
-- Name: cliente; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.cliente (
    idcliente integer NOT NULL,
    nomecliente character varying(50) NOT NULL,
    datanasccliente date NOT NULL,
    cpfcliente character(11) NOT NULL
);


ALTER TABLE hfamilia.cliente OWNER TO lucas;

--
-- Name: cliente_celcliente; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.cliente_celcliente (
    celcliente character varying(15) NOT NULL,
    idcliente integer NOT NULL
);


ALTER TABLE hfamilia.cliente_celcliente OWNER TO lucas;

--
-- Name: endereco; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.endereco (
    idendereco integer NOT NULL,
    ruaend character varying(35) NOT NULL,
    numeroend integer NOT NULL,
    complemend character varying(20),
    cepend character(8) NOT NULL,
    bairroend character varying(20) NOT NULL,
    cidadeend character varying(25) NOT NULL,
    estadoend character(2) NOT NULL,
    paisend character varying(20) NOT NULL
);


ALTER TABLE hfamilia.endereco OWNER TO lucas;

--
-- Name: enderecocliente; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.enderecocliente (
    idcliente integer NOT NULL,
    idendereco integer NOT NULL
);


ALTER TABLE hfamilia.enderecocliente OWNER TO lucas;

--
-- Name: enderecofornec; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.enderecofornec (
    idforn integer NOT NULL,
    idendereco integer NOT NULL
);


ALTER TABLE hfamilia.enderecofornec OWNER TO lucas;

--
-- Name: enderecovendedor; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.enderecovendedor (
    idvend integer NOT NULL,
    idendereco integer NOT NULL
);


ALTER TABLE hfamilia.enderecovendedor OWNER TO lucas;

--
-- Name: entradaestoque; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.entradaestoque (
    identrada integer NOT NULL,
    idforn integer NOT NULL,
    idprod integer NOT NULL,
    entradadata timestamp without time zone NOT NULL,
    entradaqtd numeric(10,3) NOT NULL,
    entradapreco numeric(10,2) NOT NULL,
    CONSTRAINT entradaestoque_entradapreco_check CHECK ((entradapreco >= (0)::numeric)),
    CONSTRAINT entradaestoque_entradaqtd_check CHECK ((entradaqtd > (0)::numeric))
);


ALTER TABLE hfamilia.entradaestoque OWNER TO lucas;

--
-- Name: fornecedor; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.fornecedor (
    idforn integer NOT NULL,
    nomeforn character varying(50) NOT NULL,
    cnpjforn character(14) NOT NULL
);


ALTER TABLE hfamilia.fornecedor OWNER TO lucas;

--
-- Name: fornecedor_celforn; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.fornecedor_celforn (
    celforn character varying(15) NOT NULL,
    idforn integer NOT NULL
);


ALTER TABLE hfamilia.fornecedor_celforn OWNER TO lucas;

--
-- Name: itempedido; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.itempedido (
    idprod integer NOT NULL,
    idpedido integer NOT NULL,
    qtditem numeric(10,3) NOT NULL,
    descitem numeric(10,2) DEFAULT 0,
    precoun numeric(10,2) NOT NULL,
    CONSTRAINT itempedido_descitem_check CHECK ((descitem >= (0)::numeric)),
    CONSTRAINT itempedido_precoun_check CHECK ((precoun >= (0)::numeric)),
    CONSTRAINT itempedido_qtditem_check CHECK ((qtditem > (0)::numeric))
);


ALTER TABLE hfamilia.itempedido OWNER TO lucas;

--
-- Name: operacaocaixa; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.operacaocaixa (
    idoperacao integer NOT NULL,
    dataopaber timestamp without time zone NOT NULL,
    valoropaber numeric(10,2) NOT NULL,
    dataopfecham timestamp without time zone NOT NULL,
    valoropfecham numeric(10,2) NOT NULL,
    saldoop numeric(10,2) NOT NULL,
    idvend integer NOT NULL,
    idcaixa integer NOT NULL,
    CONSTRAINT operacaocaixa_valoropaber_check CHECK ((valoropaber >= (0)::numeric)),
    CONSTRAINT operacaocaixa_valoropfecham_check CHECK ((valoropfecham >= (0)::numeric))
);


ALTER TABLE hfamilia.operacaocaixa OWNER TO lucas;

--
-- Name: pagamento; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.pagamento (
    idpag integer NOT NULL,
    metodopag character varying(20) NOT NULL,
    valorpag numeric(10,2) NOT NULL,
    datapag timestamp without time zone NOT NULL,
    idpedido integer NOT NULL,
    CONSTRAINT pagamento_valorpag_check CHECK ((valorpag >= (0)::numeric))
);


ALTER TABLE hfamilia.pagamento OWNER TO lucas;

--
-- Name: pedido; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.pedido (
    idpedido integer NOT NULL,
    valortotalpedido numeric(10,2) NOT NULL,
    datapedido timestamp without time zone NOT NULL,
    tipopedido character varying(20) NOT NULL,
    idcliente integer NOT NULL,
    idoperacao integer NOT NULL,
    CONSTRAINT pedido_valortotalpedido_check CHECK ((valortotalpedido >= (0)::numeric))
);


ALTER TABLE hfamilia.pedido OWNER TO lucas;

--
-- Name: perdaestoque; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.perdaestoque (
    idperda integer NOT NULL,
    dataperda timestamp without time zone NOT NULL,
    qtdperda numeric(10,3) NOT NULL,
    motivoperda character varying(100) NOT NULL,
    valorunperda numeric(10,2) NOT NULL,
    idprod integer NOT NULL,
    CONSTRAINT perdaestoque_qtdperda_check CHECK ((qtdperda > (0)::numeric)),
    CONSTRAINT perdaestoque_valorunperda_check CHECK ((valorunperda >= (0)::numeric))
);


ALTER TABLE hfamilia.perdaestoque OWNER TO lucas;

--
-- Name: produto; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.produto (
    idprod integer NOT NULL,
    nomeprod character varying(20) NOT NULL,
    descricaoprod character varying(100),
    precovendaprod numeric(10,2) NOT NULL,
    estoqueatualprod numeric(10,3) NOT NULL,
    precocustoprod numeric(10,2) NOT NULL,
    idunidade integer NOT NULL,
    idcat integer NOT NULL,
    CONSTRAINT produto_estoqueatualprod_check CHECK ((estoqueatualprod >= (0)::numeric)),
    CONSTRAINT produto_precocustoprod_check CHECK ((precocustoprod >= (0)::numeric)),
    CONSTRAINT produto_precovendaprod_check CHECK ((precovendaprod >= (0)::numeric))
);


ALTER TABLE hfamilia.produto OWNER TO lucas;

--
-- Name: unidademedida; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.unidademedida (
    idunidade integer NOT NULL,
    nomeunidade character varying(20) NOT NULL,
    siglaunidade character varying(5) NOT NULL
);


ALTER TABLE hfamilia.unidademedida OWNER TO lucas;

--
-- Name: vendedor; Type: TABLE; Schema: hfamilia; Owner: lucas
--

CREATE TABLE hfamilia.vendedor (
    idvend integer NOT NULL,
    nomevend character varying(50) NOT NULL,
    cpfvend character(11) NOT NULL,
    datanascvend date NOT NULL,
    celvend character varying(15) NOT NULL,
    salariovend numeric(10,2) NOT NULL,
    CONSTRAINT vendedor_salariovend_check CHECK ((salariovend >= (0)::numeric))
);


ALTER TABLE hfamilia.vendedor OWNER TO lucas;

--
-- Data for Name: caixa; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.caixa (idcaixa, tipocaixa) FROM stdin;
1	Normal
2	Normal
3	Rapido
4	Rapido
5	Preferencial
\.


--
-- Data for Name: categoria; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.categoria (idcat, nomecat, idcatpai) FROM stdin;
1	Hortifruti	\N
2	Mercearia	\N
3	Legumes	1
4	Frutas	1
5	Bebidas	2
6	Verduras	1
7	Limpeza	2
8	Temperos	2
9	Alimentacao	2
\.


--
-- Data for Name: cliente; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.cliente (idcliente, nomecliente, datanasccliente, cpfcliente) FROM stdin;
1	Usuario Nao identificado	2022-11-24	00000000000
2	Samyra Mara Candido Silva	2005-10-08	14523678901
3	Lucas Batista Pereira	2006-01-28	25896314722
4	Joao Gabriel Carneiro Calbo	2005-07-09	36985214733
5	Jean Domiguet	2004-07-26	45678912344
6	Eliane Moreira	2006-03-15	56812496355
7	Leonardo Verissimo	2005-12-09	65432198766
8	Julio Cesar Chaves	1986-07-02	78912345677
9	Mariana Kelly Lopes	2006-03-31	85274196388
10	Geraldo Lima	1942-05-12	96325874199
11	Benedito Sebastiao Ferreira	1951-01-15	10230450610
12	Claudio Neves	1949-11-11	20340560721
13	Samuel Uchoa	1955-03-06	30450670832
\.


--
-- Data for Name: cliente_celcliente; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.cliente_celcliente (celcliente, idcliente) FROM stdin;
(17) 99999-0000	1
(17) 98123-4567	2
(17) 3462-1111	2
(17) 99182-7364	3
(17) 99765-4321	4
(17) 98888-5555	5
(11) 97777-6666	5
(17) 99234-5678	6
(17) 99345-6789	7
(17) 99456-7890	8
(17) 3462-2222	8
(17) 99567-8901	9
(17) 3462-3333	10
(17) 99678-9012	11
(17) 3462-4444	11
(17) 99789-0123	12
(17) 99890-1234	13
\.


--
-- Data for Name: endereco; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.endereco (idendereco, ruaend, numeroend, complemend, cepend, bairroend, cidadeend, estadoend, paisend) FROM stdin;
1	Tv. Pio XII	10	Casa principal	15603504	Parque Sao Bernardo	Fernandopolis	SP	Brasil
2	Tv. Pio XII	45	Apto 2	15603504	Parque Sao Bernardo	Fernandopolis	SP	Brasil
3	Rua Sao Paulo	890	Fundos	15600020	Centro	Fernandopolis	SP	Brasil
4	Rua das Orquideas	112	Casa	15603510	Parque Sao Bernardo	Fernandopolis	SP	Brasil
5	Rua Parana	334	\N	15605020	Jardim Paulista	Fernandopolis	SP	Brasil
6	Rua dos Ipes	88	\N	15603515	Parque Sao Bernardo	Fernandopolis	SP	Brasil
7	Av. Libero de Almeida Silvares	2050	Loja 3	15606000	Coester	Fernandopolis	SP	Brasil
8	Tv. Santa Rita	12	Casa 1	15603520	Parque Sao Bernardo	Fernandopolis	SP	Brasil
9	Rua Rio de Janeiro	455	\N	15608050	Brasilandia	Fernandopolis	SP	Brasil
10	Rua Margarida	300	Bloco B Apto 101	15603530	Parque Sao Bernardo	Fernandopolis	SP	Brasil
11	Rua Minas Gerais	760	Comercial	15600045	Centro	Fernandopolis	SP	Brasil
12	Tv. Pio XII	110	Casa 2	15603504	Parque Sao Bernardo	Fernandopolis	SP	Brasil
13	Rua Espirito Santo	99	\N	15608080	Brasilandia	Fernandopolis	SP	Brasil
14	Rua das Camelias	55	\N	15603540	Parque Sao Bernardo	Fernandopolis	SP	Brasil
15	Rua Pernambuco	812	\N	15610010	Universitario	Fernandopolis	SP	Brasil
16	Tv. Joao de Barro	25	Sobrado	15603550	Parque Sao Bernardo	Fernandopolis	SP	Brasil
17	Rua Bahia	1005	Sala 2	15600060	Centro	Fernandopolis	SP	Brasil
18	Tv. Pio XII	18	\N	15603504	Parque Sao Bernardo	Fernandopolis	SP	Brasil
19	Rua Ceara	210	Edicula	15607005	Santa Helena	Fernandopolis	SP	Brasil
20	Rua das Acacias	400	\N	15603560	Parque Sao Bernardo	Fernandopolis	SP	Brasil
21	Av. Afonso Pena	670	Galpao	15600080	Centro	Fernandopolis	SP	Brasil
22	Tv. Canarios	15	Casa B	15603570	Parque Sao Bernardo	Fernandopolis	SP	Brasil
23	Rua Goias	320	\N	15612000	Por do Sol	Fernandopolis	SP	Brasil
24	Rua das Rosas	180	\N	15603580	Parque Sao Bernardo	Fernandopolis	SP	Brasil
25	Av. Expedicionarios Brasileiros	1500	Casa	15600001	Centro	Fernandopolis	SP	Brasil
26	Av. Joao Batista Vetorasso	1600	Box 45 Central	15035470	Distrito Industrial	Sao Jose do Rio Preto	SP	Brasil
27	Rodovia Washington Luis	432	Km 432 Galpao	15025999	Zona Rural	Sao Jose do Rio Preto	SP	Brasil
28	Av. Bady Bassitt	3800	Escritorio	15025000	Boa Vista	Sao Jose do Rio Preto	SP	Brasil
29	Av. Expedicionarios Brasileiros	2150	Distribuicao	15600002	Centro	Fernandopolis	SP	Brasil
30	Rua Sao Paulo	1020	Box Mercado	15600020	Centro	Fernandopolis	SP	Brasil
31	Rua Rio de Janeiro	150	Processamento	15608050	Brasilandia	Fernandopolis	SP	Brasil
32	Rua Minas Gerais	980	Entrega urbana	15600045	Centro	Fernandopolis	SP	Brasil
33	Av. Libero de Almeida Silvares	1800	Organicos	15606000	Coester	Fernandopolis	SP	Brasil
34	Rodovia Pericles Belini	0	Km 122 Armazem	15500000	Zona Rural	Votuporanga	SP	Brasil
35	Rua Parana	455	Horta comunitaria	15605020	Jardim Paulista	Fernandopolis	SP	Brasil
36	Av. Francisco Jalles	2200	Filial regional	15700000	Centro	Jales	SP	Brasil
37	Av. Afonso Pena	105	Escritorio vendas	15600080	Centro	Fernandopolis	SP	Brasil
38	Estrada Municipal FND-150	0	Km 4 Porteira Azul	15614899	Zona Rural	Fernandopolis	SP	Brasil
39	Estrada de Terra Seca	12	Sitio Santo Antonio	15615000	Corrego do Jagora	Fernandopolis	SP	Brasil
40	Rodovia Euclides da Cunha	552	Entrada de terra	15614000	Zona Rural	Fernandopolis	SP	Brasil
41	Estrada Municipal dos Coqueiros	0	Fazenda Vale Verde	15614500	Zona Rural	Fernandopolis	SP	Brasil
42	Av. dos Arnaldos	1500	Armazem 2	15607100	Parque Universitario	Fernandopolis	SP	Brasil
43	Chacara das Flores	5	Lote 2	15613200	Perimetro Urbano	Fernandopolis	SP	Brasil
44	Rua Amazonas	850	Galpao	15600030	Centro	Fernandopolis	SP	Brasil
45	Rodovia Joao Carlos Alves Borges	0	Balneario	15613899	Aguas Quentes	Fernandopolis	SP	Brasil
46	Rua Amazonas	125	Casa	15600030	Centro	Fernandopolis	SP	Brasil
47	Av. dos Arnaldos	450	Apto 34	15607100	Parque Universitario	Fernandopolis	SP	Brasil
48	Rua Sao Paulo	815	Fundos	15600020	Centro	Fernandopolis	SP	Brasil
49	Rua Rio de Janeiro	321	Casa 2	15608050	Brasilandia	Fernandopolis	SP	Brasil
50	Rua Parana	654	\N	15605020	Jardim Paulista	Fernandopolis	SP	Brasil
51	Tv. Pio XII	77	Edicula	15603504	Parque Sao Bernardo	Fernandopolis	SP	Brasil
\.


--
-- Data for Name: enderecocliente; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.enderecocliente (idcliente, idendereco) FROM stdin;
1	1
2	2
2	3
3	4
3	5
4	6
4	7
5	8
5	9
6	10
6	11
7	12
7	13
8	14
8	15
9	16
9	17
10	18
10	19
11	20
11	21
12	22
12	23
13	24
13	25
\.


--
-- Data for Name: enderecofornec; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.enderecofornec (idforn, idendereco) FROM stdin;
1	26
2	27
1	28
2	29
3	30
4	31
5	32
6	33
7	34
8	35
9	36
10	37
3	38
4	39
5	40
6	41
7	42
8	43
9	44
10	45
\.


--
-- Data for Name: enderecovendedor; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.enderecovendedor (idvend, idendereco) FROM stdin;
1	46
2	47
3	48
4	49
5	50
6	51
\.


--
-- Data for Name: entradaestoque; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.entradaestoque (identrada, idforn, idprod, entradadata, entradaqtd, entradapreco) FROM stdin;
1	2	26	2026-02-02 08:00:00	12.000	8.90
2	5	14	2026-02-03 08:00:00	60.000	1.70
3	1	18	2026-02-03 08:00:00	10.000	25.40
4	10	3	2026-02-05 08:00:00	5.000	3.00
5	6	13	2026-02-05 08:00:00	3.000	6.00
\.


--
-- Data for Name: fornecedor; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.fornecedor (idforn, nomeforn, cnpjforn) FROM stdin;
1	CEASA - CEAGESP Sao Jose Rio Preto	43123456000112
2	Coca-Cola FEMSA Brasil	55987654000199
3	Roca do Eduardinho	12345678000100
4	Sitio Santo Antonio	98765432000111
5	Sitio do Vovo Kaka	11222333000144
6	Fazenda Vale Verde	44555666000177
7	Cooperativa Agricola Regional	77888999000122
8	Hortalicas Dona Maria	33444555000188
9	Hortifruti da Familia Producoes	66777888000133
10	Seu Jair das Aguas Termais	99000111000155
\.


--
-- Data for Name: fornecedor_celforn; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.fornecedor_celforn (celforn, idforn) FROM stdin;
(17) 3232-1000	1
(17) 99123-0001	1
(17) 3211-2000	2
(17) 99666-3333	3
(17) 99777-4444	4
(17) 99777-4445	4
(17) 99888-5555	5
(17) 3462-5050	6
(17) 99999-6666	6
(17) 3462-6060	7
(17) 99111-7777	8
(17) 3462-7070	9
(17) 99222-8888	9
(17) 99333-9999	10
\.


--
-- Data for Name: itempedido; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.itempedido (idprod, idpedido, qtditem, descitem, precoun) FROM stdin;
1	1	3.000	0.00	5.00
2	2	3.000	0.00	11.99
1	3	1.000	0.00	5.00
25	4	3.000	0.00	26.59
28	4	3.000	0.00	18.00
17	5	1.000	0.00	9.99
19	6	1.000	0.00	9.99
13	6	1.000	0.00	3.99
9	7	2.000	0.00	3.69
26	7	3.000	0.00	11.99
16	7	1.000	0.00	2.99
23	8	1.000	0.00	24.99
8	8	1.000	0.00	36.99
25	8	3.000	0.00	26.59
18	9	2.000	0.00	10.00
8	10	3.000	0.00	36.99
2	10	3.000	0.00	11.99
11	10	3.000	0.00	6.49
6	11	2.000	0.00	8.00
21	11	3.000	0.00	10.00
4	12	1.000	0.00	5.99
23	13	2.000	0.00	24.99
25	13	1.000	0.00	26.59
11	14	1.000	0.00	6.49
20	14	3.000	0.00	8.00
14	15	2.000	0.00	3.79
10	15	1.000	0.00	5.99
6	15	1.000	0.00	8.00
22	15	1.000	0.00	16.99
\.


--
-- Data for Name: operacaocaixa; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.operacaocaixa (idoperacao, dataopaber, valoropaber, dataopfecham, valoropfecham, saldoop, idvend, idcaixa) FROM stdin;
1	2026-02-02 07:30:00	230.00	2026-02-02 13:20:00	383.77	153.77	2	1
2	2026-02-02 11:00:00	250.00	2026-02-02 18:00:00	285.97	35.97	1	3
3	2026-02-03 07:30:00	230.00	2026-02-03 13:20:00	486.38	256.38	4	1
4	2026-02-03 11:00:00	250.00	2026-02-03 18:00:00	444.08	194.08	3	3
5	2026-02-04 08:00:00	250.00	2026-02-04 13:00:00	395.62	145.62	5	2
\.


--
-- Data for Name: pagamento; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.pagamento (idpag, metodopag, valorpag, datapag, idpedido) FROM stdin;
1	Pix	15.00	2026-04-05 09:15:00	1
2	Cartao de Credito	35.97	2026-04-09 10:20:00	2
3	Dinheiro	5.00	2026-04-04 11:25:00	3
4	Dinheiro	50.00	2026-04-07 12:30:00	4
5	Cartao de Debito	83.77	2026-04-07 12:31:00	4
6	Pix	9.99	2026-04-07 13:35:00	5
7	Cartao de Debito	13.98	2026-04-07 14:40:00	6
8	Cartao de Credito	46.34	2026-04-07 15:45:00	7
9	Pix	141.75	2026-04-04 16:50:00	8
10	Dinheiro	20.00	2026-04-08 17:55:00	9
11	Vale Alimentacao	100.00	2026-04-02 09:05:00	10
12	Cartao de Credito	66.41	2026-04-02 09:06:00	10
13	Pix	46.00	2026-04-09 10:05:00	11
14	Dinheiro	5.99	2026-04-06 11:05:00	12
15	Cartao de Credito	76.57	2026-04-11 12:05:00	13
16	Pix	30.49	2026-04-09 13:05:00	14
17	Cartao de Debito	38.56	2026-04-03 14:05:00	15
\.


--
-- Data for Name: pedido; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.pedido (idpedido, valortotalpedido, datapedido, tipopedido, idcliente, idoperacao) FROM stdin;
1	15.00	2026-04-05 09:10:00	Venda	3	1
2	35.97	2026-04-09 10:15:00	Venda	9	2
3	5.00	2026-04-04 11:20:00	Venda	8	1
4	133.77	2026-04-07 12:25:00	Venda	7	1
5	9.99	2026-04-07 13:30:00	Delivery	4	3
6	13.98	2026-04-07 14:35:00	Venda	5	3
7	46.34	2026-04-07 15:40:00	Venda	8	4
8	141.75	2026-04-04 16:45:00	Delivery	1	4
9	20.00	2026-04-08 17:50:00	Delivery	2	3
10	166.41	2026-04-02 09:00:00	Venda	8	3
11	46.00	2026-04-09 10:00:00	Venda	10	3
12	5.99	2026-04-06 11:00:00	Delivery	4	4
13	76.57	2026-04-11 12:00:00	Delivery	6	5
14	30.49	2026-04-09 13:00:00	Delivery	11	5
15	38.56	2026-04-03 14:00:00	Venda	12	5
\.


--
-- Data for Name: perdaestoque; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.perdaestoque (idperda, dataperda, qtdperda, motivoperda, valorunperda, idprod) FROM stdin;
1	2026-02-27 10:00:00	3.980	Apodreceu	3.00	6
2	2026-03-01 10:00:00	2.000	Murchou	6.00	13
3	2026-03-01 10:00:00	1.000	Caiu e quebrou	8.90	12
4	2026-03-07 10:00:00	4.000	Azedou	5.50	18
5	2026-03-11 10:00:00	12.000	Melancia passada	2.94	14
\.


--
-- Data for Name: produto; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.produto (idprod, nomeprod, descricaoprod, precovendaprod, estoqueatualprod, precocustoprod, idunidade, idcat) FROM stdin;
1	Cebolinha	Erva aromatica de sabor suave, usada para finalizar pratos.	5.00	8.000	2.50	3	8
2	Tomate	Produto fresco para saladas, molhos e preparos diversos.	11.99	80.000	7.00	1	3
3	Acucar	Produto usado para adocar alimentos e bebidas.	5.49	15.000	3.20	2	9
4	Batata	Tuberculo versatil para diversas receitas.	5.99	60.000	3.50	1	3
5	Cebola	Vegetal usado como base de temperos e preparos.	4.99	60.000	2.80	1	3
6	Couve manteiga	Folha verde escura para saladas e refogados.	8.00	7.000	4.00	3	6
7	Rucula	Folha de sabor picante usada em saladas.	8.00	7.000	4.00	3	6
8	Alho	Bulbo aromatico usado para temperar pratos.	36.99	25.000	22.00	1	8
9	Leite	Bebida nutritiva para consumo e receitas.	3.69	36.000	2.30	2	5
10	Beterraba	Raiz vermelha usada em saladas e sucos.	5.99	20.000	3.00	1	3
11	Cenoura	Raiz laranja usada em saladas, sopas e sucos.	6.49	15.000	3.50	1	3
12	Inhame	Tuberculo de sabor suave para receitas diversas.	14.49	10.000	8.00	1	3
13	Laranja pera	Fruta citrica para consumo direto e sucos.	3.99	120.000	2.00	1	4
14	Melancia	Fruta grande e refrescante de polpa vermelha.	3.79	300.000	1.90	1	4
15	Feijao carioquinha	Leguminosa usada em pratos tradicionais.	5.99	15.000	3.50	2	9
16	Sal	Condimento essencial para realcar sabores.	2.99	20.000	1.20	2	8
17	Oleo de soja	Oleo vegetal usado para cozinhar e fritar.	9.99	36.000	6.50	2	9
18	Polpa de frutas	Produto processado para sucos e sobremesas.	10.00	140.000	5.50	2	5
19	Mandioquinha	Tuberculo de sabor adocicado para receitas.	9.99	12.000	5.50	1	3
20	Milho verde	Grao fresco para saladas, sopas e pratos diversos.	8.00	35.000	4.30	2	3
21	Mandioca	Tuberculo usado em receitas, farinhas e tapiocas.	10.00	48.000	5.00	1	3
22	Pimentao verde	Vegetal usado em saladas, refogados e preparos.	16.99	6.000	9.00	1	3
23	Pimentao vermelho	Vegetal colorido para saladas e refogados.	24.99	3.000	14.00	1	3
24	Pimentao amarelo	Vegetal colorido para saladas e refogados.	24.99	3.000	14.00	1	3
25	Arroz branco	Cereal basico para acompanhar refeicoes.	26.59	14.000	18.00	2	9
26	Coca-cola	Bebida carbonatada para consumo direto.	11.99	18.000	7.00	2	5
27	Suco de laranja	Bebida de laranja pronta para consumo.	12.00	8.000	6.00	2	5
28	Ovos	Alimento versatil para receitas e pratos principais.	18.00	24.000	11.00	5	9
\.


--
-- Data for Name: unidademedida; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.unidademedida (idunidade, nomeunidade, siglaunidade) FROM stdin;
1	Quilograma	kg
2	Unidade	un
3	Maco	mc
4	Bandeja	bdj
5	Duzia	dz
\.


--
-- Data for Name: vendedor; Type: TABLE DATA; Schema: hfamilia; Owner: lucas
--

COPY hfamilia.vendedor (idvend, nomevend, cpfvend, datanascvend, celvend, salariovend) FROM stdin;
1	Mariane Pereira	40183561880	2008-03-04	17991112222	1500.00
2	Maria Jose Batista Pereira	57862209826	1988-07-02	17992223333	1500.00
3	Agnaldo Pereira	18295937812	1987-05-09	17993334444	1500.00
4	Debora Rodrigues	30427744814	2000-08-29	17994445551	1500.00
5	Eduarda Costa	35431346806	2006-12-07	17995556666	1500.00
6	Carla Silva	21134998973	2004-11-09	17996667777	1500.00
\.


--
-- Name: caixa caixa_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.caixa
    ADD CONSTRAINT caixa_pkey PRIMARY KEY (idcaixa);


--
-- Name: categoria categoria_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.categoria
    ADD CONSTRAINT categoria_pkey PRIMARY KEY (idcat);


--
-- Name: cliente_celcliente cliente_celcliente_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.cliente_celcliente
    ADD CONSTRAINT cliente_celcliente_pkey PRIMARY KEY (celcliente, idcliente);


--
-- Name: cliente cliente_cpfcliente_key; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.cliente
    ADD CONSTRAINT cliente_cpfcliente_key UNIQUE (cpfcliente);


--
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (idcliente);


--
-- Name: endereco endereco_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.endereco
    ADD CONSTRAINT endereco_pkey PRIMARY KEY (idendereco);


--
-- Name: enderecocliente enderecocliente_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.enderecocliente
    ADD CONSTRAINT enderecocliente_pkey PRIMARY KEY (idcliente, idendereco);


--
-- Name: enderecofornec enderecofornec_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.enderecofornec
    ADD CONSTRAINT enderecofornec_pkey PRIMARY KEY (idforn, idendereco);


--
-- Name: enderecovendedor enderecovendedor_idvend_key; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.enderecovendedor
    ADD CONSTRAINT enderecovendedor_idvend_key UNIQUE (idvend);


--
-- Name: enderecovendedor enderecovendedor_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.enderecovendedor
    ADD CONSTRAINT enderecovendedor_pkey PRIMARY KEY (idvend, idendereco);


--
-- Name: entradaestoque entradaestoque_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.entradaestoque
    ADD CONSTRAINT entradaestoque_pkey PRIMARY KEY (identrada);


--
-- Name: fornecedor_celforn fornecedor_celforn_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.fornecedor_celforn
    ADD CONSTRAINT fornecedor_celforn_pkey PRIMARY KEY (celforn, idforn);


--
-- Name: fornecedor fornecedor_cnpjforn_key; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.fornecedor
    ADD CONSTRAINT fornecedor_cnpjforn_key UNIQUE (cnpjforn);


--
-- Name: fornecedor fornecedor_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.fornecedor
    ADD CONSTRAINT fornecedor_pkey PRIMARY KEY (idforn);


--
-- Name: itempedido itempedido_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.itempedido
    ADD CONSTRAINT itempedido_pkey PRIMARY KEY (idprod, idpedido);


--
-- Name: operacaocaixa operacaocaixa_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.operacaocaixa
    ADD CONSTRAINT operacaocaixa_pkey PRIMARY KEY (idoperacao);


--
-- Name: pagamento pagamento_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.pagamento
    ADD CONSTRAINT pagamento_pkey PRIMARY KEY (idpag);


--
-- Name: pedido pedido_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.pedido
    ADD CONSTRAINT pedido_pkey PRIMARY KEY (idpedido);


--
-- Name: perdaestoque perdaestoque_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.perdaestoque
    ADD CONSTRAINT perdaestoque_pkey PRIMARY KEY (idperda);


--
-- Name: produto produto_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.produto
    ADD CONSTRAINT produto_pkey PRIMARY KEY (idprod);


--
-- Name: unidademedida unidademedida_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.unidademedida
    ADD CONSTRAINT unidademedida_pkey PRIMARY KEY (idunidade);


--
-- Name: vendedor vendedor_cpfvend_key; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.vendedor
    ADD CONSTRAINT vendedor_cpfvend_key UNIQUE (cpfvend);


--
-- Name: vendedor vendedor_pkey; Type: CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.vendedor
    ADD CONSTRAINT vendedor_pkey PRIMARY KEY (idvend);


--
-- Name: categoria categoria_idcatpai_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.categoria
    ADD CONSTRAINT categoria_idcatpai_fkey FOREIGN KEY (idcatpai) REFERENCES hfamilia.categoria(idcat);


--
-- Name: cliente_celcliente cliente_celcliente_idcliente_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.cliente_celcliente
    ADD CONSTRAINT cliente_celcliente_idcliente_fkey FOREIGN KEY (idcliente) REFERENCES hfamilia.cliente(idcliente);


--
-- Name: enderecocliente enderecocliente_idcliente_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.enderecocliente
    ADD CONSTRAINT enderecocliente_idcliente_fkey FOREIGN KEY (idcliente) REFERENCES hfamilia.cliente(idcliente);


--
-- Name: enderecocliente enderecocliente_idendereco_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.enderecocliente
    ADD CONSTRAINT enderecocliente_idendereco_fkey FOREIGN KEY (idendereco) REFERENCES hfamilia.endereco(idendereco);


--
-- Name: enderecofornec enderecofornec_idendereco_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.enderecofornec
    ADD CONSTRAINT enderecofornec_idendereco_fkey FOREIGN KEY (idendereco) REFERENCES hfamilia.endereco(idendereco);


--
-- Name: enderecofornec enderecofornec_idforn_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.enderecofornec
    ADD CONSTRAINT enderecofornec_idforn_fkey FOREIGN KEY (idforn) REFERENCES hfamilia.fornecedor(idforn);


--
-- Name: enderecovendedor enderecovendedor_idendereco_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.enderecovendedor
    ADD CONSTRAINT enderecovendedor_idendereco_fkey FOREIGN KEY (idendereco) REFERENCES hfamilia.endereco(idendereco);


--
-- Name: enderecovendedor enderecovendedor_idvend_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.enderecovendedor
    ADD CONSTRAINT enderecovendedor_idvend_fkey FOREIGN KEY (idvend) REFERENCES hfamilia.vendedor(idvend);


--
-- Name: entradaestoque entradaestoque_idforn_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.entradaestoque
    ADD CONSTRAINT entradaestoque_idforn_fkey FOREIGN KEY (idforn) REFERENCES hfamilia.fornecedor(idforn);


--
-- Name: entradaestoque entradaestoque_idprod_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.entradaestoque
    ADD CONSTRAINT entradaestoque_idprod_fkey FOREIGN KEY (idprod) REFERENCES hfamilia.produto(idprod);


--
-- Name: fornecedor_celforn fornecedor_celforn_idforn_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.fornecedor_celforn
    ADD CONSTRAINT fornecedor_celforn_idforn_fkey FOREIGN KEY (idforn) REFERENCES hfamilia.fornecedor(idforn);


--
-- Name: itempedido itempedido_idpedido_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.itempedido
    ADD CONSTRAINT itempedido_idpedido_fkey FOREIGN KEY (idpedido) REFERENCES hfamilia.pedido(idpedido);


--
-- Name: itempedido itempedido_idprod_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.itempedido
    ADD CONSTRAINT itempedido_idprod_fkey FOREIGN KEY (idprod) REFERENCES hfamilia.produto(idprod);


--
-- Name: operacaocaixa operacaocaixa_idcaixa_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.operacaocaixa
    ADD CONSTRAINT operacaocaixa_idcaixa_fkey FOREIGN KEY (idcaixa) REFERENCES hfamilia.caixa(idcaixa);


--
-- Name: operacaocaixa operacaocaixa_idvend_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.operacaocaixa
    ADD CONSTRAINT operacaocaixa_idvend_fkey FOREIGN KEY (idvend) REFERENCES hfamilia.vendedor(idvend);


--
-- Name: pagamento pagamento_idpedido_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.pagamento
    ADD CONSTRAINT pagamento_idpedido_fkey FOREIGN KEY (idpedido) REFERENCES hfamilia.pedido(idpedido);


--
-- Name: pedido pedido_idcliente_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.pedido
    ADD CONSTRAINT pedido_idcliente_fkey FOREIGN KEY (idcliente) REFERENCES hfamilia.cliente(idcliente);


--
-- Name: pedido pedido_idoperacao_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.pedido
    ADD CONSTRAINT pedido_idoperacao_fkey FOREIGN KEY (idoperacao) REFERENCES hfamilia.operacaocaixa(idoperacao);


--
-- Name: perdaestoque perdaestoque_idprod_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.perdaestoque
    ADD CONSTRAINT perdaestoque_idprod_fkey FOREIGN KEY (idprod) REFERENCES hfamilia.produto(idprod);


--
-- Name: produto produto_idcat_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.produto
    ADD CONSTRAINT produto_idcat_fkey FOREIGN KEY (idcat) REFERENCES hfamilia.categoria(idcat);


--
-- Name: produto produto_idunidade_fkey; Type: FK CONSTRAINT; Schema: hfamilia; Owner: lucas
--

ALTER TABLE ONLY hfamilia.produto
    ADD CONSTRAINT produto_idunidade_fkey FOREIGN KEY (idunidade) REFERENCES hfamilia.unidademedida(idunidade);


--
-- PostgreSQL database dump complete
--

\unrestrict fzQ23f2gFQiv5F3WpD8ID4euw6sqJz5KogbSSANWMn3PodT4me6VPo1qUedXGou

