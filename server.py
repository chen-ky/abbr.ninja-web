#!/bin/python3

# Copyright 2021 Chen Kang Yang

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from bottle import Bottle, run, static_file, response
from cheroot.wsgi import Server
import requests

API_BASE_URL = "http://127.0.0.1:8081/api/v1"
app = Bottle()

@app.route("/", method = "GET")
def index():
    return static_file("index.html", "static")

@app.route("/r/<id>", method="GET")
def redirect(id):
    endpoint = f"{API_BASE_URL}/retrieve?id="
    endpoint += id
    resp = requests.get(endpoint)
    resp_json = resp.json()

    result = response
    if resp.status_code == 200:
        result.set_header("location", resp_json["encoded_uri"])
        result.status = 301
        safe_uri = resp_json["html_safe_uri"]
        result.body = f"Redirecting you to {safe_uri} ..."
    elif resp.status_code == 400:
        result.body = resp_json["msg"]
    else:
        result.status = 404
        result.body = "Not Found"
    return result

@app.route("/<path:path>", method = "GET")
def resources(path):
    return static_file(path, root="static")

if "__main__" == __name__:
    required_env = ["API_BASE_URL"]
    for env in required_env:
        assert env in os.environ, f"'{env}' environment variable not set."
    API_BASE_URL = os.getenv("API_BASE_URL").strip().strip("/")
    if not API_BASE_URL.startswith("http://") \
    and not API_BASE_URL.startswith("https://"):
        API_BASE_URL = "http://" + API_BASE_URL

    host = "localhost"
    port = 8080

    if "HOST" in os.environ:
        host = os.getenv("HOST")
    if "PORT" in os.environ:
        port = int(os.getenv("PORT"))

    server = Server((host, port), app, server_name="abbr.ninja-web/0.1.0")    
    print(f"Listening on {host}:{port}")
    print(f"API server: {API_BASE_URL}")
    try:
        server.safe_start()
    except KeyboardInterrupt:
        server.stop()