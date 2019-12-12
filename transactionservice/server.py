from flask import Flask
from flask import render_template
import connexion
from flask_cors import CORS
import argparse

app = Flask(__name__)


def parseArgs():
    parser = argparse.ArgumentParser(description="Transaction Service API")
    parser.add_argument("-p", default=5050, help="Specify port number", action="store")
    parser.add_argument("-t", action="store_true", help="Launch API and run tests")
    return parser.parse_args()


def createApp(args=False):
    if args and args.t is True:
        app = connexion.App(__name__, specification_dir="./")
        app.add_api("swagger.yaml", base_path="/test/api")
    else:
        app = connexion.App(
            __name__,
            specification_dir="./",
            arguments={"is_testing": ""},
            options={"swagger_ui": False},
        )
        app.add_api("swagger.yaml", base_path="/api")
    CORS(app.app)

    return app


if __name__ == "__main__":
    args = parseArgs()
    app = createApp(args)
    if args.t is True:
        app.run(host="0.0.0.0", port=args.p, debug=True)
    else:
        app.run(host="0.0.0.0", port=args.p)

