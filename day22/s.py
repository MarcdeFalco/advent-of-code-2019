"""Advent of Code 2019, jour 22 : mélanges de cartes et arithmétique modulaire.

Chaque mélange élémentaire est une bijection affine modulo N : retourner
le paquet, c'est x -> -x - 1 ; couper, une translation ; distribuer avec un
pas d, la multiplication par d.
Partie 1 : simulation directe sur un paquet de 10007 cartes (liste
permutée), puis position de la carte 2019.
Partie 2 : N et le nombre de répétitions T sont gigantesques. Pour savoir
quelle carte arrive en position x, on compose les inverses dans l'ordre
inverse ; l'inverse de la multiplication par d est la multiplication par
d^-1 mod N (Euclide étendu). On obtient f(x) = a x + b, puis
f^T(x) = a^T x + (a^T - 1) / (a - 1) * b (somme géométrique), la division
étant une multiplication par l'inverse de a - 1 et a^T une exponentiation
modulaire rapide.
"""

TAILLE_PARTIE1 = 10007
TAILLE_PARTIE2 = 119315717514047
REPETITIONS = 101741582076661


def bezout(x, y):
    """(d, u, v) avec u x + v y = d = pgcd(x, y)."""
    if y == 0:
        return x, 1, 0
    d, u1, v1 = bezout(y, x % y)
    return d, v1, u1 - (x // y) * v1


def inverse(k, n):
    d, u, _ = bezout(k, n)
    assert d == 1
    return u % n


def simuler(instructions, paquet):
    n = len(paquet)
    for inst in instructions:
        if inst == 'deal into new stack':
            paquet.reverse()
        elif inst.startswith('deal'):
            # la carte en position i vient de la position i * d^-1
            di = inverse(int(inst.split()[-1]), n)
            paquet = [paquet[(i * di) % n] for i in range(n)]
        else:
            k = int(inst.split()[-1])
            paquet = [paquet[(i + k - n) % n] for i in range(n)]
    return paquet


def carte_en_position(instructions, n):
    """(a, b) tels que la carte en position x après un mélange soit a x + b."""
    a, b = 1, 0
    for inst in reversed(instructions):
        if inst == 'deal into new stack':
            a, b = -a, -b - 1
        elif inst.startswith('deal'):
            di = inverse(int(inst.split()[-1]), n)
            a, b = (a * di) % n, (b * di) % n
        else:
            b += int(inst.split()[-1])
    return a % n, b % n


def partie1(instructions):
    paquet = simuler(instructions, list(range(TAILLE_PARTIE1)))
    return paquet.index(2019)


def partie2(instructions):
    n = TAILLE_PARTIE2
    a, b = carte_en_position(instructions, n)
    an = pow(a, REPETITIONS, n)
    a2, b2 = an, ((an - 1) * inverse(a - 1, n) * b) % n
    return (a2 * 2020 + b2) % n


instructions = open('input.txt').read().strip().split('\n')
print('Partie 1 :', partie1(instructions))
print('Partie 2 :', partie2(instructions))
