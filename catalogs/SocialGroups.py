from enum import Enum
import yaml
from yamlable import yaml_info, YamlAble
from typing import Any, Dict, Callable, Tuple, Type, NamedTuple
from external_modules import kiwilib
import src.TimesheetGlobals as Global
from dataclasses import fields as dataclass_fields, dataclass, make_dataclass
import i18n_l10n.internationalization as i18n


@dataclass
class Vizable:
    en_US: str = ''
    es_MX: str = ''
    color: Tuple[float] = None

    # def __getattr__(self, item):
    #     # if not hasattr(type(self), 'attrs'):
    #     if item == 'attrs':
    #         setattr(self, 'attrs', {fld.name for fld in dataclass_fields(self)})
    #         return self.attrs
    #     raise AttributeError(f'{self} has no attribute named {item}.')


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

    @classmethod
    def valueDict(cls):
        return {a.name: a for a in Gender}

    @staticmethod
    def _representer(dumper, data):
        return dumper.represent_scalar(u'!Gender', u'%s' % data.name)

    @staticmethod
    def _constructor(loader, node):
        value = loader.construct_scalar(node).strip()
        return Gender.valueDict()[value]

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


@yaml_info(yaml_tag_ns='SocialGroup')
class SocialGroupUndefined(SocialGroup): es_MX = 'Indefinido'  # Default. Marks one whose SocialGroup is not yet manually defined.
@yaml_info(yaml_tag_ns='SocialGroup')
class MultiplePeople(SocialGroup): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class Relation(SocialGroup): es_MX = 'Relación'
@yaml_info(yaml_tag_ns='SocialGroup')
class Activity(SocialGroup): es_MX = 'Actividad'

@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityProductive(Activity): es_MX = 'Actividad productiva'
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityRecreational(Activity): es_MX = 'Actividad recreacional'
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityStudy(ActivityProductive): es_MX = 'Actividad productiva'
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityWork(ActivityProductive): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityRoommate(ActivityProductive): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityGames(ActivityRecreational): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityMusic(ActivityRecreational): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityBike(ActivityRecreational): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityTravel(ActivityRecreational): pass  # Interacted while they or I are leisure traveling. Not work travel
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityHospitality(ActivityTravel): pass  # Host or guest while leisure traveling


@yaml_info(yaml_tag_ns='SocialGroup')
class Colleague(Relation):
    # Includes any professional, client, volunteer, and other structured relationships
    es_MX = 'Colega'
    color = (.9, .8, .3)


@yaml_info(yaml_tag_ns='SocialGroup')
class ColleagueWork(Colleague, ActivityWork): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class ColleagueAcademic(Colleague, ActivityStudy): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class Superior(Colleague): pass  # Not by seniority, but rather our individual work relationship, if they assign me work
@yaml_info(yaml_tag_ns='SocialGroup')
class Subordinate(Colleague): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class Peer(Colleague): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class ColleagueBall(ColleagueWork): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class ColleagueBallStructures(ColleagueBall): pass  # Includes people from other orgs
@yaml_info(yaml_tag_ns='SocialGroup')
class ColleagueBallOPIR(ColleagueBall): pass  # Includes peo[ple from other orgs

@yaml_info(yaml_tag_ns='SocialGroup')
class Family(Relation):
    es_MX = 'Familia'
    color = (.7, .2, .9)


@yaml_info(yaml_tag_ns='SocialGroup')
class Friend(Relation):
    es_MX = 'Amigo'
    color = (.2, .4, .9)


@yaml_info(yaml_tag_ns='SocialGroup')
class Acquaintance(Relation):
    # People w/out much personal bond like Friend nor structured context like Colleague
    es_MX = 'Conocido'
    # color = (.6, .9, .85)
    color = (144, 196, 198)


@yaml_info(yaml_tag_ns='SocialGroup')
class FamilyMom(Family): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class FamilyDad(Family): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class FamilyNuclear(Family): pass

@yaml_info(yaml_tag_ns='SocialGroup')
class WarmshowersHospitality(ActivityHospitality, ActivityBike, Acquaintance): pass  # Host or guest via Warmshowers or similar
