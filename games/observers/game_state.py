from games.mapping import deserialize_player_data, Dict
from games.observers.base import MessageObserver


class GameStateWriter(MessageObserver):
    def __repr__(self):
        return f"{type(self).__name__}(id={id(self)}, initialized={self.game_state.initialized})"

    @property
    def should_receive(self) -> bool:
        return not self.game_state.initialized

    async def receive_player_info(self, message: Dict):
        self.game_state.players = deserialize_player_data(message)
        self.game_state.initialized = True
