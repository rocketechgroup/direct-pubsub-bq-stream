# direct-pubsub-bq-stream

Example repo to use the BigQuery subscription of PubSub to directly stream data into BigQuery.

This example uses the `bigquery-public-data.google_trends.top_terms` public dataset.

## Example by making use of Topic Schema

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

### Create Dataset & Table

> Create Dataset

```
bq --location=EU mk -d \
    --description "Dataset to test out BigQuery pubsub subscription" \
    direct_pubsub_to_bq
```

> Create table

```
TODO
```

### Create subscription

```
gcloud pubsub subscriptions create publicdata_google_trends_top_terms_has_topic_schema1 \
  --topic=publicdata_google_trends_top_terms \
  --bigquery-table=<your project id>:direct_pubsub_to_bq.google_trends_top_terms_has_topic_schema \
  --drop-unknown-fields --use-topic-schema --write-metadata 
```

## Example without topic schema

### Create Topic

```
gcloud pubsub topics create publicdata_google_trends_top_terms_no_schema
```

When not using schema, BigQuery can also now support the JSON datatype, so you can create a BigQuery table with a
generic schema for any messages such as

> Create Dataset

```
bq --location=EU mk -d \
    --description "Dataset to test out BigQuery pubsub subscription" \
    direct_pubsub_to_bq
```

> Create table

```
bq mk \
  --table \
  --expiration 86400 \
  --description "Table with data streammed from pubsub directly with semi-structured data in the data column represented using the JSON dataset" \
  direct_pubsub_to_bq.google_trends_top_terms_no_topic_schema \
  ./bigquery_schemas/generic_with_json_type.json
```

#### Create subscription

```
gcloud pubsub subscriptions create publicdata_google_trends_top_terms_no_schema \
  --topic=publicdata_google_trends_top_terms_no_schema \
  --bigquery-table=<your project id>:direct_pubsub_to_bq.google_trends_top_terms_no_topic_schema \
  --drop-unknown-fields --use-topic-schema --write-metadata 
``` 

## Produce messages

```
pip install -r requirements.txt

export PROJECT_ID=<your gcp project id>
export TOPIC_NAME=<your pubsub topic name>
python main.py
```
