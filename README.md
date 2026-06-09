# HortifruitidaFamilia-BD

Projeto desenvolvido para a disciplina de **Banco de Dados**.

## Integrantes

- João Gabriel Carneiro Calbo
- Lucas Batista Pereira
- Samyra Mara Candido Silva

## Sobre o projeto

Este repositório implementa o banco de dados e uma aplicação CRUD para o sistema **Hortifruti da Família**.

O sistema tem como objetivo representar e gerenciar o fluxo operacional de um hortifruti, contemplando:

- cadastro de produtos, categorias e unidades de medida;
- cadastro de clientes, fornecedores, vendedores, endereços e telefones;
- entrada de estoque;
- registro de perdas de estoque;
- abertura e fechamento de operações de caixa;
- realização de vendas;
- registro de pedidos, itens de pedido e pagamentos.

O projeto foi desenvolvido com foco na modelagem relacional, criação do banco em PostgreSQL e construção de uma interface em terminal para manipulação dos dados.

![Modelo Lógico Hortifruti da Família](modelo_logico.png)

## Estrutura do projeto

A organização principal do repositório é:

```text
HortifruitidaFamilia-BD/
│
├── README.md
├── modelo_logico.png
│
├── index/
│   └── index.md
│
├── sql/
│   ├── DDL.sql
│   ├── DML.sql
│   │
│   └── seeds/
│       ├── 01_categorias.sql
│       ├── 02_unidades.sql
│       ├── 03_produtos.sql
│       ├── 04_fornecedores.sql
│       ├── 05_clientes.sql
│       ├── 06_vendedores.sql
│       ├── 07_caixas.sql
│       ├── 08_estoque.sql
│       └── ...
│
└── crud/
    │
    ├── app.py
    ├── terminal.py
    ├── conexao.py
    ├── entities.py
    ├── operacoes.py
    ├── operacoes_crud.py
    ├── operacoes_estoque.py
    ├── operacoes_venda.py
    ├── operacoes_consultas.py
    ├── operacoes_pessoa.py
    ├── requirements.txt
    ├── estilo.tcss
    │
    ├── screens/
    │   ├── __init__.py
    │   ├── initial_screen.py
    │   ├── view_screen.py
    │   └── operation_screen.py
    │
    └── modals/
        ├── __init__.py
        ├── view_modal.py
        ├── delete_modal.py
        ├── update_select_modal.py
        ├── formulario_modal.py
        └── formulario_pessoa_composto.py
```

## Organização das pastas

### Raiz do projeto

A raiz contém os arquivos gerais de documentação e representação do projeto:

- `README.md`: documentação principal do projeto;
- `modelo_logico.png`: imagem do modelo lógico do banco de dados;
- `index/`: documentação relacionada aos índices de otimização;
- `sql/`: scripts de criação e povoamento do banco;
- `crud/`: aplicação em Python para interação com o banco.

### Pasta `index/`

A pasta `index/` contém a documentação relacionada aos índices de otimização do banco de dados.

O arquivo `index.md` apresenta uma proposta de índices para melhorar o desempenho de consultas frequentes do sistema, especialmente buscas por produtos, vendas, pedidos, pagamentos, movimentações de estoque e operações de caixa.

### Pasta `sql/`

A pasta `sql/` concentra os scripts relacionados ao banco de dados.

```text
sql/
├── DDL.sql
├── DML.sql
└── seeds/
```

O arquivo `DDL.sql` contém os comandos de criação da estrutura do banco, incluindo tabelas, chaves primárias, chaves estrangeiras, restrições de integridade e tipos de dados.

O arquivo `DML.sql` contém uma carga completa de dados iniciais para o banco.

A pasta `sql/seeds/` contém arquivos menores de inserção, separados por entidade ou etapa lógica do povoamento. Essa separação facilita os testes, a execução gradual dos inserts e a identificação de erros durante o carregamento dos dados.

### Pasta `crud/`

A pasta `crud/` contém a aplicação em Python responsável pela manipulação dos dados do banco.

```text
crud/
├── app.py
├── terminal.py
├── conexao.py
├── entities.py
├── operacoes.py
├── operacoes_crud.py
├── operacoes_estoque.py
├── operacoes_venda.py
├── operacoes_consultas.py
├── operacoes_pessoa.py
├── requirements.txt
├── estilo.tcss
├── screens/
└── modals/
```

Os principais arquivos são:

- `terminal.py`: ponto de entrada da aplicação em terminal;
- `app.py`: definição da aplicação Textual, modos principais, atalhos e tela inicial;
- `conexao.py`: responsável pela conexão com o banco PostgreSQL, usando variáveis de ambiente ou arquivo `.env`;
- `entities.py`: mapeamento das tabelas, colunas, tipos esperados e funções auxiliares;
- `operacoes.py`: módulo agregador que reexporta as operações dos módulos especializados;
- `operacoes_crud.py`: operações genéricas de banco, como inserção, seleção, atualização e deleção;
- `operacoes_estoque.py`: regras de entrada, perda e baixa de estoque;
- `operacoes_venda.py`: regras de abertura de caixa e finalização transacional de vendas;
- `operacoes_consultas.py`: consultas especiais para endereços e telefones;
- `operacoes_pessoa.py`: regras de deleção segura de pessoas;
- `requirements.txt`: dependências Python necessárias para executar a aplicação;
- `estilo.tcss`: arquivo de estilo da interface construída com Textual.

## Módulos da aplicação

A aplicação foi modularizada para separar melhor responsabilidades.

### `screens/`

Contém as telas principais da aplicação:

- `initial_screen.py`: tela inicial;
- `view_screen.py`: tela de visualização de dados;
- `operation_screen.py`: tela principal de operações, incluindo cadastro, venda, atualização e deleção.

### `modals/`

Contém janelas auxiliares usadas durante as operações:

- `view_modal.py`: modal de visualização com filtros;
- `delete_modal.py`: modal de deleção por ID;
- `update_select_modal.py`: modal para selecionar registros que serão atualizados;
- `formulario_modal.py`: formulário genérico de inserção e atualização;
- `formulario_pessoa_composto.py`: formulário para cadastro completo de cliente, fornecedor ou vendedor.

### Módulos `operacoes_*.py`

A camada de operações com o banco foi separada em módulos menores:

- `operacoes_crud.py`: concentra as operações genéricas `insert`, `select`, `update` e `delete`;
- `operacoes_estoque.py`: registra entradas e perdas de estoque, atualizando o estoque dos produtos;
- `operacoes_venda.py`: abre operações de caixa e finaliza vendas em uma única transação;
- `operacoes_consultas.py`: executa consultas específicas com `JOIN` e `UNION ALL`, como endereços e telefones;
- `operacoes_pessoa.py`: contém regras específicas para deleção segura de clientes, vendedores e fornecedores;
- `operacoes.py`: mantém uma interface única para importação das funções no restante da aplicação.

## Principais entidades do banco

O banco representa as seguintes entidades principais:

- `CATEGORIA`
- `UNIDADEMEDIDA`
- `PRODUTO`
- `FORNECEDOR`
- `CLIENTE`
- `VENDEDOR`
- `CAIXA`
- `OPERACAOCAIXA`
- `PEDIDO`
- `PAGAMENTO`
- `ITEMPEDIDO`
- `PERDAESTOQUE`
- `ENTRADAESTOQUE`
- `ENDERECO`
- `ENDERECOCLIENTE`
- `ENDERECOVENDEDOR`
- `ENDERECOFORNEC`
- `FORNECEDOR_CELFORN`
- `CLIENTE_CELCLIENTE`

Essas tabelas permitem representar o funcionamento do hortifruti desde o cadastro dos produtos e pessoas envolvidas até o controle de estoque e o fluxo de vendas.

## Funcionalidades da aplicação CRUD

A aplicação permite realizar operações como:

- visualizar dados das tabelas;
- filtrar registros exibidos na interface;
- cadastrar produtos, categorias, unidades, clientes, fornecedores, vendedores, caixas e endereços;
- registrar entradas de estoque;
- registrar perdas de estoque;
- atualizar registros existentes;
- deletar registros por ID;
- abrir operação de caixa;
- montar carrinho de venda;
- finalizar pedido;
- registrar pagamento;
- baixar estoque automaticamente durante a venda;
- fechar operação de caixa.

Os filtros da interface são feitos após o carregamento dos dados da tabela: o usuário escolhe a coluna por meio de um `Select` e digita o termo de busca em um campo de texto.

## Tecnologias utilizadas

- Python
- PostgreSQL
- Psycopg2
- Textual
- Rich
- Neon PostgreSQL
- Python Dotenv

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd HortifruitidaFamilia-BD
```

### 2. Criar e ativar um ambiente virtual

Dentro da pasta do projeto, crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

No Linux/macOS:

```bash
source .venv/bin/activate
```

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instalar as dependências

Entre na pasta `crud/`:

```bash
cd crud
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Configurar a conexão com o banco

O arquivo `crud/conexao.py` é responsável por abrir a conexão com o PostgreSQL.

Para executar o projeto, é necessário configurar corretamente os dados de conexão por variáveis de ambiente ou por um arquivo `.env` dentro da pasta `crud/`.

Exemplo de arquivo `crud/.env`:

```text
PGHOST=<host-do-banco>
PGDATABASE=<nome-do-banco>
PGUSER=<usuario>
PGPASSWORD=<senha>
PGSSLMODE=require
```

Por segurança, o arquivo `.env` não deve ser versionado no GitHub.

### 5. Criar as tabelas do banco

A partir da raiz do projeto, execute o script DDL no PostgreSQL:

```bash
psql -d <nome-do-banco> -f sql/DDL.sql
```

Esse comando cria a estrutura do banco.

### 6. Popular o banco

Para executar a carga completa:

```bash
psql -d <nome-do-banco> -f sql/DML.sql
```

Também é possível popular o banco aos poucos usando os arquivos da pasta `sql/seeds/`. Essa forma é útil para testar e depurar inserções por partes.

Exemplo:

```bash
psql -d <nome-do-banco> -f sql/seeds/01_categorias.sql
psql -d <nome-do-banco> -f sql/seeds/02_unidades.sql
```

### 7. Executar a aplicação

Dentro da pasta `crud/`, execute:

```bash
python terminal.py
```

O arquivo `terminal.py` inicializa a aplicação definida em `app.py`.

## Observações sobre segurança

O projeto utiliza conexão com banco PostgreSQL. Por isso, é importante evitar expor credenciais no repositório.

Recomenda-se:

- não publicar senhas no GitHub;
- usar variáveis de ambiente ou arquivo `.env`;
- adicionar arquivos sensíveis ao `.gitignore`;
- trocar senhas caso alguma credencial tenha sido versionada por engano.

## Observações sobre integridade

O banco utiliza chaves primárias, chaves estrangeiras e restrições `CHECK` para preservar a consistência dos dados.

Entre as restrições implementadas, destacam-se:

- preços não negativos;
- estoque não negativo;
- quantidades positivas em itens, entradas e perdas;
- documentos únicos para clientes, fornecedores e vendedores;
- relacionamentos entre produtos, categorias, pedidos, pagamentos, caixas, vendedores e clientes.

Além das restrições do banco, a aplicação também realiza algumas validações antes das operações, como:

- validação de campos obrigatórios nos formulários;
- validação de tipos numéricos;
- validação de estoque suficiente antes de finalizar vendas;
- validação de dados básicos em cadastros compostos de clientes, fornecedores e vendedores.

## Implementações futuras

Algumas melhorias possíveis para versões futuras são:

- criação de testes automatizados;
- geração automática de IDs por `SERIAL`, `IDENTITY` ou sequences;
- validação mais rigorosa de datas;
- validação completa de CPF e CNPJ com dígitos verificadores;
- melhoria visual da interface;
- criação de uma pasta `services/` para separar regras de negócio adicionais, caso o projeto cresça;
- criação de uma pasta `utils/` para centralizar filtros, validadores e formatadores reutilizáveis;
- transformação dos arquivos `operacoes_*.py` em um pacote próprio;
- documentação mais detalhada das consultas e dos índices de otimização;
- revisão completa das credenciais do banco, incluindo troca de senhas que tenham sido expostas durante o desenvolvimento.

## Status do projeto

O projeto está em desenvolvimento acadêmico e foi construído para demonstrar modelagem relacional, criação de banco PostgreSQL e implementação de uma interface CRUD em Python.
