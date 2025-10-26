import json

class Autenticacao:
    """
        Gerencia o cadastro, verificação e alteração de senhas.
        É responsável pela persistência dos dados de autenticação
        no arquivo 'clientes_cadastrados.json'.
    """

    def __init__(self):
        """
            Responsável por carregar o arquivo 'clientes_cadastrados.json'
            para leitura assim que a classe é chamada tratando possíveis
            erros de arquivo inexistente ou decodificão, caso os erros
            ocorram a classe cria uma nova bibliotéca clientes
        """
        self.clientes_cadastrados = {}

        try:
            with open("clientes_cadastrados.json", "r") as arquivo:
                self.clientes_cadastrados = json.load(arquivo)
        except FileNotFoundError:
            self.clientes_cadastrados = {} # Arquivo não existe, começa do zero
        except json.JSONDecodeError:
            self.clientes_cadastrados = {}  # Arquivo existe, mas está vazio ou corrompido
            print("Aviso: Arquivo de senhas estava corrompido ou vazio. Iniciando do zero.")

    def cadastrar_senha(self, cpf, senha):
        if cpf in self.clientes_cadastrados:
            print(f"Cliente {cpf} já cadastrado!")
            return False
        if len(senha) != 6:
            print("A senha deve conter exatamente 6 caracteres")
            return False
        # TODO: Implementar hashing de senhas (lib hashlib?).
        #       Não é seguro salvar senhas em texto puro.
        self.clientes_cadastrados[cpf] = senha
        try:
            with open("clientes_cadastrados.json", "w") as arquivo:
                json.dump(self.clientes_cadastrados, arquivo, indent=4)
                print(f"Cliente {cpf} cadastrado com sucesso!")
                return True
        except OSError:
            print(f"Erro ao salvar o cadastro do cliente {cpf}.")
            return False

    def verificar_login(self, cpf, senha):
        if cpf in self.clientes_cadastrados:
            if self.clientes_cadastrados[cpf] == senha:
                return True
            else:
                print("Senha incorreta!")
                return False
        else:
            print("CPF não encontrado!")
            return False

    def alterar_senha(self, cpf, senha_atual, nova_senha):
        if cpf not in self.clientes_cadastrados:
            print("ERRO: CPF não cadastrado!")
            return False
        if self.clientes_cadastrados[cpf] != senha_atual:
            print("ERRO: Senha incorreta!")
            return False
        self.clientes_cadastrados[cpf] = nova_senha
        try:
            with open("clientes_cadastrados.json", "w") as arquivo:
                json.dump(self.clientes_cadastrados, arquivo, indent=4)
                return True
        except OSError:
                print("Falha ao cadastrar a nova senha!")
                return False