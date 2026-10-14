"""Advent of Code 2019, jour 10 : visibilité entre astéroïdes, puis balayage.

Pour deux astéroïdes, on divise le vecteur qui les relie par le PGCD de ses
coordonnées : on obtient le pas élémentaire, et les points entiers
intermédiaires sont ses multiples. L'autre astéroïde est visible si aucun de
ces points n'est occupé.
Partie 1 : astéroïde qui en voit le plus (force brute sur toutes les paires).
Partie 2 : à chaque tir, on recalcule les astéroïdes visibles, on les trie
par angle (atan2, en degrés) et on prend le premier dans le sens horaire
après l'angle du tir précédent ; réponse : 100 * x + y du 200e détruit.
"""
from itertools import product
from math import atan2, pi


def pgcd(a, b):
    if b == 0:
        return a
    return pgcd(b, a % b)


def lire_asteroides(texte):
    carte = texte.split('\n')
    largeur, hauteur = len(carte[0]), len(carte)
    return [(x, y) for x, y in product(range(largeur), range(hauteur))
            if carte[y][x] == '#']


def visibles(asteroides, x, y):
    """Astéroïdes de la liste visibles depuis (x, y)."""
    vus = []
    for x2, y2 in asteroides:
        if (x, y) == (x2, y2):
            continue
        dx, dy = x2 - x, y2 - y
        d = pgcd(abs(dx), abs(dy))
        pas_x, pas_y = dx // d, dy // d
        cache = any((x + k * pas_x, y + k * pas_y) in asteroides
                    for k in range(1, d))
        if not cache:
            vus.append((x2, y2))
    return vus


def meilleure_station(asteroides):
    return max(asteroides, key=lambda a: len(visibles(asteroides, *a)))


def tirs(asteroides, station):
    """Engendre les astéroïdes détruits, dans l'ordre des tirs."""
    restants = list(asteroides)
    restants.remove(station)
    x, y = station
    dernier_angle = 90 + 0.0001  # juste avant la verticale vers le haut
    while restants:
        angles = []
        for x2, y2 in visibles(restants, x, y):
            a = atan2(y - y2, x2 - x) * 360 / (2 * pi)
            # on tourne dans le sens horaire, donc vers les angles
            # décroissants : ce qui est au-dessus du dernier angle passe
            # au tour suivant
            if a >= dernier_angle:
                a -= 360
            angles.append((a, x2, y2))
        angles.sort()
        dernier_angle, x2, y2 = angles[-1]
        if dernier_angle <= -180:
            dernier_angle += 360
        restants.remove((x2, y2))
        yield x2, y2


def partie1(asteroides):
    station = meilleure_station(asteroides)
    return len(visibles(asteroides, *station))


def partie2(asteroides):
    station = meilleure_station(asteroides)
    for i, (x, y) in enumerate(tirs(asteroides, station), 1):
        if i == 200:
            return 100 * x + y


if __name__ == '__main__':
    asteroides = lire_asteroides(open('input.txt').read().strip())
    print('Partie 1 :', partie1(asteroides))
    print('Partie 2 :', partie2(asteroides))
