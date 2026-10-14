"""Advent of Code 2019, jour 15 : explorer un labyrinthe inconnu avec un robot.

`etape` renvoie la valeur produite par une sortie et `executer` fait tourner
la machine jusqu'à la prochaine sortie : la machine devient une fonction
qu'on appelle avec une entrée (un mouvement) ; `copie` duplique son état.
Partie 1 : parcours en largeur où chaque case découverte reçoit sa propre
copie de la machine (on explore plusieurs futurs en parallèle) ; la
distance de la case d'oxygène est la réponse.
Partie 2 : parcours en profondeur récursif avec une seule machine : après
chaque appel récursif, on ramène physiquement le robot par le mouvement
inverse, la pile d'appels suit donc le chemin réel. La carte connue, un
parcours en largeur depuis l'oxygène donne le temps de remplissage.
"""
from collections import defaultdict, deque

INCONNU, LIBRE, MUR, OXYGENE = 0, 1, 2, 3
DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # mouvements 1, 2, 3, 4
INVERSE = {1: 2, 2: 1, 3: 4, 4: 3}


class Programme:
    def __init__(self, code=None):
        self.code = defaultdict(int)
        if code is not None:
            for i, v in enumerate(code):
                self.code[i] = v
        self.pc = 0
        self.arretee = False
        self.base = 0

    def copie(self):
        q = Programme()
        q.code = self.code.copy()
        q.pc = self.pc
        q.arretee = self.arretee
        q.base = self.base
        return q

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

    def executer(self, entree):
        """Exécute jusqu'à la prochaine sortie et la renvoie."""
        while not self.arretee:
            v = self.etape(entree)
            if v is not None:
                return v


def partie1(programme):
    carte = defaultdict(int)
    a_visiter = deque([(0, 0, Programme(programme), 0, LIBRE)])
    while a_visiter:
        x, y, robot, n, t = a_visiter.popleft()
        if carte[x, y] != INCONNU:
            continue
        carte[x, y] = t
        if t == OXYGENE:
            return n
        for i, (dx, dy) in enumerate(DIRECTIONS):
            clone = robot.copie()
            reponse = clone.executer([i + 1])
            if reponse == 0:
                carte[x + dx, y + dy] = MUR
            else:
                a_visiter.append((x + dx, y + dy, clone, n + 1,
                                  LIBRE if reponse == 1 else OXYGENE))


def explorer(programme):
    """Carte complète par parcours en profondeur ; renvoie (carte, oxygène)."""
    carte = defaultdict(int)
    robot = Programme(programme)
    oxygene = None

    def dfs(x, y, est_oxygene=False):
        nonlocal oxygene
        if carte[x, y] != INCONNU:
            return
        if est_oxygene:
            oxygene = x, y
            carte[x, y] = OXYGENE
        else:
            carte[x, y] = LIBRE
        for i, (dx, dy) in enumerate(DIRECTIONS):
            reponse = robot.executer([i + 1])
            if reponse == 0:
                carte[x + dx, y + dy] = MUR
            else:
                dfs(x + dx, y + dy, reponse == 2)
                robot.executer([INVERSE[i + 1]])  # retour en arrière

    dfs(0, 0)
    return carte, oxygene


def partie2(programme):
    carte, (x, y) = explorer(programme)
    carte[x, y] = LIBRE
    a_visiter = deque([(0, x, y)])
    n = 0
    while a_visiter:
        n, x, y = a_visiter.popleft()
        if carte[x, y] != LIBRE:
            continue
        carte[x, y] = OXYGENE
        for dx, dy in DIRECTIONS:
            if carte[x + dx, y + dy] == LIBRE:
                a_visiter.append((n + 1, x + dx, y + dy))
    return n  # distance du dernier élément sorti de la file


programme = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', partie1(programme))
print('Partie 2 :', partie2(programme))
