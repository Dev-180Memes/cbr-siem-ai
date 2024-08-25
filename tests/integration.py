import requests
import json

BASE_URL = "http://203.0.113.0:8080"

def test_add_case():
    url = f"{BASE_URL}/api/add_case"
    payload = {
        "description": "Test case",
        "solution": "Test solution",
        "indicators": ["test.com", "test.exe"]
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    print("Add case test passed")

def test_ingest_log():
    url = f"{BASE_URL}/api/ingest_log"
    payload = {
        "timestamp": "2023-04-21T10:00:00Z",
        "log_type": "test",
        "source_ip": "1.1.1.1",
        "destination_ip": "2.2.2.2",
        "event": "Test event"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    print("Ingest log test passed")

def test_analyze():
    url = f"{BASE_URL}/api/analyze"
    payload = {
        "query": "SELECT * FROM `cbr-siem-ai.siem_logs.security_logs` LIMIT 10"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    result = json.loads(response.text)
    assert 'anomalies' in result
    assert 'topics' in result
    print("Analyze test passed")

if __name__ == "__main__":
    test_add_case()
    test_ingest_log()
    test_analyze()