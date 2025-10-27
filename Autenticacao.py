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
            ocorram a classe cria uma nova dicionário clientes
        """
        self.clientes_cadastrados = {}
        # Usando o try para possíveis erros e with open para não correr riscos do arquivo não ser fechado.
        try:
            with open("clientes_cadastrados.json", "r") as arquivo:
                self.clientes_cadastrados = json.load(arquivo)
        except FileNotFoundError:
            self.clientes_cadastrados = {} # Arquivo não existe, começa do zero
        except json.JSONDecodeError:
            self.clientes_cadastrados = {}  # Arquivo existe, mas está vazio ou corrompido
            print("Aviso: Arquivo de senhas estava corrompido ou vazio. Iniciando do zero.")

    def cadastrar_senha(self, cpf, senha):
        """
            Responsável por realizar o cadastro do cliente
            verificando se o CPF já não existe 'clientes_cadastrados.json'
            e se a senha tem 6 digitos. Reescrevendo e salvando o arquivo
            novamente com o método 'W'
            Args:
                cpf (str): CPF do cliente
                senha (str): senha do cliente
        """

        # --- Validação de Entrada (Guard Clauses) ---
        # Garante que um CPF existente não seja cadastrado novamente
        if cpf in self.clientes_cadastrados:
            print(f"Cliente {cpf} já cadastrado!")
            return False
        # --- Validação de Entrada (Guard Clauses) ---
        # Garante que a senha tenha exatamente 6 caracteres
        if len(senha) != 6:
            print("A senha deve conter exatamente 6 caracteres")
            return False
        # TODO: Implementar hashing de senhas (lib hashlib?).
        #       Não é seguro salvar senhas em texto puro.
        self.clientes_cadastrados[cpf] = senha
        # Garantindo o salvamento do cadastro usando o método W para garantir que todo arquivo existente seja reescrito com a alteração.
        try:
            with open("clientes_cadastrados.json", "w") as arquivo:
                json.dump(self.clientes_cadastrados, arquivo, indent=4)
                print(f"Cliente {cpf} cadastrado com sucesso!")
                return True
        except OSError:
            print(f"Erro ao salvar o cadastro do cliente {cpf}.")
            return False

    def verificar_login(self, cpf, senha):
        """
            Responsável por realizar a validação de CPF e senha
            verificando se o CFP existe nos clientes cadastrados
            e se a senha esta correta.
            Args:
                cpf (str): CPF do cliente
                senha (str): senha do cliente
        """
        # Verificando se o CPF existe na lista de cadastros e se a senha corresponde ao CPF
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
        """
            Responsável por alterar a senha do cliente verificando se o CPF
            existe, a senha atual para alterar e salvar para a senha nova.
            Args:
                cpf (str): CPF do cliente
                senha_atual (str): senha atual do cliente
                nova_senha (str): nova senha do cliente
        """

        # --- Validação de Entrada (Guard Clauses) ---
        # Verificando se o CPF existe na lista de clientes
        if cpf not in self.clientes_cadastrados:
            print("ERRO: CPF não cadastrado!")
            return False
        # --- Validação de Entrada (Guard Clauses) ---
        # Verificando se a senha está correta
        if self.clientes_cadastrados[cpf] != senha_atual:
            print("ERRO: Senha incorreta!")
            return False
        # Salvando a nova senha atrelada ao CPF
        self.clientes_cadastrados[cpf] = nova_senha
        # Reescrevendo todo o arquivo com a senha alterada
        try:
            with open("clientes_cadastrados.json", "w") as arquivo:
                json.dump(self.clientes_cadastrados, arquivo, indent=4)
                return True
        except OSError:
                print("Falha ao cadastrar a nova senha!")
                return False