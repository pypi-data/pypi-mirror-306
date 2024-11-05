import asyncio


async def main():
    async def wait():
        raise ValueError("")

    task = asyncio.create_task(wait())
    await task
    print("11")

asyncio.run(main())