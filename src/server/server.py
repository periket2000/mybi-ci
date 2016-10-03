from flask import Flask, jsonify, request, Response
from helpers.loader import Loader
from helpers.threads import Threads

app = Flask(__name__)


class Server:

    @staticmethod
    def setup():
        pass

    @staticmethod
    def run():
        Server.setup()
        app.run()

    @staticmethod
    @app.route('/')
    def g_index():
        return jsonify({"title": "Mybi-ci REST API",
                        "urls": [
                            "/ (GET)",
                            "/run (POST)"
                        ]})

    @staticmethod
    @app.route('/run', methods=['POST'])
    def p_run():
        build = request.get_json()
        task = Loader.build_root_task(build)
        if task:
            Threads.run_detached(task.run)
            return jsonify({
                "log_file": task.log_file,
                "build_id": task.build_id,
                "task": task.id
            })
        else:
            return jsonify({
                "Error": "Load error",
                "Cause": "Your build json is not valid"
            })

    @staticmethod
    @app.route('/log/<build_id>/<log_file>', methods=['GET'])
    def g_log(build_id, log_file):
        with open("/tmp/"+build_id+"/"+log_file) as f:
            content = f.readlines()
        return Response(content, mimetype='text/plain')
