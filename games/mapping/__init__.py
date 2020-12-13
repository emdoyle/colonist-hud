from ingestion.constants import Opcode
from .player import *
from .resources import *
from .board import *


MESSAGE_OPCODE_DESERIALIZERS = {
    Opcode.RESOURCE_RECEIVED.value: deserialize_resource_received,
    Opcode.ROBBED.value: deserialize_robbed,
    Opcode.RESOURCE_BOUGHT.value: deserialize_resource_bought,
    Opcode.TRADE_COMPLETED.value: deserialize_trade_completed,
    Opcode.HEX_STATE_CHANGE.value: deserialize_game_board,
    Opcode.PLAYER_INFO.value: deserialize_player_data,
}
