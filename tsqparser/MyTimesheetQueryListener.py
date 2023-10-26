"""
TimesheetQueryListener inheriting class. Overrides select class methods.
"""

import sys

import pandas as pd
from antlr4 import tree
from copy import copy, deepcopy
import kiwilib
import datetime

import src.Collectibles
from src.TimesheetDF import TimesheetDataFrame
from tsqparser.TimesheetQueryParser import TimesheetQueryParser
from tsqparser.TimesheetQueryListener import TimesheetQueryListener
from src.TimesheetDataset import TimesheetDataset
import src.TimesheetGlobals as Global
from src.Description import Description


# from src.TimesheetDF import TimesheetDataFrame


class MyTimesheetQueryListener(TimesheetQueryListener):
    """
    Implements query and command actions as the antlr4 walker walks over the parse tree.
    query branch:
    Writes ctx.data and ctx.dtype properties to the ctx objects on exit.
    The ctx.dtype in child nodes are read by parent nodes in conditionals and assertions to set the parent's procedures
    ctx.dtype defines how ctx.data should be interpreted by the parent.

    ctx.dtype definitions:
    'S': series, represented as a pandas.Series object. Could hold any arbitrary data
    'L': literal, represented as a string, custom Enum subclass, other data types to be added
    'B': pd.Series boolean mask
    'DF': pd.DataFrame. Used in the query node
    'D': For commands: deletion of the literal contained in the data
    """

    def __init__(self, tsds):
        if tsds.__class__ == TimesheetDataFrame:
            self.tsds = TimesheetDataset(tsds.df)
            self.returnClass = TimesheetDataFrame
        else:
            self.tsds = tsds
            self.returnClass = TimesheetDataset

    @staticmethod
    def collapseNonBranchingNode(ctx):
        nonTerminalChildren = [ch for ch in ctx.children if not isinstance(ch, tree.Tree.TerminalNodeImpl)]
        if len(nonTerminalChildren) == 1:
            siblings = ctx.parentCtx.children
            for i, sibling in enumerate(siblings):
                if sibling is ctx:
                    ctx.parentCtx.children[i] = nonTerminalChildren[0]
                    break
            del ctx
            return True
        else:
            # print(f'Warning: tried to collapse {ctx} when it had >1 child node: {ctx.children}')
            return False
        # return

    @staticmethod
    def trimTerminalChildren(ctx):
        ctx.children = [ch for ch in ctx.children if ch.__class__ != tree.Tree.TerminalNodeImpl]

    def getCurrentRuleTSDS(self, ctx):
        if isinstance(ctx, TimesheetQueryParser.RuleContext):
            return ctx.data
        else:
            return self.getCurrentRuleTSDS(ctx.parentCtx)

    # Enter a parse tree produced by TimesheetQueryParser#ruleList.
    def enterRuleList(self, ctx: TimesheetQueryParser.RuleListContext):
        ctx.data = self.tsds

    # Enter a parse tree produced by TimesheetQueryParser#rule.
    def enterRule(self, ctx: TimesheetQueryParser.RuleContext):
        ctx.data = copy(ctx.parentCtx.data)

    # Exit a parse tree produced by TimesheetQueryParser#rule.
    def exitRule(self, ctx: TimesheetQueryParser.RuleContext):
        # if ctx.children[0].__class__ == TimesheetQueryParser.QueryContext:
        # queryMask = ctx.children[0].data
        if len(ctx.children) > 3:  # If there are >=1 commands and >0 rows of data
            ctx.parentCtx.data.outerUpdate(ctx.data)  # Write updated tsds to ruleList ctx
        # elif len(ctx.data.timesheetdf) > 0:
        #     pass
        else:  # If no command in this rule, push the filtered df up to ruleList
            ctx.parentCtx.data = ctx.data
        del ctx.data

    """
    Command branch
    """

    # Enter a parse tree produced by TimesheetQueryParser#setLiteral.
    def enterSetLiteral(self, ctx: TimesheetQueryParser.SetLiteralContext):
        ctx.data = ctx.parentCtx.data

    # Enter a parse tree produced by TimesheetQueryParser#deleteLiteral.
    def enterDeleteLiteral(self, ctx: TimesheetQueryParser.DeleteLiteralContext):
        ctx.data = ctx.parentCtx.data

    # Enter a parse tree produced by TimesheetQueryParser#cmdFunc.
    def enterCmdFunc(self, ctx:TimesheetQueryParser.CmdFuncContext):
        ctx.data = ctx.parentCtx.data
    
    # Exit a parse tree produced by TimesheetQueryParser#setLiteral.
    def exitSetLiteral(self, ctx: TimesheetQueryParser.SetLiteralContext):
        """
        Applies changes to the current context TsDS depending on the type of the literal child.
        All modifications are preceded by a check to ensure that duplicate data isn't being appended.
        This check is either in this procedure itself or in the procedures called by it.
        Global.Tag: appends tag literal to the list
        Child classes of Global.SingleInstanceColumn: replaces the existing data with an instance of literal
        Description token: Appends the token to the end of the description
        :param ctx: antlr-generated parse tree node context object
        """
        assert len(ctx.children) == 1, f'Query must have exactly 1 child, not {len(ctx.children)}.'
        assert hasattr(ctx.children[0], 'dtype'), f'dtype of arg to a command must be defined'
        assert ctx.children[0].dtype == 'L', f'dtype of literal must be "L"'
        mytsdf = ctx.data.timesheetdf
        literal = ctx.children[0].data
        # litClass =
        if isinstance(literal, Global.ColumnEnum):
            # (Global.Epoch, Global.Tag, Global.Project, Global.Epoch, Global.Metaproject, Global.Mood)
            dfcolumn = literal.__class__.dfcolumn()
            if isinstance(literal, Global.SingleInstanceColumn):
                mytsdf.df.loc[:, dfcolumn] = literal
            elif isinstance(literal, Global.ListColumn):
                # rowsToAppend = ~mytsdf.isinListColumn(literal, dfcolumn)
                mytsdf.appendToListColumn(literal, dfcolumn)
        elif ctx.children[0].__class__ == TimesheetQueryParser.DescTokenContext:
            literal = literal.upper()
            noTokenYetBoolMask = mytsdf.df.description.apply(lambda row: not row.hasToken(literal))
            mytsdf.df.loc[noTokenYetBoolMask, 'description'].map(lambda row: row.addToken(literal))
        else:
            raise NotImplementedError(f'setLiteral() for type {ctx.children[0].__class__} not yet implemented.')

    # Exit a parse tree produced by TimesheetQueryParser#deleteLiteral.
    def exitDeleteLiteral(self, ctx: TimesheetQueryParser.DeleteLiteralContext):
        """
        Applies changes to the current context TsDS depending on the type of the literal child.
        Global.Tag: deletes tag literal from the list
        Child classes of Global.SingleInstanceColumn: replaces the existing data with an instance of literal
        Description token: Appends the token to the end of the description
        :param ctx: antlr-generated parse tree node context object
        """
        assert len(ctx.children) == 2, f'Query must have exactly 1 child, not {len(ctx.children)}.'
        assert hasattr(ctx.children[1], 'dtype'), f'dtype of arg to a command must be defined'
        assert ctx.children[1].dtype == 'L', f'dtype of literal must be "L"'
        mytsdf = ctx.data.timesheetdf
        literal = ctx.children[1].data
        if literal.__class__ in (Global.Epoch, Global.Project, Description):
            raise TypeError(f'del({literal}): This TimesheetDataFrame field cannot be deleted, only replaced')
        if isinstance(literal, Global.ColumnEnum):
            dfcolumn = literal.__class__.dfcolumn()
            if isinstance(literal, Global.SingleInstanceColumn):
                mytsdf.df.loc[:, dfcolumn] = pd.NA  # Ok, as long as exception is raised for the types above
            elif isinstance(literal, Global.ListColumn):
                mytsdf.deleteFromListColumn(literal, dfcolumn)
                pass
        elif isinstance(literal, str):  # descToken
            mytsdf.df.description.apply(lambda x: x.removeToken(literal))

    # Exit a parse tree produced by TimesheetQueryParser#cmdFunc.
    def exitCmdFunc(self, ctx:TimesheetQueryParser.CmdFuncContext):
        if self.collapseNonBranchingNode(ctx):
            del ctx
        return

    # Enter a parse tree produced by TimesheetQueryParser#commandFunc.
    def enterCommandFunc(self, ctx:TimesheetQueryParser.CommandFuncContext):
        ctx.data = ctx.parentCtx.data

    # Exit a parse tree produced by TimesheetQueryParser#commandFunc.
    def exitCommandFunc(self, ctx:TimesheetQueryParser.CommandFuncContext):
        if self.collapseNonBranchingNode(ctx):
            del ctx
        return

    # Enter a parse tree produced by TimesheetQueryParser#literalReplaceFunc.
    def enterLiteralReplaceFunc(self, ctx:TimesheetQueryParser.LiteralReplaceFuncContext):
        ctx.data = ctx.parentCtx.data

    # Exit a parse tree produced by TimesheetQueryParser#literalReplaceFunc.
    def exitLiteralReplaceFunc(self, ctx:TimesheetQueryParser.LiteralReplaceFuncContext):
        assert ctx.old is not None, f'old literal must be defined'
        assert ctx.new is not None, f'new literal must be defined'
        df = ctx.data.timesheetdf.df
        old = ctx.old.children[0].data
        new = ctx.new.children[0].data
        if isinstance(old, str) and isinstance(new, str):
            replaceRows = df.loc[df.description.apply(lambda row: row.hasToken(old)), :]
            replaceRows.description.apply(lambda d: d.replaceToken(old, new))
        else:
            raise NotImplementedError('Only strings currently supported.')

    # Enter a parse tree produced by TimesheetQueryParser#reloadDesc.
    def enterReloadDesc(self, ctx:TimesheetQueryParser.ReloadDescContext):
        ctx.data = ctx.parentCtx.data

    # Exit a parse tree produced by TimesheetQueryParser#reloadDesc.
    def exitReloadDesc(self, ctx:TimesheetQueryParser.ReloadDescContext):
        df = ctx.data.timesheetdf.df
        df.description.apply(lambda x: x.initExceptRaw(x.standardString))

    """
    Query branch
    """

    # Exit a parse tree produced by TimesheetQueryParser#query.
    def exitQuery(self, ctx: TimesheetQueryParser.QueryContext):
        assert len(ctx.children) == 1, f'Query must have exactly 1 child, not {len(ctx.children)}.'
        # assert(self.collapseNonBranchingNode(ctx), f'Query must have exactly 1 child, not {len(ctx.children)}.')
        assert ctx.children[0].dtype == 'B', f'Query takes args of dtype "B", not "{ctx.children[0].dtype}".'
        ctx.data = self.getCurrentRuleTSDS(ctx).timesheetdf.df[ctx.children[0].data]
        # ctx.data = self.tsds.timesheetdf.df[ctx.children[0].data]
        ctx.parentCtx.data.timesheetdf = ctx.data.tsdf
        # ctx.dtype = 'DF'
        # del(ctx)
        # self.tsds.timesheetdf = self.tsds.timesheetdf[ctx.children[0].data]
        return

    # Exit a parse tree produced by TimesheetQueryParser#boolExp.
    def exitBoolExp(self, ctx: TimesheetQueryParser.BoolExpContext):
        if self.collapseNonBranchingNode(ctx):
            del ctx
        return

    # Exit a parse tree produced by TimesheetQueryParser#boolDyadicExp.
    def exitBoolDyadicExp(self, ctx: TimesheetQueryParser.BoolDyadicExpContext):
        if self.collapseNonBranchingNode(ctx):
            del ctx
            return
        assert len(ctx.children) == 3, f'ComparisonExp has exactly 3 elements, not {len(ctx.children)}'
        assert hasattr(ctx.children[0], 'dtype') and ctx.children[0].dtype == 'B', f'Child 0 dtype must be "B".'
        assert hasattr(ctx.children[2], 'dtype') and ctx.children[2].dtype == 'B', f'Child 2 dtype must be "B".'
        data1 = ctx.children[0].data
        data2 = ctx.children[2].data
        boolOp = ctx.children[1].start.text
        ctx.dtype = 'B'
        ctx.data = {
            '|': data1 | data2,
            '&': data1 & data2,
        }[boolOp]
        return

    # Exit a parse tree produced by TimesheetQueryParser#comparisonExp.
    def exitComparisonExp(self, ctx: TimesheetQueryParser.ComparisonExpContext):
        def swapOperator(opString):
            return {
                '>=': '<=',
                '<=': '>=',
                '>': '<',
                '<': '>',
                '!=': '!=',
                '==': '==',
            }[opString]

        if self.collapseNonBranchingNode(ctx):
            del ctx
            return
        assert len(ctx.children) == 3, f'ComparisonExp has exactly 3 elements, not {len(ctx.children)}'
        literalData = [child.data for child in [ctx.children[0], ctx.children[2]] if child.dtype == 'L']
        assert len(literalData) == 1, f'ComparisonExp requires 1 literal dtype. {len(literalData)} found instead.'
        seriesData = [child.data for child in [ctx.children[0], ctx.children[2]] if child.dtype == 'S']
        assert len(seriesData) == 1, f'ComparisonExp requires 1 series dtype. {len(seriesData)} found instead.'

        infixOp = ctx.children[1].start.text  # default, if dtype = 'S', don't need to do any swaps
        if ctx.children[0].dtype == 'L':
            infixOp = swapOperator(ctx.children[1].start.text)
        elif ctx.children[0].dtype != 'S':
            raise TypeError('Error in ComparisonExp dtypes')
        ser = seriesData[0]

        if infixOp == 'in':
            raise NotImplementedError('"in" operations not yet supported in comparison expressions')
            # if len(literalData[0]) != 2 or literalData[0][0].__class__ != Global.EpochScheme:
            #     raise TypeError('"in" currently only supported for Global.EpochScheme dtypes')
            # ctx.data = literalData[0][0].isInGroup(ser, literalData[0][1])
        elif len(ser) == 0:
            ctx.data = ser.astype(bool)
        else:
            ctx.data = {
                '>=': ser >= literalData[0],
                '<=': ser <= literalData[0],
                '>':  ser >  literalData[0],
                '<':  ser <  literalData[0],
                '!=': ser != literalData[0],
                '==': ser == literalData[0],
            }[infixOp]
        ctx.dtype = 'B'
        return

    # Exit a parse tree produced by TimesheetQueryParser#singleInstanceImpliedExp.
    def exitSingleInstanceImpliedExp(self, ctx: TimesheetQueryParser.SingleInstanceImpliedExpContext):
        literalData = ctx.children[0].data
        if not isinstance(literalData, Global.SingleInstanceColumn):
            raise TypeError(f'The only single instance literals supported are subclasses of SingleInstanceColumn,'
                            f' not {literalData.__class__}.')
        ctx.data = self.getCurrentRuleTSDS(ctx).timesheetdf.df[literalData.__class__.dfcolumn()] == literalData
        ctx.dtype = 'B'

    # Exit a parse tree produced by TimesheetQueryParser#listElementImpliedExp.
    def exitListElementImpliedExp(self, ctx: TimesheetQueryParser.ListElementImpliedExpContext):
        literalData = ctx.children[0].data
        if not isinstance(literalData, Global.ListColumn):
            raise TypeError(f'The only list element literals supported are subclasses of ListColumn,'
                            f' not {literalData.__class__}.')
        ctx.data = self.getCurrentRuleTSDS(ctx).timesheetdf.df[literalData.__class__.dfcolumn()].apply(kiwilib.isin,
                                                                                                       val=literalData)
        ctx.dtype = 'B'

    # Exit a parse tree produced by TimesheetQueryParser#specialLiteralImpliedExp.
    def exitSpecialLiteralImpliedExp(self, ctx: TimesheetQueryParser.SpecialLiteralImpliedExpContext):
        literal = ctx.children[0].data
        df = self.getCurrentRuleTSDS(ctx).timesheetdf.df
        if isinstance(literal, str): # descToken
            literal = literal.upper()
            ctx.data =  df.description.apply(lambda row: row.hasToken(literal))
        elif len(literal) == 2 and isinstance(literal[0], Global.EpochScheme): # epochGroup
            ctx.data = df.start.apply(lambda row: literal[0].isInGroup(row, literal[1]))
        else:
            raise NotImplementedError(f'Implied exp\'s for special literals of type {literal.class__} not supported')
        ctx.dtype = 'B'

    # Exit a parse tree produced by TimesheetQueryParser#fieldImpliedExp.
    def exitFieldImpliedExp(self, ctx:TimesheetQueryParser.FieldImpliedExpContext):
        # mytsdf = self.getCurrentRuleTSDS(ctx).timesheetdf
        ctx.data = ~ctx.children[0].data.to_frame().tsdf.isEmpty()
        ctx.dtype = 'B'


    # Exit a parse tree produced by TimesheetQueryParser#atomMonadicExp.
    def exitAtomMonadicExp(self, ctx: TimesheetQueryParser.AtomMonadicExpContext):
        if self.collapseNonBranchingNode(ctx):  # If no actual monadic expression
            del ctx
            return
        # Else if there is a monadic expression to be executed
        nonTerminalChildren = [ch for ch in ctx.children if ch.__class__ != tree.Tree.TerminalNodeImpl]
        boolData = [child.data for child in nonTerminalChildren if hasattr(child, 'dtype') and child.dtype == 'B']
        assert len(boolData) == 1, f'Monadic expression takes exactly 1 bool type input, not {len(boolData)}'
        monadicOp = nonTerminalChildren[0].start.text
        assert monadicOp == '!', f'Monadic operators supported: "!". {monadicOp} not supported'
        ctx.dtype = 'B'
        ctx.data = ~boolData[0]  # Invert boolean mask
        return

    # Exit a parse tree produced by TimesheetQueryParser#atom.
    # def exitAtom(self, ctx:TimesheetQueryParser.AtomContext):
    #     if self.collapseNonBranchingNode(ctx):
    #         del(ctx)
    #     return

    # Exit a parse tree produced by TimesheetQueryParser#series.
    def exitSeries(self, ctx:TimesheetQueryParser.SeriesContext):
        """Don't delete because this context has a rule element label in the grammar"""
        assert len(ctx.children) < 2, 'Series has >1 children'
        # if self.collapseNonBranchingNode(ctx):
        #     del ctx
        # return
        ctx.dtype = 'S'
        ctx.data = ctx.children[0].data

    # Exit a parse tree produced by TimesheetQueryParser#seriesFunc.
    def exitSeriesFunc(self, ctx:TimesheetQueryParser.SeriesFuncContext):
        if self.collapseNonBranchingNode(ctx):
            del ctx
        return

    # Exit a parse tree produced by TimesheetQueryParser#epochSchemeIndex.
    def exitEpochSchemeIndex(self, ctx:TimesheetQueryParser.EpochSchemeIndexContext):
        ctx.es = Global.EpochScheme[ctx.scheme.text.upper()]
        if not hasattr(ctx, 'key') or not ctx.key:
            keyData = self.getCurrentRuleTSDS(ctx).timesheetdf.df['start'].squeeze()
            ctx.data = keyData.apply(lambda x: ctx.es.id(x))
        else:
            ctx.data = ctx.key.data.apply(lambda x: ctx.es.id(x))
        ctx.dtype = 'S'

    # Exit a parse tree produced by TimesheetQueryParser#literal.
    def exitLiteral(self, ctx: TimesheetQueryParser.LiteralContext):
        if self.collapseNonBranchingNode(ctx):
            del ctx
        return

    # Exit a parse tree produced by TimesheetQueryParser#singleInstLiteral.
    def exitSingleInstLiteral(self, ctx:TimesheetQueryParser.SingleInstLiteralContext):
        ctx.dtype = 'L'
        if self.collapseNonBranchingNode(ctx):
            del ctx
        return

    # Exit a parse tree produced by TimesheetQueryParser#listElementLiteral.
    def exitListElementLiteral(self, ctx:TimesheetQueryParser.ListElementLiteralContext):
        ctx.dtype = 'L'
        if self.collapseNonBranchingNode(ctx):
            del ctx
        return

    # Exit a parse tree produced by TimesheetQueryParser#string.
    def exitString(self, ctx:TimesheetQueryParser.StringContext):
        ctx.dtype = 'L'
        if self.collapseNonBranchingNode(ctx):
            del ctx
        return

    # Exit a parse tree produced by TimesheetQueryParser#intPrimitive.
    def exitIntPrimitive(self, ctx:TimesheetQueryParser.IntPrimitiveContext):
        ctx.dtype = 'L'
        ctx.data = int(ctx.start.text)

    # Exit a parse tree produced by TimesheetQueryParser#floatPrimitive.
    def exitFloatPrimitive(self, ctx:TimesheetQueryParser.FloatPrimitiveContext):
        ctx.dtype = 'L'
        ctx.data = float(ctx.start.text)

    # Exit a parse tree produced by TimesheetQueryParser#field.
    def exitField(self, ctx: TimesheetQueryParser.FieldContext):
        ctx.dtype = 'S'
        col = ctx.children[0].symbol.text
        if col in [leaf.__name__ for leaf in kiwilib.leafClasses(src.Collectibles.Media)]:  # From media column
            ctx.data = self.getCurrentRuleTSDS(ctx).timesheetdf.filterMedia(col.lower()).df.media.squeeze()
        else:
            ctx.data = self.getCurrentRuleTSDS(ctx).timesheetdf.df[col.lower()].squeeze()
        return

    # Exit a parse tree produced by TimesheetQueryParser#projectLiteral.
    def exitProjectLiteral(self, ctx: TimesheetQueryParser.ProjectLiteralContext):
        ctx.dtype = 'L'
        ctx.data = Global.Project[ctx.stop.text.upper()]

    # Exit a parse tree produced by TimesheetQueryParser#metaprojectLiteral.
    def exitMetaprojectLiteral(self, ctx:TimesheetQueryParser.MetaprojectLiteralContext):
        ctx.dtype = 'L'
        ctx.data = Global.Metaproject[ctx.stop.text]

    # Exit a parse tree produced by TimesheetQueryParser#epochLiteral.
    def exitEpochLiteral(self, ctx: TimesheetQueryParser.EpochLiteralContext):
        ctx.dtype = 'L'
        ctx.data = Global.Epoch[ctx.stop.text]

    # Exit a parse tree produced by TimesheetQueryParser#tagLiteral.
    def exitTagLiteral(self, ctx: TimesheetQueryParser.TagLiteralContext):
        ctx.dtype = 'L'
        ctx.data = Global.Tag[ctx.stop.text.upper()]

    # Exit a parse tree produced by TimesheetQueryParser#descToken.
    def exitDescToken(self, ctx: TimesheetQueryParser.DescTokenContext):
        ctx.dtype = 'L'
        ctx.data = ctx.stop.text[1:-1].upper()

    # Exit a parse tree produced by TimesheetQueryParser#datetimeLiteral.
    def exitDatetimeLiteral(self, ctx:TimesheetQueryParser.DatetimeLiteralContext):
        ctx.dtype = 'L'
        # self.trimTerminalChildren(ctx)
        argList = [int(ch.symbol.text) for ch in ctx.children[1::2]]
        ctx.data = datetime.datetime(*argList)

    # Exit a parse tree produced by TimesheetQueryParser#timedeltaLiteral.
    def exitTimedeltaLiteral(self, ctx:TimesheetQueryParser.TimedeltaLiteralContext):
        ctx.dtype = 'L'
        # self.trimTerminalChildren(ctx)
        # argList = [int(ch.symbol.text) for ch in ctx.children[1::2]]
        if not ctx.weeks: ctx.weeks = 0
        else: ctx.weeks = int(ctx.weeks.text)
        if not ctx.days: ctx.days = 0
        else: ctx.days = int(ctx.days.text)
        if not ctx.hours: ctx.hours = 0
        else: ctx.hours = int(ctx.hours.text)
        if not ctx.minutes: ctx.minutes = 0
        else: ctx.minutes = int(ctx.minutes.text)
        ctx.data = datetime.timedelta(weeks=ctx.weeks, days=ctx.days, hours=ctx.hours, minutes=ctx.minutes)

    # Exit a parse tree produced by TimesheetQueryParser#moodLiteral.
    def exitMoodLiteral(self, ctx:TimesheetQueryParser.MoodLiteralContext):
        ctx.dtype = 'L'
        if ctx.intKey:
            ctx.data = Global.Mood.idMap()[int(ctx.intKey.text)]
            # ctx.data = dict((a.value, a) for a in Global.Mood.__members__.values())[int(ctx.intKey.text)]
        elif ctx.nameKey:
            ctx.data = Global.Mood[ctx.nameKey.text]
        else:
            raise AttributeError('Key not parsed from Mood literal')

# todo: add support for fields: circad, mood, id
