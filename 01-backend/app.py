from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from api.routes import emotion_api

app.register_blueprint(emotion_api, url_prefix='/api/emotion')

@app.route("/")
def home():
    return "AI Model Connected Successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)