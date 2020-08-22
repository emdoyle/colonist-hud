import asyncio

from django.core.management import BaseCommand

from ingestion.ingest import WebsocketIngest


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tasks = []

    def add_arguments(self, parser):
        parser.add_argument(
            "concurrency",
            nargs="?",
            default="1",
            help="How many Tasks to run concurrently",
        )

    async def ws_ingest(self):
        await WebsocketIngest().open(
            target="wss://colonist.io/", http_target="https://colonist.io/"
        )

    async def _handle(self, *args, **options):
        concurrency = int(options.get("concurrency", 1))
        for _ in range(concurrency):
            self.tasks.append(asyncio.create_task(self.ws_ingest()))

        for task in self.tasks:
            await task

    def handle(self, *args, **options):
        try:
            asyncio.run(self._handle(*args, **options))
        except KeyboardInterrupt:
            # this doesn't actually work, might be something with threads in websocket-client library
            print("Caught KeyboardInterrupt. Exiting!")
