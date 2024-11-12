# Oque é esse trabalho? 
  Este trabalho foi realizado para a materia APS, Atividades Práticas Supervisionadasidade, na faculdade UNIP (Universidade Paulista). O Objetivo é demonstrar o funcionamento da criptografia RSA. 
  
*Em Anexo deixo video de três minutos demonstrando o funcionamento do sistema: https://jam.dev/c/bededc9e-d603-4b71-b661-6fc7fcd4e3c2*


# Bibliotecas utilizadas

tkinter: Biblioteca padrão do Python para criar interfaces gráficas (GUI).

ttk: Sub-biblioteca de tkinter para elementos de interface mais avançados.

random: Biblioteca para geração de números aleatórios.

math: Biblioteca para funções matemáticas básicas, incluindo gcd (Greatest Common Divisor - Máximo Divisor Comum).

sympy: Biblioteca simbólica para operações matemáticas avançadas, incluindo randprime (geração de números primos aleatórios).

datetime: Biblioteca para trabalhar com datas e horários.


# Funções

modular_inverse(e, phi_n): Esta função calcula o inverso modular de e módulo phi_n. O inverso modular é um número d tal que (e * d) % phi_n == 1. 
É um componente chave da criptografia RSA.

extended_gcd(a, b): Função auxiliar usada para calcular o inverso modular usando o algoritmo euclidiano estendido.

main(): Função principal do programa que inicializa a interface gráfica e define a funcionalidade dos botões.

salvar_historico(mensagem_criptografada, e, d, n): Salva os detalhes da criptografia (mensagem criptografada, chaves usadas) em um histórico para referência futura.

gerar_numeros_primos(el): Gera um número primo aleatório de el bits de tamanho usando a função randprime da biblioteca sympy.

Reset(): Limpa o campo de entrada de texto, a senha e o histórico de criptografia.

GerarSenha(): Abre uma janela separada para definir uma nova senha.

Criptografar(): Criptografa a mensagem inserida pelo usuário utilizando a chave pública (e, n) gerada aleatoriamente.

criptoMessage(message, n, e): Função que realiza a criptografia da mensagem usando a exponenciação modular.

VerHistorico(): Abre uma janela separada para exibir o histórico de criptografia.

Descriptografar(): Descriptografa a mensagem selecionada no histórico usando a chave privada correspondente salva no histórico.

decriptoMensagem(mensagem, d, n): Função que realiza a descriptografia da mensagem usando a exponenciação modular.

Erro(text_err): Exibe uma janela de erro com a mensagem de erro especificada.

# Interface Gráfica (GUI)

A interface gráfica do programa consiste em:

Caixa de texto para inserir a mensagem a ser criptografada.

Campo de entrada de senha.

Botão "Redefinir senha" para definir uma nova senha.

Botão "Histórico/Descriptografar" para visualizar o histórico de criptografia e descriptografar mensagens.

Botão "Criptografar" para criptografar a mensagem inserida.

Botão "Limpar" para limpar o campo de texto e a senha.

# Processo de Criptografia:

O usuário insere a mensagem a ser criptografada.

O usuário define uma senha.

Ao clicar em "Criptografar", o programa gera aleatoriamente um par de chaves RSA (e, n) públicos e privados (d, n).

A chave pública é usada para criptografar a mensagem.

A mensagem criptografada e as chaves usadas são salvas no histórico.

A mensagem criptografada é exibida na tela.

# Processo de Descriptografia

O usuário seleciona uma mensagem criptografada do histórico.

O sistema recupera a chave privada correspondente.

A mensagem é descriptografada usando a chave privada.
