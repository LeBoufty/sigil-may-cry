import drawsvg as draw

d = draw.Drawing(100, 100, origin="center")

def draw_lines(coords:list[list], d:draw.Drawing) -> draw.Drawing:
    coords_actual = [ [c[0]*d.width, c[1]*d.height] for c in coords ] # Mise en forme des coordonnées pour la taille réelle
    for c in range(1, len(coords_actual)):
        d.append(draw.Line(coords_actual[c-1][0], coords_actual[c-1][1],
            coords_actual[c][0], coords_actual[c][1],
            stroke="black"))
    return d

draw_lines([[0.5, 0.5], [0, -0.5], [-0.5, 0.5]], d)
d.save_png("sigil.png")
