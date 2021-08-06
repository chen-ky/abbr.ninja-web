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

from bottle import Bottle, run, static_file, response
import requests

API_BASE_URL = "http://127.0.0.1:8081/api/v1"
app = Bottle()

@app.route("/", method = "GET")
def index():
    return static_file("index.html", ".")

@app.route("/favicon.ico", method = "GET")
def get_favicon():
    response.status = 404
    return None

@app.route("/robots.txt", method = "GET")
def get_robots():
    return static_file("robots.txt", ".")

@app.route("/static/<path:path>", method = "GET")
def resources(path):
    return static_file(path, root="static")

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

if "__main__" == __name__:
    run(app, host="0.0.0.0", port=8080, server='paste')
