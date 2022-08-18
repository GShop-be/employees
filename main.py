from asyncio import new_event_loop, set_event_loop, AbstractEventLoop, run

from app import Application


async def main() -> None:
    await app.start()


if __name__ == "__main__":
    app = Application()

    loop = new_event_loop()
    set_event_loop(loop)

    loop.set_debug(True)

    loop.run_until_complete(main())

    loop.close()
