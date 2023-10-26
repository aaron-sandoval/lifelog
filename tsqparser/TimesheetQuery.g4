/*
antlr install directory:
C:\Users\Aaron\anaconda3\envs\Timesheet_Data_Analysis\envs\Timesheet_C\pkgs\antlr-4.12.0-h57928b3_0\Library\bin
command line compile: antlr4 -Dlanguage=Python3 TimesheetQuery.g4
command line run: javac -classpath C:\Users\Aaron\anaconda3\envs\Timesheet_Data_Analysis\envs\Timesheet_C\pkgs\antlr-4.12.0-h57928b3_0\Library\lib\antlr4-4.12.0-complete.jar TimesheetQuery*.java
*/

grammar TimesheetQuery;

/*
 * Parser Rules
 */
ruleList            : rule* EOF ;
rule                : query? ':' (command (';' command)*)? ';' ;
query               : boolExp ;


// Command expressions
command             : literal                   #setLiteral
//                    | (field '=' literal)       #setField
                    | '!' literal               #deleteLiteral
                    | commandFunc               #cmdFunc
                    ;


// Query expressions
// Operators, maybe these should have been in lexer rules instead, but too late since listener already built
boolMonadicPrefixOp : '!' ;
boolDyadicInfixOp   : '|' | '&' ;
comparisonInfixOp   : '>=' | '<=' | '>' | '<' | '!=' | '==' | 'in' ;

/*
Expression precedence hierarchy (high precedence to low)
(): parentheses
!: monadic prefix operators, e.g., the 'not' operator
>;==;etc.: comparison operators
&;|: boolean dyadic operators

Expression output data types not explicitly used in grammar definition
*/
boolExp             : boolDyadicExp ;
boolDyadicExp       : comparisonExp (boolDyadicInfixOp comparisonExp)?
                    | (comparisonExp boolDyadicInfixOp boolDyadicExp)
                    ; //TODO: handle multiple dyadic operators
//boolMonadicExp      : (boolMonadicPrefixOp)? comparisonExp ;
comparisonExp       : (literal (comparisonInfixOp series))
                    | ((series comparisonInfixOp) literal)
                    | impliedComparisonExp
                    | atomMonadicExp
                    //|  ('(' boolExp ')') ;
                    ;
impliedComparisonExp: singleInstLiteral #singleInstanceImpliedExp
                    | listElementLiteral #listElementImpliedExp
                    | specialLiteral #specialLiteralImpliedExp
                    | field #fieldImpliedExp
                    ;

atomMonadicExp      : boolMonadicPrefixOp? (impliedComparisonExp | ('(' boolExp ')'))  ;

series              : field | seriesFunc ;
seriesFunc          : epochSchemeIndex; // Any function which outputs a series
commandFunc         : literalReplaceFunc | reloadDesc ;
//field               : FIELD ;
field               : 'description' | 'project' | 'tags' | 'id' | 'start' | 'end' | 'duration' | 'epoch'
                    | 'mood' | 'circad' | 'metaproject' | 'bodyparts'
                    | 'Location' | 'Person' | 'Food' | 'Media' | 'Audiobook' | 'Podcast' | 'TVShow' | 'Movie' ;
literal             : singleInstLiteral | listElementLiteral | specialLiteral ;
singleInstLiteral   : projectLiteral | epochLiteral | datetimeLiteral | timedeltaLiteral | metaprojectLiteral
                    | moodLiteral
                    ;
listElementLiteral  : tagLiteral
                    ;
specialLiteral      : descToken #string
                    | INT #intPrimitive
                    | FLOAT #floatPrimitive
                    ;

// Functions
literalReplaceFunc  : old=literal '.replace' '(' new=literal ')' ;
epochSchemeIndex    : 'EpochScheme.' scheme=NAME ('[' key=series ']')? ;
reloadDesc          : 'reloadDescription()' ;

// Literals
projectLiteral      : 'Project.' NAME ;
metaprojectLiteral  : ('Metaproject.' | 'Meta.' | 'MP.') NAME ;
tagLiteral          : 'Tag.' NAME ;
epochLiteral        : 'Epoch.' NAME ;
descToken           : STRING_LITERAL ;
moodLiteral         : 'Mood.' (nameKey=NAME | intKey=INT) ;
datetimeLiteral     : 'datetime(' year=INT (',' moreArgs=INT)* ')';
timedeltaLiteral    : 'timedelta(' (('weeks='weeks=INT) | ('days='days=INT) | ('hours='hours=INT) |
                    ('minutes='minutes=INT))
                    (',' 'weeks='weeks=INT)? (',' 'days='days=INT)? (',' 'hours='hours=INT)?
                    (',' 'minutes='minutes=INT)? ','? ')';

//argument            : literal | field ;

/*
 * Lexer Rules
 */
fragment LOWERCASE  : [a-z] ;
fragment UPPERCASE  : [A-Z] ;
fragment DIACRITICS : '\u00c0' .. '\u017e' ;
fragment DIGITS     : [0-9] ;
fragment NAMESTART  : LOWERCASE | UPPERCASE | '_' | DIACRITICS;
BLOCK_COMMENT       : '"""' .*? '"""' NEWLINE -> skip;
STRING_LITERAL      : STRING_LITERAL_DQ | STRING_LITERAL_SQ;
STRING_LITERAL_DQ   : '"' (~('"' | '\r' | '\n') | '\\' ('"'))* '"';
STRING_LITERAL_SQ   : '\'' (~('\'' | '\r' | '\n') | '\\' ('\''))* '\'';
INLINE_COMMENT      : '#' ~[\r\n]* NEWLINE -> skip;
//FIELD               : ('description' | 'project' | 'tags' | 'id' | 'start' | 'end' | 'duration' | 'epoch'
//                    | 'mood' | 'circad' | 'metaproject' | 'bodyparts'
//                    | 'Location' | 'Person' | 'Food' | 'Media' | 'Audiobook' | 'Podcast' | 'TVShow' | 'Movie') {_input.LA(-1) != '.'}?;
INT                 : DIGITS+ ;
FLOAT               : DIGITS+ '.' DIGITS* ;
NAME                : NAMESTART (LOWERCASE | UPPERCASE | DIACRITICS | '_' | DIGITS)* ;
WHITESPACE          : (' ' | '\t')+ -> skip;
NEWLINE             : ('\r'? '\n' | '\r')+ -> skip;
ANY                 : . ;
