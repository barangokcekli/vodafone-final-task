from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
c = Counter("requests", "Number of requests served", ["endpoint"])


@app.route("/")
def home():
    c.labels("/").inc()
    return "Hello, DevOps!"


@app.route("/metrics")
def metrics():
    return generate_latest(), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
