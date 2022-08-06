import json
import logging
import os

import datetime
from google.cloud import bigquery
from google.cloud import pubsub_v1
from jinja2 import Template
from concurrent import futures

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

PROJECT_ID = os.getenv('PROJECT_ID')
TOPIC_NAME = os.getenv('TOPIC_NAME')

client = bigquery.Client()

topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=PROJECT_ID,
    topic=TOPIC_NAME,
)
batch_settings = pubsub_v1.types.BatchSettings(
    max_bytes=2048000,  # One kilobyte
    max_latency=5,  # One second
)

publisher_options = pubsub_v1.types.PublisherOptions(
    flow_control=pubsub_v1.types.PublishFlowControl(
        message_limit=500,
        byte_limit=2 * 1024 * 1024,
        limit_exceeded_behavior=pubsub_v1.types.LimitExceededBehavior.BLOCK,
    ),
)
publisher = pubsub_v1.PublisherClient(batch_settings=batch_settings, publisher_options=publisher_options)

published_futures = []
fields = [
    "dma_name",
    "dma_id",
    "term",
    "week",
    "score",
    "rank",
    "refresh_date"
]
jinja_data = {
    "fields": fields
}
query = """
    SELECT
      {%- for f in fields %}
         {{ f -}}{% if not loop.last %},{% endif %}
      {%  endfor -%}
    FROM `bigquery-public-data.google_trends.top_terms`
    WHERE refresh_date > DATE_SUB(CURRENT_DATE(), INTERVAL 10 DAY) 
    ORDER BY refresh_date DESC
    LIMIT 1000"""

j2_query_template = Template(query)
rendered_query = j2_query_template.render(jinja_data)
query_job = client.query(query=rendered_query)

results = query_job.result()
for r in results:
    message = {f: r[f] if type(r[f]) != datetime.date else r[f].isoformat() for f in fields}
    future = publisher.publish(topic_name, json.dumps(message).encode('utf-8'))
    published_futures.append(future)

futures.wait(published_futures, return_when=futures.ALL_COMPLETED)

logging.info(f"Published messages with batch settings to {topic_name}.")
