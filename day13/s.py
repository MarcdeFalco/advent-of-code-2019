"""Advent of Code 2019, jour 13 : casse-briques joué par un programme Intcode.

Les sorties arrivent par triplets (x, y, type de case) ; le triplet
d'abscisse -1 donne le score.
Partie 1 : sans pièce insérée, nombre de briques (type 2) à l'écran.
Partie 2 : avec deux pièces (code[0] = 2). À chaque lecture, le joystick est
orienté vers l'abscisse de la balle : cette stratégie gloutonne suffit à ne
jamais la perdre ; la réponse est le score final.
"""
from collections import defaultdict

BRIQUE, RAQUETTE, BALLE = 2, 3, 4


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


def jouer(programme):
    """Fait tourner le jeu ; renvoie l'écran final et le score."""
    ecran = defaultdict(int)
    raquette, balle = (0, 0), (0, 0)
    score = 0

    def joystick():
        # on suit la balle : -1 à gauche, 0 neutre, 1 à droite
        if balle[0] == raquette[0]:
            return 0
        return 1 if balle[0] > raquette[0] else -1

    sortie = []
    triplet = []
    machine = Programme(programme, joystick, sortie)
    while not machine.arretee:
        machine.etape()
        if sortie:
            triplet.append(sortie.pop())
            if len(triplet) == 3:
                x, y, t = triplet
                if (x, y) == (-1, 0):
                    score = t
                else:
                    ecran[x, y] = t
                    if t == RAQUETTE:
                        raquette = (x, y)
                    if t == BALLE:
                        balle = (x, y)
                triplet = []
    return ecran, score


def partie1(programme):
    ecran, _ = jouer(programme)
    return sum(1 for t in ecran.values() if t == BRIQUE)


def partie2(programme):
    programme = programme[:]
    programme[0] = 2  # deux pièces : partie gratuite
    _, score = jouer(programme)
    return score


programme = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', partie1(programme))
print('Partie 2 :', partie2(programme))
