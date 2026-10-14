"""Advent of Code 2019, jour 25 : jeu d'aventure textuel exécuté par Intcode.

L'interprète est branché sur l'entrée standard, caractère par caractère :
on joue à la main (commandes north, south, take ..., drop ..., inv).
Pour l'épreuve finale, il faut porter le bon sous-ensemble d'objets ; le
script generate.py produit les commandes qui les essaient tous, à
rediriger vers ce programme :  python3 generate.py | python3 s.py
"""
import sys
from collections import defaultdict


class Programme:
    def __init__(self, code):
        self.code = defaultdict(int)
        for i, v in enumerate(code):
            self.code[i] = v
        self.pc = 0
        self.arretee = False
        self.bloquee = False
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
            self.bloquee = True  # attend un caractère, fourni par debloquer
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

    def debloquer(self, v):
        """Termine la lecture en attente avec la valeur v."""
        p = self.code
        chiffres = '%05d' % p[self.pc]
        adresse = p[self.pc + 1]
        if chiffres[2] == '2':  # mode relatif
            adresse += self.base
        p[adresse] = v
        self.pc += 2
        self.bloquee = False


def jouer(programme):
    machine = Programme(programme)
    while not machine.arretee:
        v = machine.etape()
        if v is not None:
            sys.stdout.write(chr(v) if v < 256 else str(v))
        if machine.bloquee:
            c = sys.stdin.read(1)
            if c == '':  # fin de l'entrée
                break
            machine.debloquer(ord(c))


programme = list(map(int, open('input.txt').read().strip().split(',')))
jouer(programme)
