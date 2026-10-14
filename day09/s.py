"""Advent of Code 2019, jour 9 : Intcode complet.

Ajouts au jour 7 : le mode relatif (registre `base`, instruction 9) et une
mémoire non bornée, `code` étant un defaultdict(int) (mémoire creuse
initialisée à 0). `adresse` calcule l'adresse d'écriture : un paramètre de
destination n'est jamais en mode immédiat.
Le programme fourni teste l'interprète, puis calcule la réponse.
Partie 1 : entrée 1 ; partie 2 : entrée 2.
"""
from collections import defaultdict, deque


class Programme:
    def __init__(self, code, entree, sortie):
        self.code = defaultdict(int)
        for i, v in enumerate(code):
            self.code[i] = v
        self.pc = 0
        self.entree = entree
        self.sortie = sortie
        self.bloquee = False
        self.arretee = False
        self.base = 0

    def etape(self):
        p = self.code
        pc = self.pc
        op = p[pc] % 100
        chiffres = '%05d' % p[pc]
        # 0 = position, 1 = immédiat, 2 = relatif
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
            if len(self.entree) > 0:
                p[adresse(1)] = self.entree.popleft()
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

    def en_marche(self):
        return not (self.bloquee or self.arretee)


def executer(programme, valeur):
    sorties = deque()
    machine = Programme(programme, deque([valeur]), sorties)
    while machine.en_marche():
        machine.etape()
    # en cas d'erreur de l'interprète, le programme de test sort plusieurs
    # valeurs ; sinon une seule, la réponse
    return list(sorties)


def partie1(programme):
    return executer(programme, 1)


def partie2(programme):
    return executer(programme, 2)


programme = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', *partie1(programme))
print('Partie 2 :', *partie2(programme))
