from Conta import Conta

class Cliente:
    """
        Representa a entidade 'Cliente' no sistema.
        Armazena os dados pessoais (nome, cpf) e a(s) conta(s) bancária(s)
        associada(s) a este cliente específico.
    """

    def __init__(self, nome, cpf):
        # --- Validação de Entrada (Guard Clauses) ---
        # Garante que o CPF seja numérico e tenha 11 dígitos.
        if not cpf.isnumeric() or len(cpf) != 11:
            # Lança uma exceção se o CPF for inválido, impedindo a criação do objeto.
            raise ValueError(f"CPF inválido: '{cpf}'. O CPF deve conter 11 digitos numéricos.")

        # Garante que o nome não seja uma ‘string’ vazia.
        if not nome:
            raise ValueError("Nome não pode estar em branco.")

        # --- Atributos da Instância ---
        self.nome = nome
        self.cpf = cpf
        self.contas = [] # Um cliente pode ter múltiplas contas (Composição)

    def adicionar_conta(self, conta):
        """
            Associa um objeto Conta a este cliente.

            Este método primeiro valida se o objeto fornecido é
            realmente uma instância da classe 'Conta' antes de
            adicioná-lo à lista interna de contas do cliente.

            Args:
             conta (Conta): O objeto Conta a ser adicionado.
        """

        # Verificação de tipo para garantir a integridade da lista self.contas
        if not isinstance(conta, Conta):
            print(f"Erro: Tentativa de adicionar um objeto que não é do tipo 'Conta' ao cliente {self.nome}.")
            return # Sai do método se o tipo for inválido
        self.contas.append(conta)
        # O print aqui usa o método __str__ da classe Conta (desacoplamento)
        print(f"Conta {conta} adicionada ao cliente {self.nome}.")