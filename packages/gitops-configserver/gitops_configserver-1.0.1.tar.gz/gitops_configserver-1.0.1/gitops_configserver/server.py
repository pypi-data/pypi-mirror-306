from flask import Flask
from gitops_configserver import configs
from gitops_configserver.extensions import config_provider


class ConfigServer:
    def __init__(self, config):
        self.config = config

    def start(self):
        app = Flask(__name__)
        config_provider.init_app(app)
        app.register_blueprint(configs.views.blueprint)
        app.config["config"] = self.config
        app.run(host=self.config.HOST, port=self.config.PORT)
