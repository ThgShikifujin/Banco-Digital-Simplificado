from Cliente import Cliente
from Conta import Conta
from Autenticacao import Autenticacao
import json

class Banco:
    """
        Classe orquestradora central do sistema bancário.

        Responsável por:
        - Injetar e usar o serviço de Autenticacao.
        - Gerenciar o ciclo de vida dos objetos Cliente e Conta.
        - Orquestrar as operações (criar cliente, login, transações).
        - Lidar com a persistência (serialização/desserialização)
          dos dados de clientes e contas no 'dados_banco.json'.
    """

    def __init__(self, servico_auth: Autenticacao):
        """
            Inicializa o Banco.

            Args:
                servico_auth (Autenticacao): Uma instância do serviço de
                autenticação (Injeção de Dependência).
        """
        self.autenticacao = servico_auth
        self._arquivo_dados = "dados_banco.json"
        self.clientes = {} # Dicionário de objetos Cliente "vivos" (em memória)
        self._proximo_numero_conta = 1000 # Contador p/ garantir contas únicas

        # Carrega os dados do JSON para a memória assim que o banco é criado.
        self._carregar_dados()

    # --- MÉTODOS DE PERSISTÊNCIA (JSON) ---
    def _carregar_dados(self):
        """
            (Desserialização) Carrega os dados do 'dados_banco.json' para a memória.

            Lê o JSON e "traduz" os dicionários de volta para objetos
            'Cliente' e 'Conta' "vivos", populando 'self.clientes'.
            Também carrega o contador 'self._proximo_numero_conta'.
        """
        try:
            with open(self._arquivo_dados, "r") as f:
                dados_json = json.load(f)

                # Carrega o contador (ou usa o padrão 1000 se a chave não existir)
                self._proximo_numero_conta = dados_json.get("proximo_numero_conta", 1000)

                # Carrega APENAS o sub-dicionário "clientes"
                dados_clientes_json = dados_json.get("clientes", {})

                # Itera sobre os dados dos clientes e os "reanima" como objetos
                for cpf, dados_cliente in dados_clientes_json.items():
                    # 'dados_cliente' agora é garantido ser um dicionário
                    cliente = Cliente(dados_cliente['nome'], cpf)
                    for dados_conta in dados_cliente['contas']:
                        conta = Conta(dados_conta['numero'], dados_conta['saldo'], dados_conta['tipo'])
                        cliente.adicionar_conta(conta)
                    # Adiciona o cliente "vivo" (com suas contas) ao dicionário da memória
                    self.clientes[cpf] = cliente

        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou estiver corrompido, começa do zero.
            self.clientes = {}
            self._proximo_numero_conta = 1000  # Começa do zero se o arquivo não existir
            print("Aviso: Arquivo de dados não encontrado ou corrompido. Iniciando banco de dados vazio.")

    def _salvar_dados(self):
        """
            (Serialização) Salva o estado atual da memória ('self.clientes'
            e 'self._proximo_numero_conta') de volta no 'dados_banco.json'.

            "Traduz" os objetos 'Cliente' e 'Conta' "vivos" de volta
             para dicionários simples para que possam ser escritos em JSON.
        """
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
        """
            Orquestra o processo completo de criação de um novo cliente.

            1. Tenta cadastrar a senha no serviço de Autenticacao.
            2. Se sucesso, cria o objeto Cliente (validando dados).
            3. Cria uma Conta padrão (Corrente, saldo 0) com um número único.
            4. Associa a Conta ao Cliente.
            5. Salva o novo estado no 'dados_banco.json'.

            Args:
                nome (str): Nome do cliente.
                cpf (str): CPF do cliente (será validado).
                senha (str): Senha do cliente (será validada).

            Returns:
                bool: True se o cliente foi criado com sucesso, False caso contrário.
        """
        # 1. Orquestração: Chama o serviço de autenticação primeiro.
        sucesso_auth = self.autenticacao.cadastrar_senha(cpf,senha)
        if not sucesso_auth:
            print("Falha ao criar cliente: CPF já cadastrado ou senha inválida (precisa ter 6 caracteres).")
            return False
        # 2. Tenta criar a entidade Cliente (pode falhar com ValueError
        try:
            novo_cliente = Cliente(nome, cpf)
        except ValueError as e:
            # Captura erros de validação da classe Cliente (ex: CPF inválido)
            print(f"Falha ao criar cliente: {e}")
            # TODO: Desfazer o cadastro da senha se a criação do cliente falhar
            #       (rollback/saga pattern). Por enquanto, apenas falha.
            return False
        # Adiciona o cliente "vivo" ao dicionário da memória
        self.clientes[cpf] = novo_cliente
        self._proximo_numero_conta += 1 # Incrementa o contador para o próximo uso
        nova_conta_padrao = Conta(self._proximo_numero_conta, 0.0, "Corrente")

        # 4. Associa a conta ao cliente
        novo_cliente.adicionar_conta(nova_conta_padrao)

        # 5. Salva o novo estado (com o novo cliente) no JSON
        if self._salvar_dados():
            print(f"Cliente {nome} (CPF: {cpf}) cadastrado com sucesso!")
            return True
        else:
            # Se o salvamento falhar, o estado fica inconsistente
            # (cliente na memória, mas não no disco)
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
        # 1. Verifica no serviço de autenticação
        if not self.autenticacao.verificar_login(cpf, senha):
            print("Erro: CPF ou senha incorretos.")
            return None

        # 2. Se a senha estiver correta, busca o objeto Cliente
        # Usamos .get(cpf) em vez de [cpf] para evitar um KeyError.
        # (programação defensiva).
        cliente_logado = self.clientes.get(cpf)

        if cliente_logado:
            print(f"Login bem-sucedido! Bem-vindo, {cliente_logado.nome}.")
            return cliente_logado # Retorna o objeto "vivo"
        else:
            # Estado de erro grave: senha existe, mas dados do cliente não.
            print(f"Erro grave de integridade de dados: Senha válida, mas dados do cliente {cpf} não encontrados.")
            return None

    def fazer_deposito(self, cliente_alvo, valor):
        """
            Orquestra um depósito na conta de um cliente e salva a alteração.

            Args:
                cliente_alvo (Cliente): O objeto Cliente que está logado.
                valor (float): O valor a ser depositado.
        """
        # TODO: Remover o "atalho" [0] e permitir ao usuário
        #       escolher em qual conta depositar.
        conta_do_cliente = cliente_alvo.contas[0]

        # 1. Delega a lógica de negócio (somar) para a classe Conta
        conta_do_cliente.depositar(valor)

        # 2. Salva o novo estado (saldo atualizado) no JSON
        self._salvar_dados()

        # TODO: Refatorar 'Conta.depositar' para retornar True/False
        #       e repassar esse status para o main.py.

    def fazer_saque(self, cliente_alvo, valor):
        """
            Orquestra um saque da conta de um cliente e salva a alteração.

            Args:
                cliente_alvo (Cliente): O objeto Cliente que está logado.
                valor (float): O valor a ser sacado.
        """
        # TODO: Remover o "atalho" [0]
        conta_do_cliente = cliente_alvo.contas[0]

        # 1. Delega a lógica de negócio (subtrair) para a classe Conta
        conta_do_cliente.sacar(valor)

        # 2. Salva o novo estado (saldo atualizado) no JSON
        self._salvar_dados()

        # TODO: Refatorar 'Conta.sacar' para retornar True/False
        #       e repassar esse status para o main.py.

    def alterar_senha_logado(self,cliente_alvo, senha_atual, senha_nova):
        """
            Orquestra a alteração de senha de um cliente logado.

            Args:
                cliente_alvo (Cliente): O objeto Cliente que está logado.
                senha_atual (str): A senha antiga fornecida pelo usuário.
                nova_senha (str): A nova senha desejada.

            Returns:
                bool: True se a senha foi alterada, False caso contrário.
        """
        # Pega o CPF do objeto cliente "vivo"
        cpf = cliente_alvo.cpf

        # 1. Delega a lógica (e o salvamento no JSON de senhas)
        #    para o serviço de autenticação
        sucesso = self.autenticacao.alterar_senha(cpf,senha_atual, senha_nova)

        # 2. Reporta o resultado (que já foi impresso pela Autenticacao)
        if sucesso:
            print(f"Senha alterada com sucesso!")
            return sucesso
        else:
            # A classe Autenticacao já imprimiu o erro
            # (ex: "Senha incorreta!")
            print("Senha incorreta!")
            return sucesso