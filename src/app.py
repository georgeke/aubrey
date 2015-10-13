from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def landing():
  return render_template("index.html")

@app.route("/hotline", methods=["GET"])
def hotline():
  query = requests.args.get("query")
  return "TODO"

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=5001)
