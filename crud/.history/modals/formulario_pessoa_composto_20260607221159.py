class FormularioPessoaComposto(ModalScreen):
    DEFAULT_CSS = """
    FormularioPessoaComposto { background: black; padding: 1; }
    #caixa-formulario { width: 80%; height: auto; border: solid green; padding: 1; }
    """

    def __init__(self, tipo_pessoa: str, **kwargs):
        super().__init__(**kwargs)
        self.tipo_pessoa = tipo_pessoa.upper()
        
    def compose(self) -> ComposeResult:
        with Vertical(id="caixa-formulario"):
            yield Label(f"Cadastro Completo: {self.tipo_pessoa}", id="titulo-form")
            
            yield Static("--- Dados Básicos ---")
            yield Input(placeholder="ID (Ex: 10)", id="pes_id")
            yield Input(placeholder="Nome Completo", id="pes_nome")
            yield Input(placeholder="Documento (CPF/CNPJ)", id="pes_doc")
            
            if self.tipo_pessoa in ["CLIENTE", "VENDEDOR"]:
                yield Input(placeholder="Data de Nascimento (AAAA-MM-DD)", id="pes_nasc")
            if self.tipo_pessoa == "VENDEDOR":
                yield Input(placeholder="Salário Base", id="pes_salario")
            
            yield Input(placeholder="Celular (Apenas números)", id="pes_celular")
            
            yield Static("--- Endereço ---")
            yield Input(placeholder="ID do Endereço a criar", id="end_id")
            yield Input(placeholder="CEP", id="end_cep")
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
            try:
                d_end = {
                    "IDEndereco": self.query_one("#end_id", Input).value,
                    "RuaEnd": self.query_one("#end_rua", Input).value,
                    "NumeroEnd": self.query_one("#end_num", Input).value,
                    "ComplemEnd": None, 
                    "CEPEnd": self.query_one("#end_cep", Input).value,
                    "BairroEnd": self.query_one("#end_bairro", Input).value,
                    "CidadeEnd": self.query_one("#end_cid", Input).value,
                    "EstadoEnd": self.query_one("#end_est", Input).value,
                    "PaisEnd": self.query_one("#end_pais", Input).value,
                }
                
                id_pes = self.query_one("#pes_id", Input).value
                doc = self.query_one("#pes_doc", Input).value
                nome = self.query_one("#pes_nome", Input).value
                cel = self.query_one("#pes_celular", Input).value
                
                tabelas = ["ENDERECO"]
                valores = [d_end]

                if self.tipo_pessoa == "CLIENTE":
                    tabelas.extend(["CLIENTE", "ENDERECOCLIENTE", "CLIENTE_CELCLIENTE"])
                    valores.append({"IDCliente": id_pes, "NomeCliente": nome, "CPFCliente": doc, "DataNascCliente": self.query_one("#pes_nasc", Input).value})
                    valores.append({"IDCliente": id_pes, "IDEndereco": d_end["IDEndereco"]})
                    valores.append({"CelCliente": cel, "IDCliente": id_pes})
                    
                elif self.tipo_pessoa == "FORNECEDOR":
                    tabelas.extend(["FORNECEDOR", "ENDERECOFORNEC", "FORNECEDOR_CELFORN"])
                    valores.append({"IDForn": id_pes, "NomeForn": nome, "CNPJForn": doc})
                    valores.append({"IDForn": id_pes, "IDEndereco": d_end["IDEndereco"]})
                    valores.append({"CelForn": cel, "IDForn": id_pes})
                    
                elif self.tipo_pessoa == "VENDEDOR":
                    tabelas.extend(["VENDEDOR", "ENDERECOVENDEDOR"])
                    valores.append({"IDVend": id_pes, "NomeVend": nome, "CPFVend": doc, "DataNascVend": self.query_one("#pes_nasc", Input).value, "SalarioVend": self.query_one("#pes_salario", Input).value, "CelVend": cel})
                    valores.append({"IDVend": id_pes, "IDEndereco": d_end["IDEndereco"]})

                operacoes.insert(tabelas, valores)
                self.app.notify(f"{self.tipo_pessoa} salvo com sucesso!", severity="success")
                self.dismiss()
                
            except Exception as e:
                self.app.notify(f"Falha no cadastro (Rollback efetuado): {e}", severity="error")