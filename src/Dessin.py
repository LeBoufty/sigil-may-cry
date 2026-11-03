import logging

import drawsvg as draw

from Datatypes import Arcanum, Strophe
from src.Exceptions import FormeInconnueError

d = draw.Drawing(100, 100, origin="center")
logger = logging.getLogger(__name__)

### FONCTIONS DE DESSIN DE FORMES DE BASE
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

def draw_arc(x: float, y: float, r: float, angle1: int, angle2: int, size: int) -> draw.Group:
    g = draw.Group()
    x, y, r = x * size, y*size, r*size
    g.append(draw.Arc(x, y, r, angle1, angle2, fill="transparent", stroke="black"))
    return g

def draw_curve(coords: list, size: int) -> draw.Group:
    g = draw.Group()
    p = draw.Path(stroke="black", fill="transparent")
    sx, sy, c1x, c1y, c2x, c2y, ex, ey = tuple([c*size for c in coords])
    p.M(sx, sy)
    p.C(c1x, c1y, c2x, c2y, ex, ey)
    g.append(p)
    return g

### FONCTIONS DE DESSIN D'OBJETS / SIGILS
def draw_arcanum(arc: Arcanum, size: int) -> draw.Group:
    g = draw.Group()
    for dsn in arc.dessin:
        forme = dsn["type"]
        if forme == "lines":
            coords = dsn["coords"]
            g.append(draw_lines(coords, size))
        elif forme == "circle":
            x, y, r, fill = dsn["x"], dsn["y"], dsn["r"], dsn["fill"]
            g.append(draw_circle(x, y, r, fill, size))
        elif forme == "arc":
            x, y, r, angle1, angle2 = dsn["x"], dsn["y"], dsn["r"], dsn["angles"][0], dsn["angles"][1]
            g.append(draw_arc(x, y, r, angle1, angle2, size))
        elif forme == "curve":
            coords = dsn["coords"]
            g.append(draw_curve(coords, size))
        else:
            raise FormeInconnueError(forme)
    return g

def draw_strophe(stp: Strophe, size: int, encercler=False) -> draw.Group:
    g = draw.Group()
    x, y = 0, 0
    if encercler:
        g.append(draw.Circle(0, 0, 0.5*size, fill="transparent", stroke="black"))
        size = int(size*0.67)
    for arc in stp.arcanums:
        g.append(draw.Use(draw_arcanum(arc, size), x, y))
        suite = arc.suite
        size = int(suite.taille * size)
        x = int(x + suite.x * size)
        y = int(y + suite.y * size)
    return g

strophe = Strophe("lichen - vers - mort")

d.append(draw.Use(draw_strophe(strophe, 95, encercler=False), 0, 0))
d.set_pixel_scale(8)
d.save_png("output/sigil.png")
