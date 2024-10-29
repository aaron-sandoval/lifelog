// Generated from tsqparser/TimesheetQuery.g4 by ANTLR 4.13.2
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link TimesheetQueryParser}.
 */
public interface TimesheetQueryListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#ruleList}.
	 * @param ctx the parse tree
	 */
	void enterRuleList(TimesheetQueryParser.RuleListContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#ruleList}.
	 * @param ctx the parse tree
	 */
	void exitRuleList(TimesheetQueryParser.RuleListContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#rule}.
	 * @param ctx the parse tree
	 */
	void enterRule(TimesheetQueryParser.RuleContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#rule}.
	 * @param ctx the parse tree
	 */
	void exitRule(TimesheetQueryParser.RuleContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#query}.
	 * @param ctx the parse tree
	 */
	void enterQuery(TimesheetQueryParser.QueryContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#query}.
	 * @param ctx the parse tree
	 */
	void exitQuery(TimesheetQueryParser.QueryContext ctx);
	/**
	 * Enter a parse tree produced by the {@code setLiteral}
	 * labeled alternative in {@link TimesheetQueryParser#command}.
	 * @param ctx the parse tree
	 */
	void enterSetLiteral(TimesheetQueryParser.SetLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code setLiteral}
	 * labeled alternative in {@link TimesheetQueryParser#command}.
	 * @param ctx the parse tree
	 */
	void exitSetLiteral(TimesheetQueryParser.SetLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code deleteLiteral}
	 * labeled alternative in {@link TimesheetQueryParser#command}.
	 * @param ctx the parse tree
	 */
	void enterDeleteLiteral(TimesheetQueryParser.DeleteLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code deleteLiteral}
	 * labeled alternative in {@link TimesheetQueryParser#command}.
	 * @param ctx the parse tree
	 */
	void exitDeleteLiteral(TimesheetQueryParser.DeleteLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code cmdFunc}
	 * labeled alternative in {@link TimesheetQueryParser#command}.
	 * @param ctx the parse tree
	 */
	void enterCmdFunc(TimesheetQueryParser.CmdFuncContext ctx);
	/**
	 * Exit a parse tree produced by the {@code cmdFunc}
	 * labeled alternative in {@link TimesheetQueryParser#command}.
	 * @param ctx the parse tree
	 */
	void exitCmdFunc(TimesheetQueryParser.CmdFuncContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#boolMonadicPrefixOp}.
	 * @param ctx the parse tree
	 */
	void enterBoolMonadicPrefixOp(TimesheetQueryParser.BoolMonadicPrefixOpContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#boolMonadicPrefixOp}.
	 * @param ctx the parse tree
	 */
	void exitBoolMonadicPrefixOp(TimesheetQueryParser.BoolMonadicPrefixOpContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#boolDyadicInfixOp}.
	 * @param ctx the parse tree
	 */
	void enterBoolDyadicInfixOp(TimesheetQueryParser.BoolDyadicInfixOpContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#boolDyadicInfixOp}.
	 * @param ctx the parse tree
	 */
	void exitBoolDyadicInfixOp(TimesheetQueryParser.BoolDyadicInfixOpContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#comparisonInfixOp}.
	 * @param ctx the parse tree
	 */
	void enterComparisonInfixOp(TimesheetQueryParser.ComparisonInfixOpContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#comparisonInfixOp}.
	 * @param ctx the parse tree
	 */
	void exitComparisonInfixOp(TimesheetQueryParser.ComparisonInfixOpContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#boolExp}.
	 * @param ctx the parse tree
	 */
	void enterBoolExp(TimesheetQueryParser.BoolExpContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#boolExp}.
	 * @param ctx the parse tree
	 */
	void exitBoolExp(TimesheetQueryParser.BoolExpContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#boolDyadicExp}.
	 * @param ctx the parse tree
	 */
	void enterBoolDyadicExp(TimesheetQueryParser.BoolDyadicExpContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#boolDyadicExp}.
	 * @param ctx the parse tree
	 */
	void exitBoolDyadicExp(TimesheetQueryParser.BoolDyadicExpContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#comparisonExp}.
	 * @param ctx the parse tree
	 */
	void enterComparisonExp(TimesheetQueryParser.ComparisonExpContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#comparisonExp}.
	 * @param ctx the parse tree
	 */
	void exitComparisonExp(TimesheetQueryParser.ComparisonExpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code singleInstanceImpliedExp}
	 * labeled alternative in {@link TimesheetQueryParser#impliedComparisonExp}.
	 * @param ctx the parse tree
	 */
	void enterSingleInstanceImpliedExp(TimesheetQueryParser.SingleInstanceImpliedExpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code singleInstanceImpliedExp}
	 * labeled alternative in {@link TimesheetQueryParser#impliedComparisonExp}.
	 * @param ctx the parse tree
	 */
	void exitSingleInstanceImpliedExp(TimesheetQueryParser.SingleInstanceImpliedExpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code listElementImpliedExp}
	 * labeled alternative in {@link TimesheetQueryParser#impliedComparisonExp}.
	 * @param ctx the parse tree
	 */
	void enterListElementImpliedExp(TimesheetQueryParser.ListElementImpliedExpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code listElementImpliedExp}
	 * labeled alternative in {@link TimesheetQueryParser#impliedComparisonExp}.
	 * @param ctx the parse tree
	 */
	void exitListElementImpliedExp(TimesheetQueryParser.ListElementImpliedExpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code specialLiteralImpliedExp}
	 * labeled alternative in {@link TimesheetQueryParser#impliedComparisonExp}.
	 * @param ctx the parse tree
	 */
	void enterSpecialLiteralImpliedExp(TimesheetQueryParser.SpecialLiteralImpliedExpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code specialLiteralImpliedExp}
	 * labeled alternative in {@link TimesheetQueryParser#impliedComparisonExp}.
	 * @param ctx the parse tree
	 */
	void exitSpecialLiteralImpliedExp(TimesheetQueryParser.SpecialLiteralImpliedExpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code fieldImpliedExp}
	 * labeled alternative in {@link TimesheetQueryParser#impliedComparisonExp}.
	 * @param ctx the parse tree
	 */
	void enterFieldImpliedExp(TimesheetQueryParser.FieldImpliedExpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code fieldImpliedExp}
	 * labeled alternative in {@link TimesheetQueryParser#impliedComparisonExp}.
	 * @param ctx the parse tree
	 */
	void exitFieldImpliedExp(TimesheetQueryParser.FieldImpliedExpContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#atomMonadicExp}.
	 * @param ctx the parse tree
	 */
	void enterAtomMonadicExp(TimesheetQueryParser.AtomMonadicExpContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#atomMonadicExp}.
	 * @param ctx the parse tree
	 */
	void exitAtomMonadicExp(TimesheetQueryParser.AtomMonadicExpContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#series}.
	 * @param ctx the parse tree
	 */
	void enterSeries(TimesheetQueryParser.SeriesContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#series}.
	 * @param ctx the parse tree
	 */
	void exitSeries(TimesheetQueryParser.SeriesContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#seriesFunc}.
	 * @param ctx the parse tree
	 */
	void enterSeriesFunc(TimesheetQueryParser.SeriesFuncContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#seriesFunc}.
	 * @param ctx the parse tree
	 */
	void exitSeriesFunc(TimesheetQueryParser.SeriesFuncContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#commandFunc}.
	 * @param ctx the parse tree
	 */
	void enterCommandFunc(TimesheetQueryParser.CommandFuncContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#commandFunc}.
	 * @param ctx the parse tree
	 */
	void exitCommandFunc(TimesheetQueryParser.CommandFuncContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#field}.
	 * @param ctx the parse tree
	 */
	void enterField(TimesheetQueryParser.FieldContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#field}.
	 * @param ctx the parse tree
	 */
	void exitField(TimesheetQueryParser.FieldContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#literal}.
	 * @param ctx the parse tree
	 */
	void enterLiteral(TimesheetQueryParser.LiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#literal}.
	 * @param ctx the parse tree
	 */
	void exitLiteral(TimesheetQueryParser.LiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#singleInstLiteral}.
	 * @param ctx the parse tree
	 */
	void enterSingleInstLiteral(TimesheetQueryParser.SingleInstLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#singleInstLiteral}.
	 * @param ctx the parse tree
	 */
	void exitSingleInstLiteral(TimesheetQueryParser.SingleInstLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#listElementLiteral}.
	 * @param ctx the parse tree
	 */
	void enterListElementLiteral(TimesheetQueryParser.ListElementLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#listElementLiteral}.
	 * @param ctx the parse tree
	 */
	void exitListElementLiteral(TimesheetQueryParser.ListElementLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code string}
	 * labeled alternative in {@link TimesheetQueryParser#specialLiteral}.
	 * @param ctx the parse tree
	 */
	void enterString(TimesheetQueryParser.StringContext ctx);
	/**
	 * Exit a parse tree produced by the {@code string}
	 * labeled alternative in {@link TimesheetQueryParser#specialLiteral}.
	 * @param ctx the parse tree
	 */
	void exitString(TimesheetQueryParser.StringContext ctx);
	/**
	 * Enter a parse tree produced by the {@code intPrimitive}
	 * labeled alternative in {@link TimesheetQueryParser#specialLiteral}.
	 * @param ctx the parse tree
	 */
	void enterIntPrimitive(TimesheetQueryParser.IntPrimitiveContext ctx);
	/**
	 * Exit a parse tree produced by the {@code intPrimitive}
	 * labeled alternative in {@link TimesheetQueryParser#specialLiteral}.
	 * @param ctx the parse tree
	 */
	void exitIntPrimitive(TimesheetQueryParser.IntPrimitiveContext ctx);
	/**
	 * Enter a parse tree produced by the {@code floatPrimitive}
	 * labeled alternative in {@link TimesheetQueryParser#specialLiteral}.
	 * @param ctx the parse tree
	 */
	void enterFloatPrimitive(TimesheetQueryParser.FloatPrimitiveContext ctx);
	/**
	 * Exit a parse tree produced by the {@code floatPrimitive}
	 * labeled alternative in {@link TimesheetQueryParser#specialLiteral}.
	 * @param ctx the parse tree
	 */
	void exitFloatPrimitive(TimesheetQueryParser.FloatPrimitiveContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#literalReplaceFunc}.
	 * @param ctx the parse tree
	 */
	void enterLiteralReplaceFunc(TimesheetQueryParser.LiteralReplaceFuncContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#literalReplaceFunc}.
	 * @param ctx the parse tree
	 */
	void exitLiteralReplaceFunc(TimesheetQueryParser.LiteralReplaceFuncContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#epochSchemeIndex}.
	 * @param ctx the parse tree
	 */
	void enterEpochSchemeIndex(TimesheetQueryParser.EpochSchemeIndexContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#epochSchemeIndex}.
	 * @param ctx the parse tree
	 */
	void exitEpochSchemeIndex(TimesheetQueryParser.EpochSchemeIndexContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#reloadDesc}.
	 * @param ctx the parse tree
	 */
	void enterReloadDesc(TimesheetQueryParser.ReloadDescContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#reloadDesc}.
	 * @param ctx the parse tree
	 */
	void exitReloadDesc(TimesheetQueryParser.ReloadDescContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#projectLiteral}.
	 * @param ctx the parse tree
	 */
	void enterProjectLiteral(TimesheetQueryParser.ProjectLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#projectLiteral}.
	 * @param ctx the parse tree
	 */
	void exitProjectLiteral(TimesheetQueryParser.ProjectLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#metaprojectLiteral}.
	 * @param ctx the parse tree
	 */
	void enterMetaprojectLiteral(TimesheetQueryParser.MetaprojectLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#metaprojectLiteral}.
	 * @param ctx the parse tree
	 */
	void exitMetaprojectLiteral(TimesheetQueryParser.MetaprojectLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#tagLiteral}.
	 * @param ctx the parse tree
	 */
	void enterTagLiteral(TimesheetQueryParser.TagLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#tagLiteral}.
	 * @param ctx the parse tree
	 */
	void exitTagLiteral(TimesheetQueryParser.TagLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#epochLiteral}.
	 * @param ctx the parse tree
	 */
	void enterEpochLiteral(TimesheetQueryParser.EpochLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#epochLiteral}.
	 * @param ctx the parse tree
	 */
	void exitEpochLiteral(TimesheetQueryParser.EpochLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#descToken}.
	 * @param ctx the parse tree
	 */
	void enterDescToken(TimesheetQueryParser.DescTokenContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#descToken}.
	 * @param ctx the parse tree
	 */
	void exitDescToken(TimesheetQueryParser.DescTokenContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#moodLiteral}.
	 * @param ctx the parse tree
	 */
	void enterMoodLiteral(TimesheetQueryParser.MoodLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#moodLiteral}.
	 * @param ctx the parse tree
	 */
	void exitMoodLiteral(TimesheetQueryParser.MoodLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#datetimeLiteral}.
	 * @param ctx the parse tree
	 */
	void enterDatetimeLiteral(TimesheetQueryParser.DatetimeLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#datetimeLiteral}.
	 * @param ctx the parse tree
	 */
	void exitDatetimeLiteral(TimesheetQueryParser.DatetimeLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link TimesheetQueryParser#timedeltaLiteral}.
	 * @param ctx the parse tree
	 */
	void enterTimedeltaLiteral(TimesheetQueryParser.TimedeltaLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link TimesheetQueryParser#timedeltaLiteral}.
	 * @param ctx the parse tree
	 */
	void exitTimedeltaLiteral(TimesheetQueryParser.TimedeltaLiteralContext ctx);
}