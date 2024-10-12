from tkinter import *
import random 
from math import gcd
from sympy import randprime

#  To-do:
#   Criar um botão para confirmar o input do gerarSenha, e o action será voltar para a tela inicial
#   Adicionar uma validação p/ a senha, uma vez que o usuario DEVE digitar no minimo 8 caracteres
#   Criar um array contendo, [chaveCriptografada, mensagemDescriptografada], para assim ter um historico. 
#   Criar a função de gerar chave, não tive tempo ainda para pensar como iria funcionar esse modulo.
#   Quando o usuario coloca uma mensagem não criptografada logo apos de utilizar do sistema, 
# o sistema acaba pegando a ultima informação salva para colocar na mensagem de descriptografia
# Acaba gerando duas paginas quando inicializa o programa, talvez seja melhor colocar em uma tela o modulo de gerarSenha().

# Função que irá descriptografar, tive suporte de IA para desenvolver essa função
def modular_inverse(e, phi_n):
    # Usar o algoritmo estendido de Euclides para encontrar o inverso modular
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y

    g, x, y = extended_gcd(e, phi_n)
    if g != 1:
        raise ValueError("O inverso modular não existe.")
    else:
        return x % phi_n
    
def main():
    ## Métodos suporte
    def gerar_numeros_primos(el):
        return randprime(2**(el-1), 2**el) #Em tese precisamos a lib. sympy para ganhar processamento nos dados

    # Declaração das variaveis
    global p, q, n, e, d, password_global
    p = gerar_numeros_primos(2048)
    q = gerar_numeros_primos(2048)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537
    d = modular_inverse(e, phi_n)
    senhaSetada = False
    ## Métodos
    def Reset():
        key.set("")
        gerar_password.set("")
        repFrase.delete(1.0, END)
        senhaSetada = False

    def GerarSenha():
        screenPassword = Toplevel(screen)
        screenPassword.title("Definição de senha")
        screenPassword.geometry("400x250")
        screenPassword.configure(bg="#5e6065")

        Label(screenPassword, text="Informe a sua nova senha: ", font="ariel", fg="black", bg="#5e6065").place(x=10, y=0)
        Entry(screenPassword, textvariable=gerar_password, width=30, bd=0, font=("Ariel", 12), show="*").place(x=10, y=40)
        # Precisa fazer um botão para voltar a tela inicial

        senhaSetada = True
        return gerar_password

    def Criptografar():
        passworkKey = key.get()
        passwordRes = gerar_password.get()
        if(passwordRes != ""):
            if passworkKey == passwordRes:
                screenCriptografia = Toplevel(screen)
                screenCriptografia.title("Criptografado")
                screenCriptografia.geometry("500x250")
                screenCriptografia.configure(bg="#6c8389")

                mensagem = repFrase.get(1.0, END).strip()

                # Gerar chave RSA  
                def criptoMessage(message, n, e):
                    # Converter mensagem em inteiro
                    mensagem = int.from_bytes(message.encode('utf-8'), byteorder='big')
                    # Criptografar a mensagem
                    mensagemCriptografada = pow(mensagem, e, n)
                    global mensagem_criptografada_global #Não sei porque carambas esse global PRECISA estar aqui, se mudar ele de lugar o codigo nn vai pegar.
                    mensagem_criptografada_global = mensagemCriptografada
                    return mensagem_criptografada_global

                Label(screenCriptografia, text="Criptografado", font="ariel", fg="white", bg="#6c8389").place(x=10, y=0)
                textCripto = Text(screenCriptografia, font="Verdana", bg="white", relief=GROOVE, wrap=WORD, bd=0)
                textCripto.place(x=10, y=40, width=475, height=175)

                textCripto.insert(END, criptoMessage(mensagem, n, e))
            else: Erro("As senhas não conhecidem!")
        else: Erro("Erro no modulo de criptografia")

    def Descriptografar():
        passwordSetada = gerar_password.get()
        passwordDigitada = key.get()
        if(passwordSetada != ""):
            if passwordSetada == passwordDigitada:
                if(mensagem_criptografada_global != ""):
                    screenDescriptografia = Toplevel(screen)
                    screenDescriptografia.title("Descriptografado")
                    screenDescriptografia.geometry("500x250")
                    screenDescriptografia.configure(bg="#749594")

                    def decriptoMensagem(mensagem, d, n):

                        # Descriptografar a mensagem cifrada usando a chave privada
                        mensagemDescriptografada = pow(mensagem, d, n)

                        # Converter de volta para string
                        mensagem_bytes = mensagemDescriptografada.to_bytes((mensagemDescriptografada.bit_length() + 7) // 8, byteorder='big')
                        return mensagem_bytes.decode("utf-8")
                    
                    mensagem_descriptografada = decriptoMensagem(mensagem_criptografada_global, d, n)

                    Label(screenDescriptografia, text="Descriptografado", font="ariel", fg="white", bg="#749594").place(x=10, y=0)
                    textDecripto = Text(screenDescriptografia, font="Verdana", bg="white", relief=GROOVE, wrap=WORD, bd=0)
                    textDecripto.place(x=10, y=40, width=450, height=150)

                    textDecripto.insert(END, mensagem_descriptografada)
                else: Erro("Não foi encontrada a mensagem criptografada")
            else: Erro("A senha não conhecide...")
        else: Erro("Por favor informe a senha!")

    def GerarKey():
        screenPassword = Toplevel(screen)
        screenPassword.title("Definição de key")
        screenPassword.geometry("400x250")
        screenPassword.configure(bg="#667178")

        Label(screenPassword, text="Informe a sua nova senha: ", font="ariel", fg="black", bg="#667178").place(x=10, y=0)
        textPassword = Text(screenPassword, font="Verdana", bg="white", relief=GROOVE, wrap=WORD, bd=0)
        textPassword.place(x=10, y=40, width=400, height=150)
        


    def Erro(text_err):
        screenError = Toplevel(screen)
        screenError.title("Erro!")
        screenError.geometry("400x250")
        screenError.configure(bg="#F4796B")

        Label(screenError, text="Opss... Ocorreu um erro!", font="ariel", fg="black", bg="#F4796B").place(x=10, y=0)
        Label(screenError, text=text_err, font="ariel", fg="black").place(x=10, y=20)
        
    ## Parte GUI
    screen = Tk()
    screen.geometry("800x400")
    screen.title("Aps")
    key = StringVar()
    gerar_password = StringVar()

    if(senhaSetada == False):
        GerarSenha()

    Label(text="Informe a frase: ", font=("Ariel", 12), fg="black").place(x=12, y=12)
    repFrase = Text(font="Verdana", bg="white", relief=GROOVE, wrap=WORD, bd=0)
    repFrase.place(x=10, y=50, width=725, height=100)
    Label(text="Informe a senha: ", font=("Ariel", 12), fg="black").place(x=10, y=160)

    Entry(textvariable=key, width=725, bd=0, font=("Ariel", 12), show="*", command=print(key)).place(x=10, y=200)

    Button(text="Redefinir senha", height=2, width=15, bg="#5e6065", fg="white", bd=0, command=GerarSenha).place(x=125, y=250)
    Button(text="Key", height=2, width=15, bg="#667178", fg="white", bd=0, command=GerarKey).place(x=250, y=250)
    Button(text="Criptografar", height=2, width=15, bg="#6c8389", fg="white", bd=0, command=Criptografar).place(x=375, y=250)
    Button(text="Descriptografiar", height=2, width=15, bg="#749594", fg="white", bd=0, command=Descriptografar).place(x=500, y=250)
    Button(text="Resetar", height=2, width=70, bg="#83a79b", fg="white", bd=0, command=Reset).place(x=125, y=300)

    screen.mainloop()

main()
