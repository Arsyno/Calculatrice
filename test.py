from tkinter import *

fenetre = Tk()
fenetre.geometry("600x600")
fenetre.title("CALCULATRICE")
fenetre.resizable(False,False)

frame = Frame(fenetre,pady=150)
frame.pack()

resultat = Entry(frame, border=2,)
resultat.grid(row=0, columnspan=4, pady=15)
buttons = [
    '7','8','9','*',
    '4','5','6','+',
    '1','2','3','-',
    '.','0','=','/'
]

r = 1
c = 0

for b in buttons :
    Button(frame,text=b , padx=20,).grid(row=r, column= c, padx=5, pady= 5,)
    print(Button["text"])
    c += 1
    if c == 4 :
        c = 0
        r += 1

fenetre.mainloop()