from tkinter import *
import random 
from math import gcd
from sympy import randprime

# Função para calcular o inverso modular de e em relação a φ(n)
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
    global p, q, n, e, d
    p = gerar_numeros_primos(2048)
    q = gerar_numeros_primos(2048)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537
    d = modular_inverse(e, phi_n)

    ## Métodos
    def Reset():
        key.set("")
        repFrase.delete(1.0, END)

    def Criptografar():
        passworkKey = key.get()
        if passworkKey == "1234":
            screenCriptografia = Toplevel(screen)
            screenCriptografia.title("Criptografado")
            screenCriptografia.geometry("400x250")
            screenCriptografia.configure(bg="#00bd56")

            mensagem = repFrase.get(1.0, END).strip()

            # Gerar chave RSA  
            def criptoMessage(message, n, e):
                # Converter mensagem em inteiro
                mensagem = int.from_bytes(message.encode('utf-8'), byteorder='big')
                # Criptografar a mensagem
                mensagemCriptografada = pow(mensagem, e, n)
                global mensagem_criptografada_global
                mensagem_criptografada_global = mensagemCriptografada
                return mensagem_criptografada_global


            # Verificar se e é relativamente primo a φ(n)
            if gcd(e, phi_n) != 1:
                raise ValueError("e não é relativamente primo a φ(n)")

            Label(screenCriptografia, text="Criptografado", font="ariel", fg="white", bg="#00bd56").place(x=10, y=0)
            textCripto = Text(screenCriptografia, font="Verdana", bg="white", relief=GROOVE, wrap=WORD, bd=0)
            textCripto.place(x=10, y=40, width=380, height=150)

            textCripto.insert(END, criptoMessage(mensagem, n, e))

    def Descriptografar():
        screenDescriptografia = Toplevel(screen)
        screenDescriptografia.title("Descriptografado")
        screenDescriptografia.geometry("400x250")
        screenDescriptografia.configure(bg="#ed3833")

        def decriptoMensagem(mensagem, d, n):

            # Descriptografar a mensagem cifrada usando a chave privada
            mensagemDescriptografada = pow(mensagem, d, n)

            # Converter de volta para string
            mensagem_bytes = mensagemDescriptografada.to_bytes((mensagemDescriptografada.bit_length() + 7) // 8, byteorder='big')
            return mensagem_bytes.decode("utf-8")

        mensagem_descriptografada = decriptoMensagem(mensagem_criptografada_global, d, n)

        Label(screenDescriptografia, text="Descriptografado", font="ariel", fg="white", bg="#ed3833").place(x=10, y=0)
        textDecripto = Text(screenDescriptografia, font="Verdana", bg="white", relief=GROOVE, wrap=WORD, bd=0)
        textDecripto.place(x=10, y=40, width=380, height=150)

        textDecripto.insert(END, mensagem_descriptografada)

    ## Parte GUI
    screen = Tk()
    screen.geometry("400x400")
    screen.title("Aps")

    Label(text="Informe a frase: ", font=("Ariel", 12), fg="black").place(x=12, y=12)
    repFrase = Text(font="Verdana", bg="white", relief=GROOVE, wrap=WORD, bd=0)
    repFrase.place(x=12, y=50, width=375, height=100)

    Label(text="Informe a senha: ", font=("Ariel", 12), fg="black").place(x=12, y=160)
    key = StringVar()
    Entry(textvariable=key, width=355, bd=0, font=("Ariel", 12), show="*").place(x=20, y=200)

    Button(text="Criptografar", height=2, width=25, bg="#00bd56", fg="white", bd=0, command=Criptografar).place(x=10, y=250)
    Button(text="Descriptografiar", height=2, width=25, bg="#ed3833", fg="white", bd=0, command=Descriptografar).place(x=200, y=250)

    Button(text="Resetar", height=2, width=53, bg="#1089ff", fg="white", bd=0, command=Reset).place(x=10, y=300)

    screen.mainloop()

main()
