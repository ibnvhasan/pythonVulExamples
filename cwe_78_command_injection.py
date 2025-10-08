import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Utility Layer ---
class CommandFormatter:
    def __init__(self, prefix=""):
        self.prefix = prefix

    def format_command(self, user_input):
        # Taint propagator: modifies but still passes user input
        return f"{self.prefix}{user_input}"

# --- Business Logic Layer ---
class FileManager:
    def __init__(self):
        self.formatter = CommandFormatter(prefix="ls ")

    def list_files(self, path):
        # Propagator: tainted data flows into another layer
        cmd = self.formatter.format_command(path)
        return self._execute(cmd)

    def _execute(self, command):
        # Sink: dangerous command execution
        os.system(command)
        return f"Executed: {command}"

# --- Controller Layer ---
@app.route("/files", methods=["GET"])
def list_user_files():
    # Source: tainted input from user query parameter
    path = request.args.get("path", "")

    # Intermediate processing
    # Example of partial sanitization attempt (ineffective)
    if ";" in path or "&" in path:
        return jsonify({"error": "invalid input"}), 400

    manager = FileManager()
    result = manager.list_files(path)

    return jsonify({"message": result})

# --- Additional route to simulate indirect taint propagation ---
@app.route("/run", methods=["POST"])
def run_custom_command():
    data = request.get_json()
    # Source can also come from JSON body
    cmd = data.get("cmd", "")
    executor = FileManager()
    executor._execute(cmd)  # direct sink
    return jsonify({"status": "done"})

if __name__ == "__main__":
    app.run(debug=True)
