"""Advent of Code 2019, jour 17 : grille ASCII produite par Intcode.

Partie 1 : la sortie de la machine est une image en caractères, découpée en
lignes ; une case est un croisement si elle et ses quatre voisines sont des
échafaudages (#). Réponse : somme des produits x * y des croisements.
Partie 2 : il faut fournir l'itinéraire du robot découpé en un programme
principal et trois sous-programmes A, B, C. Cette compression est faite à
la main pour l'entrée (chaînes écrites en dur ci-dessous) ; elle est envoyée en codes ASCII, dans une liste renversée pour que `pop`
la lise dans l'ordre. La dernière sortie (> 255) est la réponse.
"""
from collections import defaultdict

# Compression faite à la main pour l'entrée.
ROUTINE = 'A,B,B,C,C,A,A,B,B,C'
A = 'L,12,R,4,R,4'
B = 'R,12,R,4,L,12'
C = 'R,12,R,4,L,6,L,8,L,8'


class Programme:
    def __init__(self, code):
        self.code = defaultdict(int)
        for i, v in enumerate(code):
            self.code[i] = v
        self.pc = 0
        self.arretee = False
        self.base = 0

    def etape(self, entree):
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
            p[adresse(1)] = entree.pop()
            self.pc += 2
        elif op == 4:
            v = param(1)
            self.pc += 2
            return v
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


def partie1(programme):
    robot = Programme(programme)
    texte = ''
    while not robot.arretee:
        c = robot.etape([])
        if c is not None:
            texte += chr(c)
    grille = texte.split('\n')[:-2]  # la sortie finit par deux sauts de ligne
    largeur, hauteur = len(grille[0]), len(grille)
    total = 0
    for y in range(1, hauteur - 1):
        for x in range(1, largeur - 1):
            if all(grille[y + dy][x + dx] == '#' for (dx, dy) in
                   [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]):
                total += x * y
    return total


def partie2(programme):
    commandes = '\n'.join([ROUTINE, A, B, C, 'n']) + '\n'  # 'n' : pas de vidéo
    entree = list(map(ord, commandes))
    entree.reverse()
    programme = programme[:]
    programme[0] = 2  # réveil du robot
    robot = Programme(programme)
    derniere = None
    while not robot.arretee:
        c = robot.etape(entree)
        if c is not None:
            derniere = c
    return derniere


programme = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', partie1(programme))
print('Partie 2 :', partie2(programme))
