from flask import Flask, request

app = Flask(__name__)

class CodeRunner:
    def run_code(self, code_str):
        # Sink: eval of untrusted input
        eval(code_str)

@app.route("/run", methods=["POST"])
def run():
    # Source: form field
    code = request.form["code"]

    runner = CodeRunner()
    runner.run_code(code)

    return "Code executed"

if __name__ == "__main__":
    app.run(debug=True)
