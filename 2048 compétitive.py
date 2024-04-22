import tkinter as tk
import random
import numpy as np 



#Fonction d'affichage de la grille.
def la_grille():
    décalage = 5 #Décalage pour centrer la grille
    for ligne in range(4):
        for colonne in range(4):
            x0, y0 = colonne * taille_de_une_case + décalage, ligne * taille_de_une_case + décalage
            x1, y1 = x0 + taille_de_une_case, y0 + taille_de_une_case
            Plateau.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")

dictionnaire_des_couleurs = {0: "white", 2: "lightyellow", 4: "moccasin", 8: "coral", 16: "tomato", 32: "yellow", 64: "lawngreen", 128: "lime", \
            256: "limegreen", 512: "cyan", 1024: "deepskyblue", 2048: "royalblue", 4096: "mediumslateblue", 8192: "slateblue", \
                16384: "blueviolet", 32768: "mediumorchid", 65536: "violet", 131072: "black"}

def affichage():
    global m
    décalage = 5 #Décalage pour centrer la grille
    for ligne in range(4):
        for colonne in range(4):
            x0, y0 = colonne * taille_de_une_case + décalage, ligne * taille_de_une_case + décalage
            x1, y1 = x0 + taille_de_une_case, y0 + taille_de_une_case
            valeur = m[ligne][colonne]
            #Récupération de la couleur correspondant à la valeur.
            couleur = dictionnaire_des_couleurs.get(valeur)
            #Affiche une couleur en fonction de la valeur.
            Plateau.create_rectangle(x0, y0, x1, y1, fill=couleur, outline="black")
            #Affiche les valeurs des tuiles dans les cellules.
            if valeur != 0:
                Plateau.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(valeur), font=('Helvetica', 20))



#Fonction de score.
def perdu():
    global m
    for ligne in range(4):
        for colonne in range(3):
            if m[ligne][colonne] == m[ligne][colonne + 1] or m[ligne][colonne] == 0:
                return False
    for colonne in range(4):
        for ligne in range(3):
            if m[ligne][colonne] == m[ligne + 1][colonne] or m[ligne][colonne] == 0:
                return False
    
    return True

def score():
    score_total = 0
    for ligne in range(4):
        for colonne in range(4):
            score_total += m[ligne][colonne]  #Ajoute la valeur de chaque case au score total.
    
    #Met à jour le texte du label avec le score total.
    Score_joueur.config(text="Votre score est :" + str(score_total), font=("Bahnschrift", 10))

    if score_total == 262140:
        Score_joueur.config(text="Vous avez gagné.", font=("Bahnschrift", 15))
    elif perdu():
        Score_joueur.config(text="Vous avez perdu.", font=("Bahnschrift", 15))



#Fonction lié au placement de tuile.
def compteur_des_additions_possibles(m):
    compteur = 0
    m_temp = [ligne[:] for ligne in m]  #Copie de la grille

    # On décale tous les éléments vers la gauche pour éliminer les zéros.
    for _ in range(2):
        for ligne in range(4):
            for colonne in range(3):
                if m_temp[ligne][colonne] == 0:
                    for k in range(colonne, 3):
                        m_temp[ligne][k] = m_temp[ligne][k + 1]
                    m_temp[ligne][3] = 0
    # On fusionne les éléments égaux adjacents.
    for ligne in range(4):
        for colonne in range(3):
            if m_temp[ligne][colonne] == m_temp[ligne][colonne + 1] : 
                compteur += 1

    # On décale tous les éléments vers la droite pour éliminer les zéros.
    for _ in range(2):
        for ligne in range(4):
            for colonne in range(3, 0, -1):
                if m_temp[ligne][colonne] == 0:
                    for k in range(colonne, 0, -1):
                        m_temp[ligne][k] = m_temp[ligne][k - 1]
                    m_temp[ligne][0] = 0
    # On fusionne les éléments égaux adjacents.
    for ligne in range(4):
        for colonne in range(3, 0, -1):
            if m_temp[ligne][colonne] == m_temp[ligne][colonne - 1]:
                compteur += 1

    # On décale tous les éléments vers le haut pour éliminer les zéros.
    for _ in range(2):
        for colonne in range(4):
            for ligne in range(3):
                if m_temp[ligne][colonne] == 0:
                    for k in range(ligne, 3):
                        m_temp[k][colonne] = m_temp[k + 1][colonne]
                    m_temp[3][colonne] = 0
    # On fusionne les éléments égaux adjacents.
    for colonne in range(4):
        for ligne in range(3):
            if m_temp[ligne][colonne] == m_temp[ligne + 1][colonne]:
                compteur += 1

    # On décale tous les éléments vers le bas pour éliminer les zéros.
    for _ in range(2):
        for colonne in range(4):
            for ligne in range(3, 0, -1):
                if m_temp[ligne][colonne] == 0:
                    for k in range(ligne, 0, -1):
                        m_temp[k][colonne] = m_temp[k - 1][colonne]
                    m_temp[0][colonne] = 0
    # On fusionne les éléments égaux adjacents.
    for colonne in range(4):
        for ligne in range(3, 0, -1):
            if m_temp[ligne][colonne] == m_temp[ligne - 1][colonne]:
                compteur += 1
    
    return compteur

def placer_une_tuile():
    global m
    tuiles_vides = [(ligne, colonne) for ligne in range(4) for colonne in range(4) if m[ligne][colonne] == 0]
    if tuiles_vides:
        dict_des_compteurs = {}
        for (ligne, colonne) in tuiles_vides:
            for valeur in [2, 4]: #Tester les deux valeurs possibles : 2 et 4
                test_des_additions = [ligne[:] for ligne in m] #Copie temporaire de la grille
                test_des_additions[ligne][colonne] = valeur #Placer une tuile de valeur 2 ou 4
                compteur = compteur_des_additions_possibles(test_des_additions)
                dict_des_compteurs[(ligne, colonne, valeur)] = compteur

        #Trouver le compteur minimum
        min_compteur = min(dict_des_compteurs.values())
        #Sélectionner aléatoirement un couple avec le compteur minimum
        couples_min_compteur = [couple for couple, compteur in dict_des_compteurs.items() if compteur == min_compteur]
        choix_final = random.choice(couples_min_compteur)
        ligne, colonne, valeur = choix_final
        #Placer une tuile de valeur 2 ou 4
        m[ligne][colonne] = valeur 



#Fonction des mouvements.
def gauche():
    global m
    for ligne in range(4):
        #On décale tous les éléments vers la gauche pour éliminer les zéros.
        for _ in range(2):
            for colonne in range(3):
                if m[ligne][colonne] == 0:
                    for k in range(colonne, 3):
                        m[ligne][k] = m[ligne][k + 1]
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
        #On décale tout les élements vers la droite pour éliminer les zéros.
        for _ in range(2):
            for colonne in range(3, 0, -1):
                if m[ligne][colonne] == 0:
                    for k in range(colonne, 0, -1):
                        m[ligne][k] = m[ligne][k - 1]
                    m[ligne][0] = 0
        #On fusionne les éléments égaux adjacents.
        for colonne in range(3, 0, -1):
            if m[ligne][colonne] == m[ligne][colonne - 1]:
                m[ligne][colonne] *= 2
                m[ligne][colonne - 1] = 0
        #On décale à nouveau tous les éléments vers la droite pour combler les trous.
        for _ in range(2):
            for colonne in range(3, 0, -1):
                if m[ligne][colonne] == 0:
                    for k in range(colonne, 0, -1):
                        m[ligne][k] = m[ligne][k - 1]
                    m[ligne][0] = 0

    #On place une nouvelle tuile, puis on affiche la grille mise à jour et on actualise le score.
    placer_une_tuile()
    affichage()
    score()

    return m

def haut():
    global m
    for colonne in range(4):
        #On décale tous les éléments vers le haut pour éliminer les zéros.
        for _ in range(2):
            for ligne in range(3):
                if m[ligne][colonne] == 0:
                    for k in range(ligne, 3):
                        m[k][colonne] = m[k + 1][colonne]
                    m[3][colonne] = 0
        #On fusionne les éléments égaux adjacents.
        for ligne in range(3):
            if m[ligne][colonne] == m[ligne + 1][colonne]:
                m[ligne][colonne] *= 2
                m[ligne + 1][colonne] = 0
        #On décale à nouveau tous les éléments vers le haut pour combler les trous.
        for _ in range(2):
            for ligne in range(3):
                if m[ligne][colonne] == 0:
                    for k in range(ligne, 3):
                        m[k][colonne] = m[k + 1][colonne]
                    m[3][colonne] = 0

    #On place une nouvelle tuile, puis on affiche la grille mise à jour et on actualise le score.
    placer_une_tuile()
    affichage()
    score()

    return m

def bas():
    global m
    for colonne in range(4):
        #On décale tout les élements vers le bas pour éliminer les zéros.
        for _ in range(2):
            for ligne in range(3, 0, -1):
                if m[ligne][colonne] == 0:
                    for k in range(ligne, 0, -1):
                        m[k][colonne] = m[k - 1][colonne]
                    m[0][colonne] = 0
        #On fusionne les éléments égaux adjacents.
        for ligne in range(3, 0, -1):
            if m[ligne][colonne] == m[ligne - 1][colonne]:
                m[ligne][colonne] *= 2
                m[ligne - 1][colonne] = 0
        #On décale à nouveau tous les éléments vers le bas pour combler les trous.
        for _ in range(2):
            for ligne in range(3, 0, -1):
                if m[ligne][colonne] == 0:
                    for k in range(ligne, 0, -1):
                        m[k][colonne] = m[k - 1][colonne]
                    m[0][colonne] = 0

    #On place une nouvelle tuile, puis on affiche la grille mise à jour et on actualise le score.
    placer_une_tuile()
    affichage()
    score()

    return m



#Fonction de démarrage et d'arrêt des parties.
def play():
    global m
    m = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    #m = [[4,8,16,32],[64,128,256,512],[1024,2048,4096,8192],[16384,32768,65536,131072]]
    #m = [[2,4,4,2],[0,0,0,2],[0,0,2,0],[2,0,0,2]]
    
    placer_une_tuile()
    placer_une_tuile()
    affichage()
    score()

def save():
    with open("sauvegarde jeu 2048.txt", "w") as fichier:
        for ligne in range(4):
            for colonne in range(4):
                fichier.write(str(m[ligne][colonne]) + '\n')

def load():
    global m
    m = np.zeros((4, 4), dtype=int)
    with open("sauvegarde jeu 2048.txt", 'r') as fichier:
        liste_des_valeurs = []
        for ligne in fichier:
            liste_des_valeurs.append(int(ligne.strip()))  # ##Convertit la chaîne en entier et supprime le caractère de saut de ligne

    indice = 0
    for ligne in range(4):
        for colonne in range(4):
            m[ligne][colonne] = liste_des_valeurs[indice]
            indice += 1

    affichage()
    score()

def exit():
   fenetre.destroy()



#Fonctions auxiliaires de notre fenêtre.
fenetre = tk.Tk()
fenetre.title("Projet 2048 Compétitive")
fenetre.configure(background = "beige")

#Création du plateau et de la grille.
taille_du_plateau = 400
taille_de_une_case = taille_du_plateau // 4

Plateau = tk.Canvas(fenetre, width = taille_du_plateau + 4, height = taille_du_plateau + 4, borderwidth = 2, relief = "groove")
Plateau.grid(column = 0, row = 3, columnspan = 3, rowspan = 3, padx = 10, pady = 10)
            
la_grille()  #Appel de la fonction pour dessiner la grille après la création du canevas.

#Création des Widgets.
Button_Play = tk.Button(fenetre, text = "Play", font = ("Bahnschrift", 10), command = play)
Button_Exit = tk.Button(fenetre, text = "Exit", font = ("Bahnschrift", 10), command = exit)
Button_Save = tk.Button(fenetre, text = "Save", font = ("Bahnschrift", 10), command = save)
Button_Load = tk.Button(fenetre, text = "Load", font = ("Bahnschrift", 10), command = load)

Button_Left = tk.Button(fenetre, text = "Left", font = ("Bahnschrift", 10), command = gauche)
Button_Right = tk.Button(fenetre, text = "Right", font = ("Bahnschrift", 10), command = droite)
Button_Up = tk.Button(fenetre, text = "Up", font = ("Bahnschrift", 10), command = haut)
Button_Down = tk.Button(fenetre, text = "Down", font = ("Bahnschrift", 10), command = bas)

Titre = tk.Label(fenetre, background = "beige",text = '2048', font = ("Bahnschrift", 25))
Score_joueur = tk.Label(fenetre,background = "beige", text = "Score : 0", font = ("Bahnschrift", 10))

#Positionnement des Widgets.
Button_Play.grid(column = 0, row = 0, padx = 10, pady = 5, sticky = "ew")
Button_Exit.grid(column = 2, row = 0, padx = 10, pady = 5, sticky = "ew")
Button_Save.grid(column = 0, row = 1, padx = 10, pady = 5, sticky = "ew")
Button_Load.grid(column = 2, row = 1, padx = 10, pady = 5, sticky = "ew")

Button_Left.grid(column = 0, row = 7, padx = 10, pady = 5, sticky = "ew")
Button_Right.grid(column = 2, row = 7, padx = 10, pady = 5, sticky = "ew")
Button_Up.grid(column = 1, row = 6, padx = 10, pady = 5, sticky = "ew")
Button_Down.grid(column = 1, row = 8, padx = 10, pady = 5, sticky = "ew")

Titre.grid(column = 1, row = 0, padx = 10, pady = 10, sticky = "ew")
Score_joueur.grid(column = 1, row = 1, padx = 10, pady = 10, sticky = "ew")

#Lancement de la boucle de notre fenétre.
fenetre.mainloop()