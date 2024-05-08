from pytest import mark, param

from scripts.Visualize import *


@mark.parametrize(
    "class_",
    [
        param(
            class_,
            id=f"{class_.__name__}",
        )
        for class_ in
        [
            kiwilib.AliasableEnum,
            i18n.EnglishSpanishEnum,
            Global.ColoredAliasable,
            genres.GenreUndefined,
            sg.SocialGroupUndefined,
            sg.Gender,
        ]
    ]
)
def test_aliasable_inheritance(class_: type):
    assert class_ in kiwilib.getAllSubclasses(kiwilib.Aliasable)


def test_aliasable_inheritance2():
    assert len(kiwilib.getAllSubclasses(kiwilib.Aliasable)) >= 59


def test_enum_alias_maps():
    assert _e(sg.ColleagueBallOPIR) in _hier_enum_alias_map
    assert _e(sg.ColleagueEA) in _hier_enum_alias_map
