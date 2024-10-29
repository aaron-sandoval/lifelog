// Generated from tsqparser/TimesheetQuery.g4 by ANTLR 4.13.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class TimesheetQueryParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, T__21=22, T__22=23, T__23=24, 
		T__24=25, T__25=26, T__26=27, T__27=28, T__28=29, T__29=30, T__30=31, 
		T__31=32, T__32=33, T__33=34, T__34=35, T__35=36, T__36=37, T__37=38, 
		T__38=39, T__39=40, T__40=41, T__41=42, T__42=43, T__43=44, T__44=45, 
		T__45=46, T__46=47, T__47=48, T__48=49, T__49=50, T__50=51, T__51=52, 
		T__52=53, T__53=54, BLOCK_COMMENT=55, STRING_LITERAL=56, STRING_LITERAL_DQ=57, 
		STRING_LITERAL_SQ=58, INLINE_COMMENT=59, INT=60, FLOAT=61, NAME=62, WHITESPACE=63, 
		NEWLINE=64, ANY=65;
	public static final int
		RULE_ruleList = 0, RULE_rule = 1, RULE_query = 2, RULE_command = 3, RULE_boolMonadicPrefixOp = 4, 
		RULE_boolDyadicInfixOp = 5, RULE_comparisonInfixOp = 6, RULE_boolExp = 7, 
		RULE_boolDyadicExp = 8, RULE_comparisonExp = 9, RULE_impliedComparisonExp = 10, 
		RULE_atomMonadicExp = 11, RULE_series = 12, RULE_seriesFunc = 13, RULE_commandFunc = 14, 
		RULE_field = 15, RULE_literal = 16, RULE_singleInstLiteral = 17, RULE_listElementLiteral = 18, 
		RULE_specialLiteral = 19, RULE_literalReplaceFunc = 20, RULE_epochSchemeIndex = 21, 
		RULE_reloadDesc = 22, RULE_projectLiteral = 23, RULE_metaprojectLiteral = 24, 
		RULE_tagLiteral = 25, RULE_epochLiteral = 26, RULE_descToken = 27, RULE_moodLiteral = 28, 
		RULE_datetimeLiteral = 29, RULE_timedeltaLiteral = 30;
	private static String[] makeRuleNames() {
		return new String[] {
			"ruleList", "rule", "query", "command", "boolMonadicPrefixOp", "boolDyadicInfixOp", 
			"comparisonInfixOp", "boolExp", "boolDyadicExp", "comparisonExp", "impliedComparisonExp", 
			"atomMonadicExp", "series", "seriesFunc", "commandFunc", "field", "literal", 
			"singleInstLiteral", "listElementLiteral", "specialLiteral", "literalReplaceFunc", 
			"epochSchemeIndex", "reloadDesc", "projectLiteral", "metaprojectLiteral", 
			"tagLiteral", "epochLiteral", "descToken", "moodLiteral", "datetimeLiteral", 
			"timedeltaLiteral"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "':'", "';'", "'!'", "'|'", "'&'", "'>='", "'<='", "'>'", "'<'", 
			"'!='", "'=='", "'in'", "'('", "')'", "'description'", "'project'", "'tags'", 
			"'id'", "'start'", "'end'", "'duration'", "'epoch'", "'mood'", "'circad'", 
			"'metaproject'", "'bodyparts'", "'Location'", "'Person'", "'Food'", "'Media'", 
			"'Audiobook'", "'Podcast'", "'TVShow'", "'Movie'", "'SubjectMatter'", 
			"'.replace'", "'EpochScheme.'", "'['", "']'", "'reloadDescription()'", 
			"'Project.'", "'Metaproject.'", "'Meta.'", "'MP.'", "'Tag.'", "'Epoch.'", 
			"'Mood.'", "'datetime('", "','", "'timedelta('", "'weeks='", "'days='", 
			"'hours='", "'minutes='"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, "BLOCK_COMMENT", "STRING_LITERAL", 
			"STRING_LITERAL_DQ", "STRING_LITERAL_SQ", "INLINE_COMMENT", "INT", "FLOAT", 
			"NAME", "WHITESPACE", "NEWLINE", "ANY"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "TimesheetQuery.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public TimesheetQueryParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RuleListContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(TimesheetQueryParser.EOF, 0); }
		public List<RuleContext> rule_() {
			return getRuleContexts(RuleContext.class);
		}
		public RuleContext rule_(int i) {
			return getRuleContext(RuleContext.class,i);
		}
		public RuleListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleList; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterRuleList(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitRuleList(this);
		}
	}

	public final RuleListContext ruleList() throws RecognitionException {
		RuleListContext _localctx = new RuleListContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_ruleList);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(65);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 3532508964853882890L) != 0)) {
				{
				{
				setState(62);
				rule_();
				}
				}
				setState(67);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(68);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RuleContext extends ParserRuleContext {
		public QueryContext query() {
			return getRuleContext(QueryContext.class,0);
		}
		public List<CommandContext> command() {
			return getRuleContexts(CommandContext.class);
		}
		public CommandContext command(int i) {
			return getRuleContext(CommandContext.class,i);
		}
		public RuleContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rule; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterRule(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitRule(this);
		}
	}

	public final RuleContext rule_() throws RecognitionException {
		RuleContext _localctx = new RuleContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_rule);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(71);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 3532508964853882888L) != 0)) {
				{
				setState(70);
				query();
				}
			}

			setState(73);
			match(T__0);
			setState(82);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 3532509858207105032L) != 0)) {
				{
				setState(74);
				command();
				setState(79);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
				while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
					if ( _alt==1 ) {
						{
						{
						setState(75);
						match(T__1);
						setState(76);
						command();
						}
						} 
					}
					setState(81);
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
				}
				}
			}

			setState(84);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class QueryContext extends ParserRuleContext {
		public BoolExpContext boolExp() {
			return getRuleContext(BoolExpContext.class,0);
		}
		public QueryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_query; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterQuery(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitQuery(this);
		}
	}

	public final QueryContext query() throws RecognitionException {
		QueryContext _localctx = new QueryContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_query);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(86);
			boolExp();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CommandContext extends ParserRuleContext {
		public CommandContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_command; }
	 
		public CommandContext() { }
		public void copyFrom(CommandContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SetLiteralContext extends CommandContext {
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public SetLiteralContext(CommandContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterSetLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitSetLiteral(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CmdFuncContext extends CommandContext {
		public CommandFuncContext commandFunc() {
			return getRuleContext(CommandFuncContext.class,0);
		}
		public CmdFuncContext(CommandContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterCmdFunc(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitCmdFunc(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DeleteLiteralContext extends CommandContext {
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public DeleteLiteralContext(CommandContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterDeleteLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitDeleteLiteral(this);
		}
	}

	public final CommandContext command() throws RecognitionException {
		CommandContext _localctx = new CommandContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_command);
		try {
			setState(92);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,4,_ctx) ) {
			case 1:
				_localctx = new SetLiteralContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(88);
				literal();
				}
				break;
			case 2:
				_localctx = new DeleteLiteralContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(89);
				match(T__2);
				setState(90);
				literal();
				}
				break;
			case 3:
				_localctx = new CmdFuncContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(91);
				commandFunc();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BoolMonadicPrefixOpContext extends ParserRuleContext {
		public BoolMonadicPrefixOpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_boolMonadicPrefixOp; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterBoolMonadicPrefixOp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitBoolMonadicPrefixOp(this);
		}
	}

	public final BoolMonadicPrefixOpContext boolMonadicPrefixOp() throws RecognitionException {
		BoolMonadicPrefixOpContext _localctx = new BoolMonadicPrefixOpContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_boolMonadicPrefixOp);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(94);
			match(T__2);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BoolDyadicInfixOpContext extends ParserRuleContext {
		public BoolDyadicInfixOpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_boolDyadicInfixOp; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterBoolDyadicInfixOp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitBoolDyadicInfixOp(this);
		}
	}

	public final BoolDyadicInfixOpContext boolDyadicInfixOp() throws RecognitionException {
		BoolDyadicInfixOpContext _localctx = new BoolDyadicInfixOpContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_boolDyadicInfixOp);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(96);
			_la = _input.LA(1);
			if ( !(_la==T__3 || _la==T__4) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ComparisonInfixOpContext extends ParserRuleContext {
		public ComparisonInfixOpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comparisonInfixOp; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterComparisonInfixOp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitComparisonInfixOp(this);
		}
	}

	public final ComparisonInfixOpContext comparisonInfixOp() throws RecognitionException {
		ComparisonInfixOpContext _localctx = new ComparisonInfixOpContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_comparisonInfixOp);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(98);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 8128L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BoolExpContext extends ParserRuleContext {
		public BoolDyadicExpContext boolDyadicExp() {
			return getRuleContext(BoolDyadicExpContext.class,0);
		}
		public BoolExpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_boolExp; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterBoolExp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitBoolExp(this);
		}
	}

	public final BoolExpContext boolExp() throws RecognitionException {
		BoolExpContext _localctx = new BoolExpContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_boolExp);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(100);
			boolDyadicExp();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BoolDyadicExpContext extends ParserRuleContext {
		public List<ComparisonExpContext> comparisonExp() {
			return getRuleContexts(ComparisonExpContext.class);
		}
		public ComparisonExpContext comparisonExp(int i) {
			return getRuleContext(ComparisonExpContext.class,i);
		}
		public BoolDyadicInfixOpContext boolDyadicInfixOp() {
			return getRuleContext(BoolDyadicInfixOpContext.class,0);
		}
		public BoolDyadicExpContext boolDyadicExp() {
			return getRuleContext(BoolDyadicExpContext.class,0);
		}
		public BoolDyadicExpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_boolDyadicExp; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterBoolDyadicExp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitBoolDyadicExp(this);
		}
	}

	public final BoolDyadicExpContext boolDyadicExp() throws RecognitionException {
		BoolDyadicExpContext _localctx = new BoolDyadicExpContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_boolDyadicExp);
		int _la;
		try {
			setState(112);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,6,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(102);
				comparisonExp();
				setState(106);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__3 || _la==T__4) {
					{
					setState(103);
					boolDyadicInfixOp();
					setState(104);
					comparisonExp();
					}
				}

				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				{
				setState(108);
				comparisonExp();
				setState(109);
				boolDyadicInfixOp();
				setState(110);
				boolDyadicExp();
				}
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ComparisonExpContext extends ParserRuleContext {
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public ComparisonInfixOpContext comparisonInfixOp() {
			return getRuleContext(ComparisonInfixOpContext.class,0);
		}
		public SeriesContext series() {
			return getRuleContext(SeriesContext.class,0);
		}
		public ImpliedComparisonExpContext impliedComparisonExp() {
			return getRuleContext(ImpliedComparisonExpContext.class,0);
		}
		public AtomMonadicExpContext atomMonadicExp() {
			return getRuleContext(AtomMonadicExpContext.class,0);
		}
		public ComparisonExpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comparisonExp; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterComparisonExp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitComparisonExp(this);
		}
	}

	public final ComparisonExpContext comparisonExp() throws RecognitionException {
		ComparisonExpContext _localctx = new ComparisonExpContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_comparisonExp);
		try {
			setState(125);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,7,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				{
				setState(114);
				literal();
				{
				setState(115);
				comparisonInfixOp();
				setState(116);
				series();
				}
				}
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				{
				{
				setState(118);
				series();
				setState(119);
				comparisonInfixOp();
				}
				setState(121);
				literal();
				}
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(123);
				impliedComparisonExp();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(124);
				atomMonadicExp();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ImpliedComparisonExpContext extends ParserRuleContext {
		public ImpliedComparisonExpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_impliedComparisonExp; }
	 
		public ImpliedComparisonExpContext() { }
		public void copyFrom(ImpliedComparisonExpContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ListElementImpliedExpContext extends ImpliedComparisonExpContext {
		public ListElementLiteralContext listElementLiteral() {
			return getRuleContext(ListElementLiteralContext.class,0);
		}
		public ListElementImpliedExpContext(ImpliedComparisonExpContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterListElementImpliedExp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitListElementImpliedExp(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SpecialLiteralImpliedExpContext extends ImpliedComparisonExpContext {
		public SpecialLiteralContext specialLiteral() {
			return getRuleContext(SpecialLiteralContext.class,0);
		}
		public SpecialLiteralImpliedExpContext(ImpliedComparisonExpContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterSpecialLiteralImpliedExp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitSpecialLiteralImpliedExp(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SingleInstanceImpliedExpContext extends ImpliedComparisonExpContext {
		public SingleInstLiteralContext singleInstLiteral() {
			return getRuleContext(SingleInstLiteralContext.class,0);
		}
		public SingleInstanceImpliedExpContext(ImpliedComparisonExpContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterSingleInstanceImpliedExp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitSingleInstanceImpliedExp(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FieldImpliedExpContext extends ImpliedComparisonExpContext {
		public FieldContext field() {
			return getRuleContext(FieldContext.class,0);
		}
		public FieldImpliedExpContext(ImpliedComparisonExpContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterFieldImpliedExp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitFieldImpliedExp(this);
		}
	}

	public final ImpliedComparisonExpContext impliedComparisonExp() throws RecognitionException {
		ImpliedComparisonExpContext _localctx = new ImpliedComparisonExpContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_impliedComparisonExp);
		try {
			setState(131);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__40:
			case T__41:
			case T__42:
			case T__43:
			case T__45:
			case T__46:
			case T__47:
			case T__49:
				_localctx = new SingleInstanceImpliedExpContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(127);
				singleInstLiteral();
				}
				break;
			case T__44:
				_localctx = new ListElementImpliedExpContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(128);
				listElementLiteral();
				}
				break;
			case STRING_LITERAL:
			case INT:
			case FLOAT:
				_localctx = new SpecialLiteralImpliedExpContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(129);
				specialLiteral();
				}
				break;
			case T__14:
			case T__15:
			case T__16:
			case T__17:
			case T__18:
			case T__19:
			case T__20:
			case T__21:
			case T__22:
			case T__23:
			case T__24:
			case T__25:
			case T__26:
			case T__27:
			case T__28:
			case T__29:
			case T__30:
			case T__31:
			case T__32:
			case T__33:
			case T__34:
				_localctx = new FieldImpliedExpContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(130);
				field();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AtomMonadicExpContext extends ParserRuleContext {
		public ImpliedComparisonExpContext impliedComparisonExp() {
			return getRuleContext(ImpliedComparisonExpContext.class,0);
		}
		public BoolMonadicPrefixOpContext boolMonadicPrefixOp() {
			return getRuleContext(BoolMonadicPrefixOpContext.class,0);
		}
		public BoolExpContext boolExp() {
			return getRuleContext(BoolExpContext.class,0);
		}
		public AtomMonadicExpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_atomMonadicExp; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterAtomMonadicExp(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitAtomMonadicExp(this);
		}
	}

	public final AtomMonadicExpContext atomMonadicExp() throws RecognitionException {
		AtomMonadicExpContext _localctx = new AtomMonadicExpContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_atomMonadicExp);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(134);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__2) {
				{
				setState(133);
				boolMonadicPrefixOp();
				}
			}

			setState(141);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__14:
			case T__15:
			case T__16:
			case T__17:
			case T__18:
			case T__19:
			case T__20:
			case T__21:
			case T__22:
			case T__23:
			case T__24:
			case T__25:
			case T__26:
			case T__27:
			case T__28:
			case T__29:
			case T__30:
			case T__31:
			case T__32:
			case T__33:
			case T__34:
			case T__40:
			case T__41:
			case T__42:
			case T__43:
			case T__44:
			case T__45:
			case T__46:
			case T__47:
			case T__49:
			case STRING_LITERAL:
			case INT:
			case FLOAT:
				{
				setState(136);
				impliedComparisonExp();
				}
				break;
			case T__12:
				{
				{
				setState(137);
				match(T__12);
				setState(138);
				boolExp();
				setState(139);
				match(T__13);
				}
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SeriesContext extends ParserRuleContext {
		public FieldContext field() {
			return getRuleContext(FieldContext.class,0);
		}
		public SeriesFuncContext seriesFunc() {
			return getRuleContext(SeriesFuncContext.class,0);
		}
		public SeriesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_series; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterSeries(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitSeries(this);
		}
	}

	public final SeriesContext series() throws RecognitionException {
		SeriesContext _localctx = new SeriesContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_series);
		try {
			setState(145);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__14:
			case T__15:
			case T__16:
			case T__17:
			case T__18:
			case T__19:
			case T__20:
			case T__21:
			case T__22:
			case T__23:
			case T__24:
			case T__25:
			case T__26:
			case T__27:
			case T__28:
			case T__29:
			case T__30:
			case T__31:
			case T__32:
			case T__33:
			case T__34:
				enterOuterAlt(_localctx, 1);
				{
				setState(143);
				field();
				}
				break;
			case T__36:
				enterOuterAlt(_localctx, 2);
				{
				setState(144);
				seriesFunc();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SeriesFuncContext extends ParserRuleContext {
		public EpochSchemeIndexContext epochSchemeIndex() {
			return getRuleContext(EpochSchemeIndexContext.class,0);
		}
		public SeriesFuncContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_seriesFunc; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterSeriesFunc(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitSeriesFunc(this);
		}
	}

	public final SeriesFuncContext seriesFunc() throws RecognitionException {
		SeriesFuncContext _localctx = new SeriesFuncContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_seriesFunc);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(147);
			epochSchemeIndex();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CommandFuncContext extends ParserRuleContext {
		public LiteralReplaceFuncContext literalReplaceFunc() {
			return getRuleContext(LiteralReplaceFuncContext.class,0);
		}
		public ReloadDescContext reloadDesc() {
			return getRuleContext(ReloadDescContext.class,0);
		}
		public CommandFuncContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_commandFunc; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterCommandFunc(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitCommandFunc(this);
		}
	}

	public final CommandFuncContext commandFunc() throws RecognitionException {
		CommandFuncContext _localctx = new CommandFuncContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_commandFunc);
		try {
			setState(151);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__40:
			case T__41:
			case T__42:
			case T__43:
			case T__44:
			case T__45:
			case T__46:
			case T__47:
			case T__49:
			case STRING_LITERAL:
			case INT:
			case FLOAT:
				enterOuterAlt(_localctx, 1);
				{
				setState(149);
				literalReplaceFunc();
				}
				break;
			case T__39:
				enterOuterAlt(_localctx, 2);
				{
				setState(150);
				reloadDesc();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FieldContext extends ParserRuleContext {
		public FieldContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_field; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterField(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitField(this);
		}
	}

	public final FieldContext field() throws RecognitionException {
		FieldContext _localctx = new FieldContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_field);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(153);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 68719443968L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LiteralContext extends ParserRuleContext {
		public SingleInstLiteralContext singleInstLiteral() {
			return getRuleContext(SingleInstLiteralContext.class,0);
		}
		public ListElementLiteralContext listElementLiteral() {
			return getRuleContext(ListElementLiteralContext.class,0);
		}
		public SpecialLiteralContext specialLiteral() {
			return getRuleContext(SpecialLiteralContext.class,0);
		}
		public LiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literal; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitLiteral(this);
		}
	}

	public final LiteralContext literal() throws RecognitionException {
		LiteralContext _localctx = new LiteralContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_literal);
		try {
			setState(158);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__40:
			case T__41:
			case T__42:
			case T__43:
			case T__45:
			case T__46:
			case T__47:
			case T__49:
				enterOuterAlt(_localctx, 1);
				{
				setState(155);
				singleInstLiteral();
				}
				break;
			case T__44:
				enterOuterAlt(_localctx, 2);
				{
				setState(156);
				listElementLiteral();
				}
				break;
			case STRING_LITERAL:
			case INT:
			case FLOAT:
				enterOuterAlt(_localctx, 3);
				{
				setState(157);
				specialLiteral();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SingleInstLiteralContext extends ParserRuleContext {
		public ProjectLiteralContext projectLiteral() {
			return getRuleContext(ProjectLiteralContext.class,0);
		}
		public EpochLiteralContext epochLiteral() {
			return getRuleContext(EpochLiteralContext.class,0);
		}
		public DatetimeLiteralContext datetimeLiteral() {
			return getRuleContext(DatetimeLiteralContext.class,0);
		}
		public TimedeltaLiteralContext timedeltaLiteral() {
			return getRuleContext(TimedeltaLiteralContext.class,0);
		}
		public MetaprojectLiteralContext metaprojectLiteral() {
			return getRuleContext(MetaprojectLiteralContext.class,0);
		}
		public MoodLiteralContext moodLiteral() {
			return getRuleContext(MoodLiteralContext.class,0);
		}
		public SingleInstLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_singleInstLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterSingleInstLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitSingleInstLiteral(this);
		}
	}

	public final SingleInstLiteralContext singleInstLiteral() throws RecognitionException {
		SingleInstLiteralContext _localctx = new SingleInstLiteralContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_singleInstLiteral);
		try {
			setState(166);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__40:
				enterOuterAlt(_localctx, 1);
				{
				setState(160);
				projectLiteral();
				}
				break;
			case T__45:
				enterOuterAlt(_localctx, 2);
				{
				setState(161);
				epochLiteral();
				}
				break;
			case T__47:
				enterOuterAlt(_localctx, 3);
				{
				setState(162);
				datetimeLiteral();
				}
				break;
			case T__49:
				enterOuterAlt(_localctx, 4);
				{
				setState(163);
				timedeltaLiteral();
				}
				break;
			case T__41:
			case T__42:
			case T__43:
				enterOuterAlt(_localctx, 5);
				{
				setState(164);
				metaprojectLiteral();
				}
				break;
			case T__46:
				enterOuterAlt(_localctx, 6);
				{
				setState(165);
				moodLiteral();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ListElementLiteralContext extends ParserRuleContext {
		public TagLiteralContext tagLiteral() {
			return getRuleContext(TagLiteralContext.class,0);
		}
		public ListElementLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_listElementLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterListElementLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitListElementLiteral(this);
		}
	}

	public final ListElementLiteralContext listElementLiteral() throws RecognitionException {
		ListElementLiteralContext _localctx = new ListElementLiteralContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_listElementLiteral);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(168);
			tagLiteral();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SpecialLiteralContext extends ParserRuleContext {
		public SpecialLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_specialLiteral; }
	 
		public SpecialLiteralContext() { }
		public void copyFrom(SpecialLiteralContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StringContext extends SpecialLiteralContext {
		public DescTokenContext descToken() {
			return getRuleContext(DescTokenContext.class,0);
		}
		public StringContext(SpecialLiteralContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterString(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitString(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FloatPrimitiveContext extends SpecialLiteralContext {
		public TerminalNode FLOAT() { return getToken(TimesheetQueryParser.FLOAT, 0); }
		public FloatPrimitiveContext(SpecialLiteralContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterFloatPrimitive(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitFloatPrimitive(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IntPrimitiveContext extends SpecialLiteralContext {
		public TerminalNode INT() { return getToken(TimesheetQueryParser.INT, 0); }
		public IntPrimitiveContext(SpecialLiteralContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterIntPrimitive(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitIntPrimitive(this);
		}
	}

	public final SpecialLiteralContext specialLiteral() throws RecognitionException {
		SpecialLiteralContext _localctx = new SpecialLiteralContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_specialLiteral);
		try {
			setState(173);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING_LITERAL:
				_localctx = new StringContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(170);
				descToken();
				}
				break;
			case INT:
				_localctx = new IntPrimitiveContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(171);
				match(INT);
				}
				break;
			case FLOAT:
				_localctx = new FloatPrimitiveContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(172);
				match(FLOAT);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LiteralReplaceFuncContext extends ParserRuleContext {
		public LiteralContext old;
		public LiteralContext new_;
		public List<LiteralContext> literal() {
			return getRuleContexts(LiteralContext.class);
		}
		public LiteralContext literal(int i) {
			return getRuleContext(LiteralContext.class,i);
		}
		public LiteralReplaceFuncContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literalReplaceFunc; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterLiteralReplaceFunc(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitLiteralReplaceFunc(this);
		}
	}

	public final LiteralReplaceFuncContext literalReplaceFunc() throws RecognitionException {
		LiteralReplaceFuncContext _localctx = new LiteralReplaceFuncContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_literalReplaceFunc);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(175);
			((LiteralReplaceFuncContext)_localctx).old = literal();
			setState(176);
			match(T__35);
			setState(177);
			match(T__12);
			setState(178);
			((LiteralReplaceFuncContext)_localctx).new_ = literal();
			setState(179);
			match(T__13);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class EpochSchemeIndexContext extends ParserRuleContext {
		public Token scheme;
		public SeriesContext key;
		public TerminalNode NAME() { return getToken(TimesheetQueryParser.NAME, 0); }
		public SeriesContext series() {
			return getRuleContext(SeriesContext.class,0);
		}
		public EpochSchemeIndexContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_epochSchemeIndex; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterEpochSchemeIndex(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitEpochSchemeIndex(this);
		}
	}

	public final EpochSchemeIndexContext epochSchemeIndex() throws RecognitionException {
		EpochSchemeIndexContext _localctx = new EpochSchemeIndexContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_epochSchemeIndex);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(181);
			match(T__36);
			setState(182);
			((EpochSchemeIndexContext)_localctx).scheme = match(NAME);
			setState(187);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__37) {
				{
				setState(183);
				match(T__37);
				setState(184);
				((EpochSchemeIndexContext)_localctx).key = series();
				setState(185);
				match(T__38);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ReloadDescContext extends ParserRuleContext {
		public ReloadDescContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_reloadDesc; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterReloadDesc(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitReloadDesc(this);
		}
	}

	public final ReloadDescContext reloadDesc() throws RecognitionException {
		ReloadDescContext _localctx = new ReloadDescContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_reloadDesc);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(189);
			match(T__39);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProjectLiteralContext extends ParserRuleContext {
		public TerminalNode NAME() { return getToken(TimesheetQueryParser.NAME, 0); }
		public ProjectLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_projectLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterProjectLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitProjectLiteral(this);
		}
	}

	public final ProjectLiteralContext projectLiteral() throws RecognitionException {
		ProjectLiteralContext _localctx = new ProjectLiteralContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_projectLiteral);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(191);
			match(T__40);
			setState(192);
			match(NAME);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class MetaprojectLiteralContext extends ParserRuleContext {
		public TerminalNode NAME() { return getToken(TimesheetQueryParser.NAME, 0); }
		public MetaprojectLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_metaprojectLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterMetaprojectLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitMetaprojectLiteral(this);
		}
	}

	public final MetaprojectLiteralContext metaprojectLiteral() throws RecognitionException {
		MetaprojectLiteralContext _localctx = new MetaprojectLiteralContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_metaprojectLiteral);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(194);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 30786325577728L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			setState(195);
			match(NAME);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TagLiteralContext extends ParserRuleContext {
		public TerminalNode NAME() { return getToken(TimesheetQueryParser.NAME, 0); }
		public TagLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tagLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterTagLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitTagLiteral(this);
		}
	}

	public final TagLiteralContext tagLiteral() throws RecognitionException {
		TagLiteralContext _localctx = new TagLiteralContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_tagLiteral);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(197);
			match(T__44);
			setState(198);
			match(NAME);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class EpochLiteralContext extends ParserRuleContext {
		public TerminalNode NAME() { return getToken(TimesheetQueryParser.NAME, 0); }
		public EpochLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_epochLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterEpochLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitEpochLiteral(this);
		}
	}

	public final EpochLiteralContext epochLiteral() throws RecognitionException {
		EpochLiteralContext _localctx = new EpochLiteralContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_epochLiteral);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(200);
			match(T__45);
			setState(201);
			match(NAME);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DescTokenContext extends ParserRuleContext {
		public TerminalNode STRING_LITERAL() { return getToken(TimesheetQueryParser.STRING_LITERAL, 0); }
		public DescTokenContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_descToken; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterDescToken(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitDescToken(this);
		}
	}

	public final DescTokenContext descToken() throws RecognitionException {
		DescTokenContext _localctx = new DescTokenContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_descToken);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(203);
			match(STRING_LITERAL);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class MoodLiteralContext extends ParserRuleContext {
		public Token nameKey;
		public Token intKey;
		public TerminalNode NAME() { return getToken(TimesheetQueryParser.NAME, 0); }
		public TerminalNode INT() { return getToken(TimesheetQueryParser.INT, 0); }
		public MoodLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_moodLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterMoodLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitMoodLiteral(this);
		}
	}

	public final MoodLiteralContext moodLiteral() throws RecognitionException {
		MoodLiteralContext _localctx = new MoodLiteralContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_moodLiteral);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(205);
			match(T__46);
			setState(208);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case NAME:
				{
				setState(206);
				((MoodLiteralContext)_localctx).nameKey = match(NAME);
				}
				break;
			case INT:
				{
				setState(207);
				((MoodLiteralContext)_localctx).intKey = match(INT);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DatetimeLiteralContext extends ParserRuleContext {
		public Token year;
		public Token moreArgs;
		public List<TerminalNode> INT() { return getTokens(TimesheetQueryParser.INT); }
		public TerminalNode INT(int i) {
			return getToken(TimesheetQueryParser.INT, i);
		}
		public DatetimeLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_datetimeLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterDatetimeLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitDatetimeLiteral(this);
		}
	}

	public final DatetimeLiteralContext datetimeLiteral() throws RecognitionException {
		DatetimeLiteralContext _localctx = new DatetimeLiteralContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_datetimeLiteral);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(210);
			match(T__47);
			setState(211);
			((DatetimeLiteralContext)_localctx).year = match(INT);
			setState(216);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__48) {
				{
				{
				setState(212);
				match(T__48);
				setState(213);
				((DatetimeLiteralContext)_localctx).moreArgs = match(INT);
				}
				}
				setState(218);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(219);
			match(T__13);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TimedeltaLiteralContext extends ParserRuleContext {
		public Token weeks;
		public Token days;
		public Token hours;
		public Token minutes;
		public List<TerminalNode> INT() { return getTokens(TimesheetQueryParser.INT); }
		public TerminalNode INT(int i) {
			return getToken(TimesheetQueryParser.INT, i);
		}
		public TimedeltaLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_timedeltaLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).enterTimedeltaLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof TimesheetQueryListener ) ((TimesheetQueryListener)listener).exitTimedeltaLiteral(this);
		}
	}

	public final TimedeltaLiteralContext timedeltaLiteral() throws RecognitionException {
		TimedeltaLiteralContext _localctx = new TimedeltaLiteralContext(_ctx, getState());
		enterRule(_localctx, 60, RULE_timedeltaLiteral);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(221);
			match(T__49);
			setState(230);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__50:
				{
				{
				setState(222);
				match(T__50);
				setState(223);
				((TimedeltaLiteralContext)_localctx).weeks = match(INT);
				}
				}
				break;
			case T__51:
				{
				{
				setState(224);
				match(T__51);
				setState(225);
				((TimedeltaLiteralContext)_localctx).days = match(INT);
				}
				}
				break;
			case T__52:
				{
				{
				setState(226);
				match(T__52);
				setState(227);
				((TimedeltaLiteralContext)_localctx).hours = match(INT);
				}
				}
				break;
			case T__53:
				{
				{
				setState(228);
				match(T__53);
				setState(229);
				((TimedeltaLiteralContext)_localctx).minutes = match(INT);
				}
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			setState(235);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,20,_ctx) ) {
			case 1:
				{
				setState(232);
				match(T__48);
				setState(233);
				match(T__50);
				setState(234);
				((TimedeltaLiteralContext)_localctx).weeks = match(INT);
				}
				break;
			}
			setState(240);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,21,_ctx) ) {
			case 1:
				{
				setState(237);
				match(T__48);
				setState(238);
				match(T__51);
				setState(239);
				((TimedeltaLiteralContext)_localctx).days = match(INT);
				}
				break;
			}
			setState(245);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,22,_ctx) ) {
			case 1:
				{
				setState(242);
				match(T__48);
				setState(243);
				match(T__52);
				setState(244);
				((TimedeltaLiteralContext)_localctx).hours = match(INT);
				}
				break;
			}
			setState(250);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,23,_ctx) ) {
			case 1:
				{
				setState(247);
				match(T__48);
				setState(248);
				match(T__53);
				setState(249);
				((TimedeltaLiteralContext)_localctx).minutes = match(INT);
				}
				break;
			}
			setState(253);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__48) {
				{
				setState(252);
				match(T__48);
				}
			}

			setState(255);
			match(T__13);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001A\u0102\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007\u0012"+
		"\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002\u0015\u0007\u0015"+
		"\u0002\u0016\u0007\u0016\u0002\u0017\u0007\u0017\u0002\u0018\u0007\u0018"+
		"\u0002\u0019\u0007\u0019\u0002\u001a\u0007\u001a\u0002\u001b\u0007\u001b"+
		"\u0002\u001c\u0007\u001c\u0002\u001d\u0007\u001d\u0002\u001e\u0007\u001e"+
		"\u0001\u0000\u0005\u0000@\b\u0000\n\u0000\f\u0000C\t\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0001\u0003\u0001H\b\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0005\u0001N\b\u0001\n\u0001\f\u0001Q\t\u0001"+
		"\u0003\u0001S\b\u0001\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002"+
		"\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0003\u0003]\b\u0003"+
		"\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001\u0006\u0001\u0006"+
		"\u0001\u0007\u0001\u0007\u0001\b\u0001\b\u0001\b\u0001\b\u0003\bk\b\b"+
		"\u0001\b\u0001\b\u0001\b\u0001\b\u0003\bq\b\b\u0001\t\u0001\t\u0001\t"+
		"\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0003"+
		"\t~\b\t\u0001\n\u0001\n\u0001\n\u0001\n\u0003\n\u0084\b\n\u0001\u000b"+
		"\u0003\u000b\u0087\b\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b"+
		"\u0001\u000b\u0003\u000b\u008e\b\u000b\u0001\f\u0001\f\u0003\f\u0092\b"+
		"\f\u0001\r\u0001\r\u0001\u000e\u0001\u000e\u0003\u000e\u0098\b\u000e\u0001"+
		"\u000f\u0001\u000f\u0001\u0010\u0001\u0010\u0001\u0010\u0003\u0010\u009f"+
		"\b\u0010\u0001\u0011\u0001\u0011\u0001\u0011\u0001\u0011\u0001\u0011\u0001"+
		"\u0011\u0003\u0011\u00a7\b\u0011\u0001\u0012\u0001\u0012\u0001\u0013\u0001"+
		"\u0013\u0001\u0013\u0003\u0013\u00ae\b\u0013\u0001\u0014\u0001\u0014\u0001"+
		"\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0015\u0001\u0015\u0001"+
		"\u0015\u0001\u0015\u0001\u0015\u0001\u0015\u0003\u0015\u00bc\b\u0015\u0001"+
		"\u0016\u0001\u0016\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0018\u0001"+
		"\u0018\u0001\u0018\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u001a\u0001"+
		"\u001a\u0001\u001a\u0001\u001b\u0001\u001b\u0001\u001c\u0001\u001c\u0001"+
		"\u001c\u0003\u001c\u00d1\b\u001c\u0001\u001d\u0001\u001d\u0001\u001d\u0001"+
		"\u001d\u0005\u001d\u00d7\b\u001d\n\u001d\f\u001d\u00da\t\u001d\u0001\u001d"+
		"\u0001\u001d\u0001\u001e\u0001\u001e\u0001\u001e\u0001\u001e\u0001\u001e"+
		"\u0001\u001e\u0001\u001e\u0001\u001e\u0001\u001e\u0003\u001e\u00e7\b\u001e"+
		"\u0001\u001e\u0001\u001e\u0001\u001e\u0003\u001e\u00ec\b\u001e\u0001\u001e"+
		"\u0001\u001e\u0001\u001e\u0003\u001e\u00f1\b\u001e\u0001\u001e\u0001\u001e"+
		"\u0001\u001e\u0003\u001e\u00f6\b\u001e\u0001\u001e\u0001\u001e\u0001\u001e"+
		"\u0003\u001e\u00fb\b\u001e\u0001\u001e\u0003\u001e\u00fe\b\u001e\u0001"+
		"\u001e\u0001\u001e\u0001\u001e\u0000\u0000\u001f\u0000\u0002\u0004\u0006"+
		"\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u001e \"$&(*,."+
		"02468:<\u0000\u0004\u0001\u0000\u0004\u0005\u0001\u0000\u0006\f\u0001"+
		"\u0000\u000f#\u0001\u0000*,\u0108\u0000A\u0001\u0000\u0000\u0000\u0002"+
		"G\u0001\u0000\u0000\u0000\u0004V\u0001\u0000\u0000\u0000\u0006\\\u0001"+
		"\u0000\u0000\u0000\b^\u0001\u0000\u0000\u0000\n`\u0001\u0000\u0000\u0000"+
		"\fb\u0001\u0000\u0000\u0000\u000ed\u0001\u0000\u0000\u0000\u0010p\u0001"+
		"\u0000\u0000\u0000\u0012}\u0001\u0000\u0000\u0000\u0014\u0083\u0001\u0000"+
		"\u0000\u0000\u0016\u0086\u0001\u0000\u0000\u0000\u0018\u0091\u0001\u0000"+
		"\u0000\u0000\u001a\u0093\u0001\u0000\u0000\u0000\u001c\u0097\u0001\u0000"+
		"\u0000\u0000\u001e\u0099\u0001\u0000\u0000\u0000 \u009e\u0001\u0000\u0000"+
		"\u0000\"\u00a6\u0001\u0000\u0000\u0000$\u00a8\u0001\u0000\u0000\u0000"+
		"&\u00ad\u0001\u0000\u0000\u0000(\u00af\u0001\u0000\u0000\u0000*\u00b5"+
		"\u0001\u0000\u0000\u0000,\u00bd\u0001\u0000\u0000\u0000.\u00bf\u0001\u0000"+
		"\u0000\u00000\u00c2\u0001\u0000\u0000\u00002\u00c5\u0001\u0000\u0000\u0000"+
		"4\u00c8\u0001\u0000\u0000\u00006\u00cb\u0001\u0000\u0000\u00008\u00cd"+
		"\u0001\u0000\u0000\u0000:\u00d2\u0001\u0000\u0000\u0000<\u00dd\u0001\u0000"+
		"\u0000\u0000>@\u0003\u0002\u0001\u0000?>\u0001\u0000\u0000\u0000@C\u0001"+
		"\u0000\u0000\u0000A?\u0001\u0000\u0000\u0000AB\u0001\u0000\u0000\u0000"+
		"BD\u0001\u0000\u0000\u0000CA\u0001\u0000\u0000\u0000DE\u0005\u0000\u0000"+
		"\u0001E\u0001\u0001\u0000\u0000\u0000FH\u0003\u0004\u0002\u0000GF\u0001"+
		"\u0000\u0000\u0000GH\u0001\u0000\u0000\u0000HI\u0001\u0000\u0000\u0000"+
		"IR\u0005\u0001\u0000\u0000JO\u0003\u0006\u0003\u0000KL\u0005\u0002\u0000"+
		"\u0000LN\u0003\u0006\u0003\u0000MK\u0001\u0000\u0000\u0000NQ\u0001\u0000"+
		"\u0000\u0000OM\u0001\u0000\u0000\u0000OP\u0001\u0000\u0000\u0000PS\u0001"+
		"\u0000\u0000\u0000QO\u0001\u0000\u0000\u0000RJ\u0001\u0000\u0000\u0000"+
		"RS\u0001\u0000\u0000\u0000ST\u0001\u0000\u0000\u0000TU\u0005\u0002\u0000"+
		"\u0000U\u0003\u0001\u0000\u0000\u0000VW\u0003\u000e\u0007\u0000W\u0005"+
		"\u0001\u0000\u0000\u0000X]\u0003 \u0010\u0000YZ\u0005\u0003\u0000\u0000"+
		"Z]\u0003 \u0010\u0000[]\u0003\u001c\u000e\u0000\\X\u0001\u0000\u0000\u0000"+
		"\\Y\u0001\u0000\u0000\u0000\\[\u0001\u0000\u0000\u0000]\u0007\u0001\u0000"+
		"\u0000\u0000^_\u0005\u0003\u0000\u0000_\t\u0001\u0000\u0000\u0000`a\u0007"+
		"\u0000\u0000\u0000a\u000b\u0001\u0000\u0000\u0000bc\u0007\u0001\u0000"+
		"\u0000c\r\u0001\u0000\u0000\u0000de\u0003\u0010\b\u0000e\u000f\u0001\u0000"+
		"\u0000\u0000fj\u0003\u0012\t\u0000gh\u0003\n\u0005\u0000hi\u0003\u0012"+
		"\t\u0000ik\u0001\u0000\u0000\u0000jg\u0001\u0000\u0000\u0000jk\u0001\u0000"+
		"\u0000\u0000kq\u0001\u0000\u0000\u0000lm\u0003\u0012\t\u0000mn\u0003\n"+
		"\u0005\u0000no\u0003\u0010\b\u0000oq\u0001\u0000\u0000\u0000pf\u0001\u0000"+
		"\u0000\u0000pl\u0001\u0000\u0000\u0000q\u0011\u0001\u0000\u0000\u0000"+
		"rs\u0003 \u0010\u0000st\u0003\f\u0006\u0000tu\u0003\u0018\f\u0000u~\u0001"+
		"\u0000\u0000\u0000vw\u0003\u0018\f\u0000wx\u0003\f\u0006\u0000xy\u0001"+
		"\u0000\u0000\u0000yz\u0003 \u0010\u0000z~\u0001\u0000\u0000\u0000{~\u0003"+
		"\u0014\n\u0000|~\u0003\u0016\u000b\u0000}r\u0001\u0000\u0000\u0000}v\u0001"+
		"\u0000\u0000\u0000}{\u0001\u0000\u0000\u0000}|\u0001\u0000\u0000\u0000"+
		"~\u0013\u0001\u0000\u0000\u0000\u007f\u0084\u0003\"\u0011\u0000\u0080"+
		"\u0084\u0003$\u0012\u0000\u0081\u0084\u0003&\u0013\u0000\u0082\u0084\u0003"+
		"\u001e\u000f\u0000\u0083\u007f\u0001\u0000\u0000\u0000\u0083\u0080\u0001"+
		"\u0000\u0000\u0000\u0083\u0081\u0001\u0000\u0000\u0000\u0083\u0082\u0001"+
		"\u0000\u0000\u0000\u0084\u0015\u0001\u0000\u0000\u0000\u0085\u0087\u0003"+
		"\b\u0004\u0000\u0086\u0085\u0001\u0000\u0000\u0000\u0086\u0087\u0001\u0000"+
		"\u0000\u0000\u0087\u008d\u0001\u0000\u0000\u0000\u0088\u008e\u0003\u0014"+
		"\n\u0000\u0089\u008a\u0005\r\u0000\u0000\u008a\u008b\u0003\u000e\u0007"+
		"\u0000\u008b\u008c\u0005\u000e\u0000\u0000\u008c\u008e\u0001\u0000\u0000"+
		"\u0000\u008d\u0088\u0001\u0000\u0000\u0000\u008d\u0089\u0001\u0000\u0000"+
		"\u0000\u008e\u0017\u0001\u0000\u0000\u0000\u008f\u0092\u0003\u001e\u000f"+
		"\u0000\u0090\u0092\u0003\u001a\r\u0000\u0091\u008f\u0001\u0000\u0000\u0000"+
		"\u0091\u0090\u0001\u0000\u0000\u0000\u0092\u0019\u0001\u0000\u0000\u0000"+
		"\u0093\u0094\u0003*\u0015\u0000\u0094\u001b\u0001\u0000\u0000\u0000\u0095"+
		"\u0098\u0003(\u0014\u0000\u0096\u0098\u0003,\u0016\u0000\u0097\u0095\u0001"+
		"\u0000\u0000\u0000\u0097\u0096\u0001\u0000\u0000\u0000\u0098\u001d\u0001"+
		"\u0000\u0000\u0000\u0099\u009a\u0007\u0002\u0000\u0000\u009a\u001f\u0001"+
		"\u0000\u0000\u0000\u009b\u009f\u0003\"\u0011\u0000\u009c\u009f\u0003$"+
		"\u0012\u0000\u009d\u009f\u0003&\u0013\u0000\u009e\u009b\u0001\u0000\u0000"+
		"\u0000\u009e\u009c\u0001\u0000\u0000\u0000\u009e\u009d\u0001\u0000\u0000"+
		"\u0000\u009f!\u0001\u0000\u0000\u0000\u00a0\u00a7\u0003.\u0017\u0000\u00a1"+
		"\u00a7\u00034\u001a\u0000\u00a2\u00a7\u0003:\u001d\u0000\u00a3\u00a7\u0003"+
		"<\u001e\u0000\u00a4\u00a7\u00030\u0018\u0000\u00a5\u00a7\u00038\u001c"+
		"\u0000\u00a6\u00a0\u0001\u0000\u0000\u0000\u00a6\u00a1\u0001\u0000\u0000"+
		"\u0000\u00a6\u00a2\u0001\u0000\u0000\u0000\u00a6\u00a3\u0001\u0000\u0000"+
		"\u0000\u00a6\u00a4\u0001\u0000\u0000\u0000\u00a6\u00a5\u0001\u0000\u0000"+
		"\u0000\u00a7#\u0001\u0000\u0000\u0000\u00a8\u00a9\u00032\u0019\u0000\u00a9"+
		"%\u0001\u0000\u0000\u0000\u00aa\u00ae\u00036\u001b\u0000\u00ab\u00ae\u0005"+
		"<\u0000\u0000\u00ac\u00ae\u0005=\u0000\u0000\u00ad\u00aa\u0001\u0000\u0000"+
		"\u0000\u00ad\u00ab\u0001\u0000\u0000\u0000\u00ad\u00ac\u0001\u0000\u0000"+
		"\u0000\u00ae\'\u0001\u0000\u0000\u0000\u00af\u00b0\u0003 \u0010\u0000"+
		"\u00b0\u00b1\u0005$\u0000\u0000\u00b1\u00b2\u0005\r\u0000\u0000\u00b2"+
		"\u00b3\u0003 \u0010\u0000\u00b3\u00b4\u0005\u000e\u0000\u0000\u00b4)\u0001"+
		"\u0000\u0000\u0000\u00b5\u00b6\u0005%\u0000\u0000\u00b6\u00bb\u0005>\u0000"+
		"\u0000\u00b7\u00b8\u0005&\u0000\u0000\u00b8\u00b9\u0003\u0018\f\u0000"+
		"\u00b9\u00ba\u0005\'\u0000\u0000\u00ba\u00bc\u0001\u0000\u0000\u0000\u00bb"+
		"\u00b7\u0001\u0000\u0000\u0000\u00bb\u00bc\u0001\u0000\u0000\u0000\u00bc"+
		"+\u0001\u0000\u0000\u0000\u00bd\u00be\u0005(\u0000\u0000\u00be-\u0001"+
		"\u0000\u0000\u0000\u00bf\u00c0\u0005)\u0000\u0000\u00c0\u00c1\u0005>\u0000"+
		"\u0000\u00c1/\u0001\u0000\u0000\u0000\u00c2\u00c3\u0007\u0003\u0000\u0000"+
		"\u00c3\u00c4\u0005>\u0000\u0000\u00c41\u0001\u0000\u0000\u0000\u00c5\u00c6"+
		"\u0005-\u0000\u0000\u00c6\u00c7\u0005>\u0000\u0000\u00c73\u0001\u0000"+
		"\u0000\u0000\u00c8\u00c9\u0005.\u0000\u0000\u00c9\u00ca\u0005>\u0000\u0000"+
		"\u00ca5\u0001\u0000\u0000\u0000\u00cb\u00cc\u00058\u0000\u0000\u00cc7"+
		"\u0001\u0000\u0000\u0000\u00cd\u00d0\u0005/\u0000\u0000\u00ce\u00d1\u0005"+
		">\u0000\u0000\u00cf\u00d1\u0005<\u0000\u0000\u00d0\u00ce\u0001\u0000\u0000"+
		"\u0000\u00d0\u00cf\u0001\u0000\u0000\u0000\u00d19\u0001\u0000\u0000\u0000"+
		"\u00d2\u00d3\u00050\u0000\u0000\u00d3\u00d8\u0005<\u0000\u0000\u00d4\u00d5"+
		"\u00051\u0000\u0000\u00d5\u00d7\u0005<\u0000\u0000\u00d6\u00d4\u0001\u0000"+
		"\u0000\u0000\u00d7\u00da\u0001\u0000\u0000\u0000\u00d8\u00d6\u0001\u0000"+
		"\u0000\u0000\u00d8\u00d9\u0001\u0000\u0000\u0000\u00d9\u00db\u0001\u0000"+
		"\u0000\u0000\u00da\u00d8\u0001\u0000\u0000\u0000\u00db\u00dc\u0005\u000e"+
		"\u0000\u0000\u00dc;\u0001\u0000\u0000\u0000\u00dd\u00e6\u00052\u0000\u0000"+
		"\u00de\u00df\u00053\u0000\u0000\u00df\u00e7\u0005<\u0000\u0000\u00e0\u00e1"+
		"\u00054\u0000\u0000\u00e1\u00e7\u0005<\u0000\u0000\u00e2\u00e3\u00055"+
		"\u0000\u0000\u00e3\u00e7\u0005<\u0000\u0000\u00e4\u00e5\u00056\u0000\u0000"+
		"\u00e5\u00e7\u0005<\u0000\u0000\u00e6\u00de\u0001\u0000\u0000\u0000\u00e6"+
		"\u00e0\u0001\u0000\u0000\u0000\u00e6\u00e2\u0001\u0000\u0000\u0000\u00e6"+
		"\u00e4\u0001\u0000\u0000\u0000\u00e7\u00eb\u0001\u0000\u0000\u0000\u00e8"+
		"\u00e9\u00051\u0000\u0000\u00e9\u00ea\u00053\u0000\u0000\u00ea\u00ec\u0005"+
		"<\u0000\u0000\u00eb\u00e8\u0001\u0000\u0000\u0000\u00eb\u00ec\u0001\u0000"+
		"\u0000\u0000\u00ec\u00f0\u0001\u0000\u0000\u0000\u00ed\u00ee\u00051\u0000"+
		"\u0000\u00ee\u00ef\u00054\u0000\u0000\u00ef\u00f1\u0005<\u0000\u0000\u00f0"+
		"\u00ed\u0001\u0000\u0000\u0000\u00f0\u00f1\u0001\u0000\u0000\u0000\u00f1"+
		"\u00f5\u0001\u0000\u0000\u0000\u00f2\u00f3\u00051\u0000\u0000\u00f3\u00f4"+
		"\u00055\u0000\u0000\u00f4\u00f6\u0005<\u0000\u0000\u00f5\u00f2\u0001\u0000"+
		"\u0000\u0000\u00f5\u00f6\u0001\u0000\u0000\u0000\u00f6\u00fa\u0001\u0000"+
		"\u0000\u0000\u00f7\u00f8\u00051\u0000\u0000\u00f8\u00f9\u00056\u0000\u0000"+
		"\u00f9\u00fb\u0005<\u0000\u0000\u00fa\u00f7\u0001\u0000\u0000\u0000\u00fa"+
		"\u00fb\u0001\u0000\u0000\u0000\u00fb\u00fd\u0001\u0000\u0000\u0000\u00fc"+
		"\u00fe\u00051\u0000\u0000\u00fd\u00fc\u0001\u0000\u0000\u0000\u00fd\u00fe"+
		"\u0001\u0000\u0000\u0000\u00fe\u00ff\u0001\u0000\u0000\u0000\u00ff\u0100"+
		"\u0005\u000e\u0000\u0000\u0100=\u0001\u0000\u0000\u0000\u0019AGOR\\jp"+
		"}\u0083\u0086\u008d\u0091\u0097\u009e\u00a6\u00ad\u00bb\u00d0\u00d8\u00e6"+
		"\u00eb\u00f0\u00f5\u00fa\u00fd";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}