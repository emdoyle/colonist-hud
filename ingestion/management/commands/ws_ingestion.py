import asyncio

from django.core.management import BaseCommand

from ingestion.ingest import WebsocketIngest


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "concurrency",
            nargs="?",
            default="1",
            help="How many Tasks to run concurrently",
        )

    async def ws_ingest(self):
        WebsocketIngest().open(
            target="wss://colonist.io/", http_target="https://colonist.io/"
        )

    async def _handle(self, *args, **options):
        concurrency = int(options.get("concurrency", 1))
        tasks = []
        for _ in range(concurrency):
            tasks.append(asyncio.create_task(self.ws_ingest()))

        for task in tasks:
            await task

    def handle(self, *args, **options):
        asyncio.run(self._handle(*args, **options))
