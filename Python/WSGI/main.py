# coding=utf-8
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import waitress
import asyncio
import threading
import logging
import uuid

import pandas as pd
import numpy as np
import cv2

import redis
import psycopg2
from psycopg2.extras import DictCursor

import sys
import os
import yaml
import argparse

# --------------------- APP 全局配置 ---------------------
app = Flask(
    __name__,
    static_folder="templates",
    static_url_path=""
)
CORS(app=app)

logger = logging.Logger("WSGI")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def get_options():
    '''获取所有的 YAML 文件'''
    args = argparse.ArgumentParser(description="Nanoka 的配置文件")
    args.add_argument("--config", type=str, default="D:\\Code\\Python\\WSGI\\config.yaml", help="输入配置 YAML 文件")
    args.add_argument("--debug", action='store_true', help="DEBUG 模式")
    return args.parse_args()

# --------------------- DATABASE 全局配置 ---------------------
opt = get_options()
data = None
with open(opt.config, mode='r', encoding='utf-8') as f:
    data = yaml.safe_load(f.read())

if data is None:
    raise RuntimeError("读取 YAML 文件失败")

logger.info("读取到文件 Data: {}".format(data))

DB_CONFIG = {
    'host': data['pgsql']['host'],
    'port': data['pgsql']['port'],
    'database': data['pgsql']['db'],
    'user': data['pgsql']['usr'],
    'password': data['pgsql']['pwd']
}

RS_CONFIG = {
    'host': data['redis']['host'],
    'port': data['redis']['port'],
    'db': data['redis']['db'],
    'password': data['redis']['pwd']
}
r = redis.ConnectionPool(**RS_CONFIG)

# --------------------- APP router 全局配置 ---------------------
@app.route("/")
def root():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(
            "SELECT * FROM username WHERE usr = %s AND pwd = %s",
            (username, password)
        )
        user = cursor.fetchone()
        if user:
            token = str(uuid.uuid4())
            return jsonify({
                'username': user['usr'],
                'token': token,
                'message': '登录成功'
            }), 200
        else:
            return jsonify({'error': '用户名或密码错误'}), 401
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    try:
        if opt.debug:
            app.run("0.0.0.0", port=81)
        else:
            waitress.serve( # WSGI 服务器静默启动，并且阻塞该进程
                app=app,
                host="0.0.0.0",
                port=81,
                threads=2
            )
    except Exception as e:
        print(f"启动失败：{e}")