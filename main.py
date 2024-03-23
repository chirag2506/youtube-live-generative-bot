from appUtils import configuration
from datetime import timedelta
from flask import Flask, render_template, redirect, jsonify
from services.auth.routeDetails import blueprint as authRoute
from waitress import serve
import os

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=60)

app.register_blueprint(authRoute,  url_prefix='/auth')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.route('/', methods= ['GET'])
def renderLogin():
    return render_template("login.html")

@app.route('/home', methods= ['GET'])
def renderHome():
    return render_template("index.html")

if __name__ == "__main__":
    if configuration["App"]["Mode"] == 0:
        app.run(
            host=configuration["App"]["Host"],
            port=configuration["App"]["Port"],
            debug=True,
            threaded=True
        )
    else:
        serve(
            app,
            host=configuration["App"]["Host"],
            port=configuration["App"]["Port"]
        )