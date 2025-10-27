from Banco import Banco
from Autenticacao import Autenticacao


def main():
    """
        Função principal (entry point) do aplicativo.
        Responsável por inicializar os serviços (Autenticacao, Banco)
        e controlar o loop principal do menu (estados logado/deslogado).
    """
    # 1. Inicializa o serviço de autenticação
    auth_service = Autenticacao()
    # 2. Injeta o serviço de autenticação no Banco (Injeção de Dependência).
    #    Isso desacopla o Banco; ele não precisa saber como criar o auth_service.
    meu_banco = Banco(auth_service)

    while True:
        # --- MENU PRINCIPAL (DESLOGADO) ---
        print("\n=== BEM VINDO AO BANCO ===")
        print("1. Criar Conta")
        print("2. Fazer Login")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome: ")
            cpf = input("Digite o cpf: ")
            senha = input("Digite uma senha (deve conter 6 dígitos numéricos): ")
            # Delega a responsabilidade de criar o cliente para a classe Banco.
            # O 'main' não sabe como um cliente é criado, ele apenas coleta os dados.
            meu_banco.criar_cliente(nome, cpf, senha)
        elif opcao == "2":
            cpf = input("Digite o cpf: ")
            senha = input("Digite uma senha: ")

            cliente_logado = meu_banco.fazer_login(cpf, senha)
            if cliente_logado:
                # --- MENU INTERNO (LOGADO) ---
                while True:
                    print(f"\n=== BEM VINDO {cliente_logado.nome} ===")
                    print("1. Depositar")
                    print("2. Sacar")
                    print("3. Extrato")
                    print("4. Alterar senha")
                    print("5. Sair")

                    opcao = input("Escolha uma opção: ")

                    if opcao == "1":
                        valor_str = input("Digite o valor do depósito: ")
                        try:
                            valor_float = float(valor_str)
                        except ValueError:
                            print("Digite apenas números!")
                            # Retorna ao início do loop do menu LOGADO
                            # se o usuário digitar um valor inválido.
                            continue
                        meu_banco.fazer_deposito(cliente_logado, valor_float)
                    elif opcao == "2":
                        valor_str = input("Digite o valor do saque: ")
                        try:
                            valor_float = float(valor_str)
                        except ValueError:
                            print("Digite apenas números!")
                            # Retorna ao início do loop do menu LOGADO
                            # se o usuário digitar um valor inválido.
                            continue
                        meu_banco.fazer_saque(cliente_logado, valor_float)
                    elif opcao == "3":
                        # Como o extrato é uma operação de 'leitura' (não
                        # altera dados), não precisamos do Banco para orquestrar
                        # ou salvar. Acessamos a conta diretamente.

                        # TODO: Remover o "atalho" [0] e permitir ao
                        #       usuário escolher de qual conta ver o extrato.
                        cliente_logado.contas[0].extrato()
                    elif opcao == "4":
                        senha_atual = input("Digite a sua senha atual: ")
                        senha_nova = input("Digite a nova senha: ")
                        meu_banco.alterar_senha_logado(cliente_logado, senha_atual, senha_nova)
                    elif opcao == "5":
                        print(f"Deslogando, até a próxima {cliente_logado.nome}")
                        # Quebra o loop INTERNO (menu logado) e retorna
                        # ao loop EXTERNO (menu principal).
                        break

        elif opcao == "3":
            print("Encerrando o sistema...")
            break

if __name__ == '__main__':
    # Garante que a função main() só seja executada quando este
    # arquivo (main.py) for rodado diretamente pelo Python,
    # e não quando for importado por outro módulo.
    main()