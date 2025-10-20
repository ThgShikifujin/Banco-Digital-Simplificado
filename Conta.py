from Cliente import Cliente

class Conta:
    # criando a lista de contas
    def __init__(self, numero, saldo, tipo):
        self.numero: int = numero
        self.saldo: float = saldo
        self.tipo: str = tipo

    # Depositar saldo na conta
    def depositar(self, valor):
        self.saldo += valor
        print(f"Depósito de R${valor} efetuado com sucesso! Depósito: R${valor} Saldo Atual :R${self.saldo}")

    # Sacar saldo da conta verificando a conta e saldo disponivel
    def sacar(self, valor):
        if valor <= conta.saldo:
            self.saldo -= valor
            print(f"Saque de R${valor} efetuado com sucesso!")
            print(f"Saldo atual: R${self.saldo}")
        else:
            print(f"Saque negado, saldo insuficiente!")
            return

    # Extrato da conta, verificando conta
    def extrato(self):
        print(f"Saldo Atual: R${conta.saldo}")