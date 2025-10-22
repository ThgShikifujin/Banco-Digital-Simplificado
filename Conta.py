class Conta:
    # criando a lista de contas
    def __init__(self, numero, saldo, tipo):
        self.numero: int = numero
        self.saldo: float = saldo
        self.tipo: str = tipo

    def __str__(self):
        return f"Conta: {self.numero}, saldo: {self.saldo}, tipo: {self.tipo}"

    # Depositar saldo na conta
    def depositar(self, valor):
        if valor <= 0:
            print(f"Falha ao depositar R${valor}, o valor não pode ser negativo ou igual a 0")
            return
        self.saldo += valor
        print(f"Depósito de R${valor} efetuado com sucesso! Depósito: R${valor} Saldo Atual :R${self.saldo}")

    # Sacar saldo da conta verificando a conta e saldo disponivel
    def sacar(self, valor):
        if valor <= 0:
            print(f"Falha ao sacar R${valor}, o valordo saque não pose ser negativo ou igual a 0")
            return
        if valor <= self.saldo:
            self.saldo -= valor
            print(f"Saque de R${valor} efetuado com sucesso!")
            print(f"Saldo atual: R${self.saldo}")
        else:
            print(f"Saque negado, saldo insuficiente!")
            return

    # Extrato da conta, verificando conta
    def extrato(self):
        print(f"Saldo Atual: R${self.saldo}")