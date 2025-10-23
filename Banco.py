from Cliente import Cliente
from Conta import Conta
from Autenticacao import Autenticacao
import json

class Banco:

    def __init__(self, servico_auth: Autenticacao):
        self.autenticacao = servico_auth
        self._arquivo_dados = "dados_banco.json"
        self.clientes = {}
        self._carregar_dados()

    def _carregar_dados(self):
        try:
            with open(self._arquivo_dados, "r") as f:
                dados_json = json.load(f)
                for cpf, dados_cliente in dados_json.items():
                    cliente = Cliente(dados_cliente['nome'], cpf)
                    for dados_conta in dados_cliente['contas']:
                        conta = Conta(dados_conta['numero'], dados_conta['saldo'], dados_conta['tipo'])
                        cliente.adicionar_conta(conta)
                    self.clientes[cpf] = cliente
        except (FileNotFoundError, json.JSONDecodeError):
            self.clientes = {}
            print("Aviso: Arquivo de dados não encontrado ou corrompido. Iniciando com banco de dados vazio.")

    def _salvar_dados(self):
        dados_para_salvar = {}
        for cpf, objeto_cliente in self.clientes.items():
            lista_de_contas_json = []
            for objeto_conta in objeto_cliente.contas:
                dicionario_da_conta = {
                    "numero": objeto_conta.numero,
                    "saldo": objeto_conta.saldo,
                    "tipo": objeto_conta.tipo,
                }
                lista_de_contas_json.append(dicionario_da_conta)
        dados_para_salvar[cpf] = {
            "nome": objeto_cliente.nome,
            "contas": lista_de_contas_json,
        }
        try:
            with open(self._arquivo_dados, "w") as f:
                json.dump(dados_para_salvar, f, indent=4)
                return True
        except OSError:
            print(f"Aviso: Falha ao salvar dados no arquivo {self._arquivo_dados}.")
            return False

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
        if self._salvar_dados():
            print(f"Cliente {nome} (CPF: {cpf}) cadastrado com sucesso!")
            return True
        else:
            print(f"Erro: Cliente criado, mas falha ao salvar no banco de dados.")
            return False