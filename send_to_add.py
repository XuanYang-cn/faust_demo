import asyncio
from as_add import Add, adding, app


@app.command()
async def send_value() -> None:
    print(await adding.ask(Add(x=2, y=2)))



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_value())
