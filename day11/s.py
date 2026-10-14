"""Advent of Code 2019, jour 11 : robot peintre piloté par Intcode.

La coque est un defaultdict(bool) indexé par les coordonnées, donc non
bornée (True = blanc). L'instruction de lecture d'Intcode renvoie
directement la couleur de la case du robot ; les sorties alternent couleur
à peindre et rotation (booléen `peindre`). La direction est un indice
modulo 4 dans DIRECTIONS.
Partie 1 : départ sur une case noire, nombre de cases peintes au moins une
fois. Partie 2 : départ sur une case blanche, le dessin obtenu se lit à
l'écran.
"""
from collections import defaultdict

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # haut, droite, bas, gauche


class Programme:
    def __init__(self, code, lire, sortie):
        self.code = defaultdict(int)
        for i, v in enumerate(code):
            self.code[i] = v
        self.pc = 0
        self.lire = lire
        self.sortie = sortie
        self.arretee = False
        self.base = 0

    def etape(self):
        p = self.code
        pc = self.pc
        op = p[pc] % 100
        chiffres = '%05d' % p[pc]
        modes = list(map(int, (chiffres[2], chiffres[1], chiffres[0])))

        def param(k):
            if modes[k - 1] == 1:
                return p[pc + k]
            elif modes[k - 1] == 2:
                return p[p[pc + k] + self.base]
            return p[p[pc + k]]

        def adresse(k):
            if modes[k - 1] == 2:
                return p[pc + k] + self.base
            return p[pc + k]

        if op in [1, 2]:
            v1, v2 = param(1), param(2)
            p[adresse(3)] = v1 + v2 if op == 1 else v1 * v2
            self.pc += 4
        elif op == 3:
            p[adresse(1)] = self.lire()
            self.pc += 2
        elif op == 4:
            self.sortie.append(param(1))
            self.pc += 2
        elif op == 5:
            if param(1) != 0:
                self.pc = param(2)
            else:
                self.pc += 3
        elif op == 6:
            if param(1) == 0:
                self.pc = param(2)
            else:
                self.pc += 3
        elif op == 7:
            p[adresse(3)] = 1 if param(1) < param(2) else 0
            self.pc += 4
        elif op == 8:
            p[adresse(3)] = 1 if param(1) == param(2) else 0
            self.pc += 4
        elif op == 9:
            self.base += param(1)
            self.pc += 2
        elif op == 99:
            self.arretee = True


def peindre_coque(programme, case_depart_blanche):
    coque = defaultdict(bool)
    coque[(0, 0)] = case_depart_blanche
    peintes = set()
    x, y, d = 0, 0, 0
    sortie = []
    robot = Programme(programme, lambda: 1 if coque[(x, y)] else 0, sortie)
    peindre = True  # la prochaine sortie est-elle une couleur ?
    while not robot.arretee:
        robot.etape()
        if sortie:
            v = sortie.pop()
            if peindre:
                coque[(x, y)] = v == 1
                peintes.add((x, y))
            else:
                d = (d + 1) % 4 if v == 1 else (d + 3) % 4
                dx, dy = DIRECTIONS[d]
                x += dx
                y += dy
            peindre = not peindre
    return coque, peintes


def partie1(programme):
    _, peintes = peindre_coque(programme, False)
    return len(peintes)


def partie2(programme):
    coque, _ = peindre_coque(programme, True)
    blanches = [p for p in coque if coque[p]]
    xmin = min(x for x, _ in blanches)
    xmax = max(x for x, _ in blanches)
    ymin = min(y for _, y in blanches)
    ymax = max(y for _, y in blanches)
    # l'axe des y est orienté vers le haut : on affiche de ymax à ymin
    return '\n'.join(''.join('#' if coque[(x, y)] else ' '
                             for x in range(xmin, xmax + 1))
                     for y in range(ymax, ymin - 1, -1))


programme = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', partie1(programme))
print('Partie 2 :')
print(partie2(programme))
