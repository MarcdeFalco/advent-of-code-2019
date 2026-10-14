"""Advent of Code 2019, jour 18 : clés et portes d'un labyrinthe.

Seules comptent les clés : on change de graphe en deux étapes.
1. Graphe réduit : un parcours en largeur depuis chaque clé et chaque point
   de départ donne la distance vers chaque autre clé et l'ensemble des
   portes traversées, codé en masque de bits. On suppose qu'il n'y a qu'un
   chemin entre deux clés (labyrinthe en arbre), ce que vérifie l'assert.
2. Dijkstra sur les états (positions des robots, masque des clés
   possédées) : on peut aller vers une clé non possédée si toutes les
   portes du chemin sont ouvertes. Le dictionnaire `meilleur` garde la
   meilleure distance connue pour (positions, masque).
Partie 1 : un seul robot. Partie 2 : on découpe le centre de la carte en
quatre (comme l'indique l'énoncé) et l'état contient les quatre positions.
Cette modification de la carte est faite par `quatre_departs`.
"""
import heapq
from collections import defaultdict, deque


def analyser(carte):
    """Départs (caractères autres que . # et lettres), clés et portes."""
    departs = {}
    cles = {}
    portes = {}
    for x in range(len(carte[0])):
        for y in range(len(carte)):
            c = carte[y][x]
            if c in '.#':
                continue
            if c.islower():
                cles[c] = (x, y)
            elif c.isupper():
                portes[x, y] = c
            else:
                departs[c] = (x, y)
    return departs, cles, portes


def masque(lettres):
    m = 0
    for c in lettres:
        m |= 1 << (ord(c) - ord('a'))
    return m


def graphe_reduit(carte, departs, cles, portes):
    """voisins[source] = liste de (clé, distance, masque des portes)."""
    cle_en = {pos: c for c, pos in cles.items()}
    sources = dict(cles)
    sources.update(departs)
    voisins = defaultdict(list)
    for source, depart in sources.items():
        chemins = defaultdict(list)
        a_visiter = deque([(0, depart, [])])
        vu = set()
        while a_visiter:
            n, (x, y), portes_vues = a_visiter.popleft()
            if (x, y) in cle_en:
                k = cle_en[x, y]
                deja = any(p == portes_vues for _, p in chemins[k])
                if k != source and not deja:
                    chemins[k].append((n, portes_vues))
            if (x, y) in portes:
                portes_vues = portes_vues + [portes[x, y].lower()]
            if (x, y) in vu:
                continue
            vu.add((x, y))
            for dx, dy in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
                if carte[y + dy][x + dx] != '#':
                    a_visiter.append((n + 1, (x + dx, y + dy), portes_vues))
        for k in chemins:
            assert len(chemins[k]) <= 1
            for n, portes_vues in chemins[k]:
                voisins[source].append((k, n, masque(portes_vues)))
    return voisins


def plus_court(carte):
    departs, cles, portes = analyser(carte)
    voisins = graphe_reduit(carte, departs, cles, portes)
    complet = (1 << len(cles)) - 1
    depart = tuple(departs)
    a_visiter = [(0, depart, 0)]
    empiles = set()
    meilleur = {}
    while a_visiter:
        n, positions, possedees = heapq.heappop(a_visiter)
        if possedees == complet:
            return n
        for i, k in enumerate(positions):
            for cle, d, besoin in voisins[k]:
                bit = 1 << (ord(cle) - ord('a'))
                if bit & possedees != 0 or besoin & possedees != besoin:
                    continue
                nouvelles = possedees | bit
                suivantes = tuple(cle if j == i else positions[j]
                                  for j in range(len(positions)))
                if meilleur.get((suivantes, nouvelles), n + d) < n + d:
                    continue
                meilleur[suivantes, nouvelles] = n + d
                etat = (n + d, suivantes, nouvelles)
                if etat not in empiles:
                    empiles.add(etat)
                    heapq.heappush(a_visiter, etat)


def quatre_departs(carte):
    """Remplace le centre .@. par quatre départs séparés par des murs."""
    carte = [list(ligne) for ligne in carte]
    y = next(i for i, ligne in enumerate(carte) if '@' in ligne)
    x = carte[y].index('@')
    motif = ['<#>', '###', '{#}']
    for dy in range(3):
        for dx in range(3):
            carte[y - 1 + dy][x - 1 + dx] = motif[dy][dx]
    return [''.join(ligne) for ligne in carte]


def partie1(carte):
    return plus_court(carte)


def partie2(carte):
    return plus_court(quatre_departs(carte))


carte = open('input.txt').read().strip().split('\n')
print('Partie 1 :', partie1(carte))
print('Partie 2 :', partie2(carte))
