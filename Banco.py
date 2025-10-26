from Cliente import Cliente
from Conta import Conta
from Autenticacao import Autenticacao
import json

class Banco:

    def __init__(self, servico_auth: Autenticacao):
        self.autenticacao = servico_auth
        self._arquivo_dados = "dados_banco.json"
        self.clientes = {}
        self._proximo_numero_conta = 1000
        self._carregar_dados()

    # --- MÉTODOS DE PERSISTÊNCIA (JSON) ---
    def _carregar_dados(self):
        try:
            with open(self._arquivo_dados, "r") as f:
                dados_json = json.load(f)

                # Carrega o contador (ou usa o padrão 1000 se a chave não existir)
                self._proximo_numero_conta = dados_json.get("proximo_numero_conta", 1000)

                # Carrega APENAS o sub-dicionário "clientes"
                dados_clientes_json = dados_json.get("clientes", {})

                # O loop itera apenas sobre os clientes
                for cpf, dados_cliente in dados_clientes_json.items():
                    # 'dados_cliente' agora é garantido ser um dicionário
                    cliente = Cliente(dados_cliente['nome'], cpf)
                    for dados_conta in dados_cliente['contas']:
                        conta = Conta(dados_conta['numero'], dados_conta['saldo'], dados_conta['tipo'])
                        cliente.adicionar_conta(conta)
                    self.clientes[cpf] = cliente

        except (FileNotFoundError, json.JSONDecodeError):
            self.clientes = {}
            self._proximo_numero_conta = 1000  # Começa do zero se o arquivo não existir
            print("Aviso: Arquivo de dados não encontrado ou corrompido. Iniciando banco de dados vazio.")

    def _salvar_dados(self):
        dados_para_salvar = {
            "proximo_numero_conta": self._proximo_numero_conta,
            "clientes": {}
        }
        for cpf, objeto_cliente in self.clientes.items():
            lista_de_contas_json = []
            for objeto_conta in objeto_cliente.contas:
                dicionario_da_conta = {
                    "numero": objeto_conta.numero,
                    "saldo": objeto_conta.saldo,
                    "tipo": objeto_conta.tipo,
                }
                lista_de_contas_json.append(dicionario_da_conta)
        dados_para_salvar["clientes"][cpf] = {
            "nome": objeto_cliente.nome,
            "contas": lista_de_contas_json
        }
        try:
            with open(self._arquivo_dados, "w") as f:
                json.dump(dados_para_salvar, f, indent=4)
                return True
        except OSError:
            print(f"Aviso: Falha ao salvar dados no arquivo {self._arquivo_dados}.")
            return False

    # --- MÉTODOS DE ORQUESTRAÇÃO (PÚBLICOS) ---
    def criar_cliente(self, nome, cpf, senha):
        sucesso_auth = self.autenticacao.cadastrar_senha(cpf,senha)
        if not sucesso_auth:
            print("Falha ao criar cliente: CPF já cadastrado ou senha inválida (precisa ter 6 caracteres).")
            return False
        try:
            novo_cliente = Cliente(nome, cpf)
        except ValueError as e:
            print(f"Falha ao criar cliente: {e}")
            return False
        self.clientes[cpf] = novo_cliente
        self._proximo_numero_conta += 1
        nova_conta_padrao = Conta(self._proximo_numero_conta, 0.0, "Corrente")
        novo_cliente.adicionar_conta(nova_conta_padrao)
        if self._salvar_dados():
            print(f"Cliente {nome} (CPF: {cpf}) cadastrado com sucesso!")
            return True
        else:
            print(f"Erro: Cliente criado, mas falha ao salvar no banco de dados.")
            return False

    def fazer_login(self, cpf, senha):
        """
            Valida as credenciais de um usuário contra os dados salvos.

            Args:
                cpf (str): O CPF do usuário tentando logar.
                senha (str): A senha fornecida pelo usuário.

            Returns:
                Cliente: O objeto Cliente "vivo", se o login for bem-sucedido.
                None: Se a autenticação falhar (CPF ou senha incorretos).
        """
        if not self.autenticacao.verificar_login(cpf, senha):
            print("Erro: CPF ou senha incorretos.")
            return None
        # Usamos .get(cpf) em vez de [cpf] para evitar um KeyError.
        # Isso é uma proteção caso os dados de autenticação e do banco
        # estejam dessincronizados (programação defensiva).
        cliente_logado = self.clientes.get(cpf)

        if cliente_logado:
            print(f"Login bem-sucedido! Bem-vindo, {cliente_logado.nome}.")
            return cliente_logado
        else:
            print(f"Erro grave de integridade de dados: Senha válida, mas dados do cliente {cpf} não encontrados.")
            return None

    def fazer_deposito(self, cliente_alvo, valor):
        conta_do_cliente = cliente_alvo.contas[0]

        conta_do_cliente.depositar(valor)

        self._salvar_dados()

    def fazer_saque(self, cliente_alvo, valor):
        conta_do_cliente = cliente_alvo.contas[0]

        conta_do_cliente.sacar(valor)

        self._salvar_dados()

    def alterar_senha_logado(self,cliente_alvo, senha_atual, senha_nova):
        cpf = cliente_alvo.cpf
        sucesso = self.autenticacao.alterar_senha(cpf,senha_atual, senha_nova)

        if sucesso:
            print(f"Senha alterada com sucesso!")
            return sucesso
        else:
            print("Senha incorreta!")
            return sucesso