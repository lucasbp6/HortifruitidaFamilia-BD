from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Footer, Placeholder, Button, Static, DataTable, Input, Label, ContentSwitcher
from textual.containers import Vertical, Horizontal
import entities
'''
# Adicionamos a Tabela 
        yield DataTable(id="minha-lista")

        # Chama a tabela para carregar os dados nela ( ver como fazer isso com o banco de dados na hora de juntar)
def on_mount(self) -> None:
        
        tabela = self.query_one(DataTable)
        
        # Muda o cursor para selecionar a linha inteira em vez de célula por célula
        tabela.cursor_type = "row" 
        
        # Adiciona colunas
        tabela.add_columns("ID", "Descrição", "Status")
        
        # Adiciona várias linhas na nossa lista
        tabela.add_rows([
            ("001", "Teclado Mecânico", "Ativo"),
            ("002", "Mouse Sem Fio", "Em Estoque"),
            ("003", "Monitor 24 polegadas", "Falta"),
            ("004", "Cabo HDMI", "Ativo"),
        ])

        # Não deve ser usado na nossa implementação

        def adicionar_na_tabela(self, dados: tuple | None) -> None:
        """Esta função é chamada automaticamente quando o Modal usa 'dismiss()'."""
        # Se o usuário clicou em cancelar, os dados virão como 'None'
        if dados is not None:
            # Desempacota a tupla que enviamos do modal
            nome, valor = dados
            
            # Pega a tabela
            tabela = self.query_one(DataTable)
            
            # Gera um ID automático baseado na quantidade de linhas atuais
            novo_id = f"{len(tabela.rows) + 1:03}"
            
            # Adiciona a nova linha na tabela!
            tabela.add_row(novo_id, nome, valor)
        '''



# POPUP para receber valores
class FormularioModal(ModalScreen):
    ''' 
    TODO: acrescentar a ideia de que eu vou ter diversos tipos de formularios a partir de uma lista de atributos que eu espero receber 
    '''
    # 1. Construtor para receber tuplas como sendo os valores que precisamos coletar
    def __init__(self, dados_iniciais: tuple, **kwargs):
        super().__init__(**kwargs)
        self.dados_iniciais = dados_iniciais[0]
        self.tipos = dados_iniciais[1]
    
    def compose(self) -> ComposeResult:
        with Vertical(id="caixa-formulario"):
            yield Label("Cadastrar Novo Item", id="titulo-form")
            
            # Campos de preenchimento
            for i in range(len(self.dados_iniciais)):
                yield Input(placeholder=f"Digite o {self.dados_iniciais[i]}...", id=f"input-{i}")
            
            
            with Horizontal(id="botoes-form"):
                yield Button("Salvar", id="btn-salvar", variant="success")
                yield Button("Cancelar", id="btn-cancelar", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        
        if event.button.id == "btn-cancelar":
            # Fecha a tela enviando 'None' 
            self.dismiss(None) 
            
        elif event.button.id == "btn-salvar":
            # Captura o texto digitado nos Inputs
            size = len(self.dados_iniciais)
            values = {}

            # Varredura de validação
            for i, (coluna, tipo_esperado) in enumerate(zip(self.dados_iniciais, self.tipos)):
                valor_texto = self.query_one(f"#input-{i}", Input).value.strip()
                
                # 1. VERIFICAÇÃO DE CAMPO VAZIO
                if not valor_texto:
                    if "None" in tipo_esperado:
                        valores_validados[coluna] = None
                        continue 
                    else:
                        self.app.notify(f"O campo '{coluna}' é obrigatório!", severity="error")
                        return 

                # 2. VERIFICAÇÃO ESTRITA DE TIPAGEM (Apenas valida, não converte)
                tipo_base = tipo_esperado.split(" | ")[0].strip()
                
                if tipo_base == "int":
                    # Rejeita se tiver letras (ex: "A", "10A", "10.5")
                    if not valor_texto.isdigit():
                        self.app.notify(f"O campo '{coluna}' aceita APENAS números inteiros.", severity="error")
                        return
                        
                elif tipo_base == "float":
                    # Testa se é possível ser um número decimal
                    try:
                        float(valor_texto.replace(",", "."))
                    except ValueError:
                        self.app.notify(f"O campo '{coluna}' aceita APENAS números (ex: 10.50).", severity="error")
                        return
                        
                elif tipo_base == "date":
                    # Testa se respeita o calendário
                    try:
                        datetime.strptime(valor_texto, "%Y-%m-%d")
                    except ValueError:
                        self.app.notify(f"Data inválida em '{coluna}'. Use AAAA-MM-DD.", severity="error")
                        return
                        
                elif tipo_base == "datetime":
                    try:
                        datetime.strptime(valor_texto, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        self.app.notify(f"Data/Hora inválida em '{coluna}'.", severity="error")
                        return

                # 3. SALVAMENTO ORIGINAL
                # Se passou por todas as barreiras acima (não caiu em nenhum return), 
                # nós salvamos o texto EXATAMENTE como o usuário digitou.
                valores_validados[coluna] = valor_texto
            
            # Fecha a tela enviando os dados validados (todos no formato string original)
            self.dismiss(valores_validados)
            
# --- TELA INICIAL ---
class InitialScreen(Screen):
    def compose(self) -> ComposeResult:

        LOGO_HORTIFRUTI = """\
        _   _               _   _  __               _     _ 
        | | | | ___  _ __  _| |_(_)/ _| _ __  _   _ | |_  (_)
        | |_| |/ _ \| '__||_   _| | |_ | '__|| | | ||  _| | |
        |  _  | (_) | |     | | | |  _|| |   | |_| || |_  | |
        |_| |_|\___/|_|     |_| |_|_|  |_|    \__,_| \__| |_|
                                                crud v26.6\
        """
        yield Static(LOGO_HORTIFRUTI, classes="titulo-tela")
        
        
        # 3. Adicionamos os botões (um para o popup, outro para mudar de tela)
        yield Button("Operar", id="btn-operar", variant="primary")
        yield Button("Visualizar dados", id="btn-vizualizar", variant="primary")
        yield Footer()


    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "btn-operar":
            self.app.switch_mode("operation")
        elif event.button.id == "btn-vizualizar":
            self.app.switch_mode("view")
            # Abre o popup e enviar a função que vai receber os valores
            #self.app.push_screen(FormularioModal(("basta", "cansei")), self.adicionar_na_tabela)
            


class ViewScreen(Screen):
    def compose(self) -> ComposeResult:

        yield Button("Tela Inicial", id="btn-inicial", variant="primary")

        #Seleção de qual tabela vizualizar, fazer com que eles chamem a função correta
        #talvez mudar o id para o nome da tabela
        yield Button("Clientes", id="btn-vw-clientes")
        yield Button("Fornecedores", id="btn-vw-forn")
        yield Button("Vendedores", id="btn-vw-vend")
        yield Button("Endereço Clientes", id="btn-vw-endclien")
        yield Button("Endereço fornecedores", id="btn-vw-endforn")
        yield Button("Endereço Vendedores", id="btn-vw-endvend")
        yield Button("Unidades", id="btn-vw-unid")
        yield Button("Produtos", id="btn-vw-prod")
        yield Button("Categorias", id="btn-vw-catg")
        yield Button("Entrada estoque", id="btn-vw-entest")
        yield Button("Perda estoque", id="btn-vw-perdaest")
        yield Button("Vendas", id="btn-vw-vendas")
        yield Button("Operações", id="btn-vw-oper")


        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-inicial":
            self.app.switch_mode("inicial")

class OperationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ident = None

    def compose(self) -> ComposeResult:
        with ContentSwitcher(initial="menu-opcoes", id="meu-switcher"):
            
            # VISÃO 1: O menu principal
            with Vertical(id="menu-opcoes"):
                yield Static("=== ESCOLHA UMA OPERAÇÃO ===")
                yield Button("Cadastros", id="btn-cadastro")
                yield Button("Iniciar operação", id="btn-vender")
                yield Button("Deletar", id="btn-deletar")
                yield Button("Atualizar", id="btn-update")

            # VISÃO 2: Tela de Cadastro
            with Vertical(id="tela-cadastro"):
                yield Static("Aqui ficaria o seu formulário de cadastro...")
                yield Button("Voltar para o Menu", id="btn-voltar", variant="error")
                yield Button("Add Produto", id="btn-adprod")
                yield Button("Add Categoria", id="btn-adcat")
                yield Button("Add estoque", id="btn-adestq")
                yield Button("Add Perda estoque", id="btn-adpestq")
                yield Button("Add Cliente", id="btn-adcliente")
                yield Button("Add Fornecedor", id="btn-adforn")
                yield Button("Add Vendedor", id="btn-advend")
                yield Button("Add Unidade", id="btn-aduni")
                yield Button("Add Caixa", id="btn-adcx")


            # VISÃO 3: Passo 1 da Venda (Identificação)
            with Vertical(id="tela-identificar"):
                yield Static("Mostrar a lista para identificar o vendedor")
                # lista vendedor
                yield Button("Prosseguir para o Caixa", id="btn-prosseg", variant="success")
                yield Button("Voltar para o Menu", id="btn-voltar-3", variant="error")

            # VISÃO 4: Passo 2 da Venda (O Caixa)
            with Vertical(id="tela-venda"):
                yield Static("Aqui ficaria o seu sistema de frente de caixa real...")
                yield Button("Voltar para o Menu", id="btn-voltar-2", variant="error")


            with Vertical(id="tela-deletar"):
                yield Static("Aqui ficaria o seu formulário de cadastro...")
                yield Button("Voltar para o Menu", id="btn-voltar", variant="error")
                yield Button("Del Produto", id="btn-dlprod")
                yield Button("Del Categoria", id="btn-dlcat")
                yield Button("Del estoque", id="btn-dlestq")
                yield Button("Del Perda estoque", id="btn-dlpestq")
                yield Button("Del Cliente", id="btn-dlcliente")
                yield Button("Del Fornecedor", id="btn-dlforn")
                yield Button("Del Vendedor", id="btn-dlvend")
                yield Button("Del Unidade", id="btn-dluni")
                yield Button("Del Caixa", id="btn-dlcx")
                
            with Vertical(id="tela-update"):
                yield Static("Aqui ficaria o seu formulário de cadastro...")
                yield Button("Voltar para o Menu", id="btn-voltar", variant="error")
                yield Button("Att Produto", id="btn-upprod")
                yield Button("Att Categoria", id="btn-upcat")
                yield Button("Att estoque", id="btn-upestq")
                yield Button("Att Perda estoque", id="btn-uppestq")
                yield Button("Att Cliente", id="btn-upcliente")
                yield Button("Att Fornecedor", id="btn-upforn")
                yield Button("Att Vendedor", id="btn-upvend")
                yield Button("Att Unidade", id="btn-upuni")
                yield Button("Att Caixa", id="btn-upcx")
                
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        switcher = self.query_one("#meu-switcher", ContentSwitcher)
        
        # 1. Clicou em Cadastros
        if event.button.id == "btn-cadastro":
            switcher.current = "tela-cadastro"
            
        # 2. Clicou em Vendas -> Manda para a tela de Identificação (Passo 1)
        elif event.button.id == "btn-vender":
            switcher.current = "tela-identificar"
            
        # 3. Clicou em Prosseguir -> Atribui o vendedor e vai pro Caixa (Passo 2)
        elif event.button.id == "btn-prosseg":
            # Aqui você pegaria o valor da sua lista. Usando (1,2) de exemplo:
            self.ident = (1, 2)
            switcher.current = "tela-venda"

        # 4. Agrupamos todos os botões de voltar na mesma regra!
        elif event.button.id in ["btn-voltar", "btn-voltar-2", "btn-voltar-3"]:
            switcher.current = "menu-opcoes"
            self.ident = None # Limpa a identificação ao cancelar/voltar

        # 5. Voltar para a tela inicial do App
        elif event.button.id == "btn-inicial":
            self.app.switch_mode("inicial")

        elif event.button.id == "btn-deletar":
            switcher.current = "tela-deletar"

        elif event.button.id == "btn-update":
            switcher.current = "tela-update"

        elif event.button.id == "btn-adprod":
            self.app.push_screen(FormularioModal(entities.TABELAS["Produto"]))


class ModesApp(App):
    CSS_PATH = "estilo.tcss" # Lembre-se de criar este arquivo!
    
    BINDINGS = [
        ("d", "switch_mode('inicial')", "inicial"),  
        ("s", "switch_mode('view')", "view"),
        ("h", "switch_mode('operation')", "operation"),
    ]
    
    MODES = {
        "inicial": InitialScreen,  
        "view": ViewScreen,
        "operation": OperationScreen,
    }

    def on_mount(self) -> None:
        self.switch_mode("inicial")  


if __name__ == "__main__":
    app = ModesApp()
    app.run()