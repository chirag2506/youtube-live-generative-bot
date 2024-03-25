from flask import Blueprint, redirect, request
from appUtils import configuration
from helpers.youtubeFunctionalities.credentials import write as writeCred
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
    writeCred(creds= credentials)
    return redirect('/home')