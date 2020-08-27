from games.mapping import deserialize_player_data, Dict
from games.observers.base import MessageObserver


class GameStateWriter(MessageObserver):
    async def receive_player_info(self, message: Dict):
        self.game_state.players = deserialize_player_data(message)
        self.game_state.initialized = True
