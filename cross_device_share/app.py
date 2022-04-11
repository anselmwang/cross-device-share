from typing import List

from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

cache: List[str] = list()
MAX_SIZE = 10


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/get")
def get():
    return jsonify(cache)


@app.route("/post_new", methods=["POST"])
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
