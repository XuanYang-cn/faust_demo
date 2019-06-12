import faust
import random

app = faust.App(
    'leader-example',
    broker='kafka://localhost:9092',
    value_serializer='raw',
)


@app.agent()
async def say(greetings):
    async for greeting in greetings:
        print(greeting)


# The timer will periodically send out a random greeting,
# to be printed by one of the workers in the cluster.
@app.timer(2.0, on_leader=True)
async def publish_greetings():
    print('PUBLISHING ON LEADER!')
    greeting = str(random.random())
    await  say.send(value=greeting)
