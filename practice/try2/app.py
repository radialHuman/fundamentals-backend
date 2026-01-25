from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return f"Hello from {os.getenv('SERVER_ID', 'unknown')}"

if __name__ == '__main__':
    app.run(host='localhost', port=80)