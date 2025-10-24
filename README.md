# Sistema Bancário em Python (Projeto Educacional)

Este é um projeto de console (terminal) desenvolvido em Python como parte de um estudo focado em Programação Orientada a Objetos (POO) e boas práticas de desenvolvimento. O objetivo foi construir um sistema bancário simulado, desde a autenticação de clientes até a persistência de dados em arquivos JSON.

## Conceitos e Tecnologias Aplicados

O principal objetivo deste projeto foi aplicar e solidificar os seguintes conceitos:

* **Programação Orientada a Objetos (POO):**
    * Criação de classes (`Banco`, `Cliente`, `Conta`, `Autenticacao`) para modelar o domínio do problema.
    * Uso de **Encapsulamento** (esconder a lógica interna) e **Responsabilidade Única (SRP)** (cada classe tem um trabalho).
    * **Composição:** Um `Cliente` *possui* uma lista de `Contas`.
* **Persistência de Dados com JSON:**
    * Utilização de dois arquivos JSON separados para gerenciar dados (um para autenticação e outro para os dados do banco).
    * **Serialização e Desserialização:** Lógica manual para "traduzir" objetos Python (`Cliente`, `Conta`) para o formato JSON (dicionários) e vice-versa.
* **Arquitetura de Software:**
    * **Separação de Responsabilidades:** O `main.py` cuida da interface com o usuário (I/O), enquanto as classes cuidam da lógica de negócios (`Conta`), orquestração (`Banco`) e serviços (`Autenticacao`).
    * **Injeção de Dependência:** A classe `Banco` recebe o serviço de `Autenticacao` em seu construtor, mantendo o baixo acoplamento.
* **Tratamento de Erros Robusto:**
    * Uso extensivo de `try...except` para lidar com falhas de I/O (`FileNotFoundError`, `OSError`), dados corrompidos (`JSONDecodeError`) e entradas inválidas do usuário (`ValueError`).
* **Estrutura de Módulos:**
    * Organização do código em múltiplos arquivos (`.py`) que importam uns aos outros, simulando um projeto real.

## Funcionalidades (Features)

* **Gerenciamento de Clientes:**
    * Criação de novos clientes (com geração automática de número de conta).
* **Autenticação Segura:**
    * Menu de Login (separação de estado "logado" e "deslogado").
    * Verificação de CPF e senha.
    * Possibilidade de alterar a senha (requer senha antiga).
* **Transações Bancárias:**
    * Depositar (com validação de valor).
    * Sacar (com validação de valor e saldo).
    * Ver Extrato (saldo atual).
* **Persistência Total:**
    * Todas as alterações (novos clientes, depósitos, saques, mudanças de senha) são salvas permanentemente nos arquivos JSON.

## Como Executar

1.  Clone este repositório.
2.  Certifique-se de ter o Python 3 instalado.
3.  Navegue até a pasta do projeto e execute o arquivo principal:

```bash
python main.py
