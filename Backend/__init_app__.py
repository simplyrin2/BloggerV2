from flask import Flask
from flask_sse import sse
from flask_caching import Cache
import os
app=Flask(__name__)


# if os.environ['ENV'] == 'development':
#     app.config['ENV'] = 'development'
# if os.environ['ENV'] == 'production':
#     app.config['ENV'] = 'production'

app.config['ENV'] = os.environ['ENV']

if app.config['ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')

elif app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')

else:
    app.config.from_object('config.TestingConfig')

app.register_blueprint(sse, url_prefix='/stream')
cache = Cache(app)
app.app_context().push()