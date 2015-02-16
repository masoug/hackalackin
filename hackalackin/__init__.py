from flask import Flask


from utils import gravatar_url, gravatar_profile

app = Flask(__name__)
app.config['DEBUG'] = True

app.jinja_env.filters["gravatar_url"] = gravatar_url
app.jinja_env.filters["gravatar_profile"] = gravatar_profile

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


import main
import profile
import event