from storage.redis import RedisPool


class LifespanApplication:
    def __init__(self, scope):
        self.scope = scope

    async def setup(self) -> None:
        await RedisPool.setup()

    async def __call__(self, receive, send) -> None:
        if self.scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await self.setup()
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return
