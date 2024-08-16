import inspect

def get_members(class_ : object) -> tuple[list[str], list[str]]:
    """
    Get members of a given class
    
    Take a class type or an object as an input
    
    Returns a tuple : (member_name, member_value)
    you can use it like this:
    names, values = get_members(T)
    if X in values:
        #do stuff
    """
    m_name = []
    m_value = []
    for member in inspect.getmembers(class_):
        if not member[0].startswith('_'):
            if not inspect.ismethod(member[1]):
                m_name.append(member[0])
                m_value.append(member[1])
    return m_name, m_value

COMMAND         = 0
SUB_COMMAND     = 1
SELECTOR        = 2
STRING          = 3
COMMENT         = 4
COMMENT_TITLE   = 5
ATTRIBUTE       = 6
NAMESPACE       = 7
RESOURCE        = 8
BRACKETS        = 9
DEFAULT         = 10
VALUES          = 11
KEYWORDS        = 12


class Commands:
    """
    List of minecraft commands
    """
    ADVANCEMENT     = "advancement"
    ATTRIBUTE       = "attribute"
    BOSSBAR         = "bossbar"
    CLEAR           = "clear"
    CLONE           = "clone"
    DAMAGE          = "damage"
    DATA            = "data"
    DATAPACK        = "datapack"
    DEFAULTGAMEMODE = "defaultgamemode"
    DIFFICULTY      = "difficulty"
    EFFECT          = "effect"
    ENCHANT         = "enchant"
    EXECUTE         = "execute"
    EXPERIENCE      = "experience"
    FILL            = "fill"
    FILLBIOME       = "fillbiome"
    FORCELOAD       = "forceload"
    FUNCTION        = "function"
    GAMEMODE        = "gamemode"
    GAMERULE        = "gamerule"
    GIVE            = "give"
    HELP            = "help"
    ITEM            = "item"
    KILL            = "kill"
    LIST            = "list"
    LOCATE          = "locate"
    LOOT            = "loot"
    ME              = "me"
    MSG             = "msg"
    PARTICLE        = "particle"
    PLACE           = "place"
    PLAYSOUND       = "playsound"
    RANDOM          = "random"
    RECIPE          = "recipe"
    RELOAD          = "reload"
    RETURN          = "return"
    RIDE            = "ride"
    SAY             = "say"
    SCHEDULE        = "schedule"
    SCOREBOARD      = "scoreboard"
    SEED            = "seed"
    SETBLOCK        = "setblock"
    SETWORLDSPAWN   = "setworldspawn"
    SPAWNPOINT      = "spawnpoint"
    SPECTATE        = "spectate"
    SPREADPLAYERS   = "spreadplayers"
    STOPSOUND       = "stopsound"
    SUMMON          = "summon"
    TAG             = "tag"
    TEAM            = "team"
    TEAMMSG         = "teammsg"
    TELEPORT        = "teleport"
    TELL            = "tell"
    TELLRAW         = "tellraw"
    TIME            = "time"
    TITLE           = "title"
    TM              = "tm"
    TP              = "tp"
    TRIGGER         = "trigger"
    W               = "w"
    WEATHER         = "weather"
    WORLDBORDER     = "worldborder"
    XP              = "xp"

class Selectors:
    """
    List of Minecraft target selectors
    """
    NEAREST_PLAYER      = "@p"
    RANDOM_PLAYER       = "@r"
    ALL_PLAYERS         = "@a"
    ALL_ENTITIES        = "@e"
    EXECUTING_ENTITY    = "@s"
    NEAREST_ENTITY      = "@n"

class SubCommands:
    """
    Sub-commands for /execute command
    """
    ALIGN       = "align"
    ANCHORED    = "anchored"
    AS          = "as"
    AT          = "at"
    FACING      = "facing"
    IF          = "if"
    IN          = "in"
    ON          = "on"
    POSITIONED  = "positioned"
    ROTATED     = "rotated"
    RUN         = "run"
    STORE       = "store"
    SUMMON      = "summon"
    UNLESS      = "unless"

class Brackets:
    LPAR        = '('
    RPAR        = ')'
    LCURLY_BR   = '{'
    RCURLY_BR   = '}'
    LSQR_BR     = '['
    RSQR_BR     = ']'

class OpeningBrackets:
    LCURLY_BR   = '{'
    LSQR_BR     = '['
    
class ClosingBrackets:
    RCURLY_BR   = '}'
    RSQR_BR     = ']'
    

class Operators:
    TILDE = '~'
    CARET = '^'
    COLON = ':'
    EQUAL = '='
    EXCLA = '!'
    DOT   = '.'
    SLASH = '/'
    PLUS  = '+'
    MINUS = '-'
    TIMES = '*'
    COMMA = ','

class Keywords:
    ADVANCEMENT = "advancement"
    DISTANCE    = "distance"
    DX          = "dx"
    DY          = "dy"
    DZ          = "dz"
    GAMEMODE    = "gamemode"
    LEVEL       = "level"
    LIMIT       = "limit"
    NAME        = "name"
    NBT         = "nbt"
    PREDICATE   = "predicate"
    SCORES      = "scores"
    SORT        = "sort"
    TAG         = "tag"
    TEAM        = "team"
    X           = "x"
    X_ROTATION  = "x_rotation"
    Y           = "y"
    Y_ROTATION  = "y_rotation"
    Z           = "z"

KEY_COMMANDS, T_COMMANDS = get_members(Commands)
KEY_SELECTORS, T_SELECTORS = get_members(Selectors)
KEY_SUBCOMMANDS, T_SUBCOMMANDS = get_members(SubCommands)
KEY_BRACKETS, T_BRACKETS = get_members(Brackets)
KEY_OPERATORS, T_OPERATORS = get_members(Operators)
KEY_KEYWORDS, T_KEYWORDS = get_members(Keywords)
KEY_OPENING_BRACKETS, T_OPENING_BRACKETS = get_members(OpeningBrackets)
KEY_CLOSING_BRACKETS, T_CLOSING_BRACKETS = get_members(ClosingBrackets)