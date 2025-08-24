import os
from flask import Flask, request, send_file

app = Flask(__name__)

class FileReader:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def read_file(self, filename):
        # Sink: vulnerable file access (path traversal possible)
        full_path = os.path.join(self.base_dir, filename)
        return send_file(full_path)

@app.route("/download", methods=["GET"])
def download():
    # Source: query parameter
    filename = request.args.get("file")

    # Propagator: passing tainted data into method
    reader = FileReader("/var/www/uploads")
    return reader.read_file(filename)

if __name__ == "__main__":
    app.run(debug=True)
