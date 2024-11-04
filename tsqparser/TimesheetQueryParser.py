# Generated from TimesheetQuery.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,65,258,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,1,0,5,0,64,8,0,10,0,12,0,
        67,9,0,1,0,1,0,1,1,3,1,72,8,1,1,1,1,1,1,1,1,1,5,1,78,8,1,10,1,12,
        1,81,9,1,3,1,83,8,1,1,1,1,1,1,2,1,2,1,3,1,3,1,3,1,3,3,3,93,8,3,1,
        4,1,4,1,5,1,5,1,6,1,6,1,7,1,7,1,8,1,8,1,8,1,8,3,8,107,8,8,1,8,1,
        8,1,8,1,8,3,8,113,8,8,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,
        9,3,9,126,8,9,1,10,1,10,1,10,1,10,3,10,132,8,10,1,11,3,11,135,8,
        11,1,11,1,11,1,11,1,11,1,11,3,11,142,8,11,1,12,1,12,3,12,146,8,12,
        1,13,1,13,1,14,1,14,3,14,152,8,14,1,15,1,15,1,16,1,16,1,16,3,16,
        159,8,16,1,17,1,17,1,17,1,17,1,17,1,17,3,17,167,8,17,1,18,1,18,1,
        19,1,19,1,19,3,19,174,8,19,1,20,1,20,1,20,1,20,1,20,1,20,1,21,1,
        21,1,21,1,21,1,21,1,21,3,21,188,8,21,1,22,1,22,1,23,1,23,1,23,1,
        24,1,24,1,24,1,25,1,25,1,25,1,26,1,26,1,26,1,27,1,27,1,28,1,28,1,
        28,3,28,209,8,28,1,29,1,29,1,29,1,29,5,29,215,8,29,10,29,12,29,218,
        9,29,1,29,1,29,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,3,30,
        231,8,30,1,30,1,30,1,30,3,30,236,8,30,1,30,1,30,1,30,3,30,241,8,
        30,1,30,1,30,1,30,3,30,246,8,30,1,30,1,30,1,30,3,30,251,8,30,1,30,
        3,30,254,8,30,1,30,1,30,1,30,0,0,31,0,2,4,6,8,10,12,14,16,18,20,
        22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,0,4,
        1,0,4,5,1,0,6,12,1,0,15,35,1,0,42,44,264,0,65,1,0,0,0,2,71,1,0,0,
        0,4,86,1,0,0,0,6,92,1,0,0,0,8,94,1,0,0,0,10,96,1,0,0,0,12,98,1,0,
        0,0,14,100,1,0,0,0,16,112,1,0,0,0,18,125,1,0,0,0,20,131,1,0,0,0,
        22,134,1,0,0,0,24,145,1,0,0,0,26,147,1,0,0,0,28,151,1,0,0,0,30,153,
        1,0,0,0,32,158,1,0,0,0,34,166,1,0,0,0,36,168,1,0,0,0,38,173,1,0,
        0,0,40,175,1,0,0,0,42,181,1,0,0,0,44,189,1,0,0,0,46,191,1,0,0,0,
        48,194,1,0,0,0,50,197,1,0,0,0,52,200,1,0,0,0,54,203,1,0,0,0,56,205,
        1,0,0,0,58,210,1,0,0,0,60,221,1,0,0,0,62,64,3,2,1,0,63,62,1,0,0,
        0,64,67,1,0,0,0,65,63,1,0,0,0,65,66,1,0,0,0,66,68,1,0,0,0,67,65,
        1,0,0,0,68,69,5,0,0,1,69,1,1,0,0,0,70,72,3,4,2,0,71,70,1,0,0,0,71,
        72,1,0,0,0,72,73,1,0,0,0,73,82,5,1,0,0,74,79,3,6,3,0,75,76,5,2,0,
        0,76,78,3,6,3,0,77,75,1,0,0,0,78,81,1,0,0,0,79,77,1,0,0,0,79,80,
        1,0,0,0,80,83,1,0,0,0,81,79,1,0,0,0,82,74,1,0,0,0,82,83,1,0,0,0,
        83,84,1,0,0,0,84,85,5,2,0,0,85,3,1,0,0,0,86,87,3,14,7,0,87,5,1,0,
        0,0,88,93,3,32,16,0,89,90,5,3,0,0,90,93,3,32,16,0,91,93,3,28,14,
        0,92,88,1,0,0,0,92,89,1,0,0,0,92,91,1,0,0,0,93,7,1,0,0,0,94,95,5,
        3,0,0,95,9,1,0,0,0,96,97,7,0,0,0,97,11,1,0,0,0,98,99,7,1,0,0,99,
        13,1,0,0,0,100,101,3,16,8,0,101,15,1,0,0,0,102,106,3,18,9,0,103,
        104,3,10,5,0,104,105,3,18,9,0,105,107,1,0,0,0,106,103,1,0,0,0,106,
        107,1,0,0,0,107,113,1,0,0,0,108,109,3,18,9,0,109,110,3,10,5,0,110,
        111,3,16,8,0,111,113,1,0,0,0,112,102,1,0,0,0,112,108,1,0,0,0,113,
        17,1,0,0,0,114,115,3,32,16,0,115,116,3,12,6,0,116,117,3,24,12,0,
        117,126,1,0,0,0,118,119,3,24,12,0,119,120,3,12,6,0,120,121,1,0,0,
        0,121,122,3,32,16,0,122,126,1,0,0,0,123,126,3,20,10,0,124,126,3,
        22,11,0,125,114,1,0,0,0,125,118,1,0,0,0,125,123,1,0,0,0,125,124,
        1,0,0,0,126,19,1,0,0,0,127,132,3,34,17,0,128,132,3,36,18,0,129,132,
        3,38,19,0,130,132,3,30,15,0,131,127,1,0,0,0,131,128,1,0,0,0,131,
        129,1,0,0,0,131,130,1,0,0,0,132,21,1,0,0,0,133,135,3,8,4,0,134,133,
        1,0,0,0,134,135,1,0,0,0,135,141,1,0,0,0,136,142,3,20,10,0,137,138,
        5,13,0,0,138,139,3,14,7,0,139,140,5,14,0,0,140,142,1,0,0,0,141,136,
        1,0,0,0,141,137,1,0,0,0,142,23,1,0,0,0,143,146,3,30,15,0,144,146,
        3,26,13,0,145,143,1,0,0,0,145,144,1,0,0,0,146,25,1,0,0,0,147,148,
        3,42,21,0,148,27,1,0,0,0,149,152,3,40,20,0,150,152,3,44,22,0,151,
        149,1,0,0,0,151,150,1,0,0,0,152,29,1,0,0,0,153,154,7,2,0,0,154,31,
        1,0,0,0,155,159,3,34,17,0,156,159,3,36,18,0,157,159,3,38,19,0,158,
        155,1,0,0,0,158,156,1,0,0,0,158,157,1,0,0,0,159,33,1,0,0,0,160,167,
        3,46,23,0,161,167,3,52,26,0,162,167,3,58,29,0,163,167,3,60,30,0,
        164,167,3,48,24,0,165,167,3,56,28,0,166,160,1,0,0,0,166,161,1,0,
        0,0,166,162,1,0,0,0,166,163,1,0,0,0,166,164,1,0,0,0,166,165,1,0,
        0,0,167,35,1,0,0,0,168,169,3,50,25,0,169,37,1,0,0,0,170,174,3,54,
        27,0,171,174,5,60,0,0,172,174,5,61,0,0,173,170,1,0,0,0,173,171,1,
        0,0,0,173,172,1,0,0,0,174,39,1,0,0,0,175,176,3,32,16,0,176,177,5,
        36,0,0,177,178,5,13,0,0,178,179,3,32,16,0,179,180,5,14,0,0,180,41,
        1,0,0,0,181,182,5,37,0,0,182,187,5,62,0,0,183,184,5,38,0,0,184,185,
        3,24,12,0,185,186,5,39,0,0,186,188,1,0,0,0,187,183,1,0,0,0,187,188,
        1,0,0,0,188,43,1,0,0,0,189,190,5,40,0,0,190,45,1,0,0,0,191,192,5,
        41,0,0,192,193,5,62,0,0,193,47,1,0,0,0,194,195,7,3,0,0,195,196,5,
        62,0,0,196,49,1,0,0,0,197,198,5,45,0,0,198,199,5,62,0,0,199,51,1,
        0,0,0,200,201,5,46,0,0,201,202,5,62,0,0,202,53,1,0,0,0,203,204,5,
        56,0,0,204,55,1,0,0,0,205,208,5,47,0,0,206,209,5,62,0,0,207,209,
        5,60,0,0,208,206,1,0,0,0,208,207,1,0,0,0,209,57,1,0,0,0,210,211,
        5,48,0,0,211,216,5,60,0,0,212,213,5,49,0,0,213,215,5,60,0,0,214,
        212,1,0,0,0,215,218,1,0,0,0,216,214,1,0,0,0,216,217,1,0,0,0,217,
        219,1,0,0,0,218,216,1,0,0,0,219,220,5,14,0,0,220,59,1,0,0,0,221,
        230,5,50,0,0,222,223,5,51,0,0,223,231,5,60,0,0,224,225,5,52,0,0,
        225,231,5,60,0,0,226,227,5,53,0,0,227,231,5,60,0,0,228,229,5,54,
        0,0,229,231,5,60,0,0,230,222,1,0,0,0,230,224,1,0,0,0,230,226,1,0,
        0,0,230,228,1,0,0,0,231,235,1,0,0,0,232,233,5,49,0,0,233,234,5,51,
        0,0,234,236,5,60,0,0,235,232,1,0,0,0,235,236,1,0,0,0,236,240,1,0,
        0,0,237,238,5,49,0,0,238,239,5,52,0,0,239,241,5,60,0,0,240,237,1,
        0,0,0,240,241,1,0,0,0,241,245,1,0,0,0,242,243,5,49,0,0,243,244,5,
        53,0,0,244,246,5,60,0,0,245,242,1,0,0,0,245,246,1,0,0,0,246,250,
        1,0,0,0,247,248,5,49,0,0,248,249,5,54,0,0,249,251,5,60,0,0,250,247,
        1,0,0,0,250,251,1,0,0,0,251,253,1,0,0,0,252,254,5,49,0,0,253,252,
        1,0,0,0,253,254,1,0,0,0,254,255,1,0,0,0,255,256,5,14,0,0,256,61,
        1,0,0,0,25,65,71,79,82,92,106,112,125,131,134,141,145,151,158,166,
        173,187,208,216,230,235,240,245,250,253
    ]

class TimesheetQueryParser ( Parser ):

    grammarFileName = "TimesheetQuery.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "':'", "';'", "'!'", "'|'", "'&'", "'>='", 
                     "'<='", "'>'", "'<'", "'!='", "'=='", "'in'", "'('", 
                     "')'", "'description'", "'project'", "'tags'", "'id'", 
                     "'start'", "'end'", "'duration'", "'epoch'", "'mood'", 
                     "'circad'", "'metaproject'", "'bodyparts'", "'Location'", 
                     "'Person'", "'Food'", "'Media'", "'Audiobook'", "'Podcast'", 
                     "'TVShow'", "'Movie'", "'SubjectMatter'", "'.replace'", 
                     "'EpochScheme.'", "'['", "']'", "'reloadDescription()'", 
                     "'Project.'", "'Metaproject.'", "'Meta.'", "'MP.'", 
                     "'Tag.'", "'Epoch.'", "'Mood.'", "'datetime('", "','", 
                     "'timedelta('", "'weeks='", "'days='", "'hours='", 
                     "'minutes='" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "BLOCK_COMMENT", 
                      "STRING_LITERAL", "STRING_LITERAL_DQ", "STRING_LITERAL_SQ", 
                      "INLINE_COMMENT", "INT", "FLOAT", "NAME", "WHITESPACE", 
                      "NEWLINE", "ANY" ]

    RULE_ruleList = 0
    RULE_rule = 1
    RULE_query = 2
    RULE_command = 3
    RULE_boolMonadicPrefixOp = 4
    RULE_boolDyadicInfixOp = 5
    RULE_comparisonInfixOp = 6
    RULE_boolExp = 7
    RULE_boolDyadicExp = 8
    RULE_comparisonExp = 9
    RULE_impliedComparisonExp = 10
    RULE_atomMonadicExp = 11
    RULE_series = 12
    RULE_seriesFunc = 13
    RULE_commandFunc = 14
    RULE_field = 15
    RULE_literal = 16
    RULE_singleInstLiteral = 17
    RULE_listElementLiteral = 18
    RULE_specialLiteral = 19
    RULE_literalReplaceFunc = 20
    RULE_epochSchemeIndex = 21
    RULE_reloadDesc = 22
    RULE_projectLiteral = 23
    RULE_metaprojectLiteral = 24
    RULE_tagLiteral = 25
    RULE_epochLiteral = 26
    RULE_descToken = 27
    RULE_moodLiteral = 28
    RULE_datetimeLiteral = 29
    RULE_timedeltaLiteral = 30

    ruleNames =  [ "ruleList", "rule", "query", "command", "boolMonadicPrefixOp", 
                   "boolDyadicInfixOp", "comparisonInfixOp", "boolExp", 
                   "boolDyadicExp", "comparisonExp", "impliedComparisonExp", 
                   "atomMonadicExp", "series", "seriesFunc", "commandFunc", 
                   "field", "literal", "singleInstLiteral", "listElementLiteral", 
                   "specialLiteral", "literalReplaceFunc", "epochSchemeIndex", 
                   "reloadDesc", "projectLiteral", "metaprojectLiteral", 
                   "tagLiteral", "epochLiteral", "descToken", "moodLiteral", 
                   "datetimeLiteral", "timedeltaLiteral" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    T__37=38
    T__38=39
    T__39=40
    T__40=41
    T__41=42
    T__42=43
    T__43=44
    T__44=45
    T__45=46
    T__46=47
    T__47=48
    T__48=49
    T__49=50
    T__50=51
    T__51=52
    T__52=53
    T__53=54
    BLOCK_COMMENT=55
    STRING_LITERAL=56
    STRING_LITERAL_DQ=57
    STRING_LITERAL_SQ=58
    INLINE_COMMENT=59
    INT=60
    FLOAT=61
    NAME=62
    WHITESPACE=63
    NEWLINE=64
    ANY=65

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RuleListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(TimesheetQueryParser.EOF, 0)

        def rule_(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimesheetQueryParser.RuleContext)
            else:
                return self.getTypedRuleContext(TimesheetQueryParser.RuleContext,i)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_ruleList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleList" ):
                listener.enterRuleList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleList" ):
                listener.exitRuleList(self)




    def ruleList(self):

        localctx = TimesheetQueryParser.RuleListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_ruleList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3532508964853882890) != 0):
                self.state = 62
                self.rule_()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 68
            self.match(TimesheetQueryParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def query(self):
            return self.getTypedRuleContext(TimesheetQueryParser.QueryContext,0)


        def command(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimesheetQueryParser.CommandContext)
            else:
                return self.getTypedRuleContext(TimesheetQueryParser.CommandContext,i)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_rule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRule" ):
                listener.enterRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRule" ):
                listener.exitRule(self)




    def rule_(self):

        localctx = TimesheetQueryParser.RuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_rule)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3532508964853882888) != 0):
                self.state = 70
                self.query()


            self.state = 73
            self.match(TimesheetQueryParser.T__0)
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3532509858207105032) != 0):
                self.state = 74
                self.command()
                self.state = 79
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 75
                        self.match(TimesheetQueryParser.T__1)
                        self.state = 76
                        self.command() 
                    self.state = 81
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,2,self._ctx)



            self.state = 84
            self.match(TimesheetQueryParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QueryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def boolExp(self):
            return self.getTypedRuleContext(TimesheetQueryParser.BoolExpContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_query

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery" ):
                listener.enterQuery(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery" ):
                listener.exitQuery(self)




    def query(self):

        localctx = TimesheetQueryParser.QueryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_query)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.boolExp()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_command

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SetLiteralContext(CommandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TimesheetQueryParser.CommandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(TimesheetQueryParser.LiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetLiteral" ):
                listener.enterSetLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetLiteral" ):
                listener.exitSetLiteral(self)


    class CmdFuncContext(CommandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TimesheetQueryParser.CommandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def commandFunc(self):
            return self.getTypedRuleContext(TimesheetQueryParser.CommandFuncContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCmdFunc" ):
                listener.enterCmdFunc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCmdFunc" ):
                listener.exitCmdFunc(self)


    class DeleteLiteralContext(CommandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TimesheetQueryParser.CommandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(TimesheetQueryParser.LiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeleteLiteral" ):
                listener.enterDeleteLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeleteLiteral" ):
                listener.exitDeleteLiteral(self)



    def command(self):

        localctx = TimesheetQueryParser.CommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_command)
        try:
            self.state = 92
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                localctx = TimesheetQueryParser.SetLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 88
                self.literal()
                pass

            elif la_ == 2:
                localctx = TimesheetQueryParser.DeleteLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 89
                self.match(TimesheetQueryParser.T__2)
                self.state = 90
                self.literal()
                pass

            elif la_ == 3:
                localctx = TimesheetQueryParser.CmdFuncContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 91
                self.commandFunc()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoolMonadicPrefixOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_boolMonadicPrefixOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolMonadicPrefixOp" ):
                listener.enterBoolMonadicPrefixOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolMonadicPrefixOp" ):
                listener.exitBoolMonadicPrefixOp(self)




    def boolMonadicPrefixOp(self):

        localctx = TimesheetQueryParser.BoolMonadicPrefixOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_boolMonadicPrefixOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.match(TimesheetQueryParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoolDyadicInfixOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_boolDyadicInfixOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolDyadicInfixOp" ):
                listener.enterBoolDyadicInfixOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolDyadicInfixOp" ):
                listener.exitBoolDyadicInfixOp(self)




    def boolDyadicInfixOp(self):

        localctx = TimesheetQueryParser.BoolDyadicInfixOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_boolDyadicInfixOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            _la = self._input.LA(1)
            if not(_la==4 or _la==5):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonInfixOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_comparisonInfixOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonInfixOp" ):
                listener.enterComparisonInfixOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonInfixOp" ):
                listener.exitComparisonInfixOp(self)




    def comparisonInfixOp(self):

        localctx = TimesheetQueryParser.ComparisonInfixOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_comparisonInfixOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8128) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoolExpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def boolDyadicExp(self):
            return self.getTypedRuleContext(TimesheetQueryParser.BoolDyadicExpContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_boolExp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolExp" ):
                listener.enterBoolExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolExp" ):
                listener.exitBoolExp(self)




    def boolExp(self):

        localctx = TimesheetQueryParser.BoolExpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_boolExp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            self.boolDyadicExp()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BoolDyadicExpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def comparisonExp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimesheetQueryParser.ComparisonExpContext)
            else:
                return self.getTypedRuleContext(TimesheetQueryParser.ComparisonExpContext,i)


        def boolDyadicInfixOp(self):
            return self.getTypedRuleContext(TimesheetQueryParser.BoolDyadicInfixOpContext,0)


        def boolDyadicExp(self):
            return self.getTypedRuleContext(TimesheetQueryParser.BoolDyadicExpContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_boolDyadicExp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolDyadicExp" ):
                listener.enterBoolDyadicExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolDyadicExp" ):
                listener.exitBoolDyadicExp(self)




    def boolDyadicExp(self):

        localctx = TimesheetQueryParser.BoolDyadicExpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_boolDyadicExp)
        self._la = 0 # Token type
        try:
            self.state = 112
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 102
                self.comparisonExp()
                self.state = 106
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==4 or _la==5:
                    self.state = 103
                    self.boolDyadicInfixOp()
                    self.state = 104
                    self.comparisonExp()


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 108
                self.comparisonExp()
                self.state = 109
                self.boolDyadicInfixOp()
                self.state = 110
                self.boolDyadicExp()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonExpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self):
            return self.getTypedRuleContext(TimesheetQueryParser.LiteralContext,0)


        def comparisonInfixOp(self):
            return self.getTypedRuleContext(TimesheetQueryParser.ComparisonInfixOpContext,0)


        def series(self):
            return self.getTypedRuleContext(TimesheetQueryParser.SeriesContext,0)


        def impliedComparisonExp(self):
            return self.getTypedRuleContext(TimesheetQueryParser.ImpliedComparisonExpContext,0)


        def atomMonadicExp(self):
            return self.getTypedRuleContext(TimesheetQueryParser.AtomMonadicExpContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_comparisonExp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonExp" ):
                listener.enterComparisonExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonExp" ):
                listener.exitComparisonExp(self)




    def comparisonExp(self):

        localctx = TimesheetQueryParser.ComparisonExpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_comparisonExp)
        try:
            self.state = 125
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 114
                self.literal()

                self.state = 115
                self.comparisonInfixOp()
                self.state = 116
                self.series()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 118
                self.series()
                self.state = 119
                self.comparisonInfixOp()
                self.state = 121
                self.literal()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 123
                self.impliedComparisonExp()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 124
                self.atomMonadicExp()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImpliedComparisonExpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_impliedComparisonExp

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ListElementImpliedExpContext(ImpliedComparisonExpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TimesheetQueryParser.ImpliedComparisonExpContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def listElementLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.ListElementLiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListElementImpliedExp" ):
                listener.enterListElementImpliedExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListElementImpliedExp" ):
                listener.exitListElementImpliedExp(self)


    class SpecialLiteralImpliedExpContext(ImpliedComparisonExpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TimesheetQueryParser.ImpliedComparisonExpContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def specialLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.SpecialLiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpecialLiteralImpliedExp" ):
                listener.enterSpecialLiteralImpliedExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpecialLiteralImpliedExp" ):
                listener.exitSpecialLiteralImpliedExp(self)


    class SingleInstanceImpliedExpContext(ImpliedComparisonExpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TimesheetQueryParser.ImpliedComparisonExpContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def singleInstLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.SingleInstLiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleInstanceImpliedExp" ):
                listener.enterSingleInstanceImpliedExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleInstanceImpliedExp" ):
                listener.exitSingleInstanceImpliedExp(self)


    class FieldImpliedExpContext(ImpliedComparisonExpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TimesheetQueryParser.ImpliedComparisonExpContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def field(self):
            return self.getTypedRuleContext(TimesheetQueryParser.FieldContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFieldImpliedExp" ):
                listener.enterFieldImpliedExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFieldImpliedExp" ):
                listener.exitFieldImpliedExp(self)



    def impliedComparisonExp(self):

        localctx = TimesheetQueryParser.ImpliedComparisonExpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_impliedComparisonExp)
        try:
            self.state = 131
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [41, 42, 43, 44, 46, 47, 48, 50]:
                localctx = TimesheetQueryParser.SingleInstanceImpliedExpContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 127
                self.singleInstLiteral()
                pass
            elif token in [45]:
                localctx = TimesheetQueryParser.ListElementImpliedExpContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 128
                self.listElementLiteral()
                pass
            elif token in [56, 60, 61]:
                localctx = TimesheetQueryParser.SpecialLiteralImpliedExpContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 129
                self.specialLiteral()
                pass
            elif token in [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]:
                localctx = TimesheetQueryParser.FieldImpliedExpContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 130
                self.field()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomMonadicExpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def impliedComparisonExp(self):
            return self.getTypedRuleContext(TimesheetQueryParser.ImpliedComparisonExpContext,0)


        def boolMonadicPrefixOp(self):
            return self.getTypedRuleContext(TimesheetQueryParser.BoolMonadicPrefixOpContext,0)


        def boolExp(self):
            return self.getTypedRuleContext(TimesheetQueryParser.BoolExpContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_atomMonadicExp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtomMonadicExp" ):
                listener.enterAtomMonadicExp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtomMonadicExp" ):
                listener.exitAtomMonadicExp(self)




    def atomMonadicExp(self):

        localctx = TimesheetQueryParser.AtomMonadicExpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_atomMonadicExp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 134
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==3:
                self.state = 133
                self.boolMonadicPrefixOp()


            self.state = 141
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45, 46, 47, 48, 50, 56, 60, 61]:
                self.state = 136
                self.impliedComparisonExp()
                pass
            elif token in [13]:
                self.state = 137
                self.match(TimesheetQueryParser.T__12)
                self.state = 138
                self.boolExp()
                self.state = 139
                self.match(TimesheetQueryParser.T__13)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SeriesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field(self):
            return self.getTypedRuleContext(TimesheetQueryParser.FieldContext,0)


        def seriesFunc(self):
            return self.getTypedRuleContext(TimesheetQueryParser.SeriesFuncContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_series

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSeries" ):
                listener.enterSeries(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSeries" ):
                listener.exitSeries(self)




    def series(self):

        localctx = TimesheetQueryParser.SeriesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_series)
        try:
            self.state = 145
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]:
                self.enterOuterAlt(localctx, 1)
                self.state = 143
                self.field()
                pass
            elif token in [37]:
                self.enterOuterAlt(localctx, 2)
                self.state = 144
                self.seriesFunc()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SeriesFuncContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def epochSchemeIndex(self):
            return self.getTypedRuleContext(TimesheetQueryParser.EpochSchemeIndexContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_seriesFunc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSeriesFunc" ):
                listener.enterSeriesFunc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSeriesFunc" ):
                listener.exitSeriesFunc(self)




    def seriesFunc(self):

        localctx = TimesheetQueryParser.SeriesFuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_seriesFunc)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self.epochSchemeIndex()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommandFuncContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literalReplaceFunc(self):
            return self.getTypedRuleContext(TimesheetQueryParser.LiteralReplaceFuncContext,0)


        def reloadDesc(self):
            return self.getTypedRuleContext(TimesheetQueryParser.ReloadDescContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_commandFunc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommandFunc" ):
                listener.enterCommandFunc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommandFunc" ):
                listener.exitCommandFunc(self)




    def commandFunc(self):

        localctx = TimesheetQueryParser.CommandFuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_commandFunc)
        try:
            self.state = 151
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [41, 42, 43, 44, 45, 46, 47, 48, 50, 56, 60, 61]:
                self.enterOuterAlt(localctx, 1)
                self.state = 149
                self.literalReplaceFunc()
                pass
            elif token in [40]:
                self.enterOuterAlt(localctx, 2)
                self.state = 150
                self.reloadDesc()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField" ):
                listener.enterField(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField" ):
                listener.exitField(self)




    def field(self):

        localctx = TimesheetQueryParser.FieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_field)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 153
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 68719443968) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def singleInstLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.SingleInstLiteralContext,0)


        def listElementLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.ListElementLiteralContext,0)


        def specialLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.SpecialLiteralContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)




    def literal(self):

        localctx = TimesheetQueryParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_literal)
        try:
            self.state = 158
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [41, 42, 43, 44, 46, 47, 48, 50]:
                self.enterOuterAlt(localctx, 1)
                self.state = 155
                self.singleInstLiteral()
                pass
            elif token in [45]:
                self.enterOuterAlt(localctx, 2)
                self.state = 156
                self.listElementLiteral()
                pass
            elif token in [56, 60, 61]:
                self.enterOuterAlt(localctx, 3)
                self.state = 157
                self.specialLiteral()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SingleInstLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def projectLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.ProjectLiteralContext,0)


        def epochLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.EpochLiteralContext,0)


        def datetimeLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.DatetimeLiteralContext,0)


        def timedeltaLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.TimedeltaLiteralContext,0)


        def metaprojectLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.MetaprojectLiteralContext,0)


        def moodLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.MoodLiteralContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_singleInstLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleInstLiteral" ):
                listener.enterSingleInstLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleInstLiteral" ):
                listener.exitSingleInstLiteral(self)




    def singleInstLiteral(self):

        localctx = TimesheetQueryParser.SingleInstLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_singleInstLiteral)
        try:
            self.state = 166
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [41]:
                self.enterOuterAlt(localctx, 1)
                self.state = 160
                self.projectLiteral()
                pass
            elif token in [46]:
                self.enterOuterAlt(localctx, 2)
                self.state = 161
                self.epochLiteral()
                pass
            elif token in [48]:
                self.enterOuterAlt(localctx, 3)
                self.state = 162
                self.datetimeLiteral()
                pass
            elif token in [50]:
                self.enterOuterAlt(localctx, 4)
                self.state = 163
                self.timedeltaLiteral()
                pass
            elif token in [42, 43, 44]:
                self.enterOuterAlt(localctx, 5)
                self.state = 164
                self.metaprojectLiteral()
                pass
            elif token in [47]:
                self.enterOuterAlt(localctx, 6)
                self.state = 165
                self.moodLiteral()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListElementLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def tagLiteral(self):
            return self.getTypedRuleContext(TimesheetQueryParser.TagLiteralContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_listElementLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListElementLiteral" ):
                listener.enterListElementLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListElementLiteral" ):
                listener.exitListElementLiteral(self)




    def listElementLiteral(self):

        localctx = TimesheetQueryParser.ListElementLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_listElementLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 168
            self.tagLiteral()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SpecialLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_specialLiteral

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class StringContext(SpecialLiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TimesheetQueryParser.SpecialLiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def descToken(self):
            return self.getTypedRuleContext(TimesheetQueryParser.DescTokenContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)


    class FloatPrimitiveContext(SpecialLiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TimesheetQueryParser.SpecialLiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(TimesheetQueryParser.FLOAT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFloatPrimitive" ):
                listener.enterFloatPrimitive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFloatPrimitive" ):
                listener.exitFloatPrimitive(self)


    class IntPrimitiveContext(SpecialLiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TimesheetQueryParser.SpecialLiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(TimesheetQueryParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntPrimitive" ):
                listener.enterIntPrimitive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntPrimitive" ):
                listener.exitIntPrimitive(self)



    def specialLiteral(self):

        localctx = TimesheetQueryParser.SpecialLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_specialLiteral)
        try:
            self.state = 173
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [56]:
                localctx = TimesheetQueryParser.StringContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 170
                self.descToken()
                pass
            elif token in [60]:
                localctx = TimesheetQueryParser.IntPrimitiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 171
                self.match(TimesheetQueryParser.INT)
                pass
            elif token in [61]:
                localctx = TimesheetQueryParser.FloatPrimitiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 172
                self.match(TimesheetQueryParser.FLOAT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralReplaceFuncContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.old = None # LiteralContext
            self.new = None # LiteralContext

        def literal(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimesheetQueryParser.LiteralContext)
            else:
                return self.getTypedRuleContext(TimesheetQueryParser.LiteralContext,i)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_literalReplaceFunc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteralReplaceFunc" ):
                listener.enterLiteralReplaceFunc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteralReplaceFunc" ):
                listener.exitLiteralReplaceFunc(self)




    def literalReplaceFunc(self):

        localctx = TimesheetQueryParser.LiteralReplaceFuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_literalReplaceFunc)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            localctx.old = self.literal()
            self.state = 176
            self.match(TimesheetQueryParser.T__35)
            self.state = 177
            self.match(TimesheetQueryParser.T__12)
            self.state = 178
            localctx.new = self.literal()
            self.state = 179
            self.match(TimesheetQueryParser.T__13)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EpochSchemeIndexContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.scheme = None # Token
            self.key = None # SeriesContext

        def NAME(self):
            return self.getToken(TimesheetQueryParser.NAME, 0)

        def series(self):
            return self.getTypedRuleContext(TimesheetQueryParser.SeriesContext,0)


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_epochSchemeIndex

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEpochSchemeIndex" ):
                listener.enterEpochSchemeIndex(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEpochSchemeIndex" ):
                listener.exitEpochSchemeIndex(self)




    def epochSchemeIndex(self):

        localctx = TimesheetQueryParser.EpochSchemeIndexContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_epochSchemeIndex)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 181
            self.match(TimesheetQueryParser.T__36)
            self.state = 182
            localctx.scheme = self.match(TimesheetQueryParser.NAME)
            self.state = 187
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==38:
                self.state = 183
                self.match(TimesheetQueryParser.T__37)
                self.state = 184
                localctx.key = self.series()
                self.state = 185
                self.match(TimesheetQueryParser.T__38)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReloadDescContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_reloadDesc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReloadDesc" ):
                listener.enterReloadDesc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReloadDesc" ):
                listener.exitReloadDesc(self)




    def reloadDesc(self):

        localctx = TimesheetQueryParser.ReloadDescContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_reloadDesc)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 189
            self.match(TimesheetQueryParser.T__39)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProjectLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(TimesheetQueryParser.NAME, 0)

        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_projectLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProjectLiteral" ):
                listener.enterProjectLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProjectLiteral" ):
                listener.exitProjectLiteral(self)




    def projectLiteral(self):

        localctx = TimesheetQueryParser.ProjectLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_projectLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 191
            self.match(TimesheetQueryParser.T__40)
            self.state = 192
            self.match(TimesheetQueryParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MetaprojectLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(TimesheetQueryParser.NAME, 0)

        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_metaprojectLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMetaprojectLiteral" ):
                listener.enterMetaprojectLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMetaprojectLiteral" ):
                listener.exitMetaprojectLiteral(self)




    def metaprojectLiteral(self):

        localctx = TimesheetQueryParser.MetaprojectLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_metaprojectLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 30786325577728) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 195
            self.match(TimesheetQueryParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TagLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(TimesheetQueryParser.NAME, 0)

        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_tagLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTagLiteral" ):
                listener.enterTagLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTagLiteral" ):
                listener.exitTagLiteral(self)




    def tagLiteral(self):

        localctx = TimesheetQueryParser.TagLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_tagLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 197
            self.match(TimesheetQueryParser.T__44)
            self.state = 198
            self.match(TimesheetQueryParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EpochLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(TimesheetQueryParser.NAME, 0)

        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_epochLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEpochLiteral" ):
                listener.enterEpochLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEpochLiteral" ):
                listener.exitEpochLiteral(self)




    def epochLiteral(self):

        localctx = TimesheetQueryParser.EpochLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_epochLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            self.match(TimesheetQueryParser.T__45)
            self.state = 201
            self.match(TimesheetQueryParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DescTokenContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_LITERAL(self):
            return self.getToken(TimesheetQueryParser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_descToken

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDescToken" ):
                listener.enterDescToken(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDescToken" ):
                listener.exitDescToken(self)




    def descToken(self):

        localctx = TimesheetQueryParser.DescTokenContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_descToken)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 203
            self.match(TimesheetQueryParser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MoodLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.nameKey = None # Token
            self.intKey = None # Token

        def NAME(self):
            return self.getToken(TimesheetQueryParser.NAME, 0)

        def INT(self):
            return self.getToken(TimesheetQueryParser.INT, 0)

        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_moodLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMoodLiteral" ):
                listener.enterMoodLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMoodLiteral" ):
                listener.exitMoodLiteral(self)




    def moodLiteral(self):

        localctx = TimesheetQueryParser.MoodLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_moodLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 205
            self.match(TimesheetQueryParser.T__46)
            self.state = 208
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [62]:
                self.state = 206
                localctx.nameKey = self.match(TimesheetQueryParser.NAME)
                pass
            elif token in [60]:
                self.state = 207
                localctx.intKey = self.match(TimesheetQueryParser.INT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DatetimeLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.year = None # Token
            self.moreArgs = None # Token

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(TimesheetQueryParser.INT)
            else:
                return self.getToken(TimesheetQueryParser.INT, i)

        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_datetimeLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDatetimeLiteral" ):
                listener.enterDatetimeLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDatetimeLiteral" ):
                listener.exitDatetimeLiteral(self)




    def datetimeLiteral(self):

        localctx = TimesheetQueryParser.DatetimeLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_datetimeLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 210
            self.match(TimesheetQueryParser.T__47)
            self.state = 211
            localctx.year = self.match(TimesheetQueryParser.INT)
            self.state = 216
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==49:
                self.state = 212
                self.match(TimesheetQueryParser.T__48)
                self.state = 213
                localctx.moreArgs = self.match(TimesheetQueryParser.INT)
                self.state = 218
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 219
            self.match(TimesheetQueryParser.T__13)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TimedeltaLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.weeks = None # Token
            self.days = None # Token
            self.hours = None # Token
            self.minutes = None # Token

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(TimesheetQueryParser.INT)
            else:
                return self.getToken(TimesheetQueryParser.INT, i)

        def getRuleIndex(self):
            return TimesheetQueryParser.RULE_timedeltaLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimedeltaLiteral" ):
                listener.enterTimedeltaLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimedeltaLiteral" ):
                listener.exitTimedeltaLiteral(self)




    def timedeltaLiteral(self):

        localctx = TimesheetQueryParser.TimedeltaLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_timedeltaLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 221
            self.match(TimesheetQueryParser.T__49)
            self.state = 230
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [51]:
                self.state = 222
                self.match(TimesheetQueryParser.T__50)
                self.state = 223
                localctx.weeks = self.match(TimesheetQueryParser.INT)
                pass
            elif token in [52]:
                self.state = 224
                self.match(TimesheetQueryParser.T__51)
                self.state = 225
                localctx.days = self.match(TimesheetQueryParser.INT)
                pass
            elif token in [53]:
                self.state = 226
                self.match(TimesheetQueryParser.T__52)
                self.state = 227
                localctx.hours = self.match(TimesheetQueryParser.INT)
                pass
            elif token in [54]:
                self.state = 228
                self.match(TimesheetQueryParser.T__53)
                self.state = 229
                localctx.minutes = self.match(TimesheetQueryParser.INT)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 235
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.state = 232
                self.match(TimesheetQueryParser.T__48)
                self.state = 233
                self.match(TimesheetQueryParser.T__50)
                self.state = 234
                localctx.weeks = self.match(TimesheetQueryParser.INT)


            self.state = 240
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.state = 237
                self.match(TimesheetQueryParser.T__48)
                self.state = 238
                self.match(TimesheetQueryParser.T__51)
                self.state = 239
                localctx.days = self.match(TimesheetQueryParser.INT)


            self.state = 245
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
            if la_ == 1:
                self.state = 242
                self.match(TimesheetQueryParser.T__48)
                self.state = 243
                self.match(TimesheetQueryParser.T__52)
                self.state = 244
                localctx.hours = self.match(TimesheetQueryParser.INT)


            self.state = 250
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.state = 247
                self.match(TimesheetQueryParser.T__48)
                self.state = 248
                self.match(TimesheetQueryParser.T__53)
                self.state = 249
                localctx.minutes = self.match(TimesheetQueryParser.INT)


            self.state = 253
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==49:
                self.state = 252
                self.match(TimesheetQueryParser.T__48)


            self.state = 255
            self.match(TimesheetQueryParser.T__13)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





