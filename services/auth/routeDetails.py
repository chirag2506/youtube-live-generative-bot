from flask import Blueprint, render_template, redirect, request
from appUtils import configuration, writeJson, json
from google_auth_oauthlib.flow import Flow

blueprint = Blueprint('authRoutes', __name__, template_folder= 'templates')

flow = Flow.from_client_secrets_file(
    client_secrets_file= configuration["GCP"]["ClientCredentials"],
    scopes= configuration["GCP"]["Scope"],
    redirect_uri= configuration["GCP"]["CallbackURL"]
)

@blueprint.route('/login')
def login():
    authorizationUrl , state = flow.authorization_url(access_type='offline')
    return redirect(authorizationUrl)

@blueprint.route("/callback")
def callback():
    print(request.url)
    flow.fetch_token(authorization_response= request.url)
    credentials = flow.credentials
    writeJson("./token.json", json.loads(credentials.to_json()))
    return redirect('/home')