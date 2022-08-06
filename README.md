# direct-pubsub-bq-stream
Example repo to use the BigQuery subscription of PubSub to directly stream data into BigQuery.

This example uses the `bigquery-public-data.google_trends.top_terms` public dataset.

## Prepare the PubSub Topic & Subscriptions

### Create PubSub Schema

```
gcloud pubsub schemas create publicdata_google_trends_top_terms \
        --type=avro \
        --definition='{"type": "record", "name": "Avro", "fields": [{"name": "dma_name", "type": "string"}, {"name": "dma_id", "type": "int"}, {"name": "term", "type": "string"}, {"name": "week", "type": "string"}, {"name": "score", "type": "int"}, {"name": "rank", "type": "int"}, {"name": "refresh_date", "type": "string"}]}'
```

### Create Topic

```
gcloud pubsub topics create publicdata_google_trends_top_terms --schema publicdata_google_trends_top_terms
```

### Create Subscriptions

> Without Schema

```
gcloud pubsub subscriptions create publicdata_google_trends_top_terms_no_topic_schema \
  --topic=publicdata_google_trends_top_terms \
  --bigquery-table=rocketech-de-pgcp-sandbox:direct_pubsub_to_bq.google_trends_top_terms_no_topic_schema
``` 

> With Schema

```
gcloud pubsub subscriptions create publicdata_google_trends_top_terms_has_topic_schema1 \
  --topic=publicdata_google_trends_top_terms \
  --bigquery-table=rocketech-de-pgcp-sandbox:direct_pubsub_to_bq.google_trends_top_terms_has_topic_schema \
  --drop-unknown-fields \
  --use-topic-schema \
  --write-metadata
``` 

## Produce messages
```
pip install -r requirements.txt

export PROJECT_ID=<your gcp project id>
export TOPIC_NAME=<your pubsub topic name>
python main.py
```
