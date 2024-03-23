import tkinter as tk
import random
import numpy as np 

color = {0: "white", 2: "lightyellow", 4: "moccasin", 8: "coral", 16: "tomato", 32: "yellow", 64: "lawngreen", 128: "lime", \
            256: "limegreen", 512: "cyan", 1024: "deepskyblue", 2048: "royalblue", 4096: "mediumslateblue", 8192: "slateblue", \
                16384: "blueviolet", 32768: "mediumorchid", 65536: "violet", 131072: "black"}

def placer_une_tuile():
    global m
    tuiles_vides = [(i, j) for i in range(4) for j in range(4) if m[i][j] == 0]
    if tuiles_vides:
        i, j = random.choice(tuiles_vides)
        m[i][j] = random.choices([2, 4], weights=[0.9, 0.1])[0]

def affichage():
    global m
    for i in range(4):
        for j in range(4):
            x0, y0 = j * taille_dune_case, i * taille_dune_case
            x1, y1 = x0 + taille_dune_case, y0 + taille_dune_case
            valeur = m[i][j]
            couleur = color.get(valeur, "white")  #Récupération de la couleur correspondant à la valeur
            
            #Affiche une couleur en fonction de la valeur
            Canva.create_rectangle(x0, y0, x1, y1, fill=couleur, outline="black")
            #Affiche les valeurs des tuiles dans les cellules
            if valeur != 0:
                Canva.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(valeur), font=('Helvetica', 20))

def score():
    total_score = 0
    for i in range(4):
        for j in range(4):
            total_score += m[i][j]  # Ajoute la valeur de chaque case au score total
    
    # Met à jour le texte du label avec le score total
    Score_joueur.config(text="Votre score est :" + str(total_score))

def play():
    global m
    m = np.zeros((4, 4), dtype=int)
    #m = [[2,4,8,16],[32,64,128,256],[512,1024,2048,4096],[8192,16384,131072]]
    
    placer_une_tuile()
    placer_une_tuile()
    affichage()
    score()

def exit():
   fenetre.destroy()



#Fonctions auxiliaires
fenetre = tk.Tk()
fenetre.title("Projet 2048")
fenetre.configure(background="beige")

#Création du canevas et de la grille.
taille_du_canva = 400
taille_dune_case = taille_du_canva // 4
Canva = tk.Canvas(fenetre, width=taille_du_canva, height=taille_du_canva, borderwidth=2, relief="groove")

def la_grille():
    for i in range(5):
        Canva.create_line(0, i * taille_dune_case, taille_du_canva, i * taille_dune_case, fill="black")
        Canva.create_line(i * taille_dune_case, 0, i * taille_dune_case, taille_du_canva, fill="black")  

la_grille()  # Appel de la fonction pour dessiner la grille après la création du canevas

#Création des Widgets
Button_Play = tk.Button(fenetre, text="Play", font=("Bahnschrift", 10), command=play)
Button_Exit = tk.Button(fenetre, text="Exit", font=("Bahnschrift", 10), command=exit)
Button_Save = tk.Button(fenetre, text="Save", font=("Bahnschrift", 10))
Button_Load = tk.Button(fenetre, text="Load", font=("Bahnschrift", 10))

Button_Left = tk.Button(fenetre, text="Left", font=("Bahnschrift", 10))
Button_Right = tk.Button(fenetre, text="Right", font=("Bahnschrift", 10))
Button_Up = tk.Button(fenetre, text="Up", font=("Bahnschrift", 10))
Button_Down = tk.Button(fenetre, text="Down", font=("", 10))

Titre = tk.Label(fenetre, background="beige",text='2048', font=("Bahnschrift", 25))
Score_joueur = tk.Label(fenetre,background="beige", text="Score : 0")

#Positionnement des Widgets
Button_Play.grid(column=0, row=0, padx=10, pady=5, sticky="ew")
Button_Exit.grid(column=2, row=0, padx=10, pady=5, sticky="ew")
Button_Save.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
Button_Load.grid(column=2, row=1, padx=10, pady=5, sticky="ew")

Button_Left.grid(column=0, row=7, padx=10, pady=5, sticky="ew")
Button_Right.grid(column=2, row=7, padx=10, pady=5, sticky="ew")
Button_Up.grid(column=1, row=6, padx=10, pady=5, sticky="ew")
Button_Down.grid(column=1, row=8, padx=10, pady=5, sticky="ew")

Canva.grid(column=0, row=3, columnspan=3, rowspan=3, padx=10, pady=10)

Titre.grid(column=1, row=1, padx=10, pady=10, sticky="ew")
Score_joueur.grid(column=1, row=0, padx=10, pady=10, sticky="ew")

#Lancement de la boucle
fenetre.mainloop()