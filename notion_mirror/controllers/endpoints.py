from flask import Flask
from flask_cors import CORS

from notion_mirror import registry


app = Flask("notion-mirror", instance_relative_config=True)
app.config.from_pyfile("settings.py")
CORS(app)


@app.route("/ping", methods=["GET"])
def ping() -> dict:
    return {"app": "ok"}


@app.route("/page/<page_id>")
def page(page_id: str) -> str:
    return registry.get_page_content.perform(page_id)
