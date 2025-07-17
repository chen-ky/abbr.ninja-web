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
import bottle
from bottle import Bottle, run, static_file, response, template, request
from cheroot.wsgi import Server
import requests

TEMPLATE_PATH = "./templates/"
NO_REDIR_USER_AGENT = ["Gecko", "WebKit", "Blink",
                       "Trident", "Chromium", "KHTML", "Chrome"]
AUTO_REDIR_USER_AGENT = ["curl", "wget"]
API_BASE_URL = "http://localhost:8081/api/v1"
app = Bottle()


@app.route("/r/<id>", method="GET")
def redirect(id):
    endpoint = f"{API_BASE_URL}/retrieve?id="
    endpoint += id
    resp = requests.get(endpoint)
    resp_json = resp.json()

    result = response
    if resp.status_code == 200:
        encoded_uri = resp_json["encoded_uri"]
        safe_uri = resp_json["html_safe_uri"]
        result.set_header("location", encoded_uri)
        if is_no_redir_agent(request.headers.get("User-Agent")):
            result.status = 200
            redirect_page(result, encoded_uri, safe_uri)
        else:
            result.status = 303
    elif resp.status_code == 400:
        error_page(result, 400, "Bad Request", resp_json["msg"])
    else:
        error_page(result, 404, "Not Found",
                   "The requested link cannot be found.")
    return result


@app.route("/", method="GET")
def index():
    return template("templates/index.tpl")


@app.route("/<path:path>", method="GET")
def resources(path):
    return static_file(path, root="static")


def is_no_redir_agent(user_agent):
    for no_redir_ua in NO_REDIR_USER_AGENT:
        if no_redir_ua.lower() in user_agent.lower():
            return True
    return False


def is_auto_redirect_agent(user_agent):
    for redir_ua in AUTO_REDIR_USER_AGENT:
        if redir_ua.lower() in user_agent.lower():
            return True
    return False


def redirect_page(resp, encoded_uri, html_safe_uri):
    resp.body = template("templates/redirect.tpl", encoded_uri=encoded_uri,
                         html_safe_uri=html_safe_uri)
    return resp


def error_page(resp, error_code, error_txt, error_msg):
    resp.status = error_code
    resp.body = template("templates/errors.tpl", error_code=error_code,
                         error_txt=error_txt, error_msg=error_msg)
    return resp


if "__main__" == __name__:
    required_env = []
    for env in required_env:
        assert env in os.environ, f"\'{env}\' environment variable not set."

    host = "localhost"
    port = 8080

    if "API_BASE_URL" in os.environ:
        API_BASE_URL = os.getenv("API_BASE_URL").strip().strip("/")
    if "HOST" in os.environ:
        host = os.getenv("HOST").strip()
    if "PORT" in os.environ:
        port = int(os.getenv("PORT").strip())

    if not API_BASE_URL.startswith("http://") \
            and not API_BASE_URL.startswith("https://"):
        API_BASE_URL = "https://" + API_BASE_URL

    server = Server((host, port), app, server_name="abbr.ninja-web/0.2.0")
    print(f"Listening on {host}:{port}")
    print(f"API server: {API_BASE_URL}")
    try:
        server.safe_start()
    except KeyboardInterrupt:
        server.stop()
