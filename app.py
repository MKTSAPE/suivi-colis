from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

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
        "data": [{
            "number": tracking_number
        }]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.route('/track', methods=['POST'])
def track_package():
    data = request.get_json()
    tracking_number = data.get('tracking_number')
    
    try:
        register_tracking(tracking_number)
        response = get_tracking_info(tracking_number)
        
        info = response['data'][0]
        status = info.get('status', 'Inconnu')
        last_info = info.get('origin_info', {}).get('trackinfo', [])
        if last_info:
            last_update = last_info[-1].get('date', 'Non précisé')
            location = last_info[-1].get('location', 'Inconnu')
        else:
            last_update = 'Non disponible'
            location = 'Inconnu'

        return jsonify({
            'status': status,
            'last_update': last_update,
            'location': location
        })
    
    except Exception as e:
        return jsonify({
            'status': 'Erreur interne',
            'last_update': '—',
            'location': '—'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
