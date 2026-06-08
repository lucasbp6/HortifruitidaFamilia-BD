from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Button, Static


class InitialScreen(Screen):
    MODO_OPERACAO = "operation"
    MODO_VISUALIZACAO = "view"

    LOGO_HORTIFRUTI = r"""
     _   _               _   _  __               _     _ 
    | | | | ___  _ __  _| |_(_)/ _| _ __  _   _ | |_  (_)
    | |_| |/ _ \| '__||_   _| | |_ | '__|| | | ||  _| | |
    |  _  | (_) | |     | | | |  _|| |   | |_| || |_  | |
    |_| |_|\___/|_|     |_| |_|_|  |_|    \__,_| \__| |_|
                                            crud v26.6
    """

    def compose(self) -> ComposeResult:
        yield Static(self.LOGO_HORTIFRUTI, classes="titulo-tela")
        yield Button("Operar", id="btn-operar", variant="primary")
        yield Button("Visualizar dados", id="btn-visualizar", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-operar":
            self.app.switch_mode(self.MODO_OPERACAO)

        elif event.button.id == "btn-visualizar":
            self.app.switch_mode(self.MODO_VISUALIZACAO)