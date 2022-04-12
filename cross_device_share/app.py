import os
from typing import List

from flask import Flask, jsonify, redirect, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

cache: List[str] = list()
MAX_SIZE = 10

USER = os.environ["USER"]
PASS = generate_password_hash(os.environ["PASS"])


@auth.verify_password
def verify_password(username, password):
    if username == USER and check_password_hash(PASS, password):
        return username


@app.route("/")
@auth.login_required
def index():
    return app.send_static_file("index.html")


@app.route("/get")
@auth.login_required
def get():
    return jsonify(cache)


@app.route("/post_new", methods=["POST"])
@auth.login_required
def post_new():
    global cache
    cache.insert(0, request.form["content"])
    if len(cache) > MAX_SIZE:
        cache = cache[:MAX_SIZE]
    return redirect("/")


def main():
    app.run(port="2156")


if __name__ == "__main__":
    main()
