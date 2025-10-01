#!/usr/bin/env python3
import threading
import time
import random
import json
import requests
import sqlite3

DEFAULT_API_BASE = "http://localhost:5007/api"
DASHBOARD_URL = "http://localhost:5008"

RFIDS = [
    "ECAAAAAAAAAAAAAAAAAAAAAAMOTTU20293",
    "EC04ABC10000",
    "string",
    "E200001161072C05",
    "A1B2C3D4E5F6G7H8"
]

BASE_POS = [
    (-23.561414, -46.655881),
    (-23.562000, -46.656500),
    (-23.560800, -46.656200)
]

def now_ms():
    return int(time.time() * 1000)

def post_api(url, payload):
    try:
        r = requests.post(url, json=payload, timeout=6)
        return r.ok, r.status_code, r.text
    except:
        return False, 0, "Error"

def post_dashboard(payload):
    try:
        requests.post(f"{DASHBOARD_URL}/new_reading", json=payload, timeout=2)
    except:
        pass

class Device(threading.Thread):
    def __init__(self, moto_id, rfid, base_pos, api_base, db_conn, interval=3, max_reads=None):
        super().__init__(daemon=True)
        self.moto_id = moto_id
        self.rfid = rfid
        self.base_pos = base_pos
        self.api_base = api_base
        self.db_conn = db_conn
        self.interval = interval
        self.max_reads = max_reads
        self.running = True
        self.count = 0

    def rand_gps(self):
        lat = self.base_pos[0] + random.uniform(-0.0006, 0.0006)
        lon = self.base_pos[1] + random.uniform(-0.0006, 0.0006)
        return {"latitude": round(lat,6), "longitude": round(lon,6)}

    def rand_mov(self):
        moving = random.random() < 0.4
        intensity = random.randint(1,10) if moving else 0
        return {"moving": moving, "intensity": intensity}

    def persist_local(self, sensor, payload):
        try:
            with self.db_conn:
                self.db_conn.execute(
                    "INSERT INTO telemetria (moto_id, sensor, value, timestamp) VALUES (?, ?, ?, ?)",
                    (self.moto_id, sensor, json.dumps(payload), now_ms())
                )
        except:
            pass

    def send(self, sensor, value):
        payload = {"moto_id": self.moto_id, "sensor": sensor, "value": value, "timestamp": now_ms(), "ok": True}
        if sensor=="rfid":
            url = f"{self.api_base}/RFID"
            api_payload = {"rfid": self.rfid, "sensorId": 17, "potenciaSinal": -30}
        elif sensor=="gps":
            url = f"{self.api_base}/GPS"
            api_payload = {"motoId": self.moto_id, **value}
        elif sensor=="movimento":
            url = f"{self.api_base}/Movimento"
            api_payload = {"motoId": self.moto_id, **value}
        else:
            payload["ok"] = False
            self.persist_local(sensor, payload)
            post_dashboard(payload)
            return

        ok, status, _ = post_api(url, api_payload)
        payload["ok"] = ok
        self.persist_local(sensor, payload)
        post_dashboard(payload)

    def run_cycle(self):
        self.send("rfid", {"dummy": True})
        time.sleep(0.2)
        self.send("gps", self.rand_gps())
        time.sleep(0.2)
        self.send("movimento", self.rand_mov())

    def run(self):
        while self.running:
            self.run_cycle()
            self.count += 1
            if self.max_reads and self.count >= self.max_reads:
                break
            time.sleep(self.interval)
