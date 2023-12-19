import trio  # async library that selenium uses
from selenium import webdriver
from selenium.webdriver.common.devtools.v120.network import ResponseReceived


async def start_listening(listener):
    async for event in listener:
        print("=" * 20)
        print(type(event), event)


async def main():
    driver = webdriver.Chrome()
    driver.bidi_connection

    async with driver.bidi_connection() as connection:
        print(connection)
        print(dir(connection))

        session, devtools = connection.session, connection.devtools

        # await session.execute(devtools.fetch.enable())
        await session.execute(devtools.network.enable())

        # listener = session.listen(devtools.fetch.RequestPaused)
        listener = session.listen(devtools.network.ResponseReceived)
        async with trio.open_nursery() as nursery:
            nursery.start_soon(start_listening, listener)  # start_listening blocks, so we run it in another coroutine

            driver.get("https://google.com")


trio.run(main)
