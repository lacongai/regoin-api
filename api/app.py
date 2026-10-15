from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_player_info(Id):
    url = "https://topup.pk/api/auth/player_id_login"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-MM,en-US;q=0.9,en;q=0.8",
        "Content-Type": "application/json",
        "Origin": "https://topup.pk",
        "Referer": "https://topup.pk/",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; RMX5070 Build/UKQ1.231108.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.157 Mobile Safari/537.36",
        "X-Requested-With": "mark.via.gp",
        "Cookie": "source=mb; region=PK; language=en; mspid2=6c3935d39acd5e1f97e1175e3c2eec91; _ga=GA1.1.430001058.1792081040; _fbp=fb.1.1792081040119.481417693715687666; _ga_6F84K2JN88=GS2.1.s1792081039$o1$g1$t1792081044$j55$l0$h0; datadome=RPyZpnJMfRQWHnDlFNBongOkbb4om6dkQGT3rMDUlNi9WdPs1GLLCvEpH6XVsGRc81RXPsNfvi~K1ki~CYqGhZzwWVM0Nm6Wq6xjwXz4kyeST3n_VLc7RAlzL84odxlv; session_key=r7a6jo93g7e0xcgbmqhbb6h7938go1bv",
    }

    payload = {
        "app_id": 100067,
        "login_id": f"{Id}",
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh} - Response: {errh.response.text if errh.response is not None else 'No response body'}")
        return errh.response if errh.response is not None else requests.Response()
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return requests.Response()
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return requests.Response()
    except requests.exceptions.RequestException as err:
        print(f"An unexpected request error occurred: {err}")
        return requests.Response()

# Route test để xem API có online chưa
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API Online"}), 200

# Route gốc đã có: lấy nickname + region
@app.route("/region", methods=["GET"])
def region():
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"message": "Please provide a UID"}), 200
    
    response = get_player_info(uid)
    try:
        if response.status_code == 200:
            original_response = response.json()
            if not original_response.get("nickname") and not original_response.get("region"):
                return jsonify({"message": "UID not found, please check the UID"}), 200
            
            return jsonify({
                "uid": uid,
                "nickname": original_response.get("nickname", ""),
                "region": original_response.get("region", "")
            })
        else:
            return jsonify({"message": "UID not found, please check the UID"}), 200
    except Exception:
        return jsonify({"message": "Error"}), 200

# Route mới: trả về raw JSON từ shop2game
@app.route("/check", methods=["GET"])
def check():
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"message": "Please provide a UID"}), 200
    
    response = get_player_info(uid)
    try:
        return jsonify(response.json()), response.status_code
    except Exception:
        return jsonify({"message": "Error parsing response"}), 200
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)