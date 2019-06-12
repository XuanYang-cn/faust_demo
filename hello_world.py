import faust

app = faust.App(
    # ID of the application, should be unique per Faust app in Kafka cluster
    # Needed for internal bookkeeping and to distribute work
    # among worker instances
    'hello-world',
    broker='kafka://localhost:9092',  # Kafka broker

    # By default Faust will use JSON serialization
    # Here specify value_serializer as raw to avoid
    # de_serializing incoming greetings. For real
    # applications you should define models , link
    # https://faust.readthedocs.io/en/latest/userguide/models.html#guide-models
    value_serializer='raw',
)

# Define a Kafka topic `greetings`
greetings_topic = app.topic('greetings')


# Agent to process streams
@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)


# Before running app, need to start Zookeeper and Kafka
# $ $KAFKA_HOME/bin/zookeeper-server-start $KAFKA_HOME/etc/kafka/zookeeper.properties
# $ $KAFKA_HOME/bin/kafka-server-start $KAFKA_HOME/etc/kafka/server.properties

# Running the Faust worker
# $ faust -A hello_world worker -l info
# $ faust worker --help

# Using @ prefix to send message to the greet agent
# $ faust -A hello_world send @greet "Hello Faust"  OR
# Using topic name greeting
# $ faust -A hello_world send greeting "Hello Faust"

