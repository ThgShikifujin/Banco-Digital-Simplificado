from Conta import Conta

class Cliente:

    def __init__(self, nome, cpf):
        if not cpf.isnumeric() or len(cpf) != 11:
            raise ValueError(f"CPF inválido: '{cpf}'. O CPF deve conter 11 digitos numéricos.")

        if not nome:
            raise ValueError("Nome não pode estar em branco.")

        self.nome = nome
        self.cpf = cpf
        self.contas = []

    def adicionar_conta(self, conta):
        if not isinstance(conta, Conta):
            print(f"Erro: Tentativa de adicionar um objeto que não é do tipo 'Conta' ao cliente {self.nome}.")
            return
        self.contas.append(conta)
        print(f"Conta {conta} adicionada ao cliente {self.nome}.")