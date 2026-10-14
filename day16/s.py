"""Advent of Code 2019, jour 16 : transformation répétée de chiffres.

Partie 1 : transformation naïve, en O(L^2) par phase, appliquée 100 fois.
Partie 2 : la suite est répétée 10 000 fois (plusieurs millions de
chiffres), le naïf est hors de portée. Le décalage demandé tombe dans la
seconde moitié, où la ligne k de la matrice vaut 0 avant k puis 1 jusqu'au
bout : le nouveau chiffre k est la somme modulo 10 des chiffres qui le
suivent (somme suffixe). On ne garde que la fin de la suite et chaque phase
devient linéaire. L'hypothèse « décalage dans la seconde moitié » n'est pas
vérifiée par le code.
"""

MOTIF = [0, 1, 0, -1]


def phase_naive(s):
    r = []
    for k in range(len(s)):
        d = 0
        for i in range(len(s)):
            d += s[i] * MOTIF[((i + 1) // (k + 1)) % 4]
        r.append(abs(d) % 10)
    return r


def phase_seconde_moitie(s):
    """Sommes suffixes modulo 10, en partant du total."""
    total = sum(s)
    r = [total % 10]
    for x in s[:-1]:
        total -= x
        r.append(total % 10)
    return r


def partie1(chiffres):
    s = chiffres
    for _ in range(100):
        s = phase_naive(s)
    return ''.join(map(str, s[:8]))


def partie2(chiffres):
    s = chiffres * 10000
    decalage = int(''.join(map(str, s[:7])))
    s = s[decalage:]
    for _ in range(100):
        s = phase_seconde_moitie(s)
    return ''.join(map(str, s[:8]))


chiffres = list(map(int, open('input.txt').read().strip()))
print('Partie 1 :', partie1(chiffres))
print('Partie 2 :', partie2(chiffres))
