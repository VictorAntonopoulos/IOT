#!/usr/bin/env python3
# api.py - simula dispositivos enviando RFID, GPS e Movimento para a API e dashboard

import argparse
from devices.leitura import Device, RFIDS, BASE_POS, DEFAULT_API_BASE
import sqlite3
import time

DEFAULT_DB = "telemetria.db"

def init_db(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS telemetria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        moto_id TEXT,
        sensor TEXT,
        value TEXT,
        timestamp INTEGER
    );
    """)
    conn.commit()
    return conn

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    parser.add_argument("--devices", type=int, default=3)
    parser.add_argument("--interval", type=float, default=3.0)
    parser.add_argument("--max-reads", type=int, default=None)
    args = parser.parse_args()

    db_conn = init_db(DEFAULT_DB)

    devices = []
    for i in range(args.devices):
        moto_id = f"moto_{i+1}"
        rfid = RFIDS[i % len(RFIDS)]
        base = BASE_POS[i % len(BASE_POS)]
        d = Device(moto_id, rfid, base, args.api_base, db_conn, interval=args.interval, max_reads=args.max_reads)
        d.start()
        devices.append(d)

    try:
        while any(d.is_alive() for d in devices):
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopping devices...")
        for d in devices:
            d.running = False

if __name__ == "__main__":
    main()
