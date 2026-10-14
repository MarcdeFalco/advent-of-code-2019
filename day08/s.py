"""Advent of Code 2019, jour 8 : image découpée en calques.

L'image est découpée en tranches de largeur * hauteur caractères.
Partie 1 : sur le calque qui contient le moins de 0, nombre de 1 fois
nombre de 2.
Partie 2 : on part du calque du fond et on remonte vers le premier en
écrasant les pixels non transparents (2 = transparent) ; le message se lit
sur l'affichage.
"""

LARGEUR, HAUTEUR = 25, 6
TAILLE = LARGEUR * HAUTEUR


def calques(texte):
    return [texte[i:i + TAILLE] for i in range(0, len(texte), TAILLE)]


def partie1(liste):
    calque = min(liste, key=lambda c: c.count('0'))
    return calque.count('1') * calque.count('2')


def partie2(liste):
    image = list(liste[-1])
    for calque in reversed(liste[:-1]):
        for i in range(TAILLE):
            if calque[i] != '2':
                image[i] = calque[i]
    symbole = {'0': '.', '1': '#', '2': ' '}
    lignes = [image[LARGEUR * y:LARGEUR * (y + 1)] for y in range(HAUTEUR)]
    return '\n'.join(''.join(symbole[c] for c in ligne) for ligne in lignes)


liste = calques(open('input.txt').read().strip())
print('Partie 1 :', partie1(liste))
print('Partie 2 :')
print(partie2(liste))
