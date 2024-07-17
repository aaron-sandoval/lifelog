'''
Created on Jan 26, 2018

@author: Aaron

A container for a task description, including methods for standardization for
easier classification. Contains data members for the raw description string and
some processed formats.
'''

import re
import pandas as pd
import src.DescriptionSTDLISTS as STDList
import anytree
from src.TimesheetGlobals import NULL_FIELD, SingleInstanceColumn, ColumnEnum
from pandas.core.dtypes.inference import is_list_like
from builtins import int, str
from typing import Iterable, List, Union
from src.Catalogs import *


class Description(SingleInstanceColumn):
    """
    classdocs
    An object field to structure the string descriptions of tasks.
    """

    '''
    location = Location()  # Location object
    people = []  # List of enums
    media = [] # list of objects
    exclusivityCollection = BodyParts() # object containing data about tokens associated with body part logic
    foods = [] # list of enums, e.g., CARNE_ACCIDENTAL, CARNE_PURPOSEFUL, MEXICANA, GRATIS, COMPRADO
    '''
    _collxTokensMarked = set()  # List used to store the tokens marked by PPDescTokens() to avoid extra work

    def __init__(self, rawString):
        self.string_RAW = rawString # Don't modify. For meta-analysis.
        self.tokens_RAW = descDelimit(rawString) # Not to be modified
        self.tokens = None  # All the None values to be overwritten shortly in initExceptRaw
        self.standardString = None
        self.tokenTree = None
        self.initExceptRaw(rawString)
        
    def initExceptRaw(self, rawString):
        self.tokens = self.PPDescTokens(descDelimit(stdDelimiters(stdDiction(stdPlural(rawString.upper())))))
        if len(self.tokens) != len(set(self.tokens)):  # Delete the later instances of any duplicate tokens
            debug = 1
        #     for i in range(len(self.tokens)-1, -1, -1):
        #         if self.tokens[i] in self.tokens[:i]:
        #             self.tokens.pop(i)
        self.standardString = '' if emptyDesc(self.tokens) else ', '.join(self.tokens)
        self.tokenTree = self.genTokenTree(self.tokens)

    @staticmethod
    def dfcolumn() -> str:
        return 'description'

    def __eq__(self, other):
        # TODO: return True for isomorphic tokenTrees
        if not isinstance(other, type(self)):
            return False
        if self.tokens != other.tokens:
            print(f'Mismatch:\n{self.tokens=}\n{other.tokens=}')
            return False
        for t1, t2 in zip(anytree.PostOrderIter(self.tokenTree), anytree.PostOrderIter(other.tokenTree)):
            if t1.name != t2.name:
                print(f'Mismatch:\n{t1.name=}\n{t2.name=}')
                return False
        return True
    
    def __str__(self):
        return self.standardString

    def __repr__(self):
        return self.standardString

    def __contains__(self, item):
        return self.hasToken(item)
    
    def printTree(self):
        print(anytree.RenderTree(self.tokenTree))
        
    def printTokens(self):
        print(f"Description: {self.tokens}")
        
    def addToken(self, tok: str, ind=None):
        """
        Adds a token to the description and updates all necessary internal data structures.
        Does NOT check for duplicate tokens.
        Calling procedures should always do that check since there might be specific cases to have duplicate tokens.
        :param tok: Token to add
        :param ind: Index at which toekn should be added. Reflected both in the list and tree
        :return: None
        """
        # TODO: implement functionality for ind is specified
        def addTokenToTree(treeRoot, tok, ind=None):
            anytree.Node(tok, parent=treeRoot)
            # treeRoot.
        if not isinstance(tok, str):
            raise TypeError(f'{tok.__class__()} {tok} must be a string')
        if ind:
            raise NotImplementedError(f"Dev hasn't yet built functionality for adding descToken at a specific index.")
        self.tokens.append(tok)
        self.standardString = catTokens(self.tokens)
        addTokenToTree(self.tokenTree, tok, ind)

    def removeToken(self, val: Union[str, Iterable, anytree.Node]) -> Union[bool, List[bool]]:
        """
        Removes a token from the object if present and updates all associated data structures
        :param val: Either the list index or string representation of the token to be removed, or a list_like thereof
        :return: Boolean to indicate if a token was removed or not, or a list_like thereof
        """
        def removeTokenFromTree(treeRoot, tok: Union[str, anytree.Node]):
            """
            Removes a token node, if present, linking all orphan children to the parent node
            :param treeRoot: Root node of the tree to be searched
            :param tok: Token to delete
            """
            if isinstance(tok, str):
                found = anytree.search.find(treeRoot, lambda node: node.name == tok)
                if not found: return treeRoot
            elif isinstance(tok, anytree.Node):
                found = tok
            orphans = found.children
            for orphan in orphans:
                orphan.parent = orphan.parent.parent
            found.parent = None # Detach node to delete from the tree
            
        if is_list_like(val):
            return [self.removeToken(v) for v in val]
        if isinstance(val, anytree.Node):
            if val.name not in self.tokens: return False
            for i, nd in enumerate(anytree.PreOrderIter(self.tokenTree)):
                if val is nd:
                    del self.tokens[i-1]
                    self.standardString = catTokens(self.tokens)
                    removeTokenFromTree(self.tokenTree, val)
                    return True           
            raise ValueError(f"{val} not found in tokenTree of {self}")
        if isinstance(val, int):
            if val >= len(self.tokens):
                raise IndexError(f'ERROR: Index {val} to remove out of bounds of {self.tokens}')
            token = self.tokens[val]
        elif isinstance(val, str): token = val
        if token not in self.tokens: return False
        self.tokens.remove(token)
        self.standardString = catTokens(self.tokens)
        removeTokenFromTree(self.tokenTree, token)
        return True

    def replaceToken(self, old: str, new: str) -> bool:
        """
        Replaces all instances of old with new in the description tokens and tokenTree.
        :return: 0 if no replacements were made, 1 if at least one was made
        """
        if old not in self.tokens: return False
        for i, tok in enumerate(self.tokens):
            if tok == old:
                self.tokens[i] = new
        self.standardString = catTokens(self.tokens)
        nodesToReplace = anytree.search.findall(self.tokenTree, lambda node: node.name == old)
        for node in nodesToReplace:
            node.name = new
        return True

    def hasToken(self, toks: Union[str, Iterable]) -> bool:
        """
        Checks if all of the toks are in the token list.
        For an input string containing a comma, checks self.standardString instead of self.tokens.
        Therefore, with a comma, it only returns True if that unbroken sequence of tokens is present.
        :param toks: A single or list-like object of tokens
        :return:
        """
        if not is_list_like(toks):
            toks = (toks,)
        for tok in toks:
            if ',' in tok:
                return tok in self.standardString
            elif tok not in self.tokens:
                return False
        return True

    def count(self, tok: str) -> int:
        """ Returns the number of instances `tok` is found in `self.tokens`.
        """
        return self.tokens.count(tok)

    def isEmpty(self) -> bool:
        return len(self.tokens) == 0

    def numChildren(self, tok: str) -> int:
        """
        Returns the number of children of a token in the token tree
        :param tok: Token to check
        :return: Number of children
        """
        found = anytree.search.find(self.tokenTree, lambda node: node.name == tok)
        if not found: return -1
        return len(found.children)

    def getSubTree(self, tok: str) -> anytree.node:
        """
        Returns the subtree of a token in the token tree
        :param tok: Token to check
        :return: Subtree
        """
        found = anytree.search.find(self.tokenTree, lambda node: node.name == tok)
        if not found: return None
        return found

    def getChildToks(self, tok: str) -> List[str]:
        """
        Returns the children of a token in the token tree.
        If >1 instances of `tok` are present, returns all children in a single list.
        :param tok: Token to check
        :return: List of children
        """
        # found = anytree.search.find(self.tokenTree, lambda node: node.name == tok)
        if not self.hasToken(tok): return pd.NA
        if self.tokens.count(tok) > 1:
            return [child.name for node in anytree.search.findall(self.tokenTree, lambda node: node.name == tok) for child in node.children]
        return [child.name for child in self.getSubTree(tok).children if child is not None]

    def getParentToks(self, tok: str) -> Tuple[str]:
        """
        Returns the parent tokens of `tok` in `self.tokenTree`.
        If `tok` is not found, returns an empty tuple.
        Almost all the time, the length of the returned tuple will be 1.
        In cases of duplicate tokens, the returned tuple may have length > 1.
        """
        # matches: tuple[anytree.Node] = anytree.search.findall(self.tokenTree, filter_=lambda node: node.name == tok)
        return tuple(m.parent.name for m in anytree.search.findall(self.tokenTree, filter_=lambda node: node.name == tok))
        # if len(matches) == 0:
        #     raise KeyError(f"'{tok}' not found in Description object {self}.")
        # if len(matches) > 1 and len({m.parent.name for m in matches}) > 1:
        #     raise ValueError(f"'{tok}' appears multiple times in {self}, with differeing parent tokens.")
        # return matches[0].parent.name

    @staticmethod
    def genTokenTree(toks: Iterable[str]):
        """ Parses predefined hierarchical tokens to generate a token tree structure """
        treeRoot = anytree.Node('ROOT')
        if emptyDesc(toks):
            return treeRoot
        # nodes = [anytree.Node] * len(toks)
        parent = treeRoot
        for tok in toks:
            while rejectChild(parent.name, tok):
                parent = parent.parent
            node = anytree.Node(tok, parent=parent)
            if tok in STDList.STD_ROOTS: parent = node
        #         else: parent = treeRoot
        #     if(len(toks) > 1):
        #         print(anytree.RenderTree(treeRoot))
        return treeRoot

    # Standardizes itemized description using
    @classmethod
    def PPDescTokens(cls, DT):  # TODO: migrate some of these to DC
        #     if(('MERIENDA' in DT) & (not isSublist(['COMER', 'MERIENDA'], DT))):
        #         if('COMER' in DT):  DT.remove('COMER')
        # #         insertInd = DT.index('MERIENDA')
        #         DT.insert(DT.index('MERIENDA'), 'COMER')
        if emptyDesc(DT):
            return []
        if ('DOCUMENTACION' in DT) & ('LEER' not in DT) & ('ESCRIBIR' not in DT):
            DT.insert(DT.index('DOCUMENTACION'), 'ESCRIBIR')
        if ('PROPUESTA DEL PROYECTO' in DT) & ('LEER' not in DT) & ('ESCRIBIR' not in DT):
            DT.insert(DT.index('PROPUESTA DEL PROYECTO'), 'ESCRIBIR')
        if ('PROPUESTA' in DT) & ('LEER' not in DT) & ('ESCRIBIR' not in DT):
            DT.insert(DT.index('PROPUESTA'), 'ESCRIBIR')
        if ('AUTO' in DT) & ('PASAJERO' in DT):
            DT.remove('PASAJERO')
        if ('JUEGOS DE MESA' in DT) & ('JUGAR' not in DT) & ('INVESTIGAR' not in DT):
            DT.insert(DT.index('JUEGOS DE MESA'), 'JUGAR')
        if ('DIARIO' in DT) & ('ESCRIBIR' not in DT) & ('LEER' not in DT):
            DT.insert(DT.index('DIARIO'), 'ESCRIBIR')
        if ('COMESTIBLES' in DT) & ('COMPRAR' not in DT):
            DT.insert(DT.index('COMESTIBLES'), 'COMPRAR')
        if ('SOLICITUDES' in DT) & ('EMPLEO' in DT):
            DT.remove('EMPLEO')
        if ('SOLICITUDES' in DT) & ('ESCRIBIR' not in DT):
            DT.insert(DT.index('SOLICITUDES'), 'ESCRIBIR')
        if ('TIMESHEET ANALISIS' in DT) & (len(DT) == 1):
            DT.append('PYTHON')
            DT.append('FM')  # It should be that all bare descs are in early FM
        if 'TV' in DT and (DT.index('TV')==len(DT)-1 or
                           DT[DT.index('TV')+1] in STDList.STD_ROOTS.union(STDList.COLLXBLE_INSTANCES)-STDList.STD_TV):
            DT.insert(DT.index('TV')+1, 'TVSHOW_UNDEFINED')
        collxbleInds = [tok in STDList.PEOPLE_ALL-cls._collxTokensMarked for tok in DT]  # Person
        if any(collxbleInds) and \
                not any([t in DT for t in (Person.INITIALIZATION_TOKENS() + ("SKYPE", "MENSAJEAR", "VISITAR"))]):
            DT.insert(collxbleInds.index(True), Person.tempInitToken())
            cls._collxTokensMarked.update([DT[1:][i] for i, b in enumerate(collxbleInds) if b])
        collxbleInds = [tok in STDList.PODCASTS - cls._collxTokensMarked for tok in DT]  # Podcast
        if any(collxbleInds) and \
                not any([t in DT for t in Podcast.INITIALIZATION_TOKENS()]):
            DT.insert(collxbleInds.index(True), Podcast.tempInitToken())
            cls._collxTokensMarked.update([DT[1:][i] for i, b in enumerate(collxbleInds) if b])
        collxbleInds = [tok in STDList.PODCASTS for tok in DT[:-1]]  # Not applicable if the only podcast is the final token
        if any(collxbleInds):
            for i in range(len(DT)-2,-1,-1):
                if collxbleInds[i] and \
                DT[i+1] != 'TEMAS' and \
                DT[i+1] not in STDList.STD_ROOTS.union(STDList.PODCASTS):
                    if DT[i+1] not in (STDList.COLLXBLE_INSTANCES.union(STDList.STD_ROOTS) - STDList.STD_SUBJECT_MATTERS):
                        DT.insert(i+1, "TEMAS")
        # collxbleInds = [tok in STDList.STD_FOODS - STDList.STD_SUBJECT_MATTERS for tok in DT]  # Food
        # if any(collxbleInds) and 'COMER' not in DT:
        #     DT.insert(collxbleInds.index(True), 'COMER')
        # cls._collxTokensMarked.update([tok for i, tok in enumerate(DT[1:]) if peopleInds[i]])
        # if any([tok in STDList.PODCASTS for tok in DT]) and\
        #         not any([t in DT for t in (Podcast.INITIALIZATION_TOKENS() + (Podcast.tempInitToken(),))]):
        #     DT.insert([tok in STDList.PODCASTS for tok in DT].index(True), Podcast.tempInitToken())
        return DT


def rejectChild(parent: str, tok: str):
    """
    Returns false unless the parent arg has been pre-determined to reject the arg tok.
    Example: 'COMER' parent should reject all elements of PEOPLE_ALL
    """
    if parent == 'ROOT': return False
    if tok in STDList.STD_ROOTS: return True
    if parent in {'INVESTIGAR', 'LEER', 'TEMAS'}:
        if tok in STDList.SOFTWARE_ALL: return False
    # TODO: A bunch of special cases to be added. COMER case is an example.
    if (parent not in Person.INITIALIZATION_TOKENS() and tok in STDList.PEOPLE_ALL):
        return True
    if parent in Person.INITIALIZATION_TOKENS() and (re.search('[0-9]', tok) or tok in (STDList.COLLXBLE_INSTANCES-STDList.PEOPLE_ALL)):
        return True
    if parent == 'COMER' and tok not in STDList.STD_FOODS:
        return True
    if parent in Podcast.INITIALIZATION_TOKENS() and tok in (STDList.COLLXBLE_INSTANCES-STDList.PODCASTS):
        return True
    # if parent in STDList.PODCASTS and tok not in (STDList.COLLXBLE_INSTANCES.union(STDList.STD_ROOTs) - STDList.STD_SUBJECT_MATTERS):
    #     return False
    return False

# Replaces certain words according to a reference list to standardize the
# diction in a dataset
def stdDiction(inputString):
    """
    Replaces certain words according to a reference list to standardize diction in a dataset
    :param inputString:
    :return:
    """
    # outputString = inputString
    for substitutionSet in STDList.STD_DICTION:
        if substitutionSet in inputString:
            inputString = dictionaryReplace(inputString, substitutionSet, STDList.STD_DICTION)
    return inputString


def stdPlural(inputString):
    """
    Replaces words based on plurality, not diction.
    :param inputString:
    :return: String with corrected plurality
    """
    for substitutionSet in STDList.STD_PLURAL:
        if substitutionSet in inputString:
            inputString = dictionaryReplace(inputString, substitutionSet, STDList.STD_PLURAL)
    return inputString


def stdDelimiters(inputString):
    """
    Inserts delimiters after certain words, with removal of some minor words
    :param inputString:
    :return: Delimited string
    """
    outputString = inputString
    for substitutionSet in STDList.STD_DELIMIT_LIST:
        if substitutionSet in outputString:
            regex = [0]*2
            regex[0] = '(?<=\w)' + '\s' + re.escape(substitutionSet)
            regex[1] = re.escape(substitutionSet) + '\s' + '(?=\w)'
            outputString = re.sub(regex[0], ', ' + substitutionSet, outputString)
            outputString = re.sub(regex[1], substitutionSet + ', ', outputString)
    return outputString


def descDelimit(inputString: str) -> List[str]:
    """
    Delimits inputString into a list, parsing commas and double quotes as delimiters.
    :raises error when inputString has an odd number of double quote chars and fallback conditions not met.
    Does not delimit by commas inside double-quoted segments.
    :return: List representing the tokenized inputString
    """
    if not '"' in inputString:
        return [tok.strip() for tok in inputString.strip(', ').split(',')]
    if inputString.count('"') % 2 != 0:  # Handle rare case of odd number of double quote chars
        if re.search(' a [^,"]+,[^,"]+"', inputString, flags=re.IGNORECASE):
            # Ex: 'Montar, cicloturismo, "Ciudad X" a Ciudad Y, Sinaloa"'
            inputString = re.sub(' a [^,"]+,[^,"]+"', lambda x: x.group(0)[:3] + '"' + x.group(0)[3:], inputString,
                                 count=1, flags=re.IGNORECASE)
        elif re.search('"[^"\']+\'', inputString, flags=re.IGNORECASE):
            #  Ex: 'Montar, cicloturismo, Belorado a "Villafranca Montes de Oca, España\''
            inputString = re.sub('"[^"\']+\'', lambda x: x.group(0)[:-1] + '"', inputString, count=1)
        else:
            raise NameError(f'Cannot tokenize string, double quotation marks are imbalanced: {inputString}')
    quoteSplit = [tok.strip() for tok in inputString.split('"')]
    for i in range(len(quoteSplit)-1, -1, -2): # For each portion outside of double quotes
        quoteSplit[i:i+1] = [tok.strip() for tok in quoteSplit[i].split(',')]
    return [q for q in quoteSplit if q != '']


def isSublist(sublist, bigList)-> bool:
    """
    Returns boolean True if the sublist is contained within bigList exactly in order without interruptions
    :param sublist: List to search for in bigList
    :param bigList: List potentially containing subList
    :return: boolean if sublist in bigList
    """
    if (len(sublist) > len(bigList)) | (sublist[0] not in bigList): return False
    st = bigList.index(sublist[0])
    sublistLen = len(sublist)
    if len(bigList) < st + sublistLen: return False
    return sublist == bigList[st:st+sublistLen]


def dictionaryReplace(inputString, target, dct):
    """
    After initial checks, replaces the target in inputString with the value in dct
    :param inputString: String to be searched on
    :param target: Search target to be replaced
    :param dct: A dictionary mapping targets to replacement values to substitute in
    :return:
    """
    if target in dct[target]:
        regex = '(?<!\w)' + target + '(?!\w)'
        outputString = re.sub(regex, dct[target], inputString)
    else:
        outputString = re.sub(target, dct[target], inputString)
    return outputString


def emptyDesc(data):
    """
    Catchall for all forms of descStrings that indicate an empty Description
    :param data: A variety of data types accepted, the data to check if it indicates an empty Description
    :return: 0 if the arg is not empty; 1 if the arg indicates an empty Description
    """
    if data is None: return 1
    if is_list_like(data):
        return len(data) == 0 or emptyDesc(data[0])
    else:
        return data == '' or data == NULL_FIELD


# Simple string concatenation
def catTokens(toks, delim = ', '):
    if emptyDesc(toks): return ''
    out = toks[0]
    for tk in toks[1:]: out += delim + tk  
    return out


# Returns a list with the index of each token in lst. If a token is not present
#, that entry = 0
# def searchList(tokens, lst):
#     retVal = [-1]*len(tokens)
#     for i, token in enumerate(tokens):
#         try:
#             retVal[i] = lst.index(token)
#         except ValueError:
#             pass
# #             retVal[i] = -1
#     return retVal
