from google.cloud import bigquery, pubsub_v1
import json


class LogManager:
    def __init__(self, project_id, dataset_id, table_id, topic_id):
        self.bigquery_client = bigquery.Client()
        self.publisher = pubsub_v1.PublisherClient()
        self.table_ref = self.bigquery_client.dataset(dataset_id).table(table_id)
        self.topic_path = self.publisher.topic_path(project_id, topic_id)

    def ingest_log(self, log_entry):
        # Publish to Pub/Sub
        self.publisher.publish(self.topic_path, json.dumps(log_entry).encode('utf-8'))

        # Insert into BigQuery
        errors = self.bigquery_client.insert_rows_json(self.table_ref, [log_entry])
        if errors:
            raise Exception(f"Error inserting rows: {errors}")

    def query_logs(self, query):
        query_job = self.bigquery_client.query(query)
        return query_job.result()