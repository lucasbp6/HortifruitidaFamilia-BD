from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Footer, Button, Static, DataTable, Input, Label, ContentSwitcher, Select
from textual.containers import Vertical, Horizontal
from textual import on
import entities
import operacoes
from datetime import datetime

if __name__ == "__main__":
    app = ModesApp()
    app.run()
