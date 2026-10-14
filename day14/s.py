"""Advent of Code 2019, jour 14 : réactions chimiques et tri topologique.

On construit le graphe « tel produit est utilisé par telle réaction ». Un
parcours en profondeur depuis ORE, avec ajout en fin de visite, donne un
ordre topologique où chaque produit précède ses ingrédients ; on propage
alors les besoins depuis FUEL dans cet ordre, si bien que le besoin total
d'un produit est connu avant qu'on le fabrique.
Partie 1 : en entiers, chaque réaction tourne un nombre entier de fois
(arrondi supérieur).
Partie 2 : en fractions (`Fraction`), une réaction peut tourner une
fraction de fois : on obtient la consommation moyenne f de minerai par
unité de FUEL quand on en produit beaucoup, et la réponse est N / f arrondi
à l'entier inférieur. C'est une approximation (exacte à la limite) ; elle
donne la bonne réponse sur cette entrée.
"""
from collections import defaultdict
from fractions import Fraction

STOCK_MINERAI = 1000000000000


def lire_reactions(texte):
    def quantite(s):
        n, produit = s.split()
        return int(n), produit

    reactions = []
    for ligne in texte.split('\n'):
        ingredients, produit = ligne.split(' => ')
        reactions.append((list(map(quantite, ingredients.split(', '))),
                          quantite(produit)))
    return reactions


def ordre_topologique(reactions):
    utilise_par = defaultdict(list)
    for ingredients, (_, produit) in reactions:
        for _, ingredient in ingredients:
            utilise_par[ingredient].append(produit)
    ordre = []

    def dfs(x):
        if x not in ordre:
            for y in utilise_par[x]:
                dfs(y)
            ordre.append(x)

    dfs('ORE')
    return ordre  # FUEL en tête, ORE à la fin


def besoins(reactions, nombre_de_tours):
    """Propage les besoins depuis une unité de FUEL.

    nombre_de_tours(besoin, produits_par_tour) dit combien de fois lancer
    la réaction qui fabrique le produit.
    """
    besoin = defaultdict(int)
    besoin['FUEL'] = 1
    for v in ordre_topologique(reactions):
        for ingredients, (n, produit) in reactions:
            if produit == v:
                k = nombre_de_tours(besoin[v], n)
                for c, x in ingredients:
                    besoin[x] += c * k
    return besoin['ORE']


def partie1(reactions):
    return besoins(reactions, lambda besoin, n: -(-besoin // n))


def partie2(reactions):
    f = besoins(reactions, lambda besoin, n: Fraction(besoin) / Fraction(n))
    return int(STOCK_MINERAI / f)


reactions = lire_reactions(open('input.txt').read().strip())
print('Partie 1 :', partie1(reactions))
print('Partie 2 :', partie2(reactions))
