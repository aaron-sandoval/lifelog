'''
Created on May 26, 2019

@author: Aaron
'''

import os
from pathlib import Path
from typing import Union

PRIVATE_ACCESS = os.path.isfile(Path(os.path.abspath(__file__)).parent/f'{os.path.splitext(__file__)[0]}_PRIVATE.py')
if PRIVATE_ACCESS:
    import src.DescriptionSTDLISTS_PRIVATE as priv


def _appendPriv(d: Union[set, list, dict], name: str) -> Union[set, list, dict]:
    if not PRIVATE_ACCESS:
        return d
    appendFuncs = {
        list: lambda c, n: c.append(getattr(priv, n)),
        set: lambda c, n: c.update(getattr(priv, n)),
        dict: lambda c, n: c.update(getattr(priv, n)),
    }
    if type(d) not in appendFuncs:
        raise NotImplementedError(f'{type(d)} not yet implemented in _appendPriv.')
    appendFuncs[type(d)](d, name)
    return d


# A dictionary of words which may appear in descriptions that should be
# standardized to a different word in def stdDiction()
# TODO: Implement a separate token-wise replacement procedure in DC, maybe consolidate this into that if practical
STD_DICTION = {
    'ALMORZAR': 'COMER',
    'ALMUERZO': 'COMER',
    # 'COMPRADO':'COMPRAR',
    # 'BUSCAR': 'INVESTIGAR',  # TODO: research. Could implement with Epoch filter if applicable
    'PRESENTACION': 'PRESENTACIÓN',
    'LA PRESENTACIÓN': 'PRESENTACIÓN',
    'REUNION': 'REUNIÓN',
    # 'REUNIÓN DE GNC': 'REUNIÓN, EQUIPO DE CU GRAVITY GNC',
    # 'REUNIÓN DE CONTROLES': 'REUNIÓN, EQUIPO DE CU GRAVITY GNC',
    'REUNIÓN DE': 'REUNIÓN,',
    'REUNIÓN CON': 'REUNIÓN,',
    'SOLICITUD DE': 'SOLICITUDES,',
    'SOLICITUD DE': 'SOLICITUDES,',
    'SOLICITUDES DE': 'SOLICITUDES,',
    'SKYPE CON LOS PADRES': 'VIDEOLLAMADA, PAPÁ, MAMÁ',
    'SKYPE CON': 'VIDEOLLAMADA,',
    'SKYPE': 'VIDEOLLAMADA',
    'CORNELL CINEMA': 'CINE',
    'JUGAR CON': 'JUGAR,',
    'CHARLAR CON': 'CHARLAR,',
    'AYUDAR A': 'AYUDAR,',
    'PREPARAR LA ': 'PREPARAR, ',
    'PREPARAR EL ': 'PREPARAR, ',
    ' AMERICANO': ' AMERICANA',
    # ' CHINO': ' CHINA', # tsqy
    'MEDITERRANEO': 'MEDITERRANEA',
    # ' INDIO': ' INDIA',# tsqy
    'MEXICANO': 'MEXICANA',
    'ARGENTINO': 'ARGENTINA',
    'PERUANO': 'PERUANA',
    'COLOMBIANO': 'COLOMBIANA',
    'ITALIANO': 'ITALIANA',
    'JAPONÉS': 'JAPONESA',
    'JAPONES': 'JAPONESA',
    'COREANO': 'COREANA',
    'KOREANA': 'COREANA',
    'KOREANO': 'COREANA',
    'TAILANDES': 'TAILANDESA',
    'TAILANDÉS': 'TAILANDESA',
    'ETIOPIO': 'ETÍOPE',
    'ETIOPIA': 'ETÍOPE',
    'MEDITERRANEA': 'MEDITERRÁNEA',
    'DESAFIO DE IMPRESION 3D': 'IMPRESIÓN 3D',
    ', TIA ': ', TÍA ',
    ', TIO ': ', TÍO ',
    'BARRER LA ALFOMBRA': 'LIMPIAR, CASA',
    'LOVE, DEATH, AND ROBOTS': 'LOVE DEATH AND ROBOTS',
    'EL DEPARTAMENTO': 'CASA',
    'YEMAS': 'TEMAS',
    'PODCAST.': 'PODCAST,',
    'CARTAS DE GRACIAS': 'CARTA',
    'ESCRIBIR, CARTAS': 'ESCRIBIR, CARTA',
}
STD_DICTION = _appendPriv(STD_DICTION, 'STD_DICTION')

# A dictionary of words whose plural nature is standardized
STD_PLURAL = {
    'SOLICITUD': 'SOLICITUDES',
    'VOLUNTARIOS': 'VOLUNTARIO',
    'RUTA': 'RUTAS',
    'IDIOMAS': 'IDIOMA',
}

# Productive software
SOFTWARE_LIST = {
    'EMAIL',
    'ANSYS',
    'VENSIM',
    'SOLIDWORKS',
    'SIMULINK',
    'MATLAB',
    'PYTHON',
    'PYTORCH',
    'C++',
    #     'C',
    #     'JAVA',
    'HDL',
    'HACK ASSEMBLY',
    'NX',
    'STK',
    'FRAP',
    'EXCEL',
    'PPT',
    'GOOGLE SHEETS',
    'NOTEPAD++',
    'ONENOTE',
    'NASGRO',
    'VA ONE',
    'I-DEAS',
    'ARDUINO',
    'RASPBERRY PI',
    'LATEX',
    'BASIS',
    'SQL',
    'BASH',
    'KAGGLE',
    }

# Software not in the strictest sense, but still implying Tag.Electronica
SOFTWARE_OTHER = {
    'REDDIT',
    'YOUTUBE',
    'STRAVA',
    'TODOIST',
    'DUOLINGO',
    'FACEBOOK',
    'CITAS EN LÍNEA',
    'SLACK',
    'STRAVA',
    }

SOFTWARE_ALL = SOFTWARE_LIST.union(SOFTWARE_OTHER)

PODCASTS = {
    'THE DAILY',
    'THE WAR ON CARS',
    'BBC GLOBAL NEWS PODCAST',
    'THE ANTHROPOCENE REVIEWED',  # TODO: figure out conflict with identical audiobook title
    'DEAR HANK AND JOHN',
    'RABBIT HOLE',
    '80000 HOURS',
    'EA FORUM PODCAST',
    'THE EZRA KLEIN SHOW',
    'MAKING SENSE WITH SAM HARRIS',
    'THE HAPPINESS LAB',
    'JOE CARLSMITH AUDIO',
}

PEOPLE_NUCLEAR_FAMILY = {
    'PAPÁ',
    'MAMÁ',
    }
PEOPLE_NUCLEAR_FAMILY = _appendPriv(PEOPLE_NUCLEAR_FAMILY, 'PEOPLE_NUCLEAR_FAMILY')

# TODO: add back diacritics
PEOPLE_DAD_FAMILY = {
    'ABUELA',
    }
PEOPLE_DAD_FAMILY = _appendPriv(PEOPLE_DAD_FAMILY, 'PEOPLE_DAD_FAMILY')

PEOPLE_MOM_FAMILY = set()
PEOPLE_MOM_FAMILY = _appendPriv(PEOPLE_MOM_FAMILY, 'PEOPLE_MOM_FAMILY')

# set containing tokens found in raw data. Full name substitution done in DC
PEOPLE_CORNELL = set()
PEOPLE_CORNELL = _appendPriv(PEOPLE_CORNELL, 'PEOPLE_CORNELL')

PEOPLE_LEHIGH = set()
PEOPLE_LEHIGH = _appendPriv(PEOPLE_LEHIGH, 'PEOPLE_LEHIGH')

PEOPLE_BALL = set()
PEOPLE_BALL = _appendPriv(PEOPLE_BALL, 'PEOPLE_BALL')

PEOPLE_CHILDHOOD = set()
PEOPLE_CHILDHOOD = _appendPriv(PEOPLE_CHILDHOOD, 'PEOPLE_CHILDHOOD')

# TODO: add more name replacements in independent.tsqy, reflect them here
PEOPLE_COLORADO = {
    'CONJUNTO',
    'CONJUNTO ACUSTICO',
}
PEOPLE_COLORADO = _appendPriv(PEOPLE_COLORADO, 'PEOPLE_COLORADO')

# TODO: reformat as a list (maybe enum) with tuples containing tags
PEOPLE_ALL = PEOPLE_NUCLEAR_FAMILY.union(PEOPLE_DAD_FAMILY, PEOPLE_MOM_FAMILY, PEOPLE_CORNELL, PEOPLE_LEHIGH,
                                         PEOPLE_BALL, PEOPLE_CHILDHOOD, PEOPLE_COLORADO)

# todo: Replace with a skeleton tree structure, EXPAND A LOT
STD_LOCATIONS = {
    'CASA',
    'CORNELL',
    }
STD_LOCATIONS = _appendPriv(STD_LOCATIONS, 'STD_LOCATIONS')

STD_ROOTS_DELIMIT = {  # Tokens which are rejected as children of any other token
    'COMER',
    'CHARLAR',
    'DORMIR',
    'ESCRIBIR',
    'ESCUCHAR',
    'LEER',
    'INVESTIGAR',
    'COMPRAR',
    'HABLAR',
    'VIDEOLLAMADA',
    'PRACTICAR',
    'APRENDER',
    'DISEÑAR',
    'EMPACAR',
    'REUNIÓN',
    'VOLUNTAR',
    'MEJORAR',
    'MANTENER',
    'PREPARAR',
    'COCINAR',
    'SACAR',
    'LIMPIAR',
    'LAVAR',
    'REPASO SEMANAL',
    'REPASO A LARGO PLAZO',
    # 'CASA A CORNELL',
    # 'CORNELL A CASA',
    'JUGAR',
    # 'EJERCICIO', #
    'FIESTA',
    'AYUDAR',
    # 'SOLICITUDES', #
    'MENSAJEAR',
    'PLANEAR',
    'ARREGLAR',
    'PENSAR',
    'GUARDAR',
    'MUDARSE',
    'SUBIR',
    'BAJAR',
    'REPARAR',
    'INICIO DE ENFERMEDAD',
    'FIN DE ENFERMEDAD',
    'TEMAS',
    'VOTAR',
    # 'ESPAÑOL',
    'CITA MÉDICA',
    'LIDERAZGO',
    # 'PRONÓSTICO',
    'AVIÓN',
    'AUDIOLIBRO',
    # 'JUEGOS DE MESA',
    '$PERSON',
    '$AUDIOBOOK',
    '$PODCAST',
    '$TVSHOW',
    '$MOVIE',
    '$SOFTWARE',
    '$VIDEOGAME',
    '$TABLETOPGAME',
    '$LOCATION',
    '$FOOD',
    '$SUBJECTMATTER',
    }

STD_ROOTS_NO_DELIMIT = {
    # 'AUTO',
    'TREN',
    'BARCO',
    'TV',
    'PODCAST',
    'CINE',
    'ÍNTIMO',
    'INTIMO',
    'MEDITAR',
    'TOCAR',
    'FFL',
    'VER',
}

STD_ROOTS = STD_ROOTS_DELIMIT.union(STD_ROOTS_NO_DELIMIT)

STD_SUBJECT_MATTERS = {  # Temporary list of subject matters, all uses to be replaced with reference to Catalog
    'INTELIGENCIA ARTIFICIAL',
    'ESTRUCTURA',
    'NAVIDAD',
    'ALGORITMOS',
    'INFORMÁTICA',
    'TECNOLOGÍA',
    'FILOSOFÍA',
    'MINIMALISMO',
    'ALTRUISMO EFECTIVO',
    'CARRERA',
    'BICI',
    'CONTROLES',
    'NEGOCIO',
    "COMIDA",
    "ESPAÑOL",
    "PYTHON",
    }

STD_FOODS = {  # Comprehensive set of acceptable food tokens. No other tokens can be children of 'COMER'.
    'COMPRADO', 'GRATIS', 'CARNE', 'ACCIDENTE', 'MERIENDA', 'RESTOS', 'COMIDA',
    'AMERICANA', 'ETÍOPE', 'MARROQUÍ',
    'LATINOAMERICANA', 'NUEVO MEXICANA', 'MEXICANA', 'ARGENTINA', 'PERUANA', 'COLOMBIANA', 'SALVADOREÑA',
        'NUEVA MEXICANA',
    'ASIÁTICA', 'CHINA', 'JAPONESA', 'COREANA', 'TAILANDESA', 'INDIA', 'VIETNAMITA', 'INDONESIA', 'NEPALESA',
        'BENGALÍ', 'ÁRABE',
    'EUROPEA', 'POLACA', 'ALEMANA', 'AUSTRIACA', 'BÉLGICA', 'FRANCESA', 'BRITÁNICA', 'CROATA', 'SUECA', 'LETONA',
        'ESPAÑOLA', 'MEDITERRÁNEA', 'ITALIANA', 'PORTUGUESA', 'FRANCESA', 'FRANCÉS',
    'ENSALADA', 'PASTA', 'SANDWICH', 'DESAYUNO', 'ARROZ', 'POROTOS', 'BRÓCOLI', 'DAL', 'LENTEJAS', 'PAN', 'FRUTA',
        'AVENA', 'VEGETALES', 'PAPAS', 'PIZZA', 'SOPA', 'POZOLE', 'GUACAMOLE', 'HUMMUS', 'SANDÍA', 'PIÑA',
        'RAJMA MASALA', 'SOPA DE LENTEJAS', 'SHAHI PANEER', 'SHAHI TOFU', 'ESPINACAS', 'TAMALES', 'CHILE VERDE',
        'KORMA DE VEGETALES', 'TOFU', 'GUISO', 'HUEVOS', 'NAAN', 'GRANADA', 'PASTEL DE PAPA', 'SALSA', 'ESPECIAS',
}

STD_TV = {
    'STRANGER THINGS',
}

COLLXBLE_INSTANCES = STD_SUBJECT_MATTERS.union(PEOPLE_ALL, STD_LOCATIONS, SOFTWARE_ALL, PODCASTS, STD_FOODS, STD_TV)

# A list of words/phrases which receive a standard delimiter
STD_DELIMIT_LIST = {
    'SOLICITUD',
    'TUTORIAL',
    'BRAINSTORMING',
    'PRESENTACION',
    'PRESENTACIÓN',
    'SKYPE',
    'LIDERAZGO',
}.union(STD_ROOTS_DELIMIT)


DC_ONE_OFF_TOKEN_REPLACEMENT_LIST = {  # TODO: fill this
    3590919: '',
    3593879: 'COMPRAR, ESCRIBIR, CARTA',
    3595499: 'CORREO',
    3595779: 'INVESTIGAR, BICI',
    3596099: 'INVESTIGAR, PUESTOS',
    3598729: 'TV, NFL',
    3697209: 'JUGAR, COMER',
    3808929: 'INVESTIGAR, EQUIPO DE CASA',
    3822339: 'INVESTIGAR, TRANSPORTE',
    3823229: 'ARREGLAR, COMPUTADORA',
    3883849: 'INVESTIGAR, INFORME DE CONTROLES',
    3911719: 'INVESTIGAR, EQUIPO DE CASA',
    4111409: 'REUNIÓN',
    5023259: 'AUDIOLIBRO, SPEAKER FOR THE DEAD',  # todo: when done w/ double-quote audiobook constructor, replace this
    5247209: 'LOGÍSTICA',
    5327189: 'AUDIOLIBRO, XENOCIDE',
    5551509: 'INVESTIGAR, CORNELL, TAMBORES',
    5629599: '$TVSHOW, DAVID LETTERMAN',
    5686539: '$TVSHOW, PLANET EARTH II',
    5715329: 'CHARLAR',
    5798959: 'REUNIÓN',
    6030919: 'INVESTIGAR, EQUIPO DE BICI',
    6205649: 'INVESTIGAR, BICI, EQUIPO DE BICI',
    6357329: 'INVESTIGAR, BICI, EQUIPO DE BICI',
    6357409: 'YOUTUBE, INVESTIGAR, CURSOS',
    6693709: 'PREPARAR, PIZZA',
    6992379: "",
    7617169: '$TVSHOW, SENSE8',
    7761319: 'LAVAR, LA ROPA, $TVSHOW, DEAR WHITE PEOPLE',
    8451059: 'HABLAR, PAPÁ',
    8778779: "INVESTIGAR, ELECTRÓNICA",
    8790999: "INVESTIGAR, ELECTRÓNICA",
    9039019: 'COMER, GRATIS, AMERICANO, CHARLAR',
    9381849: 'TV, NFL',
    9676779: '$TVSHOW, HOUSE OF CARDS',
    9972869: "INVESTIGAR, TAMBORES",
    10323359: 'YOUTUBE, INVESTIGAR, TIENDAS',
    12107799: "COCINAR, DAL, ARROZ, BRÓCOLI",
    12109459: "COCINAR, DAL, ARROZ, BRÓCOLI",
    13454159: 'HABLAR, TEMAS, EQUIPO DE CASA',
    14679229: 'AVIÓN, LOS ANGELES A DENVER, $MOVIE, TOY STORY 4',
    15128249: 'COMER, AMERICANA',
    19762669: 'ESTIRARSE, AUDIOLIBRO, HARRY POTTER Y LA PIEDRA FILOSOFAL',
    # 20915889: 'MENSAJEAR, TEMAS, ESTRUCTURA',
    21135599: 'VIDEOLLAMADA',
    22222929: 'THE DAILY, AUDIOLIBRO, HOW TO AVOID A CLIMATE DISASTER',
    22397759: "EMAIL",
    22828229: "INICIO DE ENFERMEDAD, THE DAILY",
    24067169: 'THE DAILY, INVESTIGAR, EQUIPO DE CICLOTURISMO',
    25147849: "LOGÍSTICA, COMPRAR, MÚSICA",
    26748249: 'EMAIL, INVESTIGAR, CICLOTURISMO, RUTAS',
    27256889: 'BARCO, "PICHILINGUE, BAJA CALIFORNIA SUR" A "MAZATLÁN, SINALOA, MÉXICO", $MOVIE, MULAN',
    27279219: 'MONTAR, CICLOTURISMO, "TEODORO BELTRÁN" A "EL TIGRE, SINALOA"',
    27581719: 'CIUDAD DE MÉXICO A "TEOTIHUACÁN, ESTADO DE MÉXICO", ESCRIBIR, CARTA',
    27597159: 'AVIÓN, CIUDAD DE MÉXICO A "DÜSSELDORF, ALEMANIA", $MOVIE, BLADE RUNNER 2049',
    27599389: 'AVIÓN, CIUDAD DE MÉXICO A "DÜSSELDORF, ALEMANIA", $MOVIE, YESTERDAY',
    29299669: 'MONTAR, CICLOTURISMO, VESTRE GAUSDAL A "LILLEHAMMER, NORUEGA"',
    30277619: 'TREN, LONGWY A "NANCY, FRANCIA", GOOGLE SHEETS, STRAVA, INVESTIGAR, ACTIVIDADES, ALOJAMIENTO',
    31272719: 'TREN, MURCIA A "VALENCIA, ESPAÑA", $MOVIE, CLOUDY WITH A CHANCE OF MEATBALLS 2',
    31312239: 'AVIÓN, LISBOA A "BOSTON, MASSACHUSETTS, ESTADOS UNIDOS", COMER, COMPRADO, $MOVIE, LUCA',
    31314959: 'AVIÓN, LISBOA A "BOSTON, MASSACHUSETTS, ESTADOS UNIDOS", $MOVIE, LEGO MOVIE',
    32210349: '$MOVIE, ANGELS & DEMONS',
    32307629: 'AUDIOLIBRO, "EFFORTLESS, GREG MCKEOWN"',
    32364709: "TODOIST",
    32771259: 'INVESTIGAR, PYTHON',
    33526289: "THE EZRA KLEIN SHOW, TEMAS, CIENCIA ECONÓMICA",
    33530349: "THE EZRA KLEIN SHOW, TEMAS, CIENCIA ECONÓMICA",
    33616029: 'INVESTIGAR, CARRERA',
    33685739: "80000 HOURS, TEMAS, FILOSOFÍA, MAKING SENSE WITH SAM HARRIS, TEMAS, BIOLOGÍA, CIENCIA",
    33688959: "MAKING SENSE WITH SAM HARRIS, TEMAS, GENÉTICA, BIOLOGÍA",
    34886689: "LEER, TEMAS, POLÍTICA LOCAL",
    34710079: "LIMPIAR, CASA, 80000 HOURS, TEMAS, CARRERA, INTELIGENCIA ARTIFICIAL",
    36285289: 'THE WOLF OF WALL STREET',
    # 36486849: 'THE HATEFUL EIGHT, COMER, COMPRADO, RESTOS, INDIA'
    # 35638669: 'DENVER A CASA, FF1, PODCAST, YOUR UNDIVIDED ATTENTION, TEMAS, ÉTICA, INTELIGENCIA ARTIFICIAL, POLÍTICA GLOBAL, TECNOLOGÍA',
    36888289: "INVESTIGAR, SALAS DE MÚSICA",
    36934369: "YOUTUBE, INVESTIGAR, GRABACIÓN, PRODUCCIÓN DE MÚSICA",
    37611159: "ONE FLEW OVER THE CUCKOO'S NEST",
    37619419: "INVESTIGAR, TAMBORES",
    37668829: "A CHILD'S SONG A CASA, FF1, AUDIOLIBRO, \"THE HIGH COST OF FREE PARKING, DONALD SHOUP, OPINIÓN, TEMAS, URBANISMO\"",
    38037749: "AUDIOLIBRO, \"AGAINST EMPATHY, PAUL BLOOM, OPINIÓN, TEMAS, ÉTICA, PSICOLOGÍA\"",
    39008819: 'NORTHGLENN A CASA, PENSAR, TEMAS, COLEGAS, GESTIÓN',
    393179959: "INVESTIGAR, INVESTIGACIÓN, ZOTERO",
}

DC_ONE_OFF_TOKEN_REPLACEMENT_LIST = _appendPriv(DC_ONE_OFF_TOKEN_REPLACEMENT_LIST, 'DC_ONE_OFF_TOKEN_REPLACEMENT_LIST')
# The to-do list is in the private file
