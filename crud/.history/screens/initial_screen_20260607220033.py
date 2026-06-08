from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Button, Static

class InitialScreen(Screen):
    def compose(self) -> ComposeResult:
        LOGO_HORTIFRUTI = r"""
         _   _               _   _  __               _     _ 
        | | | | ___  _ __  _| |_(_)/ _| _ __  _   _ | |_  (_)
        | |_| |/ _ \| '__||_   _| | |_ | '__|| | | ||  _| | |
        |  _  | (_) | |     | | | |  _|| |   | |_| || |_  | |
        |_| |_|\___/|_|     |_| |_|_|  |_|    \__,_| \__| |_|
                                                crud v26.6
        """
        yield Static(LOGO_HORTIFRUTI, classes="titulo-tela")
        yield Button("Operar", id="btn-operar", variant="primary")
        yield Button("Visualizar dados", id="btn-vizualizar", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-operar":
            self.app.switch_mode("operation")
        elif event.button.id == "btn-vizualizar":
            self.app.switch_mode("view")