from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_player_info(Id):    
    url = "https://shop2game.com/api/auth/player_id_login"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://shop2game.com",
        "Referer": "https://shop2game.com/app",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    payload = {
        "app_id": 100067,
        "login_id": f"{Id}",
        "app_server_id": 0,
    }
    response = requests.post(url, headers=headers, json=payload)
    return response

# Thêm route gốc để test
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Online"}), 200

@app.route("/region", methods=["GET"])
def region():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"message": "Please provide a UID"}), 200
    
    response = get_player_info(uid)
    
    try:
        if response.status_code == 200:
            original_response = response.json()
            if not original_response.get('nickname') and not original_response.get('region'):
                return jsonify({"message": "UID not found, please check the UID"}), 200
            
            return jsonify({
                "uid": uid,
                "nickname": original_response.get('nickname', ''),
                "region": original_response.get('region', '')
            })
        else:
            return jsonify({"message": "UID not found, please check the UID"}), 200
    except Exception:
        return jsonify({"message": "UID not found, please check the UID"}), 200

# KHÔNG cần app.run() vì Vercel sẽ tự load biến app