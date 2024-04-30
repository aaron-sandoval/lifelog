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
    assert class_ in kiwilib.SubclassRegistryMeta._registry


def test_aliasable_inheritance2():
    assert len(kiwilib.SubclassRegistryMeta._registry) >= 64