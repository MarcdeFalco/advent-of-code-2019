"""Advent of Code 2019, jour 21 : programme booléen pour un robot sauteur.

Le robot exécute un petit programme (« springscript ») fait de portes ET,
OU, NON sur ses capteurs (A, B, C, D... : y a-t-il du sol à 1, 2, 3, 4...
cases ?) et deux registres T et J ; il saute quand J vaut vrai à la fin.
Écrire ce programme revient à trouver une formule propositionnelle qui
décide quand sauter. Les programmes sont écrits en dur et envoyés en codes
ASCII. Si le robot survit, la dernière sortie (> 255) est la
réponse ; sinon la machine affiche la chute.
Partie 1 (WALK) : sauter si A est un trou, ou si B ou C en est un et que D
(case d'arrivée) est du sol.
Partie 2 (RUN) : même formule, en exigeant en plus du sol en H (pour
pouvoir ressauter dès l'arrivée) quand le trou n'est pas immédiat.
"""
from collections import defaultdict

# J = non A ou (non (B et C) et D) ; WALK ne voit que A à D
PROGRAMME_PARTIE1 = """NOT A J
OR B T
AND C T
NOT T T
AND D T
OR T J
WALK
"""

# J = non A ou (non (B et C) et D et H) ; RUN voit jusqu'à I
PROGRAMME_PARTIE2 = """NOT A J
OR B T
AND C T
NOT T T
AND D T
AND H T
OR T J
RUN
"""


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


def executer_springscript(programme, springscript):
    entree = list(map(ord, springscript))
    entree.reverse()  # lu avec pop
    robot = Programme(programme)
    sortie = []
    while not robot.arretee:
        c = robot.etape(entree)
        if c is not None:
            sortie.append(c)
    if sortie[-1] < 256:  # le robot est tombé : on affiche la scène
        return ''.join(map(chr, sortie))
    return sortie[-1]


def partie1(programme):
    return executer_springscript(programme, PROGRAMME_PARTIE1)


def partie2(programme):
    return executer_springscript(programme, PROGRAMME_PARTIE2)


programme = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', partie1(programme))
print('Partie 2 :', partie2(programme))
