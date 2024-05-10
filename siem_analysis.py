from flask import Flask, jsonify, request
from collections import defaultdict
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def parse_logs(log_file):
    log_data = defaultdict(list)

    with open(log_file, 'r') as f:
        logs = json.load(f)

        for log in logs:
            log_data[log["event_type"]].append(log)

    return log_data

def aggregate_logs(log_data):
    aggregated_data = defaultdict(int)
    ip_count = defaultdict(int)
    authentication_methods = defaultdict(int)
    failed_authentication_users = set()

    for event_type, logs in log_data.items():
        aggregated_data[event_type] += len(logs)
        for log in logs:
            ip_count[log.get('ip_address', 'Unknown')] += 1
            if 'request_params' in log:
                authentication_methods[log['request_params'].get('username', 'Unknown')] += 1
            if event_type == 'error' and 'user_id' in log:
                failed_authentication_users.add(log['user_id'])

    return aggregated_data, ip_count, authentication_methods, failed_authentication_users

@app.route('/get_data')
def get_data():
    log_file = "log.json"
    log_data = parse_logs(log_file)
    aggregated_data, ip_count, authentication_methods, failed_authentication_users = aggregate_logs(log_data)
    return jsonify({
        'aggregatedData': aggregated_data,
        'ipCount': ip_count,
        'authenticationMethods': authentication_methods,
        'failedAuthenticationUsers': list(failed_authentication_users)
    })

@app.route('/search_logs', methods=['GET'])
def search_logs():
    log_file = "log.json"
    query = request.args.get('query').lower()
    log_data = parse_logs(log_file)
    results = []

    for event_type, logs in log_data.items():
        for log in logs:
            for key, value in log.items():
                if query in str(value).lower():
                    results.append(log)
                    break  # Pour éviter d'ajouter plusieurs fois le même log

    return jsonify({'results': results})

if __name__ == "__main__":
    app.run(debug=True)
