from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return {"message": "Hello depuis Flask sur Render !"}

if __name__ == "__main__":
    app.run()