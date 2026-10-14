"""Advent of Code 2019, jour 4.

Force brute : on parcourt tous les entiers de l'intervalle et on teste
chacun sur sa chaîne décimale (chiffres croissants, présence d'un doublon).
Partie 2 : le doublon ne doit pas faire partie d'un groupe plus long ; on
regarde les voisins de la paire, avec des cas particuliers aux deux bords.
"""


def croissant(s):
    return all(s[i] <= s[i + 1] for i in range(5))


def valide1(n):
    s = str(n)
    if len(s) != 6:
        return False
    if not any(s[i] == s[i + 1] for i in range(5)):
        return False
    return croissant(s)


def valide2(n):
    s = str(n)
    if len(s) != 6:
        return False
    doublon = False
    for i in range(5):
        if s[i] == s[i + 1]:
            # la paire (i, i+1) ne doit pas se prolonger à gauche ni à droite
            if i == 0 and s[i + 2] != s[i]:
                doublon = True
            if i == 4 and s[i - 1] != s[i]:
                doublon = True
            if 0 < i < 4 and s[i - 1] != s[i] and s[i + 2] != s[i]:
                doublon = True
    if not doublon:
        return False
    return croissant(s)


def partie1(bas, haut):
    return sum(1 for n in range(bas, haut + 1) if valide1(n))


def partie2(bas, haut):
    return sum(1 for n in range(bas, haut + 1) if valide2(n))


bas, haut = map(int, open('input.txt').read().strip().split('-'))
print('Partie 1 :', partie1(bas, haut))
print('Partie 2 :', partie2(bas, haut))
