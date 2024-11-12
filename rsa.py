from tkinter import *
from tkinter import ttk
import random 
from math import gcd
from sympy import randprime
from datetime import datetime


def modular_inverse(e, phi_n):
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
    global key_cript_history 
    key_cript_history = []

    def salvar_historico(mensagem_criptografada, e, d, n):
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key_cript_history.append({
            "mensagem_criptografada": mensagem_criptografada,
            "data": data_atual,
            "e": e,
            "d": d,
            "n": n
        })

    def gerar_numeros_primos(el):
        return randprime(2**(el-1), 2**el)

    def Reset():
        key.set("")
        gerar_password.set("")
        key_cript_history.clear()
        repFrase.delete(1.0, END)

    def GerarSenha():
        screenPassword = Toplevel(screen)
        screenPassword.title("Definição de senha")
        screenPassword.geometry("400x250")
        screenPassword.configure(bg="#5e6065")

        Label(screenPassword, text="Informe a sua nova senha: ", font="ariel", fg="white", bg="#5e6065").place(x=10, y=0)
        Entry(screenPassword, textvariable=gerar_password, width=30, bd=0, font=("Ariel", 12), show="*").place(x=10, y=40)
        Button(screenPassword, text="Confirmar", command=screenPassword.destroy).place(x=10, y=80)

        return gerar_password

    def Criptografar():
        passworkKey = key.get()
        passwordRes = gerar_password.get()
        mensagem = repFrase.get(1.0, END).strip()

        if(mensagem != ""):
            if(passwordRes != ""):
                if passworkKey == passwordRes:
                    screenCriptografia = Toplevel(screen)
                    screenCriptografia.title("Criptografado")
                    screenCriptografia.geometry("500x250")
                    screenCriptografia.configure(bg="#6c8389")


                    # Gerar nova chave RSA para cada criptografia
                    p = gerar_numeros_primos(2048)
                    q = gerar_numeros_primos(2048)
                    n = p * q
                    phi_n = (p - 1) * (q - 1)
                    e = 65537
                    d = modular_inverse(e, phi_n)

                    def criptoMessage(message, n, e):
                        mensagem = int.from_bytes(message.encode('utf-8'), byteorder='big')
                        mensagemCriptografada = pow(mensagem, e, n)
                        return mensagemCriptografada

                    criptografada = criptoMessage(mensagem, n, e)
                    salvar_historico(criptografada, e, d, n)

                    Label(screenCriptografia, text="Criptografado", font="ariel", fg="white", bg="#6c8389").place(x=10, y=0)
                    textCripto = Text(screenCriptografia, font="Verdana", bg="white", relief=GROOVE, wrap=WORD, bd=0)
                    textCripto.place(x=10, y=40, width=475, height=175)

                    textCripto.insert(END, criptografada)
                    
                else:
                    Erro("As senhas não coincidem!")
            else:
                Erro("Não foi possivel encontrar a sua senha... Por favor, clique no primeiro botão de 'Redefinir Senha'!")
        else:
            Erro("Não foi possivel encontrar a sua mensagem... Por favor, informe uma mensagem p/ criptografar!")

    def VerHistorico():
        screenHistorico = Toplevel(screen)
        screenHistorico.title("Histórico de Chaves")
        screenHistorico.geometry("600x400")
        screenHistorico.configure(bg="#d3d3d3")
        
        Label(screenHistorico, text="Histórico de Chaves Utilizadas", font=("Ariel", 14), bg="#d3d3d3").pack(pady=10)
        
        columns = ("data", "chave")
        tree = ttk.Treeview(screenHistorico, columns=columns, show="headings")
        tree.heading("data", text="Data")
        tree.heading("chave", text="Mensagem Criptografada")

        tree.column("data", width=200, anchor="center")
        tree.column("chave", width=380, anchor="center")
        
        for chave in key_cript_history:
            data = chave["data"]
            mensagem_cripto = str(chave['mensagem_criptografada'])
            # Exibir as primeiras e últimas 4 letras da mensagem com reticências no meio
            if len(mensagem_cripto) > 8:
                mensagem_cripto_exibida = mensagem_cripto[:4] + "..." + mensagem_cripto[-4:]
            else:
                mensagem_cripto_exibida = mensagem_cripto

            tree.insert("", "end", values=(data, mensagem_cripto_exibida))

        tree.pack(fill=BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(screenHistorico, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        def Descriptografar():
            selected_item = tree.selection()  # Pega o item selecionado no Treeview
            if selected_item:
                item = tree.item(selected_item)
                mensagem_cripto_abreviada = item["values"][1]
                
                # Recuperar a mensagem completa a partir do histórico
                mensagem_cripto_completa = next(
                    (ch['mensagem_criptografada'] for ch in key_cript_history 
                    if mensagem_cripto_abreviada.startswith(str(ch['mensagem_criptografada'])[:4]) 
                    and mensagem_cripto_abreviada.endswith(str(ch['mensagem_criptografada'])[-4:])), 
                    None
                )
                
                if mensagem_cripto_completa:
                    data = next((ch for ch in key_cript_history if ch["mensagem_criptografada"] == mensagem_cripto_completa), None)
                    if data:
                        screenDescriptografia = Toplevel(screen)
                        screenDescriptografia.title("Descriptografado")
                        screenDescriptografia.geometry("500x250")
                        screenDescriptografia.configure(bg="#749594")

                        def decriptoMensagem(mensagem, d, n):
                            mensagemDescriptografada = pow(mensagem, d, n)
                            mensagem_bytes = mensagemDescriptografada.to_bytes((mensagemDescriptografada.bit_length() + 7) // 8, byteorder='big')
                            return mensagem_bytes.decode("utf-8")

                        mensagem_descriptografada = decriptoMensagem(data["mensagem_criptografada"], data["d"], data["n"])

                        Label(screenDescriptografia, text="Descriptografado", font="ariel", fg="white", bg="#749594").place(x=10, y=0)
                        textDecripto = Text(screenDescriptografia, font="Verdana", bg="white", relief=GROOVE, wrap=WORD, bd=0)
                        textDecripto.place(x=10, y=40, width=450, height=150)

                        textDecripto.insert(END, mensagem_descriptografada)
                    else:
                        Erro("Chave não encontrada para a descriptografia")
        
        Button(screenHistorico, text="Descriptografar Selecionado", command=Descriptografar).pack(pady=10)

    def Erro(text_err):
        screenError = Toplevel(screen)
        screenError.title("Erro!")
        screenError.geometry("800x250")
        screenError.configure(bg="#9e1a0b")

        Label(screenError, text="Opss... Ocorreu um erro!", font="ariel", fg="black", bg="#c27a72").place(x=10, y=0)
        Label(screenError, text=text_err, font="ariel", fg="black", bg="#c27a72").place(x=10, y=20)
        Button(screenError, text="Voltar", height=2, width=20, command=screenError.destroy).place(x=10, y=80)

    screen = Tk()
    screen.geometry("800x400")
    screen.title("Aps")
    key = StringVar()
    gerar_password = StringVar()

    Label(text="Informe a frase: ", font=("Ariel", 12), fg="black").place(x=12, y=12)
    repFrase = Text(font="Verdana", bg="white", relief=GROOVE, wrap=WORD, bd=0)
    repFrase.place(x=10, y=50, width=725, height=100)
    Label(text="Informe a senha: ", font=("Ariel", 12), fg="black").place(x=10, y=160)

    Entry(textvariable=key, width=725, bd=0, font=("Ariel", 12), show="*").place(x=10, y=200)

    Button(text="Redefinir senha", height=2, width=15, bg="#5e6065", fg="white", bd=0, command=GerarSenha).place(x=125, y=250)
    Button(text="Histórico/Descriptografar", height=2, width=20, bg="#667178", fg="white", bd=0, command=VerHistorico).place(x=250, y=250)
    Button(text="Criptografar", height=2, width=20, bg="#36454f", fg="white", bd=0, command=Criptografar).place(x=400, y=250)
    Button(text="Restar", height=2, width=15, bg="#36454f", fg="white", bd=0, command=Reset).place(x=565, y=250)

    screen.mainloop()

main()
