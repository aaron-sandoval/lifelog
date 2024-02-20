import sys, os
from pathlib import Path

sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.absolute()))
from src.Description import *


def test_genTokenTree():
    Description._collxTokensMarked = set()
    d1 = Description.genTokenTree(['AUDIOLIBRO'])
    assert d1.children[0].name == 'AUDIOLIBRO'
    assert len(d1.children) == 1
    d2 = Description.genTokenTree(['AUDIOLIBRO', 'MY TITLE', 'LEER', 'NOTICIAS'])
    assert len(d2.children) == 2
    assert len(d2.children[0].children) == 1
    assert len(d2.children[1].children) == 1
    d3 = Description.genTokenTree(["COMER", 'GRATIS', 'CARNE', "AUDIOLIBRO", "SEVENTH SON"])
    assert len(d3.children) == 2
    assert len(d3.children[0].children) == 2
    assert len(d3.children[1].children) == 1
    d4 = Description.genTokenTree(["COMER", 'GRATIS', 'CHARLAR', "JACK F", "998"])
    assert len(d4.children) == 3
    assert len(d4.children[0].children) == 1
    assert len(d4.children[1].children) == 1
    d5 = Description.genTokenTree('ESCRIBIR, SOLICITUDES, SPACEX'.split(', '))
    assert len(d5.children) == 1
    assert len(d5.children[0].children) == 2
    d5 = Description('Haarlem a "Amsterdam, Países Bajos"')
    assert len(d5.tokens) == 2
    assert len(d5.tokenTree.children) == 2
    d5 =  Description('Montar, cicloturismo, Haarlem a "Amsterdam, Países Bajos"')
    assert len(d5.tokens) == 4
    assert len(d5.tokenTree.children) == 4
    d5 =  Description('"Haarlem, PB" a "Amsterdam, Países Bajos"')
    assert len(d5.tokens) == 3
    assert len(d5.tokenTree.children) == 3
    d5 =  Description('"Haarlem, PB" a "Amsterdam, Países Bajos", charlar, Suzie')
    assert len(d5.tokens) == 5
    assert len(d5.tokenTree.children) == 4
    d5 = Description('Charlar, Doug Juarez, NX')
    assert len(d5.tokenTree.children) == 2
    d5 = Description('Charlar, Doug Juarez, leer, noticias')
    assert len(d5.tokenTree.children) == 2
    d5 = Description('Charlar, Doug Juarez, español')
    assert len(d5.tokenTree.children) == 2
    d5 = Description('Audiolibro, Doug Juarez, español')
    assert len(d5.tokenTree.children) == 2
    d5 = Description('Audiolibro, español, charlar, Bianca J')
    assert len(d5.tokenTree.children) == 3
    d5 = Description('ESCRIBIR, CARLOS, blup, blip')
    assert all([tok in Description._collxTokensMarked for tok in ['BLUP', 'BLIP', 'CARLOS']])
    assert d5.standardString == 'ESCRIBIR, $PERSON, CARLOS, BLUP, BLIP'
    assert len(d5.tokenTree.children) == 2
    assert len(d5.tokenTree.children[0].children) == 0
    assert len(d5.tokenTree.children[1].children) == 3
    d5 = Description('CHARLAR, SOME DUDE')
    assert 'SOME DUDE' not in Description._collxTokensMarked
    assert len(d5.tokenTree.children) == 1


def test_genTokensSequence():
    Description._collxTokensMarked = set()
    assert Description('Skype con los padres').standardString == 'VIDEOLLAMADA, PAPÁ, MAMÁ'
    assert Description('REUNIÓN DE CONTROLES').standardString == 'REUNIÓN, CONTROLES'
    assert Description('PREPARAR la presentacion').standardString == 'PREPARAR, PRESENTACIÓN'
    assert Description('BARRER LA ALFOMBRA').standardString == 'LIMPIAR, CASA'
    assert Description('solicitud').standardString == 'ESCRIBIR, SOLICITUDES'
    assert Description('liderazgo reunion').standardString == 'LIDERAZGO, REUNIÓN'
    assert Description('solicitUd de spacex').standardString == 'ESCRIBIR, SOLICITUDES, SPACEX'
    assert Description('ESCRIBIR, J lo').standardString == 'ESCRIBIR, J LO'
    assert Description('').standardString == ''
    assert Description('').standardString == ''


test_genTokenTree()
# test_genTokensSequence()