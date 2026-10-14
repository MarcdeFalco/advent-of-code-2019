"""Advent of Code 2019, jour 12 : quatre lunes en interaction.

Partie 1 : simulation directe de 1000 pas, puis énergie totale.
Partie 2 : les trois axes évoluent indépendamment. Pour chaque axe, on
simule en rangeant les états (positions et vitesses sur cet axe) dans un
ensemble, ce qui détecte la première répétition ; une liste garde l'ordre
pour retrouver l'indice du premier passage. Le système complet revient à un
état déjà vu au bout du PPCM des périodes des trois axes.
"""
import re
from itertools import product


class Lune:
    def __init__(self, position):
        self.position = list(position)
        self.vitesse = [0, 0, 0]

    def attraction(self, autre):
        for i in range(3):
            if autre.position[i] > self.position[i]:
                self.vitesse[i] += 1
            if autre.position[i] < self.position[i]:
                self.vitesse[i] -= 1

    def deplacer(self):
        for i in range(3):
            self.position[i] += self.vitesse[i]

    def energie(self):
        potentielle = sum(abs(v) for v in self.position)
        cinetique = sum(abs(v) for v in self.vitesse)
        return potentielle * cinetique


def pgcd(a, b):
    if b == 0:
        return a
    return pgcd(b, a % b)


def ppcm(a, b):
    return (a * b) // pgcd(a, b)


def ppcm_liste(liste):
    p = liste[0]
    for a in liste[1:]:
        p = ppcm(p, a)
    return p


def partie1(positions, nb_pas=1000):
    lunes = [Lune(p) for p in positions]
    for _ in range(nb_pas):
        for a, b in product(lunes, repeat=2):
            if a != b:
                a.attraction(b)
        for lune in lunes:
            lune.deplacer()
    return sum(lune.energie() for lune in lunes)


def periode_axe(coords):
    """Longueur du cycle des états (positions, vitesses) sur un axe."""
    c = list(coords)
    v = [0] * 4
    etats = [(tuple(c), (0, 0, 0, 0))]
    deja_vus = set(etats)
    n = 0
    while True:
        for a, b in product(range(4), repeat=2):
            if a != b:
                if c[b] > c[a]:
                    v[a] += 1
                if c[b] < c[a]:
                    v[a] -= 1
        for a in range(4):
            c[a] += v[a]
        etat = (tuple(c), tuple(v))
        if etat in deja_vus:
            premier = etats.index(etat)
            return n - premier + 1
        etats.append(etat)
        deja_vus.add(etat)
        n += 1


def partie2(positions):
    return ppcm_liste([periode_axe([p[axe] for p in positions])
                       for axe in range(3)])


positions = [tuple(map(int, re.findall(r'-?\d+', ligne)))
             for ligne in open('input.txt').read().strip().split('\n')]
print('Partie 1 :', partie1(positions))
print('Partie 2 :', partie2(positions))
