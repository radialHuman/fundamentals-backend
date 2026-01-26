from flask import Flask

app = Flask(__name__)

@app.route("/*")
def serve():
    return f"Served by {port}"

if __name__ == "__main__":
    port = 3000

    app.run(host="0.0.0.0", port=port)
    print(f"listening on {port}")