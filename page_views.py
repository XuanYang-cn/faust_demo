import faust

app = faust.App(
    'page_views',
    broker='kafka://localhost:9092',

    # The topic_partitions setting defines the maximum number
    # of workers we can distribute the workload to (also sometimes
    # referred as the “sharding factor”).
    topic_partitions=4
)


# Define a model that each page view event
# from the stream deserializes into
class PageView(faust.Record):
    id: str
    user: str


# Define the source topic to read the`page view` events from,
# and we specify that every value in this topic is of the PageView type
page_view_topic = app.topic('page_views', value_type=PageView)


# Define a Table, This is like a Python dictionary,
# but is distributed across the cluster, partitioned by the dictionary key
page_views = app.Table('page_views', default=int)


# Define an agent reading each page view event coming into the stream
@app.agent(page_view_topic)
async def count_page_views(views):

    # Here we use `group_by` to repartition the input stream by the page id.
    # This is so that we maintain counts on each instance sharded by the page id.
    # This way in the case of failure, when we move the processing of
    # some partition to another node, the counts for that partition
    # (hence, those page ids) also move together.
    async for view in views.group_by(PageView.id):
        page_views[view.id] += 1
