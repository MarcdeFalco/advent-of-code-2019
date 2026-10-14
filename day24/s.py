"""Advent of Code 2019, jour 24 : automate cellulaire 5x5, puis emboîté.

La grille est un entier de 25 bits (bit 5y + x), et le voisinage de chaque
case un masque précalculé : compter les voisins est un & suivi d'un
comptage de bits.
Partie 1 : on itère jusqu'à retrouver un état déjà vu (ensemble d'entiers) ;
la note demandée est exactement la valeur de l'entier.
Partie 2 : une liste d'entiers, un par niveau d'emboîtement ; chaque case a
trois masques (même niveau, niveau extérieur, niveau intérieur). À chaque
minute on ajoute un niveau vide de chaque côté, si bien que la liste
grandit de 2 à chaque pas (même si les niveaux extrêmes restent vides).
"""
from itertools import product

VOISINS = [(-1, 0), (1, 0), (0, 1), (0, -1)]
CENTRE = 12  # case (2, 2), qui contient le niveau intérieur


def lire_grille(texte):
    etat = 0
    for y, ligne in enumerate(texte.split('\n')):
        for x, c in enumerate(ligne):
            if c == '#':
                etat += 1 << (5 * y + x)
    return etat


def nb_bits(n):
    v = 0
    while n != 0:
        v += n % 2
        n //= 2
    return v


def regle(insecte, voisins):
    """Un insecte survit avec exactement 1 voisin, naît avec 1 ou 2."""
    if insecte:
        return voisins == 1
    return voisins in [1, 2]


# Partie 1 : voisinage dans une seule grille
MASQUES = {}
for x, y in product(range(5), repeat=2):
    m = 0
    for dx, dy in VOISINS:
        if 0 <= x + dx < 5 and 0 <= y + dy < 5:
            m += 1 << (x + dx + 5 * (y + dy))
    MASQUES[5 * y + x] = m


def evoluer(etat):
    suivant = 0
    for k in range(25):
        if regle(etat & (1 << k) != 0, nb_bits(etat & MASQUES[k])):
            suivant += 1 << k
    return suivant


def partie1(etat):
    vus = {etat}
    while True:
        etat = evoluer(etat)
        if etat in vus:
            return etat
        vus.add(etat)


# Partie 2 : pour chaque case, masques (même niveau, extérieur, intérieur)
MASQUES_RECURSIFS = {}
for x, y in product(range(5), repeat=2):
    m, m_ext, m_int = 0, 0, 0
    for dx, dy in VOISINS:
        if (x + dx, y + dy) == (2, 2):
            # voisine du centre : tout un bord de la grille intérieure
            if (dx, dy) == (-1, 0):
                # colonne droite
                m_int = sum(1 << (5 * k + 4) for k in range(5))
            if (dx, dy) == (1, 0):
                m_int = sum(1 << (5 * k) for k in range(5))  # colonne gauche
            if (dx, dy) == (0, -1):
                m_int = sum(1 << k for k in range(20, 25))  # ligne du bas
            if (dx, dy) == (0, 1):
                m_int = sum(1 << k for k in range(5))  # ligne du haut
        elif 0 <= x + dx < 5 and 0 <= y + dy < 5:
            m += 1 << (x + dx + 5 * (y + dy))
        else:
            # au bord : voisine du centre de la grille extérieure
            if x + dx < 0:
                m_ext += 1 << 11
            if x + dx == 5:
                m_ext += 1 << 13
            if y + dy < 0:
                m_ext += 1 << 7
            if y + dy == 5:
                m_ext += 1 << 17
    MASQUES_RECURSIFS[5 * y + x] = m, m_ext, m_int


def evoluer_niveau(etat, exterieur, interieur):
    suivant = 0
    for k in range(25):
        if k == CENTRE:
            continue
        m, m_ext, m_int = MASQUES_RECURSIFS[k]
        voisins = (nb_bits(etat & m) + nb_bits(exterieur & m_ext)
                   + nb_bits(interieur & m_int))
        if regle(etat & (1 << k) != 0, voisins):
            suivant += 1 << k
    return suivant


def evoluer_niveaux(niveaux):
    """niveaux[0] est le plus extérieur ; ajoute un niveau de chaque côté."""
    n = len(niveaux)
    suivants = [evoluer_niveau(0, 0, niveaux[0])]
    for i in range(n):
        exterieur = niveaux[i - 1] if i > 0 else 0
        interieur = niveaux[i + 1] if i < n - 1 else 0
        suivants.append(evoluer_niveau(niveaux[i], exterieur, interieur))
    suivants.append(evoluer_niveau(0, niveaux[-1], 0))
    return suivants


def partie2(etat, minutes=200):
    niveaux = [etat]
    for _ in range(minutes):
        niveaux = evoluer_niveaux(niveaux)
    return sum(nb_bits(e) for e in niveaux)


etat = lire_grille(open('input.txt').read().strip())
print('Partie 1 :', partie1(etat))
print('Partie 2 :', partie2(etat))
