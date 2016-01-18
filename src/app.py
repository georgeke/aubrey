import time
from flask import Flask, request, render_template
from answerer import Answerer

app = Flask(__name__)
answerer = Answerer()

def _sanitize(string):
    if len(string) <= 0:
        return string
    output = ""
    for c in string:
        if (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "'" or c == " " or (c >= "0" and c <= "9"):
            output += c
    return output

@app.route("/", methods=["GET"])
def landing():
    return render_template("index.html")

@app.route("/hotline", methods=["GET"])
def hotline():
    MIN_LOAD_TIME = 3

    then = time.time()
    question = _sanitize(request.args.get("question"))
    answer = answerer.answer(question)

    time_passed = time.time() - then
    if time_passed < MIN_LOAD_TIME:
        time.sleep(MIN_LOAD_TIME - time_passed)

    if answer is None:
        return "Invalid question.", 404
    else:
        return answer

if __name__ == "__main__":
    app.run(debug=True)
