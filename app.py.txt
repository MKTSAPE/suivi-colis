from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

API_KEY = 'CB9AF5E9849A76AD6B7177F53800F813'
BASE_URL = 'https://api.17track.net/track/v2'

def register_tracking(tracking_number):
    url = f"{BASE_URL}/register"
    headers = {
        '17token': API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "data": [{
            "number": tracking_number
        }]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code

def get_tracking_info(tracking_number):
    url = f"{BASE_URL}/get"
    headers = {
        '17token': API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "numbers": [tracking_number]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.route('/track', methods=['POST'])
def track_package():
    data = request.get_json()
    tracking_number = data.get('tracking_number')

    register_tracking(tracking_number)
    time.sleep(5)

    response = get_tracking_info(tracking_number)

    try:
        item = response['data'][0]
        info = item.get('origin_info', {}).get('trackinfo', []) or item.get('destination_info', {}).get('trackinfo', [])
        last_update = info[-1]['date'] if info else "—"
        location = info[-1].get('location', "—") if info else "—"
        status = item.get('status', 'Inconnu')

        return jsonify({
            "status": status,
            "last_update": last_update,
            "location": location
        })

    except Exception as e:
        return jsonify({
            "status": "Erreur interne",
            "last_update": "—",
            "location": "—",
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
