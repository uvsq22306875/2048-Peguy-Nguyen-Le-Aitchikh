import tkinter as tk
import random
import numpy as np 

#m = np.zeros((4, 4), dtype=int)

def exit():
    fenetre.destroy()

def placer_une_tuiles():
    global m
    tuile0 = [(i, j) for i in range(4) for j in range(4) if m[i][j] == 0]
    if tuile0:
        i, j = random.choice(tuile0)
        m[i][j] = random.choices([2, 4], weights=[0.9, 0.1])[0]

def play():
    global m
    m = np.zeros((4, 4), dtype=int)
    placer_une_tuiles()
    placer_une_tuiles()
    print(m)

# Fonctions auxiliaires 
fenetre = tk.Tk()
fenetre.title("Projet 2048")
fenetre.configure(background="beige")

# Création des Widgets
Button_Play = tk.Button(fenetre, text="Play", font=("Helvetica", 10), command= play)
Button_Exit = tk.Button(fenetre, text="Exit", font=("Helvetica", 10), command= exit)
Button_Save = tk.Button(fenetre, text="Save", font=("Helvetica", 10))
Button_Load = tk.Button(fenetre, text="Load", font=("Helvetica", 10))

Button_Left = tk.Button(fenetre, text="Left", font=("Helvetica", 10))
Button_Right = tk.Button(fenetre, text="Right", font=("Helvetica", 10))
Button_Up = tk.Button(fenetre, text="Up", font=("Helvetica", 10))
Button_Down = tk.Button(fenetre, text="Down", font=("Helvetica", 10))

canva_rouge = tk.Canvas(fenetre, width=400, height=400, borderwidth=2, relief="groove")

# Positionnement des Widgets
Button_Play.grid(column=0, row=0, padx=10, pady=5, sticky="ew")
Button_Exit.grid(column=2, row=0, padx=10, pady=5, sticky="ew")
Button_Save.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
Button_Load.grid(column=2, row=1, padx=10, pady=5, sticky="ew")

Button_Left.grid(column=0, row=7, padx=10, pady=5, sticky="ew")
Button_Right.grid(column=2, row=7, padx=10, pady=5, sticky="ew")
Button_Up.grid(column=1, row=6, padx=10, pady=5, sticky="ew")
Button_Down.grid(column=1, row=8, padx=10, pady=5, sticky="ew")

canva_rouge.grid(column=0, row=3, columnspan=3, rowspan=3, padx=10)

# Lancement de la boucle 
fenetre.mainloop()
