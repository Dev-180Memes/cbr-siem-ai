import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN

class AnomalyDetector:
    def __init__(self):
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.dbscan = DBSCAN(eps=0.5, min_samples=5)

    def detect_anomalies(self, data):
        # Isolation Forest
        if_predictions = self.isolation_forest.fit_predict(data)
        if_anomalies = if_predictions == -1

        # DBSCAN
        dbscan_clusters = self.dbscan.fit_predict(data)
        dbscan_anomalies = dbscan_clusters == -1

        # Combine results (anomaly if detected by either method)
        combined_anomalies = np.logical_or(if_anomalies, dbscan_anomalies)

        return combined_anomalies