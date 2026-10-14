"""Advent of Code 2019, jour 6.

Les orbites forment un arbre enraciné en COM, stocké en listes d'enfants.
Partie 1 : somme des profondeurs, par une récursion qui passe la profondeur
courante.
Partie 2 : chemin depuis la racine jusqu'à YOU et jusqu'à SAN (parcours en
profondeur) ; on saute leur plus long préfixe commun, qui mène au plus
proche ancêtre commun, et on additionne les longueurs restantes.
"""
from collections import defaultdict


def lire_arbre(texte):
    enfants = defaultdict(list)
    for ligne in texte.split('\n'):
        centre, satellite = ligne.split(')')
        enfants[centre].append(satellite)
    return enfants


def somme_profondeurs(enfants, v, profondeur):
    return profondeur + sum(somme_profondeurs(enfants, c, profondeur + 1)
                            for c in enfants[v])


def chemin(enfants, v, cible):
    """Liste des ancêtres de cible depuis v (cible exclue), ou None."""
    if v == cible:
        return []
    for c in enfants[v]:
        suite = chemin(enfants, c, cible)
        if suite is not None:
            return [v] + suite
    return None


def partie1(enfants):
    return somme_profondeurs(enfants, 'COM', 0)


def partie2(enfants):
    chemin1 = chemin(enfants, 'COM', 'YOU')
    chemin2 = chemin(enfants, 'COM', 'SAN')
    i = 0
    while chemin1[i] == chemin2[i]:
        i += 1
    return len(chemin1[i:]) + len(chemin2[i:])


enfants = lire_arbre(open('input.txt').read().strip())
print('Partie 1 :', partie1(enfants))
print('Partie 2 :', partie2(enfants))
