from Cliente import Cliente
from Conta import Conta

class Autenticacao:

    def __init__(self):
        self.clientes_cadastrados = {}

    def cadastrar_senha(self, cpf, senha):
        if cpf in self.clientes_cadastrados:
            print(f"Cliente {cpf} já cadastrado!")
            return False
        if len(senha) != 6:
            print("A senha deve conter exatamente 6 caracteres")
            return False
        self.clientes_cadastrados[cpf] = senha
        print("Cliente {cpf} cadastrado com sucesso!")
        return True

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
        if self.clientes_cadastrados[cpf] == senha_atual:
            self.clientes_cadastrados[cpf] = nova_senha
            return True
        else:
            print("Senha incorreta tente novamente!")
            return False