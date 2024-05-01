from aenum import Enum
import yaml
from yamlable import yaml_info, YamlAble
from typing import Any, Dict, Callable, Tuple, Type, NamedTuple
from external_modules import kiwilib
import src.TimesheetGlobals as Global


class Gender(Global.ColoredAliasable):
    # UNDEFINED = -1  # Use pd.NA for instances which are yet to be defined/unknown
    NOTAPPLICABLE = 0
    MALE = 1
    FEMALE = 2
    NONBINARY = 3

    @classmethod
    def _enum_data(cls) -> Dict[Enum, 'cls.dataclass']:
        c = cls.dataclass
        return {
            cls.NOTAPPLICABLE: c(  # Person instances w/out gender, e.g., MultiplePeople
                en_US='N/A',
                es_MX='N/A',
                color=(.6, .6, .6),
            ),
            cls.MALE: c(
                es_MX='HOMBRE',
                color=(.54, .81, .94),
            ),
            cls.FEMALE: c(
                es_MX='MUJER',
                color=(.96, .76, .76),
            ),
            cls.NONBINARY: c(
                es_MX='NO BINARIO',
                color=(.7, .7, .1),
            ),
        }

    # @classmethod
    # def _get_dataclass(cls) -> kiwilib.IsDataclass:
    #     @dataclass
    #     class GenderDataclass(Global.Colored.dataclass, i18n.EnglishSpanishEnum.dataclass): pass
    #     return GenderDataclass

    # @classmethod
    # def valueDict(cls):
    #     return {a.name: a for a in Gender}

    @staticmethod
    def _representer(dumper, data):
        return dumper.represent_scalar(u'!Gender', u'%s' % data.name)

    @staticmethod
    def _constructor(loader, node):
        value = loader.construct_scalar(node).strip()
        return getattr(Gender, value)

    @classmethod
    def _aliasFuncs(cls):
        """Defines a map between locale strings and Callables returning the localization of an instance."""
        return {
           'en_US': lambda slf: slf.en_US if slf.en_US != '' else slf.name,
           'es_MX': lambda slf: slf.es_MX,
        }


class Review(Global.ColoredAliasable):
    # UNDEFINED = -1  # Use pd.NA for undefined
    NOREVIEW  = 0
    POOR      = 1
    FAIR      = 2
    GOOD      = 3
    EXCELLENT = 4

    @classmethod
    def _enum_data(cls) -> Dict[Enum, 'cls.dataclass']:
        c: kiwilib.IsDataclass = cls.dataclass
        return {
            cls.NOREVIEW: c(
                en_US='NO REVIEW',
                es_MX='SIN OPINIÓN',
                color=(128, 128, 128),
            ),
            cls.POOR: c(
                es_MX='MALO',
                color=(220, 60, 40),
            ),
            cls.FAIR: c(
                es_MX='PASABLE',
                color=(230, 220, 70),
            ),
            cls.GOOD: c(
                es_MX='BUENO',
                color=(160, 240, 80),
            ),
            cls.EXCELLENT: c(
                es_MX='EXCELENTE',
                color=(20, 250, 100),
            ),
        }


    # @classmethod
    # def valueDict(cls) -> dict:
    #     return {a.name: a for a in cls}

    @staticmethod
    def _representer(dumper, data):
        return dumper.represent_scalar(u'!Review', u'%s' % data.name)

    @staticmethod
    def _constructor(loader, node):
        value = loader.construct_scalar(node).strip()
        return getattr(Review, value)

    @classmethod
    def moodMap(cls, mood: Global.Mood):
        """ Map to extract reviews for Reviewable objects, which are encoded in the mood field of a tsdf."""
        if not hasattr(cls, '_moodMap'):
            cls._moodMap = {
                Global.Mood.AWFUL:       Review.POOR,
                Global.Mood.BAD:         Review.FAIR,
                Global.Mood.NEUTRAL:     Review.NOREVIEW,
                Global.Mood.HAPPY:       Review.GOOD,
                Global.Mood.OVERJOYED:   Review.EXCELLENT,
            }
        return cls._moodMap[mood]

    # @classmethod
    # def aliasFuncs(cls) -> Dict[str, Callable]:
    #     return {
    #            'en_US': lambda slf: slf.value[1] if slf.value[1] != '' else slf.name,
    #            'es_MX': lambda slf: slf.value[2],
    #     }


# TODO: Refactor yaml ops below into a decorator procedure defined in kiwilib, probably
yaml.add_constructor(u'!Gender', Gender._constructor, Loader=yaml.SafeLoader)
yaml.add_representer(Gender, Gender._representer)
yaml.add_constructor(u'!Review', Review._constructor, Loader=yaml.SafeLoader)
yaml.add_representer(Review, Review._representer)


@yaml_info(yaml_tag_ns='SocialGroup')
class SocialGroup(kiwilib.AliasableHierEnum, YamlAble):
    es_MX = 'Grupo social'
    color = (0.5, 0.5, 0.5)

    @classmethod
    def root_class(cls) -> type:
        return SocialGroup

    def __init_subclass__(cls, **kwargs):
        """Register all subclasses in the 'SocialGroup' namespace."""
        super().__init_subclass__(**kwargs)
        yaml_info(yaml_tag_ns='SocialGroup')(cls)

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable[['SocialGroup'], str]]:
        return {
               # 'en_US': lambda slf: re.sub(r"([a-z])([A-Z])", r"\1 \2", type(slf).__name__),
               'en_US': lambda slf: type(slf).__name__,
               'es_MX': lambda slf: slf.es_MX if kiwilib.is_locally_defined(type(slf), 'es_MX') else type(slf).__name__ + 'o'
               # 'es_MX': lambda slf: type(slf).__name__ + 'o'
        }

    @property
    def color_hex(self) -> str:
        """Hexadecimal string representation of the float color tuple."""
        if isinstance(self.color[0], int):
            return "#{0:02x}{1:02x}{2:02x}".format(*self.color)
        else:
            return "#{0:02x}{1:02x}{2:02x}".format(*[max(0, min(round(x*256), 255)) for x in self.color])

class SocialGroupUndefined(SocialGroup): es_MX = 'Grupo Social Indefinido'  # Default. Marks one whose SocialGroup is not yet manually defined.
class MultiplePeople(SocialGroup):
    es_MX = 'Personas Múltiples'
class Relation(SocialGroup): es_MX = 'Relación'
class Activity(SocialGroup): es_MX = 'Actividad'
class ActivityProductive(Activity): es_MX = 'Actividad productiva'
class ActivityRecreational(Activity): es_MX = 'Actividad recreacional'
class ActivityStudy(ActivityProductive): es_MX = 'Actividad productiva'
class ActivityWork(ActivityProductive): pass
class ActivityRoommate(ActivityProductive): pass
class ActivityGames(ActivityRecreational): pass
class ActivityMusic(ActivityRecreational): pass
class ActivityBike(ActivityRecreational): pass
class ActivityTravel(ActivityRecreational): pass  # Interacted while they or I are leisure traveling. Not work travel
class ActivityHospitality(ActivityTravel): pass  # Host or guest while leisure traveling

class Colleague(Relation):
    # Includes any professional, client, volunteer, and other structured relationships
    es_MX = 'Colega'
    color = (.9, .8, .3)

class ColleagueWork(Colleague, ActivityWork): pass
class ColleagueAcademic(Colleague, ActivityStudy): pass
class Superior(Colleague): pass  # Not by seniority, but rather our individual work relationship, if they assign me work
class Subordinate(Colleague): pass
class Peer(Colleague): pass
class ColleagueBall(ColleagueWork): pass
class ColleagueBallStructures(ColleagueBall): pass  # Includes people from other orgs
class ColleagueBallOPIR(ColleagueBall): pass  # Includes people from other orgs
class ColleagueEA(Colleague): pass
class ColleagueAISC(ColleagueWork, ColleagueEA): pass
class Family(Relation):
    es_MX = 'Familia'
    color = (.7, .2, .9)

class Friend(Relation):
    es_MX = 'Amigo'
    color = (.2, .4, .9)

class Acquaintance(Relation):
    # People w/out much personal bond like Friend nor structured context like Colleague
    es_MX = 'Conocido'
    # color = (.6, .9, .85)
    color = (144, 196, 198)

class FamilyMom(Family): pass
class FamilyDad(Family): pass
class FamilyNuclear(Family): pass
class WarmshowersHospitality(ActivityHospitality, ActivityBike, Acquaintance): pass  # Host or guest via Warmshowers or similar
