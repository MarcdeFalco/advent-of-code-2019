"""Commandes pour l'épreuve finale du jour 25, à rediriger vers s.py.

Le fichier `script` contient le trajet (propre à chaque entrée, non fourni)
qui ramasse les huit objets et mène devant le point de contrôle, situé à
l'ouest. On essaie ensuite les 2^8 = 256 sous-ensembles d'objets en
comptant en binaire : le bit k de i dit si l'objet k est posé avant de
tenter le passage, puis on le reprend.
"""

OBJETS = [
    'fuel cell', 'polygon', 'shell', 'whirled peas',
    'candy cane', 'hologram', 'fixed point', 'antenna',
]

for ligne in open('script'):
    print(ligne.strip())
for i in range(2 ** 8):
    for k in range(8):
        if i & (1 << k) != 0:
            print('drop ' + OBJETS[k])
    print('west')
    for k in range(8):
        if i & (1 << k) != 0:
            print('take ' + OBJETS[k])
