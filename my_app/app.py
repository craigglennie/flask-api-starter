from flask import Flask

app = Flask(__name__)
# Load test settings by default, unless overridden by an
# environment variable
app.config.from_pyfile('../settings/test_settings.py')
# app.config.from_envvar("IHELPER_SETTINGS", silent=True)

from my_app.v2014_01_19.views import api as v2014_01_19
app.register_blueprint(v2014_01_19.blueprint)
