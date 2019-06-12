import faust

app = faust.App(
    'myapp',
    broker='kafka://localhost:9092',
)


class Add(faust.Record):
    x: int
    y: int


topic = app.topic('adding', value_type=Add)


@app.agent(topic)
async def adding(stream):
    async for op in stream:
        print(op)
        yield op['x'] + op['y']
