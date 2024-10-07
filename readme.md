TKinter é um modulo nativo do python que permite criar GUI (Graphic User Interface) diretamente do python.

Olha a doc. desse módulo é bem interresante: https://www.devmedia.com.br/tkinter-interfaces-graficas-em-python/33956

estrutura básica: 
    def main_screen():
        screen = Tk()
        screen.geometry("400x400")
        screen.title("Aps")

        screen.mainloop()
        
    main_screen()