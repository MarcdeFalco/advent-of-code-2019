"""Advent of Code 2019, jour 5 : interprète Intcode.

L'interprète est récursif : `executer` décode l'instruction en p[pc]
(p[pc] % 100 donne le code d'opération, les chiffres suivants les modes des
paramètres : 0 = position, 1 = immédiat) puis s'appelle sur le compteur
ordinal suivant. Les entrées-sorties sont des fonctions passées en paramètre.
Partie 1 : entrée 1 ; partie 2 : entrée 5. La réponse est la dernière sortie.
"""
import sys

# Chaque instruction exécutée ajoute un appel récursif (Python n'optimise pas
# les appels terminaux) : on relève la limite de récursion par précaution.
sys.setrecursionlimit(10000)


def executer(p, pc, lire, ecrire):
    op = p[pc] % 100
    chiffres = '%05d' % p[pc]
    # modes[k-1] vaut True si le paramètre k est en mode immédiat
    modes = chiffres[2] == '1', chiffres[1] == '1', chiffres[0] == '1'

    def param(k):
        if modes[k - 1]:
            return p[pc + k]
        return p[p[pc + k]]

    if op in [1, 2]:
        v1, v2 = param(1), param(2)
        p[p[pc + 3]] = v1 + v2 if op == 1 else v1 * v2
        return executer(p, pc + 4, lire, ecrire)
    elif op == 3:
        p[p[pc + 1]] = lire()
        return executer(p, pc + 2, lire, ecrire)
    elif op == 4:
        ecrire(param(1))
        return executer(p, pc + 2, lire, ecrire)
    elif op == 5:  # saut si non nul
        if param(1) != 0:
            return executer(p, param(2), lire, ecrire)
        return executer(p, pc + 3, lire, ecrire)
    elif op == 6:  # saut si nul
        if param(1) == 0:
            return executer(p, param(2), lire, ecrire)
        return executer(p, pc + 3, lire, ecrire)
    elif op == 7:
        p[p[pc + 3]] = 1 if param(1) < param(2) else 0
        return executer(p, pc + 4, lire, ecrire)
    elif op == 8:
        p[p[pc + 3]] = 1 if param(1) == param(2) else 0
        return executer(p, pc + 4, lire, ecrire)
    elif op == 99:
        return p[0]


def diagnostic(programme, valeur):
    sorties = []
    executer(programme[:], 0, lambda: valeur, sorties.append)
    return sorties[-1]


def partie1(programme):
    return diagnostic(programme, 1)


def partie2(programme):
    return diagnostic(programme, 5)


programme = list(map(int, open('input.txt').read().strip().split(',')))
print('Partie 1 :', partie1(programme))
print('Partie 2 :', partie2(programme))
