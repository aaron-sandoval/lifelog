from yamlable import yaml_info, YamlAble
from typing import Dict, Callable
from external_modules import kiwilib


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
               'es_MX': lambda slf: slf.es_MX if kiwilib.is_locally_defined(type(slf), 'es_MX') else type(slf).__name__ + 'o'
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
    es_MX = 'Género Indefinido'


class Fiction(Genre):
    es_MX = 'Ficción'
class NonFiction(Genre):
    es_MX = 'No Ficción'
class Comedy(Genre):
    es_MX = 'Comedia'
class Mystery(Genre):
    es_MX = 'Misterio'
class Historical(Genre):
    es_MX = 'Histórico'
class Drama(Genre):
    es_MX = 'Drama'
class SciFi(Fiction):
    es_MX = 'Ciencia Ficción'
class Fantasy(Fiction):
    es_MX = 'Fantasía'
class Educational(NonFiction):
    es_MX = 'Educacional'
class Opinion(NonFiction):
    es_MX = 'Opinión'
class SelfHelp(Educational):
    es_MX = 'Autoayuda'