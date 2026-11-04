from Datatypes import Cercle, ContraintePlace, Sigil, Strophe

strophe = Strophe("sigil - augmenter - vitesse")
cercleFeu = Cercle("eau - augmenter - chaleur ; terre - augmenter - chaleur ; air - augmenter - chaleur", ContraintePlace.AUCUNE)
cercleLapis = Cercle("métal - diminuer - taille ; métal - augmenter - masse", ContraintePlace.AUCUNE)
cercleLichen = Cercle("lichen - vers - mort", ContraintePlace.AUCUNE)

sigilFeu = Sigil("3 * terre - augmenter - chaleur / 3 * air - augmenter - chaleur / 3 * eau - augmenter - chaleur")
sigilLapis = Sigil("métal - augmenter - masse ; métal - diminuer - taille")
sigilBrume = Sigil("3*liquide-augmenter-chaleur/2*air-augmenter-FROID;air-augmenter-taille")
sigilSigil = Sigil("3 * sigil - diminuer - résistance / 3 * sigil - augmenter - vitesse")
