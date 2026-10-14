"""Advent of Code 2019, jour 7 : amplificateurs Intcode en série.

L'interprète devient une classe dont la méthode `etape` exécute une seule
instruction : on peut donc suspendre une machine et la reprendre. Une
lecture sur une file d'entrée vide met la machine en attente (`bloquee`).
Cinq machines sont reliées par cinq files (la sortie de l'une est l'entrée
de la suivante, E reboucle sur A) ; on les fait tourner à tour de rôle
jusqu'à l'arrêt de toutes, et on essaie toutes les permutations de réglages.
Partie 1 : réglages 0 à 4 (chaque machine s'arrête après un passage) ;
partie 2 : réglages 5 à 9 (boucle de rétroaction).
"""
from collections import deque
from itertools import permutations


class Programme:
    def __init__(self, code, entree, sortie):
        self.code = code[:]
        self.pc = 0
        self.entree = entree
        self.sortie = sortie
        self.bloquee = False
        self.arretee = False

    def debloquer(self):
        """Termine une lecture en attente si une valeur est disponible."""
        if len(self.entree) > 0:
            self.code[self.code[self.pc + 1]] = self.entree.popleft()
            self.pc += 2
            self.bloquee = False

    def etape(self):
        if self.bloquee:
            return self.debloquer()
        p = self.code
        pc = self.pc
        op = p[pc] % 100
        chiffres = '%05d' % p[pc]
        modes = chiffres[2] == '1', chiffres[1] == '1', chiffres[0] == '1'

        def param(k):
            if modes[k - 1]:
                return p[pc + k]
            return p[p[pc + k]]

        if op in [1, 2]:
            v1, v2 = param(1), param(2)
            p[p[pc + 3]] = v1 + v2 if op == 1 else v1 * v2
            self.pc += 4
        elif op == 3:
            if len(self.entree) > 0:
                p[p[pc + 1]] = self.entree.popleft()
                self.pc += 2
            else:
                self.bloquee = True
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
            p[p[pc + 3]] = 1 if param(1) < param(2) else 0
            self.pc += 4
        elif op == 8:
            p[p[pc + 3]] = 1 if param(1) == param(2) else 0
            self.pc += 4
        elif op == 99:
            self.arretee = True


def signal(programme, reglages):
    a, b, c, d, e = reglages
    # entree_X_sortie_Y : file d'entrée de X et de sortie de Y
    entree_A_sortie_E = deque([a, 0])
    entree_B_sortie_A = deque([b])
    entree_C_sortie_B = deque([c])
    entree_D_sortie_C = deque([d])
    entree_E_sortie_D = deque([e])
    machines = [
        Programme(programme, entree_A_sortie_E, entree_B_sortie_A),
        Programme(programme, entree_B_sortie_A, entree_C_sortie_B),
        Programme(programme, entree_C_sortie_B, entree_D_sortie_C),
        Programme(programme, entree_D_sortie_C, entree_E_sortie_D),
        Programme(programme, entree_E_sortie_D, entree_A_sortie_E),
    ]
    while True:
        for m in machines:
            m.debloquer()
            while not m.bloquee and not m.arretee:
                m.etape()
        if all(m.arretee for m in machines):
            break
    # la dernière valeur produite par E reste dans la file d'entrée de A
    return entree_A_sortie_E[0]


def meilleur_signal(programme, phases):
    return max(signal(programme, reglages)
               for reglages in permutations(phases))


def partie1(programme):
    return meilleur_signal(programme, range(5))


def partie2(programme):
    return meilleur_signal(programme, range(5, 10))


programme = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', partie1(programme))
print('Partie 2 :', partie2(programme))
