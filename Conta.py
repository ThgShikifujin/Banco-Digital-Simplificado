class Conta:
    """
        Representa a entidade Conta no sistema,
        responsábilizando-se por fazer as operações de uma conta
        como depositar, sacar e exibir o extrato.
    """
    def __init__(self, numero, saldo, tipo):
        # --- Atributos da Instância ---
        self.numero: int = numero
        self.saldo: float = saldo
        self.tipo: str = tipo

    def __str__(self):
        """
            Retorna uma representação em string da conta.
            Usado para exibir os detalhes da conta de forma legível
            (ex: no print da classe Cliente).
        """
        return f"Conta: {self.numero}, saldo: {self.saldo}, tipo: {self.tipo}"

    def depositar(self, valor):
        """
            Soma o valor do depósito a conta em questão

            Args:
                valor (float): O valor a ser depositado. Deve ser positivo.
        """
        # --- Validação de Entrada (Guard Clauses) ---
        # Garante que o valor não seja negativo ou 0 e interrompe a operção
        if valor <= 0:
            print(f"Falha ao depositar R${valor}, o valor não pode ser negativo ou igual a 0")
            return
        # Soma o valor a instancia saldo da conta
        self.saldo += valor
        # Feedback de depósito bem sussedido
        print(f"Depósito de R${valor} efetuado com sucesso! Depósito: R${valor} Saldo Atual :R${self.saldo}")

    def sacar(self, valor):
        """
            Subtrai um valor do saldo da conta, se houver fundos suficientes.

            Args:
                valor (float): O valor a ser sacado. Deve ser positivo.
        """

        # --- Validação de Entrada (Guard Clauses) ---
        # Garante que o valor não seja negativo ou 0 e interrompe a operção
        if valor <= 0:
            print(f"Falha ao sacar R${valor}, o valordo saque não pose ser negativo ou igual a 0")
            return

        # Subtrai o valor a instancia saldo da conta
        if valor <= self.saldo:
            self.saldo -= valor
            # Feedback de saque bem sussedido
            # TODO: Refatorar para 'return True' e mover o print para o main.py
            print(f"Saque de R${valor} efetuado com sucesso!")
            # return True (seria o ideal)
            print(f"Saldo atual: R${self.saldo}")
        else:
            # Feedback de saque mal sussedido
            # TODO: Refatorar para 'return False' e mover o print para o main.py
            print(f"Saque negado, saldo insuficiente!")
            # return False (seria o ideal
            return

    def extrato(self):
        """
            Responsável por extrair o saldo e exibir na tela
        """
        print(f"Saldo Atual: R${self.saldo}")