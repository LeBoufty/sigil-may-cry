import argparse

from sigilmc.dessin import dessin
from sigilmc.exceptions import FormatNonSupporteError


def main():
    parser = argparse.ArgumentParser(
        prog="sigilmc",
        description="Dessinateur de sigils pour les Hermétistes pressés"
    )
    parser.add_argument("sigil", help="Le sigil à dessiner")
    parser.add_argument("-o", "--output", help="Chemin vers le fichier à générer")
    parser.add_argument("-s", "--strophe",
        action="store_true",
        help="Active le mode strophe, permettant de générer qu'une strophe ou un arcanum")
    parser.add_argument("-p", "--pixelscale", type=int, help="Définit la qualité du rendu")
    args = parser.parse_args()

    # Lecture des arguments
    pixel_scale = 16
    if args.pixelscale: pixel_scale = args.pixelscale
    strophe = args.strophe
    sigil = args.sigil
    output = "sigil.png"
    output_type = "png"
    if args.output:
        output = args.output
        output_type = output.split(".")[-1]
    # Dessin
    d = dessin(sigil, strophe, pixel_scale)
    # Sauvegarde
    if output_type == "png":
        d.save_png(output)
    elif output_type == "svg":
        d.save_svg(output)
    elif output_type == "gif":
        d.save_gif(output,
            fps=1,
            duration=0)
    else:
        raise FormatNonSupporteError(output_type)

if __name__ == "__main__":
    main()
