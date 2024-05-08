import gettext
# from src.TimesheetGlobals import rootProjectPath
import os
import builtins
from datetime import datetime
from external_modules import kiwilib
from typing import Union, List, Iterable, Dict, Tuple, Set, Callable, NamedTuple
from dataclasses import dataclass
from pathlib import Path
# import googletrans

def test1():
    lang_en.install()  # Magically make the _ function globally available
    print('***ENGLISH***')
    print(_a('helloworld'))
    print(_b('test1'))

    lang_es.install()  # Magically make the _ function globally available
    print('***ESPAÑOL***')
    print(_a('helloworld'))
    print(_b('test1'))


localeDir = os.path.join(os.path.dirname(__file__), 'locale')
lang_en = gettext.translation(
    domain='timesheet',
    localedir=localeDir,
    languages=['en_US']
)
lang_es = gettext.translation(
    domain='timesheet',
    localedir=localeDir,
    languages=['es_MX'])
localeDict = {
    'en_US': lang_en,
    'es_MX': lang_es,
}
locale_to_str = {v: k for k, v in localeDict.items()}
# _google_locale_dict: Dict[gettext.GNUTranslations, str] = {
#     lang_es: 'es',
# }
# _google_translator = googletrans.Translator(service_urls=['translate.google.com'])


class BabelIntermediateExtractor:
    """
    Wrapper for GNUTranslations.gettext in the gettext library.
    If enabled, allows babel to be used for dynamic translations.
    At runtime, extracts all calls to the gettext() wrapper to an intermediate text file.
    The intermediate file may be processed with the command line `babel extract` to extract messages for translation.
    Strings are processed with repr() before writing to the intermediate text file, and decoded before loading.
    This is to ensure that every entry occupies a single line, i.e., no explicit newlines are written.
    If disabled, no extraction occurs and the class acts similarly to gettext.
    Inspired by prose description: https://stackoverflow.com/a/77174097/21933315.
    """
    lang_alternative = {
        lang_en: (lang_es,),
        lang_es: (lang_en,),
    }

    def __init__(self, extract=True, fileSuffix: str = '', locale: gettext.GNUTranslations = lang_en, bufferSize=100):
        self.toExtract = extract  # Should this object extract messages into intermediate file or just duplicate gettext
        self.file = str(Path(
            os.path.abspath(__file__)).parent.parent.absolute()/'i18n_l10n'/f'babel_intermediate{fileSuffix}.txt')
        self.words = set()  # Existing set of words, all languages together, read from the intermediate file.
        self.newWords = dict()  # Words found via extract() not yet in self.words. A dict to preserve insertion order.
        self.bufferSize = bufferSize  # Num words to accumulate in self.newWords before appending contents to self.file
        self.curLocale: gettext.GNUTranslations = None  # Current language assigned by last call to self.setLang().
        self.setLang(locale)
        self.firstWrite = True  # Stores if the object has or hasn't yet written via flush().
        if extract:
            self.load()

    # def __del__(self):
    #     self.flush()
        # super().__del__()

    def load(self) -> None:
        """
        Loads a previously written babel intermediate file into memory.
        The only parsing and checking of the file is what's implemented in this method.
        Any line not starting with a '_' is ignored, all other lines are read in assuming they are enclosed in '_()'.
        """
        with open(self.file, 'r', encoding='utf-8') as words:
            # bytes.decode() is to invert the repr() done in flush().
            self.words = {bytes(x[3:-3], 'utf-8').decode('unicode_escape') for x in words.readlines()
                          if len(x) > 0 and x[0] == '_'}

    def extract(self, x: str, locale: gettext.GNUTranslations = None) -> str:
        """
        Adds s to self.newWords to be added to the .pot file later.
        Returns the translation of s according to the indicated language.
        :param locale: Language to use for the immediate translation.
        :param x: Any string to be extracted and translated, passed in any language.
        If data of any other type is passed, it is converted to a string via str(s).
        :return: s translated according to lang
        """
        if locale is None:
            locale = self.curLocale
        if not isinstance(x, str):
            x = str(x)
        strings = x.split('\n\n')
        # translated: List[str] = []
        for s in strings:
            decoded = bytes(s, 'utf-8').decode('unicode_escape')
            if decoded not in self.words and decoded not in self.newWords:
                self.newWords[decoded] = None
            # translated.append(locale.gettext(s))
            # if translated[-1] == s and locale is not lang_en:  # Str is in another language and nothing provided in .po file
            #     translated[-1] = _google_translator.translate(s, src='en', dest=_google_locale_dict[locale])
        if len(self.newWords) >= self.bufferSize:
            self.flush()
        return '\n\n'.join([locale.gettext(s) for s in strings]) if len(strings) > 1 else locale.gettext(x)
    #     if s not in self.words and s not in self.newWords:
    #         self.newWords.add(s)
    #         if len(self.newWords) >= self.bufferSize:
    #             self.flush()
    #     return locale.gettext(s)

    def setLang(self, locale: gettext.GNUTranslations) -> None:
        """
        Sets the locale to be used by builtin translation functions.
        Sets bindings for several functions in builtins which are visible across all modules.
        If self.toExtract is True, then the bound functions both translate and extract new tokens to intermediate file.
        Else, the bound functions simply wrap gettext.gettext with postprocessing on the translated strings.
        _a: simple gettext, no postprocessing
        _b: simple gettext for the alternate language specified in cls.lang_alternative
        _k: 'keep capitalization': Duplicates functionality of _a. Uses: titles
        _e: 'enums': Uses: kiwilib.Aliasable instances that contain their own translation data. Only standardize caps.
        _ebt: 'enum backticks': Uses: Same as `_e` but surrounds output with backticks for markdown printing.
        _t: 'tokens': Uses: Description tokens and strings, whose presented capitalization should be uniform.
        :param locale: Locale to set
        """
        self.curLocale = locale
        if not self.toExtract:  # Normal gettext functions
            builtins._a = locale.gettext
            builtins._b = self.lang_alternative[locale][0].gettext
            builtins._k = locale.gettext
            builtins._e = lambda x: x.alias(locale_to_str[locale]).upper()
            builtins._ebt = lambda x: ''.join(['`', x.alias(locale_to_str[locale]).upper(), '`'])
            builtins._t = lambda x: locale.gettext(x).capitalize()
            # locale.install()
        else:  # Extract and return normal gettext
            builtins._a = self.extract
            builtins._b = lambda x: self.extract(x, self.lang_alternative[locale][0])
            builtins._k = self.extract
            builtins._e = lambda x: x.alias(locale_to_str[locale]).upper()
            builtins._ebt = lambda x: ''.join(['`', x.alias(locale_to_str[locale]).upper(), '`'])
            builtins._t = lambda x: self.extract(x).capitalize()
        # print(f'***SETTING LOCALE***\n  _a(): {locale._info["language"]}\n'
        #       f'  _b(): {self.lang_alternative[locale][0]._info["language"]}\n')

    def flush(self):
        """ FLush the buffer in self.newWords."""
        if len(self.newWords) == 0:
            return
        with open(self.file, 'a', encoding='utf-8') as f:
            if self.firstWrite:
                f.write(f'\n***WRITE*** {datetime.now()}\nEXTRACTION SUMMARY (MANUAL ENTRY): \n')
                self.firstWrite = False
            f.writelines([''.join(['_(', repr(s), ')\n']) for s in self.newWords])
        self.words.update(self.newWords)
        self.newWords.clear()


babelx = BabelIntermediateExtractor(extract=True, locale=lang_en, bufferSize=50)


class EnglishSpanishEnum(kiwilib.AliasableEnum):
    @staticmethod
    def _get_dataclass() -> kiwilib.IsDataclass:
        @dataclass(frozen=True)
        class L10nEngEsp:
            en_US: str = ""
            es_MX: str = ""
        return L10nEngEsp

    @classmethod
    def aliasFuncs(cls) -> Dict[str, Callable]:
        return {
           'en_US': lambda slf: slf.en_US if slf.en_US != "" else slf.name.replace('_', ' '),
           'es_MX': lambda slf: slf.es_MX if slf.es_MX != "" else slf.name.replace('_', ' ')+'o',
        }


def test2():
    babelx = BabelIntermediateExtractor(extract=False, locale=lang_es, bufferSize=5)
    _a('Test 1')
    _a('Avg Sleep by Weekday and Epoch Group')
    _a('REUNIÓN')
    _a('Reunión')
    # _a()


# if __name__ == '__main__':
#     test2()