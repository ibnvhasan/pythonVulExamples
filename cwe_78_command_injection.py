import os
from flask import Flask, request

app = Flask(__name__)

class CommandExecutor:
    def run(self, cmd):
        # Sink: dangerous os.system execution
        os.system(cmd)

@app.route("/exec", methods=["GET"])
def exec_cmd():
    # Source: query parameter
    command = request.args.get("cmd")

    # Propagator: directly passing to sink
    executor = CommandExecutor()
    executor.run(command)

    return "Command executed"

if __name__ == "__main__":
    app.run(debug=True)
