from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static
from textual.containers import Vertical, Horizontal

import operacoes


class FormularioPessoaComposto(ModalScreen):
    DEFAULT_CSS = """
    FormularioPessoaComposto { background: black; padding: 1; }
    #caixa-formulario { width: 80%; height: auto; border: solid green; padding: 1; }
    """

    TIPOS_VALIDOS = {"CLIENTE", "FORNECEDOR", "VENDEDOR"}

    def __init__(self, tipo_pessoa: str, **kwargs):
        super().__init__(**kwargs)
        self.tipo_pessoa = tipo_pessoa.upper()

        if self.tipo_pessoa not in self.TIPOS_VALIDOS:
            raise ValueError(
                "Tipo de pessoa inválido. Use CLIENTE, FORNECEDOR ou VENDEDOR."
            )

    def compose(self) -> ComposeResult:
        with Vertical(id="caixa-formulario"):
            yield Label(f"Cadastro Completo: {self.tipo_pessoa}", id="titulo-form")

            yield Static("--- Dados Básicos ---")
            yield Input(placeholder="ID (Ex: 10)", id="pes_id")
            yield Input(placeholder="Nome Completo", id="pes_nome")
            yield Input(placeholder="Documento (CPF/CNPJ - apenas números)", id="pes_doc")

            if self.tipo_pessoa in ["CLIENTE", "VENDEDOR"]:
                yield Input(placeholder="Data de Nascimento (AAAA-MM-DD)", id="pes_nasc")

            if self.tipo_pessoa == "VENDEDOR":
                yield Input(placeholder="Salário Base", id="pes_salario")

            yield Input(placeholder="Celular (apenas números)", id="pes_celular")

            yield Static("--- Endereço ---")
            yield Input(placeholder="ID do Endereço a criar", id="end_id")
            yield Input(placeholder="CEP (apenas números)", id="end_cep")
            yield Input(placeholder="Rua", id="end_rua")
            yield Input(placeholder="Número", id="end_num")
            yield Input(placeholder="Bairro", id="end_bairro")
            yield Input(placeholder="Cidade", id="end_cid")
            yield Input(placeholder="Estado (Ex: SP)", id="end_est")
            yield Input(placeholder="País", id="end_pais")

            with Horizontal(id="botoes-form"):
                yield Button("Salvar Tudo", id="btn-salvar-comp", variant="success")
                yield Button("Cancelar", id="btn-cancelar-comp", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancelar-comp":
            self.dismiss()
            return

        if event.button.id == "btn-salvar-comp":
            self._salvar_cadastro_composto()

    def _valor_input(self, widget_id: str) -> str:
        return self.query_one(widget_id, Input).value.strip()

    def _validar_obrigatorio(self, valor: str, nome_campo: str) -> None:
        if not valor:
            raise ValueError(f"O campo '{nome_campo}' é obrigatório.")

    def _validar_inteiro(self, valor: str, nome_campo: str) -> int:
        self._validar_obrigatorio(valor, nome_campo)

        if not valor.isdigit():
            raise ValueError(f"O campo '{nome_campo}' deve conter apenas números inteiros.")

        return int(valor)

    def _validar_float(self, valor: str, nome_campo: str) -> float:
        self._validar_obrigatorio(valor, nome_campo)

        try:
            return float(valor.replace(",", "."))
        except ValueError:
            raise ValueError(f"O campo '{nome_campo}' deve conter um número válido.")

    def _validar_texto(self, valor: str, nome_campo: str, tamanho_minimo: int = 1) -> str:
        self._validar_obrigatorio(valor, nome_campo)

        if len(valor) < tamanho_minimo:
            raise ValueError(f"O campo '{nome_campo}' está curto demais.")

        return valor

    def _validar_documento(self, documento: str) -> str:
        self._validar_obrigatorio(documento, "Documento")

        if not documento.isdigit():
            raise ValueError("O documento deve conter apenas números.")

        if self.tipo_pessoa in ["CLIENTE", "VENDEDOR"] and len(documento) != 11:
            raise ValueError("CPF deve ter exatamente 11 dígitos.")

        if self.tipo_pessoa == "FORNECEDOR" and len(documento) != 14:
            raise ValueError("CNPJ deve ter exatamente 14 dígitos.")

        return documento

    def _validar_celular(self, celular: str) -> str:
        self._validar_obrigatorio(celular, "Celular")

        if not celular.isdigit():
            raise ValueError("O celular deve conter apenas números.")

        if len(celular) < 10 or len(celular) > 15:
            raise ValueError("O celular deve ter entre 10 e 15 dígitos.")

        return celular

    def _validar_cep(self, cep: str) -> str:
        self._validar_obrigatorio(cep, "CEP")

        if not cep.isdigit():
            raise ValueError("O CEP deve conter apenas números.")

        if len(cep) != 8:
            raise ValueError("O CEP deve ter exatamente 8 dígitos.")

        return cep

    def _validar_estado(self, estado: str) -> str:
        estado = estado.upper()
        self._validar_obrigatorio(estado, "Estado")

        if len(estado) != 2:
            raise ValueError("O estado deve ter exatamente 2 caracteres. Exemplo: SP.")

        return estado

    def _montar_endereco(self) -> dict:
        return {
            "IDEndereco": self._validar_inteiro(self._valor_input("#end_id"), "ID do Endereço"),
            "RuaEnd": self._validar_texto(self._valor_input("#end_rua"), "Rua"),
            "NumeroEnd": self._validar_inteiro(self._valor_input("#end_num"), "Número"),
            "ComplemEnd": None,
            "CEPEnd": self._validar_cep(self._valor_input("#end_cep")),
            "BairroEnd": self._validar_texto(self._valor_input("#end_bairro"), "Bairro"),
            "CidadeEnd": self._validar_texto(self._valor_input("#end_cid"), "Cidade"),
            "EstadoEnd": self._validar_estado(self._valor_input("#end_est")),
            "PaisEnd": self._validar_texto(self._valor_input("#end_pais"), "País"),
        }

    def _montar_dados_base(self) -> tuple[int, str, str, str]:
        id_pessoa = self._validar_inteiro(self._valor_input("#pes_id"), "ID")
        nome = self._validar_texto(self._valor_input("#pes_nome"), "Nome Completo")
        documento = self._validar_documento(self._valor_input("#pes_doc"))
        celular = self._validar_celular(self._valor_input("#pes_celular"))

        return id_pessoa, nome, documento, celular

    def _montar_insert_cliente(self, id_pessoa: int, nome: str, documento: str, celular: str, id_endereco: int):
        data_nasc = self._validar_texto(
            self._valor_input("#pes_nasc"),
            "Data de Nascimento"
        )

        tabelas = ["CLIENTE", "ENDERECOCLIENTE", "CLIENTE_CELCLIENTE"]

        valores = [
            {
                "IDCliente": id_pessoa,
                "NomeCliente": nome,
                "CPFCliente": documento,
                "DataNascCliente": data_nasc,
            },
            {
                "IDCliente": id_pessoa,
                "IDEndereco": id_endereco,
            },
            {
                "CelCliente": celular,
                "IDCliente": id_pessoa,
            },
        ]

        return tabelas, valores

    def _montar_insert_fornecedor(self, id_pessoa: int, nome: str, documento: str, celular: str, id_endereco: int):
        tabelas = ["FORNECEDOR", "ENDERECOFORNEC", "FORNECEDOR_CELFORN"]

        valores = [
            {
                "IDForn": id_pessoa,
                "NomeForn": nome,
                "CNPJForn": documento,
            },
            {
                "IDForn": id_pessoa,
                "IDEndereco": id_endereco,
            },
            {
                "CelForn": celular,
                "IDForn": id_pessoa,
            },
        ]

        return tabelas, valores

    def _montar_insert_vendedor(self, id_pessoa: int, nome: str, documento: str, celular: str, id_endereco: int):
        data_nasc = self._validar_texto(
            self._valor_input("#pes_nasc"),
            "Data de Nascimento"
        )

        salario = self._validar_float(
            self._valor_input("#pes_salario"),
            "Salário Base"
        )

        tabelas = ["VENDEDOR", "ENDERECOVENDEDOR"]

        valores = [
            {
                "IDVend": id_pessoa,
                "NomeVend": nome,
                "CPFVend": documento,
                "DataNascVend": data_nasc,
                "CelVend": celular,
                "SalarioVend": salario,
            },
            {
                "IDVend": id_pessoa,
                "IDEndereco": id_endereco,
            },
        ]

        return tabelas, valores

    def _montar_tabelas_e_valores(self):
        endereco = self._montar_endereco()
        id_pessoa, nome, documento, celular = self._montar_dados_base()

        tabelas = ["ENDERECO"]
        valores = [endereco]

        id_endereco = endereco["IDEndereco"]

        if self.tipo_pessoa == "CLIENTE":
            tabelas_pessoa, valores_pessoa = self._montar_insert_cliente(
                id_pessoa,
                nome,
                documento,
                celular,
                id_endereco
            )

        elif self.tipo_pessoa == "FORNECEDOR":
            tabelas_pessoa, valores_pessoa = self._montar_insert_fornecedor(
                id_pessoa,
                nome,
                documento,
                celular,
                id_endereco
            )

        elif self.tipo_pessoa == "VENDEDOR":
            tabelas_pessoa, valores_pessoa = self._montar_insert_vendedor(
                id_pessoa,
                nome,
                documento,
                celular,
                id_endereco
            )

        else:
            raise ValueError(f"Tipo de pessoa inválido: {self.tipo_pessoa}")

        tabelas.extend(tabelas_pessoa)
        valores.extend(valores_pessoa)

        return tabelas, valores

    def _salvar_cadastro_composto(self) -> None:
        try:
            tabelas, valores = self._montar_tabelas_e_valores()

            operacoes.insert(tabelas, valores)

            self.app.notify(
                f"{self.tipo_pessoa} salvo com sucesso!",
                severity="success"
            )
            self.dismiss()

        except Exception as erro:
            self.app.notify(
                f"Falha no cadastro (rollback efetuado): {erro}",
                severity="error",
                timeout=6
            )