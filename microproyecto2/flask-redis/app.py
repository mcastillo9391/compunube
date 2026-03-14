from flask import Flask, request, redirect, jsonify
import redis
import random
import string

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379)

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route("/")
def home():
    return {"message": "URL Shortener API"}

@app.route("/shorten", methods=["POST"])
def shorten():

    url = request.json.get("url")

    code = generate_code()

    r.set(code, url)

    return {"short_url": f"http://localhost:5000/{code}"}

@app.route("/<code>")
def redirect_url(code):

    url = r.get(code)

    if url:
        return redirect(url.decode())

    return {"error": "URL not found"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)