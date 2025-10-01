import sqlite3, threading, time, os, json
from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO

DB_PATH = "telemetria.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = "dashboard.html"

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, HTML_FILE)

@app.route("/api/telemetry/recent")
def recent():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM telemetria ORDER BY id DESC LIMIT 20")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"motoId":r["moto_id"], "sensor":r["sensor"], "value":json.loads(r["value"]), "timestamp":r["timestamp"]} for r in reversed(rows)])

def monitor_db():
    last_id = 0
    while True:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM telemetria WHERE id>? ORDER BY id ASC", (last_id,))
        rows = cur.fetchall()
        for r in rows:
            socketio.emit("new_reading", {"motoId":r["moto_id"], "sensor":r["sensor"], "value":json.loads(r["value"]), "timestamp":r["timestamp"]})
            last_id = r["id"]
        conn.close()
        time.sleep(0.5)

threading.Thread(target=monitor_db, daemon=True).start()

if __name__ == "__main__":
    print("Dashboard rodando em http://localhost:5008")
    socketio.run(app, host="0.0.0.0", port=5008)
