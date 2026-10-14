"""Visualisation du balayage du jour 10 (nécessite PIL).

Une image par tir (ast000.png, ast001.png, ...) : la station en rouge,
l'astéroïde visé en vert, les astéroïdes déjà détruits en gris.
"""
from random import randint

from PIL import Image, ImageDraw

from s import lire_asteroides, meilleure_station, tirs

texte = open('input.txt').read().strip()
largeur, hauteur = len(texte.split('\n')[0]), len(texte.split('\n'))
asteroides = lire_asteroides(texte)
x, y = meilleure_station(asteroides)
restants = set(asteroides)
detruits = []

for i, (x2, y2) in enumerate(tirs(asteroides, (x, y))):
    restants.discard((x2, y2))
    im = Image.new('RGB', (largeur * 10, hauteur * 10))
    dessin = ImageDraw.Draw(im)
    for y3 in range(hauteur):
        for x3 in range(largeur):
            if (x3, y3) in [(x, y), (x2, y2)]:
                couleur = (255, 0, 0) if (x3, y3) == (x, y) else (0, 255, 0)
                dessin.rectangle(((10 * x3 + 3, 10 * y3 + 3),
                                  (10 * x3 + 7, 10 * y3 + 7)), fill=couleur)
            elif (x3, y3) in detruits:
                for _ in range(10):  # quelques débris au hasard
                    im.putpixel((10 * x3 + randint(0, 9),
                                 10 * y3 + randint(0, 9)), (50, 50, 50))
            elif (x3, y3) in restants:
                dessin.ellipse(((10 * x3 + 4, 10 * y3 + 4),
                                (10 * x3 + 6, 10 * y3 + 6)),
                               fill=(255, 255, 255))
    dessin.line(((10 * x + 5, 10 * y + 5), (10 * x2 + 5, 10 * y2 + 5)),
                (255, 120, 120))
    im.save('ast%03d.png' % i)
    detruits.append((x2, y2))
