from textual.app import App

from screens.initial_screen import InitialScreen
from screens.view_screen import ViewScreen
from screens.operation_screen import OperationScreen


class ModesApp(App):
    CSS_PATH = "estilo.tcss"

    BINDINGS = [
        ("d", "switch_mode('inicial')", "Tela inicial"),
        ("s", "switch_mode('view')", "Visualizar dados"),
        ("h", "switch_mode('operation')", "Operar"),
    ]

    MODES = {
        "inicial": InitialScreen,
        "view": ViewScreen,
        "operation": OperationScreen,
    }

    def on_mount(self) -> None:
        self.switch_mode("inicial")