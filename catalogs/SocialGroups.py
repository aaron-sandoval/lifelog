from enum import Enum
import yaml
from yamlable import yaml_info, YamlAble
from typing import Any, Dict, Callable, Tuple, Type, NamedTuple
from external_modules import kiwilib
import src.TimesheetGlobals as Global
from dataclasses import fields as dataclass_fields, dataclass, make_dataclass
import i18n_l10n.internationalization as i18n


@kiwilib.DataclassValuedEnum.init
class Gender(Global.Colored, i18n.AliasableEnum):
    # UNDEFINED = -1  # Use pd.NA for instances which are yet to be defined/unknown
    NOTAPPLICABLE = 0
    MALE = 1
    FEMALE = 2
    NONBINARY = 3

    @classmethod
    def _enum_data(cls, c: kiwilib.IsDataclass) -> Dict[Enum, 'c']:
        return {
            cls.NOTAPPLICABLE: c(  # Person instances w/out gender, e.g., MultiplePeople
                en_US='N/A',
                es_MX='N/A',
                color=(.6, .6, .6)
            ),
            cls.MALE: c(
                en_US='',
                es_MX='HOMBRE',
                color=(.54, .81, .94)
            ),
            cls.FEMALE: c(
                en_US='',
                es_MX='MUJER',
                color=(.96, .76, .76)
            ),
            cls.NONBINARY: c(
                en_US='',
                es_MX='NO BINARIO',
                color=(.7, .7, .1)
            ),
        }

    @classmethod
    def _get_dataclass(cls) -> Type[dataclass]:
        @dataclass
        class GenderDataclass(Global.Colored.dataclass, i18n.AliasableEnum.dataclass): pass
        return GenderDataclass

    # @classmethod
    # def valueDict(cls):
    #     return {a.name: a for a in Gender}

    @staticmethod
    def _representer(dumper, data):
        return dumper.represent_scalar(u'!Gender', u'%s' % data.name)

    @staticmethod
    def _constructor(loader, node):
        value = loader.construct_scalar(node).strip()
        return Gender(value)

    @classmethod
    def _aliasFuncs(cls):
        """Defines a map between locale strings and Callables returning the localization of an instance."""
        return {
           'en_US': lambda slf: slf.en_US if slf.en_US != '' else slf.name,
           'es_MX': lambda slf: slf.es_MX,
        }


class Review(kiwilib.Aliasable, Enum, metaclass=kiwilib.EnumABCMeta):
    # UNDEFINED = -1  # Use pd.NA for undefined
    NOREVIEW  = 0, 'NO REVIEW', 'SIN OPINIÓN'
    POOR      = 1, ''         , 'MALO'
    FAIR      = 2, ''         , 'PASABLE'
    GOOD      = 3, ''         , 'BUENO'
    EXCELLENT = 4, ''         , 'EXCELENTE'

    @classmethod
    def valueDict(cls) -> dict:
        return {a.name: a for a in cls}

    @staticmethod
    def _representer(dumper, data):
        return dumper.represent_scalar(u'!Review', u'%s' % data.name)

    @staticmethod
    def _constructor(loader, node):
        value = loader.construct_scalar(node).strip()
        return Review.valueDict()[value]

    @classmethod
    def moodMap(cls, mood: Global.Mood):
        """ Map to extract reviews for Reviewable objects, which are encoded in the mood field of a tsdf."""
        if not hasattr(cls, '_moodMap'):
            cls._moodMap = {
                Global.Mood.Awful: Review.POOR,
                Global.Mood.Bad: Review.FAIR,
                Global.Mood.Neutral: Review.NOREVIEW,
                Global.Mood.Happy: Review.GOOD,
                Global.Mood.Overjoyed: Review.EXCELLENT,
            }
        return cls._moodMap[mood]

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        if not hasattr(cls, '_aliasFuncs'):
            cls._aliasFuncs = {
               'en_US': lambda slf: slf.value[1] if slf.value[1] != '' else slf.name,
               'es_MX': lambda slf: slf.value[2],
            }
        return cls._aliasFuncs


# TODO: Refactor yaml ops below into a decorator procedure defined in kiwilib, probably
# Gender._get_enum_data()
yaml.add_constructor(u'!Gender', Gender._constructor, Loader=yaml.SafeLoader)
yaml.add_representer(Gender, Gender._representer)
yaml.add_constructor(u'!Review', Review._constructor, Loader=yaml.SafeLoader)
yaml.add_representer(Review, Review._representer)


@yaml_info(yaml_tag_ns='SocialGroup')
class SocialGroup(kiwilib.HierarchicalEnum, kiwilib.Aliasable, YamlAble):
    es_MX = 'Grupo social'
    color = (0.5, 0.5, 0.5)

    def __init_subclass__(cls, **kwargs):
        """Register all subclasses in the 'SocialGroup' namespace."""
        super().__init_subclass__(**kwargs)
        yaml_info(yaml_tag_ns='SocialGroup')(cls)

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        if not hasattr(cls, '_aliasFuncs'):
            cls._aliasFuncs = {
               'en_US': lambda slf: type(slf).__name__,
               'es_MX': lambda slf: type(slf).es_MX,
            }
        return cls._aliasFuncs

    @property
    def color_hex(self) -> str:
        """Hexadecimal string representation of the float color tuple."""
        if isinstance(self.color[0], int):
            return "#{0:02x}{1:02x}{2:02x}".format(*self.color)
        else:
            return "#{0:02x}{1:02x}{2:02x}".format(*[max(0, min(round(x*256), 255)) for x in self.color])

class SocialGroupUndefined(SocialGroup): es_MX = 'Indefinido'  # Default. Marks one whose SocialGroup is not yet manually defined.
class MultiplePeople(SocialGroup): pass
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
class ColleagueBallOPIR(ColleagueBall): pass  # Includes peo[ple from other orgs
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
