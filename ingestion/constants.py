from enum import Enum


class SendingOpcode(Enum):
    INIT_ONE = 1
    INIT_TWO = 4
    PLAY_VS_BOTS = 7
    JOIN_GAME = 11
    OPEN_TRADE_WINDOW = 32


class Opcode(Enum):
    UNKNOWN = -1
    INIT_ZERO = 0  # website sends false before game multiple times
    INIT_ONE = 1
    TEXT = 4
    GAME_TEXT = 5
    PLAY_ORDER = 7
    TURN_STATE_CHANGE = 8
    BANK_STATE_CHANGE = 9
    HEX_STATE_CHANGE = 10
    DICE_STATE_CHANGE = 11
    PLAYER_INFO = 12
    DISCARD_ROBBER = 13
    RESOURCE_RECEIVED = 14
    PLAYERS_TO_ROB = 15
    ROBBED = 16
    RESOURCE_BOUGHT = 17  # specifically from the bank
    OPEN_HEXES = 18
    OPEN_EDGES = 19
    OPEN_HEXES_ROBBER = 20
    TRADE_RATIOS = 21
    OFFER_MADE = 22  # also used for counteroffers
    PLACEMENT_TWO = 23  # is this a SendingOpcode?
    OFFER_FINAL_REJECTION = 24
    PLACEMENT_ONE = 25  # is this a SendingOpcode?
    OFFER_REJECTED = 26  # uncertain
    OFFER_ACCEPTED = 27
    RESOURCE_PAID = 32
    TRADE_COMPLETED = 33
    DISCARDED_CARDS = 34
    PLAYER_GAME_COUNTS = 35
    AVAILABLE_GAMES = 36
    SINGLE_GAME_LISTING = 38
    COMPOSITE_GAME_LISTINGS = 39
    GAME_SETTINGS = 40
    GAME_OVER_MESSAGE = 45
    # 48 is still unknown but seems to only occur shortly after join


OPCODES_BY_VALUE = {str(opcode.value): opcode for opcode in Opcode}
