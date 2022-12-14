import os
from flask import Flask, render_template

import pulumi.automation as auto
import sites
import virtual_machines

def ensure_plugins():
    # Getting access to pulumi local workspace (execution context of single project)
    ws = auto.LocalWorkspace()

    # Install aws plugin to that workspaces
    ws.install_plugin("aws", "v4.0.0")

# Creating main app
def create_app():
    ensure_plugins()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="secret",
        PROJECT_NAME="pyrocool",
        PULUMI_ORG=os.environ.get("PULUMI_ORG")
    )

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    app.register_blueprint(sites.bp)
    app.register_blueprint(virtual_machines.bp)
    return app