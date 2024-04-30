from yamlable import yaml_info, YamlAble
from typing import Dict, Callable
import kiwilib


@yaml_info(yaml_tag_ns='Genre')
class Genre(kiwilib.AliasableHierEnum, YamlAble):
    es_MX = 'Género'
    color = (0.5, 0.5, 0.5)

    @classmethod
    def root_class(cls) -> type:
        return Genre

    def __init_subclass__(cls, **kwargs):
        """Register all subclasses in the namespace. Substitute for decorating every subclass."""
        super().__init_subclass__(**kwargs)
        yaml_info(yaml_tag_ns='Genre')(cls)

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable[['Genre'], str]]:
        return {
               # 'en_US': lambda slf: re.sub(r"([a-z])([A-Z])", r"\1 \2", type(slf).__name__),
               'en_US': lambda slf: type(slf).__name__,
               'es_MX': lambda slf: slf.es_MX if hasattr(slf, 'es_MX') else lambda slf: type(slf).__name__ + 'o'
        }

    @property
    def color_hex(self) -> str:
        """Hexadecimal string representation of the float color tuple."""
        if isinstance(self.color[0], int):
            return "#{0:02x}{1:02x}{2:02x}".format(*self.color)
        else:
            return "#{0:02x}{1:02x}{2:02x}".format(*[max(0, min(round(x*256), 255)) for x in self.color])


class GenreUndefined(Genre):
    # Marks a Media instance as needing Genre(s) assigned. Used in DEFAULT_MEMBERS.
    es_MX = 'Indefinido'


class Fiction(Genre): pass
class NonFiction(Genre): pass
class Comedy(Genre): pass
class Mystery(Genre): pass
class Historical(Genre): pass
class Drama(Genre): pass
class SciFi(Fiction): pass
class Fantasy(Fiction): pass
class Educational(NonFiction): pass
class Opinion(NonFiction): pass
class SelfHelp(Educational): pass