import json
import os

import drawsvg as draw

from sigilmc.datatypes import Arcanum, Cercle, ContraintePlace, Sigil, Strophe
from sigilmc.exceptions import FormeInconnueError

CERCLES_FILE_PATH = os.path.join(os.path.dirname(__file__), "../data/cercles.json")
with open(CERCLES_FILE_PATH) as f:
    AGENCEMENTS = json.load(f)["agencements"]

### FONCTIONS DE DESSIN DE FORMES DE BASE
def draw_lines(coords:list[list], size: int,
    stroke_width = 1.0) -> draw.Group:
    g = draw.Group()
    coords_actual = [ [c[0]*size, c[1]*size] for c in coords ] # Mise en forme des coordonnées pour la taille réelle
    for c in range(1, len(coords_actual)):
        g.append(draw.Line(coords_actual[c-1][0], coords_actual[c-1][1],
            coords_actual[c][0], coords_actual[c][1],
            stroke="black",
            stroke_width=stroke_width))
    return g

def draw_circle(x: float, y: float, r: float,
    fill: str, size: int, stroke_width=1.0) -> draw.Group:
    g = draw.Group()
    x, y, r = x*size, y*size, r*size
    g.append(draw.Circle(x, y, r,
        fill=fill,
        stroke="black",
        stroke_width=stroke_width))
    return g

def draw_arc(x: float, y: float, r: float,
    angle1: int, angle2: int,
    size: int, stroke_width=1.0) -> draw.Group:
    g = draw.Group()
    x, y, r = x * size, y*size, r*size
    g.append(draw.Arc(x, y, r, angle1, angle2,
        fill="transparent",
        stroke="black",
        stroke_width=stroke_width))
    return g

def draw_curve(coords: list, size: int, stroke_width=1.0) -> draw.Group:
    g = draw.Group()
    p = draw.Path(stroke="black", fill="transparent", stroke_width=stroke_width)
    sx, sy, c1x, c1y, c2x, c2y, ex, ey = tuple([c*size for c in coords])
    p.M(sx, sy)
    p.C(c1x, c1y, c2x, c2y, ex, ey)
    g.append(p)
    return g

### FONCTIONS DE DESSIN D'OBJETS / SIGILS
def draw_arcanum(arc: Arcanum, size: int, stroke_width=1.0) -> draw.Group:
    g = draw.Group()
    for dsn in arc.dessin:
        forme = dsn["type"]
        if forme == "lines":
            coords = dsn["coords"]
            g.append(draw_lines(coords, size, stroke_width))
        elif forme == "circle":
            x, y, r, fill = dsn["x"], dsn["y"], dsn["r"], dsn["fill"]
            g.append(draw_circle(x, y, r, fill, size, stroke_width))
        elif forme == "arc":
            x, y, r, angle1, angle2 = dsn["x"], dsn["y"], dsn["r"], dsn["angles"][0], dsn["angles"][1]
            g.append(draw_arc(x, y, r, angle1, angle2, size, stroke_width))
        elif forme == "curve":
            coords = dsn["coords"]
            g.append(draw_curve(coords, size, stroke_width))
        else:
            raise FormeInconnueError(forme)
    return g

def draw_strophe(stp: Strophe, size: int, encercler=False, stroke_width=1.0) -> draw.Group:
    g = draw.Group()
    x, y = 0, 0
    if encercler:
        g.append(draw.Circle(0, 0, 0.5*size,
            fill="white", stroke="black",
            stroke_width=stroke_width))
        size = int(size*0.7)
    for arc in stp.arcanums:
        g.append(draw.Use(draw_arcanum(arc, size, stroke_width), x, y))
        suite = arc.suite
        size = int(suite.taille * size)
        x = int(x + suite.x * size)
        y = int(y + suite.y * size)
    return g

def agencement(taille_cercle: int, contrainte: ContraintePlace) -> str:
    if taille_cercle == 1:
        if contrainte == ContraintePlace.BAS: return "mono_bas"
        else: return "mono_haut"
    if taille_cercle == 2:
        if contrainte == ContraintePlace.COTES: return "duo_hrzn"
        else: return "duo_vert"
    else:
        if contrainte == ContraintePlace.BAS: return "triangle_bas"
        else: return "triangle_haut"

def draw_cercle(ccl: Cercle, size: int, max_size: int) -> draw.Group:
    g = draw.Group()
    agcm = AGENCEMENTS[agencement(ccl.nb_strophes, ccl.contrainte)]
    coords = agcm["coords"]
    stp_size = int(max_size / 6)
    g.append(draw.Circle(0, 0, 0.4*size, fill="white", stroke="black", stroke_width=0.25))
    for i in range(ccl.nb_strophes):
        stp_draw = draw_strophe(ccl.strophes[i], stp_size, encercler=True, stroke_width=0.25)
        x, y = coords[i][0] * size, coords[i][1] * size
        g.append(draw.Use(stp_draw, x, y))
    return g

def draw_sigil(sigil: Sigil, size: int) -> draw.Group:
    g = draw.Group()
    ccl_size = int((1/3) * sigil.nb_cercles * size)
    for ccl in sigil.cercles:
        g.append(draw.Use(draw_cercle(ccl, ccl_size, size), 0, 0))
        ccl_size = int(ccl_size - 0.3 * size)
    return g

def dessin(sigil: str, strophe: bool, pixel_scale: int) -> draw.Drawing:
    d = draw.Drawing(100, 100, origin="center")
    if strophe:
        d.append(draw.Use(draw_strophe(Strophe(sigil), 95, encercler=False), 0, 0))
    else:
        d.append(draw.Use(draw_sigil(Sigil(sigil), 100), 0 ,0))
    d.set_pixel_scale(pixel_scale)
    return d
