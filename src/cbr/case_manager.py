from google.cloud import spanner


class CaseManager:
    def __init__(self, instance_id, database_id):
        self.spanner_client = spanner.Client()
        self.instance = self.spanner_client.instance(instance_id)
        self.database = self.instance.database(database_id)

    def add_case(self, description, solution, indicators):
        with self.database.batch() as batch:
            batch.insert(
                table='Cases',
                columns=('CaseId', 'Timestamp', 'Description', 'Solution', 'Indicators'),
                values=[(spanner.COMMIT_TIMESTAMP, description, solution, indicators)]
            )

    def get_similar_cases(self, indicators):
        query = """
        SELECT CaseId, Description, Solution
        FROM Cases
        WHERE ARRAY_LENGTH(ARRAY(
            SELECT x FROM UNNEST(Indicators) AS x
            INTERSECT DISTINCT
            SELECT y FROM UNNEST(@indicators) AS y
        )) > 0
        """
        params = {'indicators': indicators}
        param_types = {'indicators': spanner.param_types.Array(spanner.param_types.STRING)}

        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(query, params=params, param_types=param_types)
            return list(results)