from flask import Flask, jsonify, request
from quote import calculate_quote

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/api/quote")
def quote():
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415
    data = request.get_json(silent=True)
    try:
        result = calculate_quote(data)
    except ValueError as exc:
        return jsonify(error=str(exc)), 422
    return jsonify(result)


@app.errorhandler(413)
def too_large(_error):
    return jsonify(error="Request too large"), 413
