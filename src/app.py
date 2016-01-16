from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def landing():
  return render_template("index.html")

@app.route("/hotline", methods=["GET"])
def hotline():
  query = request.args.get("question")
  return "TODO"

if __name__ == "__main__":
    # TODO:: remove debug
  app.run(debug=True)
