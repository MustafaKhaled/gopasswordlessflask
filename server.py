import os
import base64
import json
from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/hello")
def hello2():
    return "This is a test"

@app.route("/register/begin/", methods=["POST"])
def register_begin():
    try:
        username = request.json.get('username')
        if not username:
            return jsonify({'error': 'Username is required'}), 400

        user_id = base64.urlsafe_b64encode(os.urandom(16)).decode("utf-8")

        # Generate a challenge
        challenge = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")
        session["challenge"] = challenge

        response = {
              "challenge": challenge,
              "rp": {
                  "id": "passkeys-codelab.glitch.me",
                  "name": "CredMan App Test"
              },
              "pubKeyCredParams": [
                  {
                      "type": "public-key",
                      "alg": -7
                  },
                  {
                      "type": "public-key",
                      "alg": -257
                  }
              ],
              "authenticatorSelection": {
                  "authenticatorAttachment": "platform",
                  "residentKey": "required"
              },
              "user": {
                     "id": user_id,
                     "name": "<userName>",
                     "displayName": "<userDisplayName>"
                 }
          }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
