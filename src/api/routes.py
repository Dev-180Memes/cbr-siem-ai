from flask import Blueprint, request, jsonify
from cbr.case_manager import CaseManager
from siem.log_manager import LogManager
from ai.anomaly_detector import AnomalyDetector
# from ai.nlp_processor import NLPProcessor
import pandas as pd

api = Blueprint('api', __name__)

# case_manager = CaseManager('cbr-instance', 'cbr-database')
# log_manager = LogManager('cbr-siem-ai', 'siem_logs', 'security_logs', 'siem-logs-topic')
# anomaly_detector = AnomalyDetector()
# nlp_processor = NLPProcessor()


@api.route('/add_case', methods=['POST'])
def add_case():
    data = request.json
    case_manager.add_case(data['description'], data['solution'], data['indicators'])
    return jsonify({'status': 'success'}), 201


@api.route('/ingest_log', methods=['POST'])
def ingest_log():
    log_entry = request.json
    log_manager.ingest_log(log_entry)
    return jsonify({'status': 'ingested'}), 201


@api.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    logs = log_manager.query_logs(data['query'])

    # Convert logs to a pandas DataFrame
    df = pd.DataFrame(logs)

    # Perform anomaly detection
    anomalies = anomaly_detector.detect_anomalies(df)

    # Process text data
    preprocessed_text = [nlp_processor.preprocess_text(doc) for doc in df['event']]
    topics = nlp_processor.extract_topics(df['event'])

    return jsonify({
        'anomalies': anomalies.tolist(),
        'topics': topics.tolist()
    }), 200