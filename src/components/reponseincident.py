from flask import Flask, jsonify
import json
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

def load_logs():
    # Load data from a JSON file
    with open('log.json', 'r') as file:
        logs = json.load(file)
    return logs

def preprocess_data(logs):
    # Convert the loaded JSON logs into a DataFrame
    df = pd.DataFrame(logs)

    # Extract resource usage as integer values, handle NaN and format issues
    df['cpu_usage'] = df['resource_usage'].apply(
        lambda x: int(x['cpu'].replace('%', '')) if 'cpu' in x and x['cpu'].replace('%', '').isdigit() else 0)
    df['ram_usage'] = df['resource_usage'].apply(
        lambda x: int(x['ram'].replace('%', '')) if 'ram' in x and x['ram'].replace('%', '').isdigit() else 0)
    df['storage_usage'] = df['resource_usage'].apply(
        lambda x: int(x['storage'].replace('%', '')) if 'storage' in x and x['storage'].replace('%', '').isdigit() else 0)

    # Convert 'http_status_code' to integer, handling NaN values by filling with 0
    df['http_status'] = df['http_status_code'].fillna(0).astype(int)

    # Include 'user_id' and 'ip_address'
    return df[['timestamp', 'event_type', 'message', 'user_id', 'ip_address', 'cpu_usage', 'ram_usage', 'storage_usage', 'http_status']]

def analyze_logs(df):
    # Simple analysis to generate recommendations based on log data
    recommendations = []
    for _, row in df.iterrows():
        recommendation = {
            "timestamp": row['timestamp'],
            "event_type": row['event_type'],
            "message": row['message'],
            "user_id": row['user_id'],
            "ip_address": row['ip_address']
        }
        if row['event_type'] == 'error' and row['http_status'] == 401:
            recommendation["recommendation"] = "Verify user credentials and security policies."
            recommendations.append(recommendation)
        elif row['event_type'] == 'warning' and row['cpu_usage'] > 80:
            recommendation["recommendation"] = "Consider upgrading CPU resources or optimizing system performance."
            recommendations.append(recommendation)

    return recommendations

@app.route('/classification-report', methods=['GET'])
def classification_report():
    logs = load_logs()
    data = preprocess_data(logs)
    recommendations = analyze_logs(data)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
