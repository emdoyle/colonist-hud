from enum import Enum


class Opcode(Enum):
    UNKNOWN = -1
    INIT_ZERO = 0  # website sends false before game multiple times
    INIT_ONE = 1
    TEXT = 4
    GAME_TEXT = 5
    COMPOSITE_GAME_LISTINGS = 39
    SINGLE_GAME_LISTING = 38
    JOIN_GAME = 11
    PLAYER_INFO = 12
    PLAY_ORDER = 7  # sent this to play vs bots but receive as play order
    SPECTATE_MESSAGE = 4
    TURN_STATE_CHANGE = 8
    BANK_STATE_CHANGE = 9
    HEX_STATE_CHANGE = 10
    DICE_STATE_CHANGE = 11
    GAME_SETTINGS = 40
    GAME_OVER_MESSAGE = 45
    OFFER_MADE = 22  # also used for counteroffers
    OFFER_FINAL_REJECTION = 24
    OFFER_REJECTED = 26  # uncertain
    OFFER_ACCEPTED = 27
    PLAYERS_TO_ROB = 15
    ROBBED = 16
    OPEN_HEXES = 18
    OPEN_EDGES = 19
    OPEN_HEXES_ROBBER = 20
    PLACEMENT_ONE = 25
    PLACEMENT_TWO = 23
    RESOURCE_RECEIVED = 14
    RESOURCE_PAID = 32  # also sent when opening trade window
    RESOURCE_BOUGHT = 17  # specifically from the bank
    TRADE_RATIOS = 21
    TRADE_COMPLETED = 33
    DISCARD_ROBBER = 13
    DISCARDED_CARDS = 34
    AVAILABLE_GAMES = 36
    PLAYER_GAME_COUNTS = 35
    # 48 is still unknown


OPCODES_BY_VALUE = {str(opcode.value): opcode for opcode in Opcode}
