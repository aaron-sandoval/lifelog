"""
Created on Jan 15, 2018

@author: Aaron

Holds all global variables, data standards, etc. needed in multiple stages of
the data analysis
"""
import os.path
import shutil
import sys
from pathlib import Path
import pickle
import time
from datetime import datetime, timedelta
import portion as P
from enum import Enum
from src.TimePeriod import TimePeriod
import pandas as pd
# import numpy as np
from collections import defaultdict
from pandas.core.dtypes.inference import is_list_like
from typing import Union, List, Iterable, Dict, Set, Callable
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
# from external_modules
import kiwilib


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
class EnumABCMeta(abc.ABCMeta, type(Enum)):
    pass


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


class Metaproject(SingleInstanceColumn, kiwilib.Aliasable, Enum, metaclass=EnumABCMeta):
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
        return self.value[0]

    @classmethod
    def idMap(cls):
        if not hasattr(cls, '_idMap'):
            cls._idMap = {a.id: a for a in cls}
        return cls._idMap

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        if not hasattr(cls, '_aliasFuncs'):
            cls._aliasFuncs: Dict[str, Callable] = {
               'en_US': lambda slf: slf.value[1],
               'es_MX': lambda slf: slf.name,
            }
        return cls._aliasFuncs
    
    @staticmethod
    def dfcolumn() -> str:
        return 'metaproject'

    Carrera = 0, 'Career'
    Academico = 1, 'Academics'
    Logistica = 2, 'Logistics'
    Recreo = 3, 'Recreation'
    Dormir = 4, 'Sleep'


class Project(SingleInstanceColumn, kiwilib.Aliasable, Enum, metaclass=EnumABCMeta):
    #     Project = (project id, metaproject id)

    @staticmethod
    def dfcolumn() -> str:
        return 'project'

    def __le__(self, other):
        return self.value[0] <= other.value[0]

    def __lt__(self, other):
        return self.value[0] < other.value[0]

    def __ge__(self, other):
        return self.value[0] >= other.value[0]

    def __gt__(self, other):
        return self.value[0] > other.value[0]

    def defaultMetaproject(self) -> Metaproject:
        return Metaproject.idMap()[self.value[1]]

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        if not hasattr(cls, '_aliasFuncs'):
            cls._aliasFuncs: Dict[str, Callable] = {
               'en_US': lambda slf: slf.value[2] if slf.value[2] != '' else slf.name.replace('_', ' '),
               'es_MX': lambda slf: slf.name.replace('_', ' ') if slf.value[3] == '' else slf.value[3],
            }
        return cls._aliasFuncs

    MAE_5700                                =  1, 1, ''                         , ''
    MAE_5730                                =  2, 1, ''                         , ''
    MAE_5780                                =  3, 1, ''                         , ''
    SYSEN_5220                              =  4, 1, ''                         , ''
    SYSEN_5220_CALIFICACIÓN                 =  5, 1, 'SYSEN 5220 GRADING'       , ''
    SYSEN_5220_C                            =  5, 1, 'SYSEN 5220 GRADING'       , ''
    MENG_PROYECTO                           =  6, 1, 'MENG PROJECT'             , ''
    MENG                                    =  6, 1, 'MENG PROJECT'             , ''
    TRANSPORTE                              =  7, 2, 'TRANSPORT'                , ''
    ERRANDS_AFUERAS                         =  8, 2, 'ERRANDS'                  , 'MANDADOS'
    ERRANDS                                 =  8, 2, 'ERRANDS'                  , 'MANDADOS'
    CARRERA                                 =  9, 0, 'CAREER'                   , ''
    TAREAS_DOMÉSTICAS                       = 10, 2, 'HOUSEHOLD CHORES'         , ''
    TAREAS                                  = 10, 2, 'HOUSEHOLD CHORES'         , ''
    EMAIL_Y_LOGÍSTICA                       = 11, 2, 'EMAIL & LOGISTICS'        , ''
    EMAIL                                   = 11, 2, 'EMAIL & LOGISTICS'        , ''
    COMER_VESTIRSE_U_HIGIENE                = 12, 2, 'EAT DRESS & HYGIENE'      , ''
    COMER                                   = 12, 2, 'EAT DRESS & HYGIENE'      , ''
    RECREO_SOCIAL                           = 13, 3, 'SOCIAL FUN'               , ''
    RECREO_ELECTRÓNICO                      = 14, 3, 'SCREEN TIME FUN'          , ''
    RECREO_E                                = 14, 3, 'SCREEN TIME FUN'          , ''
    RECREO_MISC                             = 15, 3, 'MISC FUN'                 , ''
    TRABAJO_MISC                            = 16, 1, 'MISC WORK'                , ''
    DORMIR                                  = 17, 4, 'SLEEP'                    , ''
    RECREO_LEER                             = 18, 3, 'READ'                     , ''
    MAE_6060                                = 19, 1, ''                         , ''
    MAE_5710                                = 20, 1, ''                         , ''
    MAE_6780                                = 21, 1, ''                         , ''
    MAE_2030_TA                             = 22, 1, ''                         , ''
    CLASES_EXTRAS                           = 23, 1, 'EXTRA CLASSES'            , ''
    CARRERA_ENTRENAMIENTO_DISCRECIONAL      = 24, 0, 'DISCRETIONARY TRAINING'   , 'ENTRENAMIENTO DISCRECIONAL'
    CARRERA_ED                              = 24, 0, 'DISCRETIONARY TRAINING'   , 'ENTRENAMIENTO DISCRECIONAL'
    CARRERA_ENTRENAMIENTO_MANDATORIO        = 25, 0, 'MANDATORY TRAINING'       , 'ENTRENAMIENTO MANDATORIO'
    CARRERA_EM                              = 25, 0, 'MANDATORY TRAINING'       , 'ENTRENAMIENTO MANDATORIO'
    CARRERA_OMPS                            = 26, 0, 'BALL OMPS'                , 'BALL OMPS'
    CARRERA_OPIR                            = 27, 0, 'BALL OPIR'                , 'BALL OPIR'
    ACADÉMICO                               = 28, 1, 'ACADEMICS'                , ''
    ACADEMICO                               = 28, 1, 'ACADEMICS'                , ''
    TIMESHEET_ANÁLISIS                      = 29, 1, 'LIFELOG PROJECT'          , 'REGISTRO DE VIDA'
    TIMESHEET                               = 29, 1, 'LIFELOG PROJECT'          , 'REGISTRO DE VIDA'
    PÉNDULO_INVERTIDO                       = 30, 1, 'INVERTED PENDULUM'        , ''
    PENDULO                                 = 30, 1, 'INVERTED PENDULUM'        , ''
    TAMBORES                                = 31, 3, 'DRUMS'                    , ''
    OPIR_INGENIERÍA_DE_SISTEMAS_MECÁNICOS   = 32, 0, 'OPIR MECHANICAL SYSTEMS'  , 'OPIR SISTEMAS MECÁNICOS'
    OPIR_ISM                                = 32, 0, 'OPIR MECHANICAL SYSTEMS'  , 'OPIR SISTEMAS MECÁNICOS'
    OPIR_OTA_OPTOMECÁNICA_DISEÑO_Y_ANÁLISIS = 33, 0, 'OPIR OTA'                 , 'OPIR OTA'
    OPIR_OTA                                = 33, 0, 'OPIR OTA'                 , 'OPIR OTA'
    OPIR_PRB_DISEÑO_Y_ANÁLISIS              = 34, 0, 'OPIR PRB'                 , 'OPIR PRB'
    OPIR_PRB                                = 34, 0, 'OPIR PRB'                 , 'OPIR PRB'
    CARRERA_MENTOR_DE_PASANTÍA              = 35, 0, 'INTERN MENTORSHIP'        , 'MENTOR DE PASANTÍA'
    CARRERA_MENTOR                          = 35, 0, 'INTERN MENTORSHIP'        , 'MENTOR DE PASANTÍA'
    OPIR_PDR                                = 36, 0, 'OPIR PDR'                 , ''
    OPIR_CDR                                = 37, 0, 'OPIR CDR'                 , ''
    OPIR_ARQUITECTURA_DE_SISTEMAS           = 38, 0, 'OPIR SYSTEMS ARCHITECTURE', ''
    OPIR_ARQ                                = 38, 0, 'OPIR SYSTEMS ARCHITECTURE', ''
    OPIR_PROPÓSITO_ACÚSTICO                 = 39, 0, 'OPIR ACOUSTIC PROPOSAL'   , ''
    OPIR_ACUSTICO                           = 39, 0, 'OPIR ACOUSTIC PROPOSAL'   , ''
    OPIR_ICU                                = 40, 0, 'OPIR ICU'                 , ''
    OPIR_OTA_SUSTITUTA_DE_LENTE             = 41, 0, 'OPIR LENS SURROGATE'      , 'OPIR SUSTITUTA DE LENTE'
    OPIR_OTA_SL                             = 41, 0, 'OPIR LENS SURROGATE'      , 'OPIR SUSTITUTA DE LENTE'
    OPIR_RADIADOR_ANÁLISIS_ESTRUCTURAL      = 42, 0, 'OPIR RADIATOR'            , 'OPIR RADIADOR'
    OPIR_RADIADOR                           = 42, 0, 'OPIR RADIATOR'            , 'OPIR RADIADOR'
    OPIR_GSE_AI_T                           = 43, 0, 'OPIR GSE AI&T'            , 'OPIR GSE AI&T'
    OPIR_GSE_AIT                            = 43, 0, 'OPIR GSE AI&T'            , 'OPIR GSE AI&T'
    OPIR_GSE_SOC                            = 44, 0, ''                         , ''
    NGP                                     = 45, 0, ''                         , ''
    NGP_STOP                                = 46, 0, ''                         , ''
    NGP_OTA                                 = 47, 0, ''                         , ''
    NGP_ESTRUCTURA                          = 48, 0, 'NGP STRUCTURE'            , ''
    OPIR_B1_OTA                             = 49, 0, ''                         , ''
    CS_AUTOAPRENDIZAJE                      = 50, 1, 'CS SELF-TEACHING'         , ''
    CS                                      = 50, 1, 'CS SELF-TEACHING'         , ''
    MÚSICA                                  = 51, 3, 'MUSIC'                    , ''
    MUSICA                                  = 51, 3, 'MUSIC'                    , ''
    BAJO                                    = 52, 3, 'BASS'                     , ''
    CICLISMO                                = 53, 3, 'CYCLING'                  , ''
    ESCRITURA_Y_VÍDEOS                      = 54, 3, 'WRITING AND VIDEOS'       , ''
    ESCRITURA                               = 54, 3, 'WRITING AND VIDEOS'       , ''
    MAE_4060                                = 55, 1, ''                         , ''
    EA_COMUNIDAD                            = 56, 1, 'EA COMMUNITY'             , ''
    EA                                      = 56, 1, 'EA COMMUNITY'             , ''


# noinspection NonAsciiCharacters
class Tag(ListColumn, kiwilib.Aliasable, Enum, metaclass=EnumABCMeta):
    @staticmethod
    def dfcolumn() -> str:
        return 'tags'

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        if not hasattr(cls, '_aliasFuncs'):
            cls._aliasFuncs: Dict[str, Callable] = {
               'en_US': lambda slf: slf.value[2],
               'es_MX': lambda slf: slf.name.replace('_', ' ') if slf.value[1] == '' else slf.value[1],
            }
        return cls._aliasFuncs

    BICI               =  1, ''                  , 'BIKE'
    COLECTIVO          =  2, ''                  , 'BUS'
    ELECTRÓNICA        =  3, 'TIEMPO DE PANTALLA', 'SCREEN TIME'
    ELEC               =  3, 'TIEMPO DE PANTALLA', 'SCREEN TIME'
    EN_CLASE           =  4, ''                  , 'IN CLASS'
    FAMILIA            =  5, ''                  , 'FAMILY'
    HW                 =  6, 'TAREA'             , 'HOMEWORK'
    LECTURA            =  7, ''                  , 'READING'
    NETFLIX            =  8, 'TV/PELÍCULA'       , 'TV/MOVIE'
    NFL                =  9, ''                  , 'NFL'
    PAPEL              = 10, ''                  , 'PAPER'
    PIE                = 11, ''                  , 'WALK'
    PROYECTO_ACADÉMICO = 12, ''                  , 'ACADEMIC PROJECT'
    PROYECTO_A         = 12, ''                  , 'ACADEMIC PROJECT'
    RUTINA             = 13, ''                  , 'ROUTINE'
    SOCIAL_GRUPO       = 14, 'SOCIAL'            , 'SOCIAL'
    SOCIAL             = 14, 'SOCIAL'            , 'SOCIAL'
    EJERCICIO          = 15, ''                  , 'EXERCISE'
    COMER              = 16, ''                  , 'EATING'
    AUTO               = 17, ''                  , 'CAR'
    BICI_ELÉCTRICA     = 18, ''                  , 'E-BIKE'
    BICI_E             = 18, ''                  , 'E-BIKE'
    PODCAST            = 19, ''                  , 'PODCAST'
    MÚSICA             = 20, ''                  , 'MUSIC'
    TREN               = 21, ''                  , 'TRAIN'
    AVIÓN              = 22, ''                  , 'AIRPLANE'


class Epoch(SingleInstanceColumn, kiwilib.Aliasable, Enum, metaclass=EnumABCMeta):
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
        return self.dt() <= other.dt()

    def __lt__(self, other):
        return self.dt() < other.dt()

    def __ge__(self, other):
        return self.dt() >= other.dt()

    def __gt__(self, other):
        return self.dt() > other.dt()

    def __str__(self):
        return f'{self.name}: {self.dt().strftime("%Y-%m-%d %H:%M")}'

    def dt(self) -> datetime:
        """Returns the datetime object for a given Epoch instance"""
        return self.value[1]

    def id(self) -> int:
        """Returns the id for a given Epoch instance"""
        return self.value[0]

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        """
        if not hasattr(cls, '_aliasFuncs'):
            cls._aliasFuncs: Dict[str, Callable] = {
               'en_US': lambda slf: slf.name[1:].replace('_', ' '),
               'es_MX': lambda slf: slf.value[2],
            }
        return cls._aliasFuncs

    END =                     0, datetime(2025, 1, 1, 0, 0, 0), 'FIN'
    e2017_Cornell =           1, datetime(2017, 9, 6, 0, 0, 0), '2017 Cornell'  # Start of data collection
    e2017_Winter =            2, datetime(2017, 12, 13, 9, 36, 0), '2017 Invierno'
    e2018_Cornell =           3, datetime(2018, 1, 12, 21, 58, 0), '2018 Cornell'
    e2018_Interim =           4, datetime(2018, 5, 22, 3, 0, 0), ' 2018 Interregno'  # End of finals, before CO move
    e2018_Boulder_Solo =      5, datetime(2018, 6, 18, 3, 0, 0), '2018 Boulder Solo'  # I move to Boulder
    e2018_Boulder_Padraig =   6, datetime(2018, 8, 24, 3, 0, 0), '2018 Boulder Padraig'  # Padraig moves in
    e2018_BCH =               7, datetime(2018, 10, 28, 0, 0, 0), '2018 BCH'  # Office move to BCH
    e2019_Tour_Start =        8, datetime(2019, 8, 4, 7, 19, 0), '2019 Inicio de Gira'  # 2019 tour start
    e2019_Tour_End =          9, datetime(2019, 8, 13, 12, 17, 0), '2019 Fin de Gira'  # 2019 tour end
    e2020_WFH =               10, datetime(2020, 3, 18, 0, 0, 0), '2020 Teletrabajo'  # Start WFH
    e2020_Boulder_Dip =       11, datetime(2020, 3, 29, 18, 42, 0), '2020 Boulder Dip'  # Dip move to CO
    e2021_COVID_Ease =        12, datetime(2021, 4, 10, 0, 0, 0), '2021 Alivio de COVID'  # Ease of COVID restrictions
    e2021_Tour_Start =        13, datetime(2021, 8, 11, 7, 14, 0), '2021 Inicio de Gira'  # 2021 tour start
    e2021_Tour_End =          14, datetime(2021, 8, 21, 12, 46, 0), '2021 Fin de Gira'  # 2021 tour end
    e2022_Tour_Start =        15, datetime(2022, 1, 7, 18, 7, 0), '2022 Inicio de Gira'  # 2022 tour start
    e2022_Suzie_Start =       16, datetime(2022, 3, 12, 19, 13, 0), '2022 Inicio con Suzie'  # Start Suzie
    e2022_Suzie_End =         17, datetime(2022, 3, 25, 15, 34, 0), '2022 Fin con Suzie'  # ENd SVF
    e2022_Alexandre_Start =   18, datetime(2022, 6, 4, 9, 7, 0), '2022 Inicio con Alexandre'  # Start ride  w/ Alexandre
    e2022_Alexandre_End =     19, datetime(2022, 6, 11, 7, 52), '2022 Fin con Alexandre'  # End ride w/ Alexandre
    e2022_Tim_Start =         20, datetime(2022, 7, 10, 14, 58, 0), '2022 Inicio con Tim'  # Start TIm Sprinz
    e2022_Tim_End =           21, datetime(2022, 7, 12, 5, 5, 0), '2022 Fin con Tim'  # End Tim Sprinz, or really Lars
    e2022_USA_Friends_Start = 22, datetime(2022, 9, 14, 16, 54, 0), '2022 Inicio con amigos de EEUU'  # Start BFish+
    e2022_USA_Friends_End =   23, datetime(2022, 9, 21, 10, 33, 0), '2022 Fin con amigos de EEUU'  # End BFish+
    e2022_Tour_End =          24, datetime(2022, 12, 15, 10, 10, 0), '2022 Fin de Gira'  # 2022 tour end
    e2020_Tech_Start =        25, datetime(2020, 9, 19, 20, 35, 0), '2020 Inicio con Tech' # Tech arrival in CO
    e2020_Tech_End =          26, datetime(2020, 11, 1, 8, 30, 0), '2020 Fin con Tech' # Tech leave from CO
    e2022_Europe_Start =      27, datetime(2022, 4, 2, 6, 9, 0), '2022 Inicio en Europa' # Flight CDMX >> Europe
    e2022_MEX_GER_TZ_SHIFT =  28, datetime(2022, 4, 2, 0, 0, 0), '2022 MEX ALE ZH CAMBIO' # Marks time zone shift in data
    e2022_ESP_USA_TZ_SHIFT =  29, datetime(2022, 12, 15, 7, 42, 0), '2022 ESP EEUU ZH CAMBIO'
    e2023_EA_Discovery =      30, datetime(2023, 4, 17, 9, 51, 0), '2023 EA Descubrimiento'  # Podcast triggers EA interest
    e2019_SpChg_Glenn_End =   31, datetime(2019, 4, 1, 0, 0, 0), '2019 SpChg Fin con Glenn'  # Glenn leaves Spare Change
    e2019_SpChg_Alex_End =    32, datetime(2019, 11, 1, 0, 0, 0), '2019 SpChg Fin con Alex'  # Alex leaves, Steve joins Spare Change
    e2019_SpChg_Nick_End =    33, datetime(2020, 1, 1, 0, 0, 0), '2019 SpChg Fin con Nick'  # Nick leaves, George joins Spare Change
    e2021_SpChg_KO_Start =    34, datetime(2021, 9, 10, 0, 0, 0), '2021 SpChg Inicio con KO'  # Kristin joins Spare Change
    e2022_SpChg_JW_KS_Start = 35, datetime(2022, 9, 1, 0, 0, 0), '2022 SpChg Inicio con JW KS'  # Kirsten, Jonathan join Spare Change


def appendIntervalDictComplement(dct: P.IntervalDict, complementVal, bigInterval: P.IntervalDict = P.closedopen(
        Epoch.e2017_Cornell.dt(), Epoch.END.dt())) -> P.IntervalDict:
    # temp = P.closedopen(Epoch.e2017_Cornell.dt(), Epoch.END.dt())
    for interval in dct.keys():
        bigInterval = bigInterval - interval
    dct[bigInterval] = complementVal
    return dct


class EpochScheme(kiwilib.Aliasable, Enum, metaclass=EnumABCMeta):
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
        Returns the string representation of the epoch group containing dt for an EpochScheme.
        String returned is dependent on the specified locale. If unspecified, self.defaultLocale() is used.
        :param dt: Datetimes to be mapped to epoch groups.
        :param locale: String representation of locale. See epochGroupAliasFuncs() for allowable locale values.
        :return:
        """
        if locale is None:
            locale = self.defaultLocale()
        if is_list_like(dt):
            return kiwilib.mapOverListLike(lambda x: EpochScheme.labelDT(self, x, locale), dt)
        return self.epochGroupAliasFuncs()[locale](self, dt)

    def sortedEpochGroups(self) -> List[str]:
        if not hasattr(self, '_sortedEpochGroups'):
            temp = {self.labelDT(iv.lower): iv.lower for iv, names in self.value.items()}
            self._sortedEpochGroups: List[str] = sorted(temp.keys(), key=lambda x: temp[x])
        return self._sortedEpochGroups

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        if not hasattr(cls, '_aliasFuncs'):
            cls._aliasFuncs: Dict[str, Callable] = defaultdict(lambda: lambda slf: slf.name)  # Ignore language
            cls._aliasFuncs['en_US'] = lambda slf: slf.name  # Have to include >=1 key for Aliasable.defaultLocale()
        return cls._aliasFuncs

    def epochGroupAliasFuncs(self):
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
         P.closedopen(Epoch.e2022_Tour_End.dt(), Epoch.END.dt()))
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
             P.closedopen(Epoch.e2022_Tour_End.dt(), Epoch.END.dt())
             ): (0, 'Academics Focus Epochs', 'Épocas Enfocados en la Académica'),
            (P.closedopen(Epoch.e2018_Boulder_Solo.dt(), Epoch.e2019_Tour_Start.dt()) |
             P.closedopen(Epoch.e2019_Tour_End.dt(), Epoch.e2021_Tour_Start.dt()) |
             P.closedopen(Epoch.e2021_Tour_End.dt(), Epoch.e2022_Tour_Start.dt())
             ): (2, 'Career Focus Epochs', 'Épocas Enfocados en la Carrera'),
        }), complementVal=(1, 'Recreation Focus Epochs', 'Épocas Enfocados en el Recreo'))
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
        (P.closedopen(Epoch.e2022_Tour_End.dt(), Epoch.END.dt()))
        : (0, '2023 Career Pivot', '2023 Cambio de Carrera'),
    })
    # TODO: sequential life phases, like 1 but each group is only a single period: Cornell, Ball, Tour22, post-tour
    # TODO: meal 'Rutina' default groups
    # TODO: 'Casa' location groups


class Mood(SingleInstanceColumn, kiwilib.Aliasable, Enum, metaclass=EnumABCMeta):
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