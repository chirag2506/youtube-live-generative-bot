from flask import Blueprint, redirect, request, session
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
    authorizationUrl , state = flow.authorization_url(prompt= 'consent', access_type='offline', include_granted_scopes='true')
    return redirect(authorizationUrl)

@blueprint.route("/callback")
def callback():
    flow.fetch_token(authorization_response= request.url)
    credentials = flow.credentials
    writeJson(configuration["GCP"]["OAuthToken"], json.loads(credentials.to_json()))
    return redirect('/home')