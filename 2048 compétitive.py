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
            Plateau.create_rectangle((x0, y0), (x1, y1), fill="white", outline="black")

dictionnaire_des_couleurs = {0: "#FFFFFF", 2: "#FFEBF0", 4: "#FFD1DC", 8: "#FFB6C1", 16: "#FFC0CB", \
                             32: "#FFE4E1", 64: "#FFDAB9", 128: "#FFCC99", \
                             256: "#FFE699", 512: "#FFFF99", 1024: "#D8FFD1", 4096: "#AFFFA1", \
                             8192: "#A0E687", 16384: "#C5E5F0", 32768: "#ADD8E6", 65536: "#B0E0FF", \
                             131072: "#90B4F4" }

# Rose pastel, Rose clair, Rose bonbon, Saumon clair, Rose clair (répété), Pêche, Vert menthe ,Vert clair
# Vert pastel, Vert citron, Teinte vert pastel supplémentaire,Teinte vert pastel supplémentaire (répété)
# Bleu clair, Bleu ciel pâle, Bleu acier, Bleu acier moyen, Bleu acier très clair

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
            Plateau.create_rectangle((x0, y0), (x1, y1), fill=couleur, outline="black")
            #Affiche les valeurs des tuiles dans les cellules.
            if valeur != 0:
                Plateau.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(valeur), font=("Cambria", 20))



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
            score_total += m[ligne][colonne] #Ajoute la valeur de chaque case au score total.
    
    #Met à jour le texte du label avec le score total.
    Score_joueur.config(text="Votre score est :" + str(score_total), font=("Cambria", 12))

    if score_total == 262140:
        Score_joueur.config(text="Vous avez gagné.", font=("Cambria", 12))
    elif perdu():
        Score_joueur.config(text="Vous avez perdu.", font=("Cambria", 12))
 


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
        tuples_min_compteur = [tuple for tuple, compteur in dict_des_compteurs.items() if compteur == min_compteur]
        choix_final = random.choice(tuples_min_compteur)
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


def flèche_direction(event):
    if event.keysym == "Right":  #Touche droite
        droite()
    if event.keysym == "Left":   #Touche gauche
        gauche()
    if event.keysym == "Up":     #Touche haut
        haut()
    if event.keysym == "Down":   #Touche bas
        bas()



#Fonction de démarrage et d'arrêt des parties.
def play():
    global m
    m = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    #m = [[4,8,16,32],[64,128,256,512],[1024,2048,4096,8192],[16384,32768,65536,131072]]
    
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
Button_Play = tk.Button(fenetre, text = "Play", font = ("Cambria", 11), command = play)
Button_Exit = tk.Button(fenetre, text = "Exit", font = ("Cambria", 11), command = exit)
Button_Save = tk.Button(fenetre, text = "Save", font = ("Cambria", 11), command = save)
Button_Load = tk.Button(fenetre, text = "Load", font = ("Cambria", 11), command = load)

Button_Left = tk.Button(fenetre, text = "Left", font = ("Cambria", 11), command = gauche)
Button_Right = tk.Button(fenetre, text = "Right", font = ("Cambria", 11), command = droite)
Button_Up = tk.Button(fenetre, text = "Up", font = ("Cambria", 11), command = haut)
Button_Down = tk.Button(fenetre, text = "Down", font = ("Cambria", 11), command = bas)

Titre = tk.Label(fenetre, background = "beige",text = '2048', font = ("Cambria", 25))
Score_joueur = tk.Label(fenetre,background = "beige", text = "Score : 0", font = ("Cambria", 12))

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

#Associe les touches directionnelles a la fonction qui gére les mouvements.
fenetre.bind("<Right>", flèche_direction)
fenetre.bind("<Left>", flèche_direction)
fenetre.bind("<Up>", flèche_direction)
fenetre.bind("<Down>", flèche_direction)

#Lancement de la boucle de notre fenétre.
fenetre.mainloop()