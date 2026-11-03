import logging

import drawsvg as draw

from Datatypes import Arcanum

d = draw.Drawing(100, 100, origin="center")
logger = logging.getLogger(__name__)

def draw_lines(coords:list[list], size: int) -> draw.Group:
    g = draw.Group()
    coords_actual = [ [c[0]*size, c[1]*size] for c in coords ] # Mise en forme des coordonnées pour la taille réelle
    for c in range(1, len(coords_actual)):
        g.append(draw.Line(coords_actual[c-1][0], coords_actual[c-1][1],
            coords_actual[c][0], coords_actual[c][1],
            stroke="black"))
    return g

def draw_circle(x: float, y: float, r: float, fill: str, size: int) -> draw.Group:
    g = draw.Group()
    x, y, r = x*size, y*size, r*size
    g.append(draw.Circle(x, y, r, fill=fill, stroke="black"))
    return g

def draw_arcanum(arc: Arcanum, size: int) -> draw.Group:
    g = draw.Group()
    for dsn in arc.dessin:
        forme = dsn["type"]
        if forme == "lines":
            coords = dsn["coords"]
            g.append(draw_lines(coords, size))
        if forme == "circle":
            x, y, r, fill = dsn["x"], dsn["y"], dsn["r"], dsn["fill"]
            g.append(draw_circle(x, y, r, fill, size))
    return g

d.append(draw.Use(draw_arcanum(Arcanum("métal"), 95), 0, 0))
d.set_pixel_scale(8)
d.save_png("output/sigil.png")
