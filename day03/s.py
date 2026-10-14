"""Advent of Code 2019, jour 3.

Chaque fil est stocké comme la liste de ses sommets (un point à chaque
changement de direction), pas case par case. On teste toutes les paires
(segment du fil 1, segment du fil 2) pour trouver les croisements.
Partie 1 : croisement le plus proche de l'origine (distance de Manhattan).
Partie 2 : pour chaque croisement, on longe chaque fil en ajoutant la
longueur des segments jusqu'à celui qui contient le croisement.
"""

DIRECTIONS = {'U': (0, 1), 'L': (-1, 0), 'R': (1, 0), 'D': (0, -1)}


def lire_fils(texte):
    fils = []
    for ligne in texte.split('\n'):
        sommets = [(0, 0)]
        x, y = 0, 0
        for instruction in ligne.split(','):
            dx, dy = DIRECTIONS[instruction[0]]
            n = int(instruction[1:])
            x += n * dx
            y += n * dy
            sommets.append((x, y))
        fils.append(sommets)
    return fils


def intervalle(u, v):
    return min(u, v), max(u, v)


def croisement(a, b, c, d):
    """Point de croisement du segment [a, b] avec [c, d], ou None.

    Seul le cas d'un segment vertical et d'un segment horizontal est traité.
    """
    if a[0] == b[0] and c[1] == d[1]:  # [a, b] vertical, [c, d] horizontal
        xmin, xmax = intervalle(c[0], d[0])
        ymin, ymax = intervalle(a[1], b[1])
        if xmin <= a[0] <= xmax and ymin <= c[1] <= ymax:
            return (a[0], c[1])
    if a[1] == b[1] and c[0] == d[0]:  # [a, b] horizontal, [c, d] vertical
        ymin, ymax = intervalle(c[1], d[1])
        xmin, xmax = intervalle(a[0], b[0])
        if ymin <= a[1] <= ymax and xmin <= c[0] <= xmax:
            return (c[0], a[1])
    return None


def croisements(fils):
    fil1, fil2 = fils
    points = []
    for i in range(len(fil1) - 1):
        for j in range(len(fil2) - 1):
            p = croisement(fil1[i], fil1[i + 1], fil2[j], fil2[j + 1])
            if p is not None:
                points.append(p)
    if (0, 0) in points:
        points.remove((0, 0))
    return points


def longueur_jusqu_a(fil, x, y):
    """Nombre de pas le long du fil avant d'atteindre (x, y)."""
    pas = 0
    for i in range(len(fil) - 1):
        a, b = fil[i], fil[i + 1]
        xmin, xmax = intervalle(a[0], b[0])
        ymin, ymax = intervalle(a[1], b[1])
        if a[0] == b[0] == x and ymin <= y <= ymax:
            return pas + abs(y - a[1])
        if a[1] == b[1] == y and xmin <= x <= xmax:
            return pas + abs(x - a[0])
        pas += (xmax - xmin) + (ymax - ymin)
    return pas


def partie1(fils):
    return min(abs(x) + abs(y) for x, y in croisements(fils))


def partie2(fils):
    return min(sum(longueur_jusqu_a(fil, x, y) for fil in fils)
               for x, y in croisements(fils))


fils = lire_fils(open('input.txt').read().strip())
print('Partie 1 :', partie1(fils))
print('Partie 2 :', partie2(fils))
