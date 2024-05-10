import json

# Charge les logs à partir du fichier log.json
with open('../../log.json', 'r') as file:
    logs = json.load(file)

# Trie les logs par type d'événement
logs_by_type = {}
for log in logs:
    event_type = log["event_type"]
    if event_type not in logs_by_type:
        logs_by_type[event_type] = []
    logs_by_type[event_type].append(log)

# Écrit les logs triés dans un fichier JSON
with open('../data/sorted_logs.json', 'w') as sorted_file:
    json.dump(logs_by_type, sorted_file, indent=4)  # Indentation pour une meilleure lisibilité
