"""Advent of Code 2019, jour 23 : réseau de 50 machines Intcode.

Les cinquante machines tournent en tourniquet, une instruction chacune par
tour : c'est un ordonnancement coopératif simulé. Chaque machine a une file
d'entrée et une file de sortie ; dès que trois valeurs (adresse, x, y) sont
produites, le paquet est routé vers la file du destinataire. Une lecture
sur file vide renvoie -1 et marque la machine comme inactive.
Partie 1 : y du premier paquet envoyé à l'adresse 255.
Partie 2 : quand toutes les machines sont inactives depuis plus de 1000
tours (seuil empirique), on renvoie le dernier paquet reçu à l'adresse 255
vers la machine 0 ; réponse : première valeur de y renvoyée deux fois.
Remarques : le drapeau `inactive` n'est remis à faux que lorsqu'une
machine écrit, pas lorsqu'elle reçoit un paquet ; et l'arrêt teste si y a
déjà été envoyé à un moment quelconque, alors que l'énoncé parle de deux
envois consécutifs (les valeurs envoyées décroissent sur cette entrée,
les deux tests coïncident).
"""
from collections import defaultdict, deque


class Programme:
    def __init__(self, code):
        self.code = defaultdict(int)
        for i, v in enumerate(code):
            self.code[i] = v
        self.pc = 0
        self.arretee = False
        self.base = 0
        self.entree = deque()  # on ajoute à gauche, on lit à droite
        self.sortie = deque()
        self.inactive = False

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
        elif op == 3:  # lecture non bloquante
            if len(self.entree) == 0:
                p[adresse(1)] = -1
                self.inactive = True
            else:
                p[adresse(1)] = self.entree.pop()
            self.pc += 2
        elif op == 4:
            self.inactive = False
            self.sortie.appendleft(param(1))
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


def reseau(programme, partie):
    machines = [Programme(programme) for _ in range(50)]
    for i, m in enumerate(machines):
        m.entree.append(i)  # adresse de la machine
    nat = None
    envoyes = []
    tours_inactifs = 0
    while True:
        for m in machines:
            m.etape()
            if len(m.sortie) == 3:
                a, x, y = m.sortie.pop(), m.sortie.pop(), m.sortie.pop()
                if a == 255:
                    if partie == 1:
                        return y
                    nat = x, y
                else:
                    machines[a].entree.appendleft(x)
                    machines[a].entree.appendleft(y)

        if all(m.inactive for m in machines):
            tours_inactifs += 1
        else:
            tours_inactifs = 0

        if tours_inactifs > 1000:
            x, y = nat
            machines[0].entree.appendleft(x)
            machines[0].entree.appendleft(y)
            if y in envoyes:
                return y
            envoyes.append(y)
            tours_inactifs = 0


def partie1(programme):
    return reseau(programme, 1)


def partie2(programme):
    return reseau(programme, 2)


programme = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', partie1(programme))
print('Partie 2 :', partie2(programme))
