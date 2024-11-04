class ConfigProvider:
    app = None

    def init_app(self, app):
        self.app = app


config_provider = ConfigProvider()
