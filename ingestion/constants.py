from enum import Enum


class Opcode(Enum):
    UNKNOWN = -1
    INIT_ONE = 1
    INIT_TWO = 4
    COMPOSITE_GAME_LISTINGS = 39
    SINGLE_GAME_LISTING = 38
    JOIN_GAME = 11
    INITIAL_PLAYER_INFO = 12
    PLAY_ORDER = 7
    SPECTATE_MESSAGE = 4
    TURN_STATE_CHANGE = 8
    BANK_STATE_CHANGE = 9
    HEX_STATE_CHANGE = 10
    DICE_STATE_CHANGE = 11
    GAME_SETTINGS = 40


OPCODES_BY_VALUE = {str(opcode.value): opcode for opcode in Opcode}
