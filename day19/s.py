"""Advent of Code 2019, jour 19 : loger un carré dans un faisceau en cône.

Chaque sondage relance une machine neuve, qui répond 1 si le point (x, y)
est dans le faisceau. Plutôt que de sonder tout le plan, on avance colonne
par colonne en ne sondant qu'autour des bords trouvés à la colonne
précédente (les bords bougent peu). Les bornes de chaque colonne sont
rangées dans le dictionnaire `faisceau`. Dès qu'une colonne est assez haute,
on vérifie que les 99 colonnes précédentes couvrent les mêmes lignes.
Réponse : 10000 * x + y du coin supérieur gauche du carré.
Partie 1 : pas de solution.
"""
from collections import defaultdict

COTE = 100
X_DEPART = 20


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

    def executer(self, entree):
        """Exécute jusqu'à la prochaine sortie et la renvoie."""
        while not self.arretee:
            v = self.etape(entree)
            if v is not None:
                return v


def sonder(programme, x, y):
    return Programme(programme).executer([y, x])  # lu avec pop : x d'abord


def partie2(programme):
    # bornes du faisceau dans la colonne X_DEPART
    ymin, ymax = 30, 0
    for y in range(20):
        if sonder(programme, X_DEPART, y) == 1:
            ymin = min(ymin, y)
            ymax = max(ymax, y)
    faisceau = {}
    x = X_DEPART + 1
    while True:
        nouveau_min, nouveau_max = ymax + 1, ymin - 1
        autour_des_bords = (list(range(ymin - 3, ymin + 3))
                            + list(range(ymax - 3, ymax + 3)))
        for y in autour_des_bords:
            if sonder(programme, x, y) == 1:
                nouveau_min = min(nouveau_min, y)
                nouveau_max = max(nouveau_max, y)
        ymin, ymax = nouveau_min, nouveau_max
        faisceau[x] = (ymin, ymax)
        if ymax - ymin + 1 >= COTE:
            # les lignes ymin..ymin+COTE-1 sont-elles couvertes par les
            # COTE-1 colonnes précédentes ?
            if all(faisceau[xg][0] <= ymin
                   and ymin + COTE - 1 <= faisceau[xg][1]
                   for xg in range(x - COTE + 1, x)):
                return 10000 * (x - COTE + 1) + ymin
        x += 1


programme = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 2 :', partie2(programme))
