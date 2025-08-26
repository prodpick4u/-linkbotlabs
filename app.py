from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    # Use environment variable PORT if set (helpful for cloud platforms)
    port = int(os.environ.get("PORT", 5000))
    
    # Bind to all interfaces for LAN/external access
    app.run(host="0.0.0.0", port=port)
