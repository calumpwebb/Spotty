import asyncio
from spotty.worker.worker import Worker


async def main():
    worker = Worker()
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
