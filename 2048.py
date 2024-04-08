import tkinter as tk
import random
import numpy as np 



def placer_une_tuile():
    global m
    tuiles_vides = [(ligne, colonne) for ligne in range(4) for colonne in range(4) if m[ligne][colonne] == 0]
    if tuiles_vides:
        ligne, colonne = random.choice(tuiles_vides)
        m[ligne][colonne] = random.choices([2, 4], weights=[0.9, 0.1])[0]

dictionnaire_des_couleurs = {0: "white", 2: "lightyellow", 4: "moccasin", 8: "coral", 16: "tomato", 32: "yellow", 64: "lawngreen", 128: "lime", \
            256: "limegreen", 512: "cyan", 1024: "deepskyblue", 2048: "royalblue", 4096: "mediumslateblue", 8192: "slateblue", \
                16384: "blueviolet", 32768: "mediumorchid", 65536: "violet", 131072: "black"}

def affichage():
    global m
    decalage = 5  #Décalage pour centrer la grille
    for ligne in range(4):
        for colonne in range(4):
            x0, y0 = colonne * taille_de_une_case + decalage, ligne * taille_de_une_case + decalage
            x1, y1 = x0 + taille_de_une_case, y0 + taille_de_une_case
            valeur = m[ligne][colonne]
            #Récupération de la couleur correspondant à la valeur.
            couleur = dictionnaire_des_couleurs.get(valeur)
            #Affiche une couleur en fonction de la valeur.
            Canva.create_rectangle(x0, y0, x1, y1, fill=couleur, outline="black")
            #Affiche les valeurs des tuiles dans les cellules.
            if valeur != 0:
                Canva.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(valeur), font=('Helvetica', 20))

def score():
    score_total = 0
    for ligne in range(4):
        for colonne in range(4):
            score_total += m[ligne][colonne]  #Ajoute la valeur de chaque case au score total.
    
    #Met à jour le texte du label avec le score total.
    Score_joueur.config(text="Votre score est :" + str(score_total), font=("Bahnschrift", 10))

def play():
    global m
    m = np.zeros((4, 4), dtype=int)
    #m = [[2,4,8,16],[32,64,128,256],[512,1024,2048,4096],[8192,16384,131072]]
    #m = [[2,4,4,2],[0,0,0,2],[0,0,2,0],[2,0,0,2]]
    
    placer_une_tuile()
    placer_une_tuile()
    affichage()
    score()

def gauche():
    global m
    for ligne in range(4):
        #On décale tous les éléments vers la gauche pour éliminer les zéros.
        for _ in range(2):
            for colonne in range(3):
                if m[ligne][colonne] == 0:
                    for i in range(colonne, 3):
                        m[ligne][i] = m[ligne][i + 1]
                    m[ligne][3] = 0
        #On fusionne les éléments égaux adjacents.
        for colonne in range(3):
            if m[ligne][colonne] == m[ligne][colonne + 1]:
                m[ligne][colonne] *= 2
                m[ligne][colonne + 1] = 0
        #On décale à nouveau tous les éléments vers la gauche pour combler les trous.
        for _ in range(2):
            for colonne in range(3):
                if m[ligne][colonne] == 0:
                    for k in range(colonne, 3):
                        m[ligne][k] = m[ligne][k + 1]
                    m[ligne][3] = 0

    #On place une nouvelle tuile, puis on affiche la grille mise à jour et on actualise le score.
    placer_une_tuile()
    affichage()
    score()

    return m

def droite():
    global m
    for ligne in range(4):
        #On décale tout les élements vers la droite qu'il n'y est plus de 0.
        for _ in range(2):
            for colonne in range(3, 0, -1):
                if m[ligne][colonne] == 0:
                    for k in range(colonne, 0, -1):
                        m[ligne][k] = m[ligne][k - 1]
                    m[ligne][0] = 0
        #On ajoute les éléments égaux deux a deux.
        for colonne in range(3, 0, -1):
            if m[ligne][colonne] == m[ligne][colonne - 1]:
                m[ligne][colonne] *= 2
                m[ligne][colonne - 1] = 0
        #En ajoutant les éléments égaux deux a deux cela peut crée des 0 donc on redecale les éléments.
        for _ in range(2):
            for colonne in range(3, 0, -1):
                if m[ligne][colonne] == 0:
                    for k in range(colonne, 0, -1):
                        m[ligne][k] = m[ligne][k - 1]
                    m[ligne][0] = 0

    #On ajoute une tuile, puis modifie l'affichage des case enfin nous actualisont le score.
    placer_une_tuile()
    affichage()
    score()

    return m

def exit():
   fenetre.destroy()



#Fonctions auxiliaires
fenetre = tk.Tk()
fenetre.title("Projet 2048")
fenetre.configure(background="beige")

#Création du canevas et de la grille.
taille_du_canva = 400
taille_de_une_case = taille_du_canva // 4

Canva = tk.Canvas(fenetre, width=taille_du_canva+4, height=taille_du_canva+4, borderwidth=2, relief="groove")
Canva.grid(column=0, row=3, columnspan=3, rowspan=3, padx=10, pady=10)

def la_grille():
    decalage = 5  #Décalage pour centrer la grille
    for i in range(5):
        Canva.create_line(decalage, i * taille_de_une_case + decalage, taille_du_canva + decalage, i * taille_de_une_case + decalage, fill="black")
        Canva.create_line(i * taille_de_une_case + decalage, decalage, i * taille_de_une_case + decalage, taille_du_canva + decalage, fill="black")

la_grille()  #Appel de la fonction pour dessiner la grille après la création du canevas.

#Création des Widgets
Button_Play = tk.Button(fenetre, text="Play", font=("Bahnschrift", 10), command=play)
Button_Exit = tk.Button(fenetre, text="Exit", font=("Bahnschrift", 10), command=exit)
Button_Save = tk.Button(fenetre, text="Save", font=("Bahnschrift", 10))
Button_Load = tk.Button(fenetre, text="Load", font=("Bahnschrift", 10))

Button_Left = tk.Button(fenetre, text="Left", font=("Bahnschrift", 10), command=gauche)
Button_Right = tk.Button(fenetre, text="Right", font=("Bahnschrift", 10), command=droite)
Button_Up = tk.Button(fenetre, text="Up", font=("Bahnschrift", 10))
Button_Down = tk.Button(fenetre, text="Down", font=("Bahnschrift", 10))

Titre = tk.Label(fenetre, background="beige",text='2048', font=("Bahnschrift", 25))
Score_joueur = tk.Label(fenetre,background="beige", text="Score : 0", font=("Bahnschrift", 10))

#Positionnement des Widgets
Button_Play.grid(column=0, row=0, padx=10, pady=5, sticky="ew")
Button_Exit.grid(column=2, row=0, padx=10, pady=5, sticky="ew")
Button_Save.grid(column=0, row=1, padx=10, pady=5, sticky="ew")
Button_Load.grid(column=2, row=1, padx=10, pady=5, sticky="ew")

Button_Left.grid(column=0, row=7, padx=10, pady=5, sticky="ew")
Button_Right.grid(column=2, row=7, padx=10, pady=5, sticky="ew")
Button_Up.grid(column=1, row=6, padx=10, pady=5, sticky="ew")
Button_Down.grid(column=1, row=8, padx=10, pady=5, sticky="ew")

Titre.grid(column=1, row=0, padx=10, pady=10, sticky="ew")
Score_joueur.grid(column=1, row=1, padx=10, pady=10, sticky="ew")

#Lancement de la boucle
fenetre.mainloop()