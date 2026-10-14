"""Advent of Code 2019, jour 20 : labyrinthe à téléporteurs, puis à niveaux.

L'analyse de la carte repère les étiquettes de deux lettres et la case
libre adjacente (`entrees` : case -> étiquette, `cases` : étiquette ->
cases).
Partie 1 : parcours en largeur où un téléporteur ajoute une arête vers
l'autre case de même étiquette.
Partie 2 : on réduit d'abord le graphe en calculant par BFS la distance
entre portails, en distinguant le côté extérieur ou intérieur ; puis
Dijkstra sur les états (portail, côté, niveau) : un passage par l'extérieur
fait remonter d'un niveau et est interdit au niveau 0. La sortie ZZ est
traitée comme un téléporteur vers le niveau -1, d'où le « - 1 » final.
Remarque : un état n'est ajouté au tas qu'à sa première découverte, même si
un chemin plus court y mène ensuite ; ce n'est pas l'algorithme de Dijkstra
correct en général, mais la réponse est juste sur cette entrée.
"""
from collections import defaultdict, deque
from heapq import heappop, heappush
from itertools import product

VOISINS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def analyser(carte):
    largeur, hauteur = len(carte[0]), len(carte)
    seconde_lettre = set()
    entrees = {}
    cases = defaultdict(list)

    def ajouter(position, etiquette):
        entrees[position] = etiquette
        cases[etiquette].append(position)

    for x, y in product(range(largeur), range(hauteur)):
        if not carte[y][x].isalpha() or (x, y) in seconde_lettre:
            continue
        # étiquette horizontale
        if x < largeur - 1 and carte[y][x + 1].isalpha():
            seconde_lettre.add((x + 1, y))
            etiquette = carte[y][x] + carte[y][x + 1]
            if x > 0 and carte[y][x - 1] == '.':
                ajouter((x - 1, y), etiquette)
            else:
                ajouter((x + 2, y), etiquette)
        # étiquette verticale
        if y < hauteur - 1 and carte[y + 1][x].isalpha():
            seconde_lettre.add((x, y + 1))
            etiquette = carte[y][x] + carte[y + 1][x]
            if y > 0 and carte[y - 1][x] == '.':
                ajouter((x, y - 1), etiquette)
            else:
                ajouter((x, y + 2), etiquette)
    return entrees, cases


def partie1(carte):
    entrees, cases = analyser(carte)
    x, y = cases['AA'][0]
    a_visiter = deque([(0, x, y)])
    vu = set()
    while a_visiter:
        n, x, y = a_visiter.popleft()
        if (x, y) in vu:
            continue
        vu.add((x, y))
        if (x, y) in entrees:
            etiquette = entrees[x, y]
            if etiquette == 'ZZ':
                return n
            # autre case de même étiquette (AA n'en a qu'une)
            autre = next((c for c in cases[etiquette] if c != (x, y)), (x, y))
            a_visiter.append((n + 1, *autre))
        for dx, dy in VOISINS:
            if carte[y + dy][x + dx] == '.':
                a_visiter.append((n + 1, x + dx, y + dy))


def partie2(carte):
    entrees, _ = analyser(carte)
    largeur, hauteur = len(carte[0]), len(carte)

    def exterieur(x, y):
        return x in [2, largeur - 3] or y in [2, hauteur - 3]

    # graphe réduit : (étiquette, côté) -> [(étiquette, distance, côté)]
    distances = defaultdict(list)
    for x0, y0 in entrees:
        a_visiter = deque([(0, x0, y0)])
        vu = set()
        while a_visiter:
            n, x, y = a_visiter.popleft()
            if (x, y) in vu:
                continue
            vu.add((x, y))
            if ((x, y) in entrees and (x, y) != (x0, y0)
                    and entrees[x, y] != 'AA'):
                distances[entrees[x0, y0], exterieur(x0, y0)].append(
                    (entrees[x, y], n, exterieur(x, y)))
            for dx, dy in VOISINS:
                if carte[y + dy][x + dx] == '.':
                    a_visiter.append((n + 1, x + dx, y + dy))

    # Dijkstra sur (étiquette, côté où l'on se trouve, niveau)
    a_visiter = [(0, 'AA', True, 0)]
    decouverts = set()
    traites = set()
    while a_visiter:
        n, etiquette, cote, niveau = heappop(a_visiter)
        if (etiquette, cote, niveau) in traites:
            continue
        traites.add((etiquette, cote, niveau))
        if (etiquette, cote, niveau) == ('ZZ', False, -1):
            return n - 1  # le dernier « saut » vers le niveau -1 ne compte pas
        for etiquette2, d, cote2 in distances[etiquette, cote]:
            if cote2 and niveau == 0 and etiquette2 != 'ZZ':
                continue  # pas de sortie par l'extérieur au niveau 0
            niveau2 = niveau - 1 if cote2 else niveau + 1
            # on traverse le portail : on arrive de l'autre côté
            etat = (etiquette2, not cote2, niveau2)
            if etat not in decouverts:
                decouverts.add(etat)
                heappush(a_visiter, (n + d + 1, *etat))


# pas de strip : les espaces en début de ligne comptent
carte = open('input.txt').read().split('\n')[:-1]
print('Partie 1 :', partie1(carte))
print('Partie 2 :', partie2(carte))
