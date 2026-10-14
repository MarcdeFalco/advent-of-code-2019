"""Advent of Code 2019, jour 1.

Partie 1 : on applique la formule masse // 3 - 2 à chaque module.
Partie 2 : on réapplique la formule au carburant ajouté, tant que le
résultat reste positif (boucle while, nombre de tours logarithmique).
"""


def carburant(masse):
    return masse // 3 - 2


def carburant_total(masse):
    """Carburant du module, plus le carburant de ce carburant, etc."""
    total = 0
    dernier = masse
    while carburant(dernier) > 0:
        dernier = carburant(dernier)
        total += dernier
    return total


def partie1(masses):
    return sum(carburant(m) for m in masses)


def partie2(masses):
    return sum(carburant_total(m) for m in masses)


masses = [int(ligne) for ligne in open('input.txt').read().split()]
print('Partie 1 :', partie1(masses))
print('Partie 2 :', partie2(masses))
