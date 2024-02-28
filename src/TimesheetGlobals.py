"""
Created on Jan 15, 2018

@author: Aaron

Holds all global variables, data standards, etc. needed in multiple stages of
the data analysis
"""
import enum
import os.path
import shutil
import sys
from pathlib import Path
import pickle
import time
from datetime import datetime, timedelta, date
import portion as P
from enum import Enum

from external_modules.kiwilib import IsDataclass
import i18n_l10n.internationalization as i18n
from src.TimePeriod import TimePeriod
import pandas as pd
# import numpy as np
from collections import defaultdict
from pandas.core.dtypes.inference import is_list_like
from typing import Union, List, Iterable, Dict, Tuple, Set, Callable, NamedTuple, Type
from dataclasses import dataclass
import abc


####################
# Project Constants#
####################
PREFIX_PHASE = ('Raw', 'FM', 'PP', 'DC', 'VS')  # File prefixes by project phase
PERSISTENT_PHRASE = '_Persistent'
NULL_FIELD = 'NULL'  # String placeholder for empty field in CSVs
TASK_ID_EPOCH = datetime(2017, 1, 1, 0, 0, 0)
BIRTHDAY_EPOCH = datetime(1995, 10, 10, 0, 0, 0)


######################
# File Paths & Names #
######################


def rootProjectPath() -> str:
    """
    Returns string representing the root folder for this project. This is not the
    bottommost directory containing the source files.
    :return: Project file path,including final '\'
    """
    return str(Path(os.path.abspath(__file__)).parent.parent.absolute())
    # curPath = os.path.abspath(__file__)
    # rootDirName = 'Timesheet Data Analysis\\'
    # return curPath.split(rootDirName)[0] + rootDirName


sys.path.append(rootProjectPath())
sys.path.append(os.path.join(rootProjectPath(), 'external_modules'))
from external_modules import kiwilib


def PPPath():
    return os.path.join(rootProjectPath(), 'PP_Persistent')


def VSPath():
    return os.path.join(rootProjectPath(), 'VS_Figures')


def getFileNameByTasks(startTask, endTask, phaseFlag):
    # Returns string for std filename given 2 task objects
    TP = startTask.spanningTimePeriod(endTask)
    return getFileName(TP, phaseFlag)


def getFileName(TP, phaseFlag):
    # Returns string for std filename for a TimePeriod and phaseFlag
    return PREFIX_PHASE[phaseFlag] + '_' + TP.start.strftime('%Y-%m-%d-%H%M_') + TP.end.strftime('%Y-%m-%d-%H%M')


def writePersistent(df: Union[pd.DataFrame, list], phaseFlag: int, fileSuffix='', **kwargs) -> str:
    """
    Writes a dataframe to persistent storage. Currently uses pickle filetype
    :param df: Dataframe, TimesheetDataset, or GraphicExhibit whose data to write
    :param phaseFlag: Encoding of the most recently completed data processing phase. See PREFIX_PHASE for options.
    :param fileSuffix: Suffix to be added to the end of the filename.
    :return: Full path of the file just written
    """

    def getPersistentFilePath(fileName, phaseFlag):
        # Returns the path for the given file according to standard directory org
        # return rootProjectPath() + PREFIX_PHASE[phaseFlag] + PERSISTENT_PHRASE + '\\' + fileName
        return os.path.join(rootProjectPath(), PREFIX_PHASE[phaseFlag] + PERSISTENT_PHRASE, fileName)

    def getPersistentFileName(df: pd.DataFrame, phaseFlag: int) -> str:
        """
        Returns string for the persistent filename given a df and the phase according to TimePeriod naming conventions
        :param df:
        :param phaseFlag: See Global.PREFIX_PHRASE
        :return:
        """
        #     df.sort_values('id')
        #     start = df.head(1).loc[:,'start'].values[0].astype(datetime)
        start = kiwilib.dt64_2_dt(df.head(1).loc[:, 'start'].values[0])
        end = kiwilib.dt64_2_dt(df.tail(1).loc[:, 'end'].values[0])
        return getFileName(TimePeriod(start, end), phaseFlag)

    # from src.TimesheetDataset import TimesheetDataset
    # if obj.__class__ == TimesheetDataset:
    #     df = obj.timesheetdf.df
    # else: df = obj
    if phaseFlag != 4:
        name = getPersistentFileName(df, phaseFlag)
        path = getPersistentFilePath(name, phaseFlag) + fileSuffix + '.pkl'
        pd.to_pickle(df, path)
        return path
    else:
        privacyPaths = {
        Privacy.PUBLIC : '_PUBL',
        Privacy.FRIENDS: '_FRND',
        Privacy.PRIVATE: '_PRIV',
        }
        name1 = 'figs' + privacyPaths[kwargs['privacy']] + pd.Timestamp.now().strftime('_%Y-%m-%d_%H-%M')
        name2 = 'figs' + privacyPaths[kwargs['privacy']]
        path1 = getPersistentFilePath(name1, phaseFlag) + fileSuffix + '.pkl'
        path2 = getPersistentFilePath(name2, phaseFlag) + fileSuffix + '.pkl'
        with open(path1, 'wb') as file:
            pickle.dump(df, file, protocol=-1)
        shutil.copyfile(path1, path2)
        return path2


##############
# Enum Fields#
##############
class Colored(kiwilib.DataclassValuedEnum):
    @staticmethod
    def _get_dataclass() -> IsDataclass:
        @dataclass(frozen=True)
        class Color:
            color: Tuple[int, int, int] = 128, 128, 128
        return Color

    @property
    def color_hex(self) -> str:
        """Hexadecimal string representation of the float color tuple."""
        if isinstance(self.color[0], int):
            return "#{0:02x}{1:02x}{2:02x}".format(*self.color)
        else:
            return "#{0:02x}{1:02x}{2:02x}".format(*[max(0, min(round(x * 256), 255)) for x in self.color])


class ColoredAliasable(Colored, i18n.AliasableEnum):
    @classmethod
    def _get_dataclass(cls) -> kiwilib.IsDataclass:
        @dataclass(frozen=True)
        class ColoredAliasableDataclass(Colored.dataclass, i18n.AliasableEnum.dataclass): pass
        return ColoredAliasableDataclass


class TestColor(Colored, i18n.AliasableEnum):
    RED = enum.auto()
    GREEN = enum.auto()

    @staticmethod
    def _get_dataclass() -> IsDataclass:
        @dataclass(frozen=True)
        class ColoredAliasableEnum(Colored.dataclass, i18n.AliasableEnum.dataclass): pass
        return ColoredAliasableEnum

    @classmethod
    def _enum_data(cls) -> Dict[Enum, 'c']:
        c = cls.dataclass
        return {
            cls.RED: c(
                color=(255, 0, 0),
                en_US='',
                es_MX='ROJO'
            ),
            cls.GREEN: c(
                color=(0, 255, 0),
                # es_MX='VERDE'
            ),
        }


class ColumnEnum(abc.ABC):
    """Marks association of child classes to a string column name of a TimesheetDF"""
    @staticmethod
    @abc.abstractmethod
    def dfcolumn() -> str:
        raise NotImplementedError('dfcolumn() not implemented in child class')

    @classmethod
    def getColumnClassDict(cls):
        return {leaf: leaf.dfcolumn() for leaf in kiwilib.leafClasses(cls)}


class SingleInstanceColumn(ColumnEnum):
    """Marks dtypes in columns which only ever have exactly 1 instance of the class in a TimesheetDF row"""
    @staticmethod
    @abc.abstractmethod
    def dfcolumn() -> str:
        raise NotImplementedError('dfcolumn() not implemented in child class')


class ListColumn(ColumnEnum):
    """Marks dtypes in TsDF columns whose top-level contents are a list of ListColumn subclass instances"""
    @staticmethod
    @abc.abstractmethod
    def dfcolumn() -> str:
        raise NotImplementedError('dfcolumn() not implemented in child class')


class Metaproject(SingleInstanceColumn, ColoredAliasable):
    #     Each project falls into a metaproject category y default, though that broad assumption is refined in DC
    def __le__(self, other):
        return self.id <= other.id

    def __lt__(self, other):
        return self.id < other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __gt__(self, other):
        return self.id > other.id

    @property
    def id(self):
        return self.value

    @classmethod
    def idMap(cls):
        # TODO: refactor and delete this unnecessary method. Just replace Metaproject.idMap[id] with Metaproject(id)
        if not hasattr(cls, '_idMap'):
            cls._idMap = {a.id: a for a in cls}
        return cls._idMap

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        return {
               'en_US': lambda slf: slf.en_US,
               'es_MX': lambda slf: slf.name.replace('_', ' '),
            }

    @staticmethod
    def dfcolumn() -> str:
        return 'metaproject'

    SIN_DATOS = -1
    CARRERA = 0
    ACADEMICO = 1
    LOGISTICA = 2
    RECREO = 3
    DORMIR = 4

    @classmethod
    def _enum_data(cls) -> Dict[Enum, 'Type[DataclassValuedEnum]._DATACLASS']:
        c = cls.dataclass
        return {
            cls.SIN_DATOS: c(
                color=(181, 181, 181),
                en_US='NO DATA'
                             ),
            cls.CARRERA: c(
                color=(220, 60, 40),
                en_US='CAREER'
                           ),
            cls.ACADEMICO: c(
                color=(60, 160, 30),
                en_US='ACADEMICS'
                             ),
            cls.LOGISTICA: c(
                color=(120, 200, 190),
                en_US='LOGISTICS'
                             ),
            cls.RECREO: c(
                color=(0, 220, 250),
                en_US='RECREATION'
                          ),
            cls.DORMIR: c(
                color=(20, 40, 140),
                en_US='SLEEP'
                          ),
        }


class Project(SingleInstanceColumn, ColoredAliasable):
    #     Project = (project id, metaproject id)

    @staticmethod
    def dfcolumn() -> str:
        return 'project'

    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __gt__(self, other):
        return self.value > other.value

    def defaultMetaproject(self) -> Metaproject:
        return Metaproject(self.default_metaproject)

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        return {
           'en_US': lambda slf: slf.en_US if slf.en_US != '' else slf.name.replace('_', ' '),
           'es_MX': lambda slf: slf.name.replace('_', ' ') if slf.es_MX == '' else slf.es_MX,
        }

    @staticmethod
    def _get_dataclass() -> kiwilib.IsDataclass:
        @dataclass(frozen=True)
        class ProjectDC(ColoredAliasable.dataclass):
            default_metaproject: int = 0  # Default Metaproject initially assigned to tasks with this project.
        return ProjectDC

    SIN_DATOS                               =  0
    MAE_5700                                =  1
    MAE_5730                                =  2
    MAE_5780                                =  3
    SYSEN_5220                              =  4
    SYSEN_5220_CALIFICACIÓN                 =  5
    SYSEN_5220_C                            =  5
    MENG_PROYECTO                           =  6
    MENG                                    =  6
    TRANSPORTE                              =  7
    ERRANDS_AFUERAS                         =  8
    ERRANDS                                 =  8
    CARRERA                                 =  9
    TAREAS_DOMÉSTICAS                       = 10
    TAREAS                                  = 10
    EMAIL_Y_LOGÍSTICA                       = 11
    EMAIL                                   = 11
    COMER_VESTIRSE_U_HIGIENE                = 12
    COMER                                   = 12
    RECREO_SOCIAL                           = 13
    RECREO_ELECTRÓNICO                      = 14
    RECREO_E                                = 14
    RECREO_MISC                             = 15
    TRABAJO_MISC                            = 16
    DORMIR                                  = 17
    RECREO_LEER                             = 18
    MAE_6060                                = 19
    MAE_5710                                = 20
    MAE_6780                                = 21
    MAE_2030_TA                             = 22
    CLASES_EXTRAS                           = 23
    CARRERA_ENTRENAMIENTO_DISCRECIONAL      = 24
    CARRERA_ED                              = 24
    CARRERA_ENTRENAMIENTO_MANDATORIO        = 25
    CARRERA_EM                              = 25
    CARRERA_OMPS                            = 26
    CARRERA_OPIR                            = 27
    ACADÉMICO                               = 28
    ACADEMICO                               = 28
    TIMESHEET_ANÁLISIS                      = 29
    TIMESHEET                               = 29
    PÉNDULO_INVERTIDO                       = 30
    PENDULO                                 = 30
    TAMBORES                                = 31
    OPIR_INGENIERÍA_DE_SISTEMAS_MECÁNICOS   = 32
    OPIR_ISM                                = 32
    OPIR_OTA_OPTOMECÁNICA_DISEÑO_Y_ANÁLISIS = 33
    OPIR_OTA                                = 33
    OPIR_PRB_DISEÑO_Y_ANÁLISIS              = 34
    OPIR_PRB                                = 34
    CARRERA_MENTOR_DE_PASANTÍA              = 35
    CARRERA_MENTOR                          = 35
    OPIR_PDR                                = 36
    OPIR_CDR                                = 37
    OPIR_ARQUITECTURA_DE_SISTEMAS           = 38
    OPIR_ARQ                                = 38
    OPIR_PROPÓSITO_ACÚSTICO                 = 39
    OPIR_ACUSTICO                           = 39
    OPIR_ICU                                = 40
    OPIR_OTA_SUSTITUTA_DE_LENTE             = 41
    OPIR_OTA_SL                             = 41
    OPIR_RADIADOR_ANÁLISIS_ESTRUCTURAL      = 42
    OPIR_RADIADOR                           = 42
    OPIR_GSE_AI_T                           = 43
    OPIR_GSE_AIT                            = 43
    OPIR_GSE_SOC                            = 44
    NGP                                     = 45
    NGP_STOP                                = 46
    NGP_OTA                                 = 47
    NGP_ESTRUCTURA                          = 48
    OPIR_B1_OTA                             = 49
    CS_AUTOAPRENDIZAJE                      = 50
    CS                                      = 50
    MÚSICA                                  = 51
    MUSICA                                  = 51
    BAJO                                    = 52
    CICLISMO                                = 53
    ESCRITURA_Y_VÍDEOS                      = 54
    ESCRITURA                               = 54
    MAE_4060                                = 55
    EA_COMUNIDAD                            = 56
    EA                                      = 56
    AISC                                    = 57

    @classmethod
    def _enum_data(cls) -> Dict[Enum, 'Type[DataclassValuedEnum]._DATACLASS']:
        c = cls.dataclass
        return {
            cls.SIN_DATOS     : c(default_metaproject=-1,en_US='NO DATA'                  , es_MX=''),
            cls.MAE_5700      : c(default_metaproject=1, en_US=''                         , es_MX=''),
            cls.MAE_5730      : c(default_metaproject=1, en_US=''                         , es_MX=''),
            cls.MAE_5780      : c(default_metaproject=1, en_US=''                         , es_MX=''),
            cls.SYSEN_5220    : c(default_metaproject=1, en_US=''                         , es_MX=''),
            cls.SYSEN_5220_C  : c(default_metaproject=1, en_US='SYSEN 5220 GRADING'       , es_MX=''),
            cls.MENG_PROYECTO : c(default_metaproject=1, en_US='MENG PROJECT'             , es_MX=''),
            cls.MENG          : c(default_metaproject=1, en_US='MENG PROJECT'             , es_MX=''),
            cls.TRANSPORTE    : c(default_metaproject=2, en_US='TRANSPORT'                , es_MX=''),
            cls.ERRANDS       : c(default_metaproject=2, en_US='ERRANDS'                  , es_MX='MANDADOS'),
            cls.CARRERA       : c(default_metaproject=0, en_US='CAREER'                   , es_MX=''),
            cls.TAREAS        : c(default_metaproject=2, en_US='HOUSEHOLD CHORES'         , es_MX=''),
            cls.EMAIL         : c(default_metaproject=2, en_US='EMAIL & LOGISTICS'        , es_MX=''),
            cls.COMER         : c(default_metaproject=2, en_US='EAT DRESS & HYGIENE'      , es_MX=''),
            cls.RECREO_SOCIAL : c(default_metaproject=3, en_US='SOCIAL FUN'               , es_MX=''),
            cls.RECREO_E      : c(default_metaproject=3, en_US='SCREEN TIME FUN'          , es_MX=''),
            cls.RECREO_MISC   : c(default_metaproject=3, en_US='MISC FUN'                 , es_MX=''),
            cls.TRABAJO_MISC  : c(default_metaproject=1, en_US='MISC WORK'                , es_MX=''),
            cls.DORMIR        : c(default_metaproject=4, en_US='SLEEP'                    , es_MX=''),
            cls.RECREO_LEER   : c(default_metaproject=3, en_US='READ'                     , es_MX=''),
            cls.MAE_6060      : c(default_metaproject=1, en_US=''                         , es_MX=''),
            cls.MAE_5710      : c(default_metaproject=1, en_US=''                         , es_MX=''),
            cls.MAE_6780      : c(default_metaproject=1, en_US=''                         , es_MX=''),
            cls.MAE_2030_TA   : c(default_metaproject=1, en_US=''                         , es_MX=''),
            cls.CLASES_EXTRAS : c(default_metaproject=1, en_US='EXTRA CLASSES'            , es_MX=''),
            cls.CARRERA_ED    : c(default_metaproject=0, en_US='DISCRETIONARY TRAINING'   , es_MX='ENTRENAMIENTO DISCRECIONAL'),
            cls.CARRERA_EM    : c(default_metaproject=0, en_US='MANDATORY TRAINING'       , es_MX='ENTRENAMIENTO MANDATORIO'),
            cls.CARRERA_OMPS  : c(default_metaproject=0, en_US='BALL OMPS'                , es_MX='BALL OMPS'),
            cls.CARRERA_OPIR  : c(default_metaproject=0, en_US='BALL OPIR'                , es_MX='BALL OPIR'),
            cls.ACADEMICO     : c(default_metaproject=1, en_US='ACADEMICS'                , es_MX=''),
            cls.TIMESHEET     : c(default_metaproject=1, en_US='LIFELOG PROJECT'          , es_MX='REGISTRO DE VIDA'),
            cls.PENDULO       : c(default_metaproject=1, en_US='INVERTED PENDULUM'        , es_MX=''),
            cls.TAMBORES      : c(default_metaproject=3, en_US='DRUMS'                    , es_MX=''),
            cls.OPIR_ISM      : c(default_metaproject=0, en_US='OPIR MECHANICAL SYSTEMS'  , es_MX='OPIR SISTEMAS MECÁNICOS'),
            cls.OPIR_OTA      : c(default_metaproject=0, en_US='OPIR OTA'                 , es_MX='OPIR OTA'),
            cls.OPIR_PRB      : c(default_metaproject=0, en_US='OPIR PRB'                 , es_MX='OPIR PRB'),
            cls.CARRERA_MENTOR: c(default_metaproject=0, en_US='INTERN MENTORSHIP'        , es_MX='MENTOR DE PASANTÍA'),
            cls.OPIR_PDR      : c(default_metaproject=0, en_US='OPIR PDR'                 , es_MX=''),
            cls.OPIR_CDR      : c(default_metaproject=0, en_US='OPIR CDR'                 , es_MX=''),
            cls.OPIR_ARQ      : c(default_metaproject=0, en_US='OPIR SYSTEMS ARCHITECTURE', es_MX=''),
            cls.OPIR_ACUSTICO : c(default_metaproject=0, en_US='OPIR ACOUSTIC PROPOSAL'   , es_MX=''),
            cls.OPIR_ICU      : c(default_metaproject=0, en_US='OPIR ICU'                 , es_MX=''),
            cls.OPIR_OTA_SL   : c(default_metaproject=0, en_US='OPIR LENS SURROGATE'      , es_MX='OPIR SUSTITUTA DE LENTE'),
            cls.OPIR_RADIADOR : c(default_metaproject=0, en_US='OPIR RADIATOR'            , es_MX='OPIR RADIADOR'),
            cls.OPIR_GSE_AIT  : c(default_metaproject=0, en_US='OPIR GSE AI&T'            , es_MX='OPIR GSE AI&T'),
            cls.OPIR_GSE_SOC  : c(default_metaproject=0, en_US=''                         , es_MX=''),
            cls.NGP           : c(default_metaproject=0, en_US=''                         , es_MX=''),
            cls.NGP_STOP      : c(default_metaproject=0, en_US=''                         , es_MX=''),
            cls.NGP_OTA       : c(default_metaproject=0, en_US=''                         , es_MX=''),
            cls.NGP_ESTRUCTURA: c(default_metaproject=0, en_US='NGP STRUCTURE'            , es_MX=''),
            cls.OPIR_B1_OTA   : c(default_metaproject=0, en_US=''                         , es_MX=''),
            cls.CS            : c(default_metaproject=1, en_US='CS SELF-TEACHING'         , es_MX=''),
            cls.MUSICA        : c(default_metaproject=3, en_US='MUSIC'                    , es_MX=''),
            cls.BAJO          : c(default_metaproject=3, en_US='BASS'                     , es_MX=''),
            cls.CICLISMO      : c(default_metaproject=3, en_US='CYCLING'                  , es_MX=''),
            cls.ESCRITURA     : c(default_metaproject=3, en_US='WRITING AND VIDEOS'       , es_MX=''),
            cls.MAE_4060      : c(default_metaproject=1, en_US=''                         , es_MX=''),
            cls.EA_COMUNIDAD  : c(default_metaproject=1, en_US='EA COMMUNITY'             , es_MX=''),
            cls.EA            : c(default_metaproject=1, en_US='EA COMMUNITY'             , es_MX=''),
            cls.AISC          : c(default_metaproject=0, en_US='AI SAFETY CAMP'           , es_MX='CAMPAMENTO DE LA SEGURIDAD DE IA'),
        }


# noinspection NonAsciiCharacters
class Tag(ListColumn, ColoredAliasable):
    @staticmethod
    def dfcolumn() -> str:
        return 'tags'

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        return {
           'en_US': lambda slf: slf.en_US if slf.en_US != '' else slf.name.replace('_', ' '),
           'es_MX': lambda slf: slf.es_MX if slf.es_MX != '' else slf.name.replace('_', ' '),
        }

    BICI               =  1
    COLECTIVO          =  2
    ELECTRÓNICA        =  3
    ELEC               =  3
    EN_CLASE           =  4
    FAMILIA            =  5
    HW                 =  6
    LECTURA            =  7
    NETFLIX            =  8
    NFL                =  9
    PAPEL              = 10
    PIE                = 11
    PROYECTO_ACADÉMICO = 12
    PROYECTO_A         = 12
    RUTINA             = 13
    SOCIAL_GRUPO       = 14
    SOCIAL             = 14
    EJERCICIO          = 15
    COMER              = 16
    AUTO               = 17
    BICI_ELÉCTRICA     = 18
    BICI_E             = 18
    PODCAST            = 19
    MÚSICA             = 20
    MUSICA             = 20
    TREN               = 21
    AVIÓN              = 22

    @classmethod
    def _enum_data(cls) -> Dict[Enum, 'Type[DataclassValuedEnum]._DATACLASS']:
        c = cls.dataclass
        return {
            cls.BICI : c(es_MX='', en_US='BIKE'),
            cls.COLECTIVO : c(es_MX='', en_US='BUS'),
            cls.ELEC : c(es_MX='TIEMPO DE PANTALLA', en_US='SCREEN TIME'),
            cls.EN_CLASE : c(es_MX='', en_US='IN CLASS'),
            cls.FAMILIA : c(es_MX='', en_US='FAMILY'),
            cls.HW : c(es_MX='TAREA', en_US= 'HOMEWORK'),
            cls.LECTURA : c(es_MX='', en_US='READING'),
            cls.NETFLIX : c(es_MX='TV/PELÍCULA', en_US='TV/MOVIE'),
            cls.NFL : c(es_MX='', en_US='NFL'),
            cls.PAPEL : c(es_MX='', en_US='PAPER'),
            cls.PIE : c(es_MX='', en_US='WALK'),
            cls.PROYECTO_A : c(es_MX='', en_US='ACADEMIC PROJECT'),
            cls.RUTINA : c(es_MX='', en_US='ROUTINE'),
            cls.SOCIAL : c(es_MX='SOCIAL', en_US='SOCIAL'),
            cls.EJERCICIO : c(es_MX='', en_US='EXERCISE'),
            cls.COMER : c(es_MX='', en_US='EATING'),
            cls.AUTO : c(es_MX='', en_US='CAR'),
            cls.BICI_E : c(es_MX='', en_US='E-BIKE'),
            cls.PODCAST : c(es_MX='', en_US='PODCAST'),
            cls.MUSICA : c(es_MX='', en_US='MUSIC'),
            cls.TREN : c(es_MX='', en_US='TRAIN'),
            cls.AVIÓN : c(es_MX='', en_US='AIRPLANE'),
        }


class Epoch(SingleInstanceColumn, ColoredAliasable):
    """
    Enum class to define all the global significant dates marking transitions.
    These dates are here called epochs, and are used in VS for analysis considering different periods of life
    """

    @staticmethod
    def dfcolumn() -> str:
        return 'epoch'

    @classmethod
    def sortedIter(cls) -> list:
        """
        Returns a list of epochs sorted by date,
        useful for iterating or faster evaluation of what epoch period some datetime is in
        :return: List of Epoch enums sorted chronologically
        """
        if not hasattr(cls, '_srted'):
            cls._srted = sorted(cls._member_map_.values(), key=lambda x: x.dt())
        return cls._srted

    def __le__(self, other):
        if isinstance(other, Epoch):
            return self.dt() <= other.dt()
        return self.dt() <= other

    def __lt__(self, other):
        if isinstance(other, Epoch):
            return self.dt() < other.dt()
        return self.dt() < other

    def __ge__(self, other):
        if isinstance(other, Epoch):
            return self.dt() >= other.dt()
        return self.dt() >= other

    def __gt__(self, other):
        if isinstance(other, Epoch):
            return self.dt() > other.dt()
        return self.dt() > other

    def __str__(self):
        return f'{self.name}: {self.dt().strftime("%Y-%m-%d %H:%M")}'

    def dt(self) -> datetime:
        """Returns the datetime object for a given Epoch instance"""
        return self.start

    def id(self) -> int:
        """Returns the id for a given Epoch instance"""
        return self.value

    @staticmethod
    def _get_dataclass() -> kiwilib.IsDataclass:
        @dataclass(frozen=True)
        class EpochDataClass(ColoredAliasable.dataclass):
            start: datetime = NotImplemented  # Sentinel value, must define, but can't enforce it in Python 3.8 dataclasses
        return EpochDataClass

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        return {
           'en_US': lambda slf: slf.en_US if slf.en_US != "" else slf.name[1:].replace('_', ' '),
           'es_MX': lambda slf: slf.es_MX if slf.es_MX != "" else slf.name[1:].replace('_', ' '),
        }
        
    eEND =                    0
    e2017_Cornell =           1
    e2017_Winter =            2
    e2018_Cornell =           3
    e2018_Interim =           4
    e2018_Boulder_Solo =      5
    e2018_Boulder_Padraig =   6
    e2018_BCH =               7
    e2019_Tour_Start =        8
    e2019_Tour_End =          9
    e2020_WFH =               10
    e2020_Boulder_Dip =       11
    e2021_COVID_Ease =        12
    e2021_Tour_Start =        13
    e2021_Tour_End =          14
    e2022_Tour_Start =        15
    e2022_Suzie_Start =       16
    e2022_Suzie_End =         17
    e2022_Alexandre_Start =   18
    e2022_Alexandre_End =     19
    e2022_Tim_Start =         20
    e2022_Tim_End =           21
    e2022_USA_Friends_Start = 22
    e2022_USA_Friends_End =   23
    e2022_Tour_End =          24
    e2020_Tech_Start =        25
    e2020_Tech_End =          26
    e2022_Europe_Start =      27
    e2022_MEX_GER_TZ_SHIFT =  28
    e2022_ESP_USA_TZ_SHIFT =  29
    e2023_EA_Discovery =      30
    e2019_SpChg_Glenn_End =   31
    e2019_SpChg_Alex_End =    32
    e2019_SpChg_Nick_End =    33
    e2021_SpChg_KO_Start =    34
    e2022_SpChg_JW_KS_Start = 35
    e2024_AISC =              36
    e2018_Data_Log_Person =   37
    
    @classmethod
    def _enum_data(cls) -> Dict[Enum, 'Type[DataclassValuedEnum]._DATACLASS']:
        c = cls.dataclass
        return {
            cls.eEND:                    c(start=datetime(2025, 1, 1, 0, 0), es_MX='FIN'),
            cls.e2017_Cornell:           c(start=datetime(2017, 9, 6, 0, 0), es_MX='2017 Cornell'), # Start of data collection
            cls.e2017_Winter:            c(start=datetime(2017, 12, 13, 9, 36), es_MX='2017 Invierno'), # Start winter break
            cls.e2018_Cornell:           c(start=datetime(2018, 1, 12, 21, 58), es_MX='2018 Cornell'), # Start semester
            cls.e2018_Interim:           c(start=datetime(2018, 5, 22, 3, 0), es_MX='2018 Interregno'), # End of finals, before CO move
            cls.e2018_Boulder_Solo:      c(start=datetime(2018, 6, 18, 3, 0), es_MX='2018 Boulder Solo'), # I move to Boulder
            cls.e2018_Boulder_Padraig:   c(start=datetime(2018, 8, 24, 3, 0), es_MX='2018 Boulder Padraig'), # Padraig moves in
            cls.e2018_BCH:               c(start=datetime(2018, 10, 28, 0, 0), es_MX='2018 BCH'), # Office move to BCH
            cls.e2019_Tour_Start:        c(start=datetime(2019, 8, 4, 7, 19), es_MX='2019 Inicio de Gira'), # 2019 tour start
            cls.e2019_Tour_End:          c(start=datetime(2019, 8, 13, 12, 17), es_MX='2019 Fin de Gira'), # 2019 tour end
            cls.e2020_WFH:               c(start=datetime(2020, 3, 18, 0, 0), es_MX='2020 Teletrabajo'), # Start WFH
            cls.e2020_Boulder_Dip:       c(start=datetime(2020, 3, 29, 18, 42), es_MX='2020 Boulder Dip'), # Dip move to CO
            cls.e2021_COVID_Ease:        c(start=datetime(2021, 4, 10, 0, 0), es_MX='2021 Alivio de COVID'), # Ease of COVID restrictions
            cls.e2021_Tour_Start:        c(start=datetime(2021, 8, 11, 7, 14), es_MX='2021 Inicio de Gira'), # 2021 tour start
            cls.e2021_Tour_End:          c(start=datetime(2021, 8, 21, 12, 46), es_MX='2021 Fin de Gira'), # 2021 tour end
            cls.e2022_Tour_Start:        c(start=datetime(2022, 1, 7, 18, 7), es_MX='2022 Inicio de Gira'), # 2022 tour start
            cls.e2022_Suzie_Start:       c(start=datetime(2022, 3, 12, 19, 13), es_MX='2022 Inicio con Suzie'), # Start Suzie
            cls.e2022_Suzie_End:         c(start=datetime(2022, 3, 25, 15, 34), es_MX='2022 Fin con Suzie'), # ENd SVF
            cls.e2022_Alexandre_Start:   c(start=datetime(2022, 6, 4, 9, 7), es_MX='2022 Inicio con Alexandre'), # Start ride  w/ Alexandre
            cls.e2022_Alexandre_End:     c(start=datetime(2022, 6, 11, 7, 52), es_MX='2022 Fin con Alexandre'), # End ride w/ Alexandre
            cls.e2022_Tim_Start:         c(start=datetime(2022, 7, 10, 14, 58), es_MX='2022 Inicio con Tim'), # Start TIm Sprinz
            cls.e2022_Tim_End:           c(start=datetime(2022, 7, 12, 5, 5), es_MX='2022 Fin con Tim'), # End Tim Sprinz, or really Lars
            cls.e2022_USA_Friends_Start: c(start=datetime(2022, 9, 14, 16, 54), es_MX='2022 Inicio con amigos de EEUU'), # Start BFish+
            cls.e2022_USA_Friends_End:   c(start=datetime(2022, 9, 21, 10, 33), es_MX='2022 Fin con amigos de EEUU'), # End BFish+
            cls.e2022_Tour_End:          c(start=datetime(2022, 12, 15, 10, 10), es_MX='2022 Fin de Gira'), # 2022 tour end
            cls.e2020_Tech_Start:        c(start=datetime(2020, 9, 19, 20, 35), es_MX='2020 Inicio con Tech'),# Tech arrival in CO
            cls.e2020_Tech_End:          c(start=datetime(2020, 11, 1, 8, 30), es_MX='2020 Fin con Tech'),# Tech leave from CO
            cls.e2022_Europe_Start:      c(start=datetime(2022, 4, 2, 6, 9), es_MX='2022 Inicio en Europa'),# Flight CDMX >> Europe
            cls.e2022_MEX_GER_TZ_SHIFT:  c(start=datetime(2022, 4, 2, 0, 0), es_MX='2022 MEX ALE ZH CAMBIO'), # Marks time zone shift in data
            cls.e2022_ESP_USA_TZ_SHIFT:  c(start=datetime(2022, 12, 15, 7, 42), es_MX='2022 ESP EEUU ZH CAMBIO'), # Marks time zone shift in data
            cls.e2023_EA_Discovery:      c(start=datetime(2023, 4, 17, 9, 51), es_MX='2023 EA Descubrimiento'), # Podcast triggers EA interest
            cls.e2019_SpChg_Glenn_End:   c(start=datetime(2019, 4, 1, 0, 0), es_MX='2019 SpChg Fin con Glenn'), # Glenn leaves Spare Change
            cls.e2019_SpChg_Alex_End:    c(start=datetime(2019, 11, 1, 0, 0), es_MX='2019 SpChg Fin con Alex'), # Alex leaves, Steve joins Spare Change
            cls.e2019_SpChg_Nick_End:    c(start=datetime(2020, 1, 1, 0, 0), es_MX='2019 SpChg Fin con Nick'), # Nick leaves, George joins Spare Change
            cls.e2021_SpChg_KO_Start:    c(start=datetime(2021, 9, 10, 0, 0), es_MX='2021 SpChg Inicio con KO'), # Kristin joins Spare Change
            cls.e2022_SpChg_JW_KS_Start: c(start=datetime(2022, 9, 1, 0, 0), es_MX='2022 SpChg Inicio con JW KS'), # Kirsten, Jonathan join Spare Change
            cls.e2024_AISC:              c(start=datetime(2024, 1, 13, 3, 0), es_MX='2023 Campamento de Securidad de IA'), # AISC starts
            cls.e2018_Data_Log_Person:   c(start=datetime(2018, 2, 10, 3), es_MX='2018 Datos Persona'), # Data on time spent with individuals somewhat consistent
        }
# TODO: add epochs for data feature introductions
# Naps: 2021-05-05
# Overnight sleep interruptions: 2023-05-15
# People: 2017-12-??


def appendIntervalDictComplement(dct: P.IntervalDict, complementVal, bigInterval: P.IntervalDict = P.closedopen(
        Epoch.e2017_Cornell.dt(), Epoch.eEND.dt())) -> P.IntervalDict:
    # temp = P.closedopen(Epoch.e2017_Cornell.dt(), Epoch.eEND.dt())
    for interval in dct.keys():
        bigInterval = bigInterval - interval
    dct[bigInterval] = complementVal
    return dct


class EpochScheme(kiwilib.Aliasable, Enum, metaclass=kiwilib.EnumABCMeta):
    """
    Enum class containing all the global data and procedures for epoch schemes and groups.
    Each enum member is a scheme for creating a set of epoch groups.
    Schemes are to be used in VS and FC to slice and group data into various time periods for analysis
    Each scheme has a different theme:
    E.g. the primary metaproject focus of my life, separating periods of differing token conventions, etc.
    Format: scheme_name = (scheme_id, {epochGroupID: ((epochIDstart, epochIDend), ..., epochGroupName) ... })
    The tuple pairs are epoch IDs defining the start and end of multiple TImePeriods within an epochGroup
    """
    # KEY_DEFAULT_VAL = 'OTHER'  # The label to be referenced by calls to
    # IntervalDict.get(<>, default=EpochScheme.KEY_DEFAULT_VAL)
    # Effectively acts as the value for the complement of intervals defined in an EpochScheme instance

    def id(self, dt: Union[datetime, Iterable[datetime]]) -> Union[int, Iterable[int]]:
        if is_list_like(dt):
            return kiwilib.mapOverListLike(lambda x: EpochScheme.id(self, x), dt)
        return self.value[dt][0]

    def labelDT(self, dt: Union[datetime, Iterable[datetime]], locale: str = None) -> Union[str, Iterable[str]]:
        """
        String returned is dependent on the specified locale. If unspecified, self.defaultLocale() is used.
        :param dt: Datetimes to be mapped to epoch groups.
        :param locale: String representation of locale. See epochGroupAliasFuncs() for allowable locale values.
        :return: string representation of the epoch group containing dt for an EpochScheme
        """
        if locale is None:
            locale = self.defaultLocale()
        if is_list_like(dt):
            return kiwilib.mapOverListLike(lambda x: EpochScheme.labelDT(self, x, locale), dt)
        return self.epochGroupAliasFuncs()[locale](self, dt)

    def sortedEpochGroupNames(self) -> List[str]:
        if not hasattr(self, '_sortedEpochGroupNames'):
            temp = {self.labelDT(iv.lower): iv.lower for iv, names in self.value.items()}
            self._sortedEpochGroupNames: List[str] = sorted(temp.keys(), key=lambda x: temp[x])
        return self._sortedEpochGroupNames

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        if not hasattr(cls, '_aliasFuncs'):
            cls._aliasFuncs: Dict[str, Callable] = defaultdict(lambda: lambda slf: slf.name)  # Ignore language
            cls._aliasFuncs['en_US'] = lambda slf: slf.name  # Have to include >=1 key for Aliasable.defaultLocale()
        return cls._aliasFuncs

    def epochGroupAliasFuncs(self):
        def getAlias(ind: int, slf, dt: Union[datetime, date]):
            # TODO: type check and convert date and datetime. Change base method to a functools.partial of getAlias
            pass

        if not hasattr(type(self), '_epochGroupAliasFuncs'):
            type(self)._epochGroupAliasFuncs: dict[str, Callable] = {
                'en_US': lambda slf, dt: slf.value[dt][1],
                'es_MX': lambda slf, dt: slf.value[dt][2],
            }
        return self._epochGroupAliasFuncs

    INDIVIDUAL = P.IntervalDict({P.closedopen(Epoch.sortedIter()[i - 1].dt(), ep.dt()): (ep.id(), ep.name, ep.name)
                                 for i, ep in enumerate(Epoch.sortedIter()[1:])}) # TODO: modify 2nd ep.name for es_MX
    # TODO: update usage of epochGroups in VS to account for new data format
    MP_COARSE = P.IntervalDict({  # Coarse-grained metaproject and lifestyle focus, what I spend most of my attention on
        (P.closedopen(Epoch.e2017_Cornell.dt(), Epoch.e2018_Boulder_Solo.dt()) |
         P.closedopen(Epoch.e2022_Tour_End.dt(), Epoch.eEND.dt()))
        : (0, 'Academics Focus Epochs', 'Épocas Enfocados en la Académica'),
        P.closedopen(Epoch.e2022_Tour_Start.dt(), Epoch.e2022_Tour_End.dt())
        : (1, 'Recreation Focus Epochs', 'Épocas Enfocados en el Recreo'),
        P.closedopen(Epoch.e2018_Boulder_Solo.dt(), Epoch.e2022_Tour_Start.dt())
        : (2, 'Career Focus Epochs', 'Épocas Enfocados en la Carrera'),
    })
    MP_FINE = appendIntervalDictComplement(
        P.IntervalDict({  # Fine-grained metaproject and lifestyle focus, includes short bike tours, et al
            (P.closedopen(Epoch.e2017_Cornell.dt(), Epoch.e2017_Winter.dt()) |
             P.closedopen(Epoch.e2018_Cornell.dt(), Epoch.e2018_Interim.dt()) |
             P.closedopen(Epoch.e2022_Tour_End.dt(), Epoch.eEND.dt())
             ): (0, 'Academics Focus Epochs', 'Épocas Enfocados en la Académica'),
            (P.closedopen(Epoch.e2018_Boulder_Solo.dt(), Epoch.e2019_Tour_Start.dt()) |
             P.closedopen(Epoch.e2019_Tour_End.dt(), Epoch.e2021_Tour_Start.dt()) |
             P.closedopen(Epoch.e2021_Tour_End.dt(), Epoch.e2022_Tour_Start.dt())
             ): (2, 'Career Focus Epochs', 'Épocas Enfocados en la CARRERA'),
        }), complementVal=(1, 'Recreation Focus Epochs', 'Épocas Enfocados en el RECREO'))
    WORK_LOCATION = appendIntervalDictComplement(  # Where is my primary work/study location?
        P.IntervalDict({  # First set of epoch groups commonly needed for DC queries
            P.closedopen(Epoch.e2017_Cornell.dt(), Epoch.e2018_Boulder_Solo.dt())
            : (0, 'Cornell', 'Cornell'),
            P.closedopen(Epoch.e2018_Boulder_Solo.dt(), Epoch.e2018_BCH.dt())
            : (1, 'Ball Boulder', 'Ball Boulder'),
            P.closedopen(Epoch.e2018_BCH.dt(), Epoch.e2020_WFH.dt())
            : (2, 'Ball Broomfield', 'Ball Broomfield'),
            P.closedopen(Epoch.e2020_WFH.dt(), Epoch.e2022_Tour_Start.dt())
            : (3, 'WFH', 'WFH'),
        }), complementVal=(4, 'Unemployed', 'Sin Empleo'))
    SPARE_CHANGE_PERSONNEL = appendIntervalDictComplement(
        P.IntervalDict({  # Spare Change band membership
            P.closedopen(Epoch.e2018_Boulder_Solo.dt(), Epoch.e2019_SpChg_Glenn_End.dt())
            : (0, 'Spare Change with Glenn', 'Spare Change con Glenn'),
            P.closedopen(Epoch.e2019_SpChg_Glenn_End.dt(), Epoch.e2019_SpChg_Alex_End.dt())
            : (1, 'Spare Change without Glenn', 'Spare Change sin Glenn'),
            P.closedopen(Epoch.e2019_SpChg_Alex_End.dt(), Epoch.e2019_SpChg_Nick_End.dt())
            : (2, 'Spare Change with Steve on Guitar', 'Spare Change con Steve en la Guitarra'),
            P.closedopen(Epoch.e2019_SpChg_Nick_End.dt(), Epoch.e2021_SpChg_KO_Start.dt())
            : (3, 'Spare Change with George', 'Spare Change con George'),
            P.closedopen(Epoch.e2021_SpChg_KO_Start.dt(), Epoch.e2022_SpChg_JW_KS_Start.dt())
            : (4, 'Spare Change with Kristin', 'Spare Change con Kristin'),
        }), complementVal=(5, 'Spare Change with Jonathan and Kirsten', 'Spare Change con Jonathan y Kirsten'))
    MP_COARSE_ATOMIC = P.IntervalDict({  # Coarse-grained metaproject and lifestyle focus, only atomic intervals
        (P.closedopen(Epoch.e2017_Cornell.dt(), Epoch.e2018_Boulder_Solo.dt()))
        : (0, 'Grad School', 'Posgrado'),
        P.closedopen(Epoch.e2022_Tour_Start.dt(), Epoch.e2022_Tour_End.dt())
        : (1, '2022 Cycle Tour', '2022 Cicloturismo'),
        P.closedopen(Epoch.e2018_Boulder_Solo.dt(), Epoch.e2022_Tour_Start.dt())
        : (2, 'First Job', 'First Job'),
        (P.closedopen(Epoch.e2022_Tour_End.dt(), Epoch.eEND.dt()))
        : (0, '2023 Career Pivot', '2023 Cambio de CARRERA'),
    })
    # TODO: sequential life phases, like 1 but each group is only a single period: Cornell, Ball, Tour22, post-tour
    # TODO: meal 'Rutina' default groups
    # TODO: 'Casa' location groups


class Mood(SingleInstanceColumn, kiwilib.Aliasable, Enum, metaclass=kiwilib.EnumABCMeta):
    @staticmethod
    def dfcolumn() -> str:
        return 'mood'

    @property
    def id(self):
        return self.value[0]

    @classmethod
    def idMap(cls):
        if not hasattr(cls, '_idMap'):
            cls._idMap = {a.id: a for a in cls}
        return cls._idMap

    def __le__(self, other):
        if isinstance(other, Mood):
            return self.id <= other.id
        else:
            return self.id <= other

    def __lt__(self, other):
        if isinstance(other, Mood):
            return self.id < other.id
        else:
            return self.id < other

    def __ge__(self, other):
        if isinstance(other, Mood):
            return self.id >= other.id
        else:
            return self.id >= other

    def __gt__(self, other):
        if isinstance(other, Mood):
            return self.id > other.id
        else:
            return self.id > other

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        if not hasattr(cls, '_aliasFuncs'):
            cls._aliasFuncs: Dict[str, Callable] = {
               'en_US': lambda slf: slf.name,
               'es_MX': lambda slf: slf.value[1],
            }
        return cls._aliasFuncs
    
    Awful = -2, 'Horrible'
    Bad = -1, 'Malo'
    Neutral = 0, 'Neutral'
    Happy = 1, 'Contento'
    Overjoyed = 2, 'Extático'

# Map raw string input to encoded data storage value 
MOOD_RAW_STRINGS = {'Very Bad': -2,
                    'Bad': -1,
                    '-': 0,
                    'Normal': 1,
                    'Good': 2,  # Output from app, English
                    'Muy malo': -2,  # Output from app, Spanish
                    'Malo': -1,
                    '-': 0,
                    'Normal': 1,
                    'Bueno': 2}  # Output from app


####################
# Standard Columns #
####################
"""Each of these sets of columns lists the standard set of columns produced at the conclusion of that phase"""
RAW_COLUMN_STRINGS = ('Date', 'Start time', 'End time',
                      'rel. Duration', 'Project', 'Tags', 'Description', 'Feeling')
# At some point, Timesheet.io app updated to export column titles in the app selected language
RAW_COLUMN_STRINGS_2 = ('Fecha', 'Tiempo de Inicio', 'Tiempo fianl', 'Duracion real.',
                        'Proyecto', 'Etiquetas', 'Descripcion', 'Sentimiento')
FM_COLUMN_STRINGS = ('Date', 'Start time', 'End time', 'Duration'
                     , 'Project', 'Tags', 'Description', 'Mood')
# If adding more Collectible columns later, add between 'location' and 'media'
PP_COLUMN_STRINGS = ('id', 'start', 'end', 'duration', 'project', 'tags', 'description', 'epoch', 'mood',
                     'circad', 'metaproject', 'bodyparts', 'location', 'person', 'food', 'subjectmatter', 'media')

# From PP onward, these indices apply to all base df's
IND_id = PP_COLUMN_STRINGS.index('id') - 1
IND_start = PP_COLUMN_STRINGS.index('start') - 1
IND_end = PP_COLUMN_STRINGS.index('end') - 1
IND_duration = PP_COLUMN_STRINGS.index('duration') - 1
IND_project = PP_COLUMN_STRINGS.index('project') - 1
IND_tags = PP_COLUMN_STRINGS.index('tags') - 1
IND_description = PP_COLUMN_STRINGS.index('description') - 1
IND_epoch = PP_COLUMN_STRINGS.index('epoch') - 1
IND_mood = PP_COLUMN_STRINGS.index('mood') - 1
IND_circad = PP_COLUMN_STRINGS.index('circad') - 1


class Privacy(Enum):
    """
    Defines the privacy level of an analysis run or an individual visualization. Used mostly in Visualize.py.
    """
    def __lt__(self, other):
        if type(self) is type(other):
            return self.value < other.value
        raise NotImplementedError

    def __gt__(self, other):
        if type(self) is type(other):
            return self.value > other.value
        raise NotImplementedError

    def __le__(self, other):
        if type(self) is type(other):
            return self.value <= other.value
        raise NotImplementedError

    def __ge__(self, other):
        if type(self) is type(other):
            return self.value == other.value
        raise NotImplementedError

    PUBLIC = 0
    FRIENDS = 1
    PRIVATE = 2


class DataEntryException(Exception): pass

########################
# Dataframe Operations #
########################

def getDF(stdListList, phaseFlag: int) -> pd.DataFrame:
    """
    Returns a df given a list of lists in std format of some phase. Supports partial
    input datasets using the first n columns of the XX_COLUMN_STRINGS tuple
    :param phaseFlag: Encoding of what columns the df should have, as encoded in colMap. Depends on the processing phase
    :param stdListList: A list of lists representing 2D Task data.
    Outer index indexes each Task, and inner index are the columns of data.
    Column assignments are standardized by XX_COLUMN_STRINGS
    """
    colMap: Dict = {
        0: RAW_COLUMN_STRINGS,
        1: FM_COLUMN_STRINGS,
        2: PP_COLUMN_STRINGS
    }
    if phaseFlag in colMap.keys():
        strs: List = colMap[phaseFlag]
    else:
        exit('Invalid phaseFlag for column list selection')
    df = pd.DataFrame(stdListList, columns=strs[0:len(stdListList[0])])  # OK if some columns not present in stdListList
    if phaseFlag >= 2:
        df = df.set_index(strs[0])
    df = df[~df.index.duplicated(keep='first')]  # Removes rare duplicate indices
    return df


def getTaskID(start: datetime, end: datetime) -> int:
    """
    Generates an ID for a task based on its start time and duration.
    Duration only necessary to discriminate between tasks with identical start fields.
    This is a possible result from logging mistakes, duration==0 tasks in the dataset, etc.
    The ID may be used for sorting purposes, but does not represent accurate duration encoding.
    The ID is not guaranteed to encode accurately the start datetime, merely good enough for sorting.
    :param start: Task start datetime
    :param end: Task end datetime
    :return: int Task ID which may be used for sorting chronologically
    """
    #         return int(start.strftime('%y%m%d%H%M')+end.strftime('%M'))
    minEpoch = int((start - TASK_ID_EPOCH).total_seconds() / 60)
    minDur = int((end - start).total_seconds() / 60)  # int duration in minutes
    if minDur > 2:
        durCode = 9  # Only 1 digit used to discriminate on duration.
    else:
        durCode = minDur % 10  # Either 9 for long durations, 0 or 1 or 2 for tasks w/ duration 0, 1 or 2 minutes.
    return int("{0}{num:1d}".format(minEpoch, num=durCode))


def taskID2datetime(tid: int) -> datetime:
    """ Extracts the start datetime from a task ID created from getTaskID(). """
    return TASK_ID_EPOCH + timedelta(minutes=tid // 10)


def timedelta2taskID(td: timedelta) -> int:
    """
    Represents a timedelta as an int as a taskID represents the difference between the task start and TASK_ID_EPOCH.
    The difference of 2 taskIDs will be approximately equal (round the least significant digit) to the return value
    when the starts of each task represented by the taskIDs are separated by timedelta td.
    :param td: Usefulness degrades for td !>> 10 minutes
    """
    # return getTaskID(TASK_ID_EPOCH + td, TASK_ID_EPOCH + td + timedelta(minutes=1))
    return int(td.total_seconds() / 6)