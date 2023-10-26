from enum import Enum
import yaml
from yamlable import yaml_info, YamlAble
from typing import Dict, Callable
import kiwilib
import src.TimesheetGlobals as Global


class Gender(kiwilib.Aliasable, Enum, metaclass=Global.EnumABCMeta):
    # UNDEFINED = -1  # Use pd.NA for instances which are yet to be defined
    NOTAPPLICABLE = 0, 'N/A', 'N/A'   # This is for Person instances which have no gender, e.g., MultiplePeople.
    MALE          = 1, ''   , 'HOMBRE'
    FEMALE        = 2, ''   , 'MUJER'
    NONBINARY     = 3, ''   , 'NO BINARIO'

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

    def aliasFuncs(self) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        if not hasattr(type(self), '_aliasFuncs'):
            type(self)._aliasFuncs = {
               'en_US': lambda slf: slf.value[1] if slf.value[1] != '' else slf.name,
               'es_MX': lambda slf: slf.value[2],
            }
        return type(self)._aliasFuncs


class Review(kiwilib.Aliasable, Enum, metaclass=Global.EnumABCMeta):
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

    def aliasFuncs(self) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        if not hasattr(type(self), '_aliasFuncs'):
            type(self)._aliasFuncs = {
               'en_US': lambda slf: slf.value[1] if slf.value[1] != '' else slf.name,
               'es_MX': lambda slf: slf.value[2],
            }
        return type(self)._aliasFuncs


yaml.add_constructor(u'!Gender', Gender._constructor, Loader=yaml.SafeLoader)
yaml.add_representer(Gender, Gender._representer)
yaml.add_constructor(u'!Review', Review._constructor, Loader=yaml.SafeLoader)
yaml.add_representer(Review, Review._representer)


@yaml_info(yaml_tag_ns='SocialGroup')
class SocialGroup(kiwilib.HierarchicalEnum, YamlAble): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class SocialGroupUndefined(SocialGroup): pass  # Default. Marks one whose SocialGroup is not yet manually defined.
@yaml_info(yaml_tag_ns='SocialGroup')
class Relation(SocialGroup): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class Activity(SocialGroup): pass

@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityProductive(Activity): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityRecreational(Activity): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class ActivityStudy(ActivityProductive): pass
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
class WarmshowersHospitality(ActivityHospitality, ActivityBike): pass  # Host or guest through Warmshowers or similar

@yaml_info(yaml_tag_ns='SocialGroup')
class Colleague(Relation): pass  # Includes any professional, client, volunteer, etc. relationship.
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
class Family(Relation): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class Friend(Relation): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class FamilyMom(Family): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class FamilyDad(Family): pass
@yaml_info(yaml_tag_ns='SocialGroup')
class FamilyNuclear(Family, ActivityRoommate): pass

@yaml_info(yaml_tag_ns='SocialGroup')
class MultiplePeople(Relation): pass
