# Generated from TimesheetQuery.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .TimesheetQueryParser import TimesheetQueryParser
else:
    from TimesheetQueryParser import TimesheetQueryParser

# This class defines a complete listener for a parse tree produced by TimesheetQueryParser.
class TimesheetQueryListener(ParseTreeListener):

    # Enter a parse tree produced by TimesheetQueryParser#ruleList.
    def enterRuleList(self, ctx:TimesheetQueryParser.RuleListContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#ruleList.
    def exitRuleList(self, ctx:TimesheetQueryParser.RuleListContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#rule.
    def enterRule(self, ctx:TimesheetQueryParser.RuleContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#rule.
    def exitRule(self, ctx:TimesheetQueryParser.RuleContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#query.
    def enterQuery(self, ctx:TimesheetQueryParser.QueryContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#query.
    def exitQuery(self, ctx:TimesheetQueryParser.QueryContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#setLiteral.
    def enterSetLiteral(self, ctx:TimesheetQueryParser.SetLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#setLiteral.
    def exitSetLiteral(self, ctx:TimesheetQueryParser.SetLiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#deleteLiteral.
    def enterDeleteLiteral(self, ctx:TimesheetQueryParser.DeleteLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#deleteLiteral.
    def exitDeleteLiteral(self, ctx:TimesheetQueryParser.DeleteLiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#cmdFunc.
    def enterCmdFunc(self, ctx:TimesheetQueryParser.CmdFuncContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#cmdFunc.
    def exitCmdFunc(self, ctx:TimesheetQueryParser.CmdFuncContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#boolMonadicPrefixOp.
    def enterBoolMonadicPrefixOp(self, ctx:TimesheetQueryParser.BoolMonadicPrefixOpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#boolMonadicPrefixOp.
    def exitBoolMonadicPrefixOp(self, ctx:TimesheetQueryParser.BoolMonadicPrefixOpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#boolDyadicInfixOp.
    def enterBoolDyadicInfixOp(self, ctx:TimesheetQueryParser.BoolDyadicInfixOpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#boolDyadicInfixOp.
    def exitBoolDyadicInfixOp(self, ctx:TimesheetQueryParser.BoolDyadicInfixOpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#comparisonInfixOp.
    def enterComparisonInfixOp(self, ctx:TimesheetQueryParser.ComparisonInfixOpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#comparisonInfixOp.
    def exitComparisonInfixOp(self, ctx:TimesheetQueryParser.ComparisonInfixOpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#boolExp.
    def enterBoolExp(self, ctx:TimesheetQueryParser.BoolExpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#boolExp.
    def exitBoolExp(self, ctx:TimesheetQueryParser.BoolExpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#boolDyadicExp.
    def enterBoolDyadicExp(self, ctx:TimesheetQueryParser.BoolDyadicExpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#boolDyadicExp.
    def exitBoolDyadicExp(self, ctx:TimesheetQueryParser.BoolDyadicExpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#comparisonExp.
    def enterComparisonExp(self, ctx:TimesheetQueryParser.ComparisonExpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#comparisonExp.
    def exitComparisonExp(self, ctx:TimesheetQueryParser.ComparisonExpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#singleInstanceImpliedExp.
    def enterSingleInstanceImpliedExp(self, ctx:TimesheetQueryParser.SingleInstanceImpliedExpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#singleInstanceImpliedExp.
    def exitSingleInstanceImpliedExp(self, ctx:TimesheetQueryParser.SingleInstanceImpliedExpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#listElementImpliedExp.
    def enterListElementImpliedExp(self, ctx:TimesheetQueryParser.ListElementImpliedExpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#listElementImpliedExp.
    def exitListElementImpliedExp(self, ctx:TimesheetQueryParser.ListElementImpliedExpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#specialLiteralImpliedExp.
    def enterSpecialLiteralImpliedExp(self, ctx:TimesheetQueryParser.SpecialLiteralImpliedExpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#specialLiteralImpliedExp.
    def exitSpecialLiteralImpliedExp(self, ctx:TimesheetQueryParser.SpecialLiteralImpliedExpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#fieldImpliedExp.
    def enterFieldImpliedExp(self, ctx:TimesheetQueryParser.FieldImpliedExpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#fieldImpliedExp.
    def exitFieldImpliedExp(self, ctx:TimesheetQueryParser.FieldImpliedExpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#atomMonadicExp.
    def enterAtomMonadicExp(self, ctx:TimesheetQueryParser.AtomMonadicExpContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#atomMonadicExp.
    def exitAtomMonadicExp(self, ctx:TimesheetQueryParser.AtomMonadicExpContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#series.
    def enterSeries(self, ctx:TimesheetQueryParser.SeriesContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#series.
    def exitSeries(self, ctx:TimesheetQueryParser.SeriesContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#seriesFunc.
    def enterSeriesFunc(self, ctx:TimesheetQueryParser.SeriesFuncContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#seriesFunc.
    def exitSeriesFunc(self, ctx:TimesheetQueryParser.SeriesFuncContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#commandFunc.
    def enterCommandFunc(self, ctx:TimesheetQueryParser.CommandFuncContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#commandFunc.
    def exitCommandFunc(self, ctx:TimesheetQueryParser.CommandFuncContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#field.
    def enterField(self, ctx:TimesheetQueryParser.FieldContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#field.
    def exitField(self, ctx:TimesheetQueryParser.FieldContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#literal.
    def enterLiteral(self, ctx:TimesheetQueryParser.LiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#literal.
    def exitLiteral(self, ctx:TimesheetQueryParser.LiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#singleInstLiteral.
    def enterSingleInstLiteral(self, ctx:TimesheetQueryParser.SingleInstLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#singleInstLiteral.
    def exitSingleInstLiteral(self, ctx:TimesheetQueryParser.SingleInstLiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#listElementLiteral.
    def enterListElementLiteral(self, ctx:TimesheetQueryParser.ListElementLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#listElementLiteral.
    def exitListElementLiteral(self, ctx:TimesheetQueryParser.ListElementLiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#string.
    def enterString(self, ctx:TimesheetQueryParser.StringContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#string.
    def exitString(self, ctx:TimesheetQueryParser.StringContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#intPrimitive.
    def enterIntPrimitive(self, ctx:TimesheetQueryParser.IntPrimitiveContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#intPrimitive.
    def exitIntPrimitive(self, ctx:TimesheetQueryParser.IntPrimitiveContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#floatPrimitive.
    def enterFloatPrimitive(self, ctx:TimesheetQueryParser.FloatPrimitiveContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#floatPrimitive.
    def exitFloatPrimitive(self, ctx:TimesheetQueryParser.FloatPrimitiveContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#literalReplaceFunc.
    def enterLiteralReplaceFunc(self, ctx:TimesheetQueryParser.LiteralReplaceFuncContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#literalReplaceFunc.
    def exitLiteralReplaceFunc(self, ctx:TimesheetQueryParser.LiteralReplaceFuncContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#epochSchemeIndex.
    def enterEpochSchemeIndex(self, ctx:TimesheetQueryParser.EpochSchemeIndexContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#epochSchemeIndex.
    def exitEpochSchemeIndex(self, ctx:TimesheetQueryParser.EpochSchemeIndexContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#reloadDesc.
    def enterReloadDesc(self, ctx:TimesheetQueryParser.ReloadDescContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#reloadDesc.
    def exitReloadDesc(self, ctx:TimesheetQueryParser.ReloadDescContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#projectLiteral.
    def enterProjectLiteral(self, ctx:TimesheetQueryParser.ProjectLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#projectLiteral.
    def exitProjectLiteral(self, ctx:TimesheetQueryParser.ProjectLiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#metaprojectLiteral.
    def enterMetaprojectLiteral(self, ctx:TimesheetQueryParser.MetaprojectLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#metaprojectLiteral.
    def exitMetaprojectLiteral(self, ctx:TimesheetQueryParser.MetaprojectLiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#tagLiteral.
    def enterTagLiteral(self, ctx:TimesheetQueryParser.TagLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#tagLiteral.
    def exitTagLiteral(self, ctx:TimesheetQueryParser.TagLiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#epochLiteral.
    def enterEpochLiteral(self, ctx:TimesheetQueryParser.EpochLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#epochLiteral.
    def exitEpochLiteral(self, ctx:TimesheetQueryParser.EpochLiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#descToken.
    def enterDescToken(self, ctx:TimesheetQueryParser.DescTokenContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#descToken.
    def exitDescToken(self, ctx:TimesheetQueryParser.DescTokenContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#moodLiteral.
    def enterMoodLiteral(self, ctx:TimesheetQueryParser.MoodLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#moodLiteral.
    def exitMoodLiteral(self, ctx:TimesheetQueryParser.MoodLiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#datetimeLiteral.
    def enterDatetimeLiteral(self, ctx:TimesheetQueryParser.DatetimeLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#datetimeLiteral.
    def exitDatetimeLiteral(self, ctx:TimesheetQueryParser.DatetimeLiteralContext):
        pass


    # Enter a parse tree produced by TimesheetQueryParser#timedeltaLiteral.
    def enterTimedeltaLiteral(self, ctx:TimesheetQueryParser.TimedeltaLiteralContext):
        pass

    # Exit a parse tree produced by TimesheetQueryParser#timedeltaLiteral.
    def exitTimedeltaLiteral(self, ctx:TimesheetQueryParser.TimedeltaLiteralContext):
        pass



del TimesheetQueryParser