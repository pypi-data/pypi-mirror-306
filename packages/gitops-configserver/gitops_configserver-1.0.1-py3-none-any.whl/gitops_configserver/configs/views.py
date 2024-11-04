from os.path import join
from flask import Blueprint, jsonify, request, abort
from flask_restful import Resource
from gitops_configserver.extensions import config_provider
from gitops_configserver.utils import load_yaml

blueprint = Blueprint("configs", __name__)


class ConfigsAPI(Resource):
    def get(self):
        config = config_provider.app.config["config"]
        filename = join(config.CONFIG_DIR, "index.yml")
        index = load_yaml(filename)
        return jsonify(index)


blueprint.add_url_rule(
    "/configs",
    view_func=ConfigsAPI.as_view("configs"),
    methods=["GET"],
)
