from flask import Flask, request, render_template_string

app = Flask(__name__)

class TemplateRenderer:
    def __init__(self, template):
        self.template = template

    def render(self, context):
        # Sink: unsafe template rendering
        return render_template_string(self.template, **context)

@app.route("/greet")
def greet():
    # Source: query parameter
    name = request.args.get("name")

    # Propagator: context dict holding tainted value
    context = {"name": name}
    renderer = TemplateRenderer("<h1>Hello {{ name }}</h1>")
    return renderer.render(context)

if __name__ == "__main__":
    app.run(debug=True)
