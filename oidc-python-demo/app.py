import os
from flask import Flask, render_template
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

# Secret key for the user session.
app.secret_key = 'randomkey'

# Application credentials.
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Endpoint for the connection are based on the tenant ID.
TENANT_ID = os.getenv("TENANT_ID")
ACCESSS_TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
AUTHORIZE_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"

# Connection to the Microsoft Entra ID API using the application previously created.
oauth = OAuth()
oauth.init_app(app)
oauth.register(
    name='entra',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token_url=ACCESSS_TOKEN_URL,
    authorize_url=AUTHORIZE_URL,
    client_kwargs={
        'scope': 'User.Read'
    },
)


@app.route('/')
def login():
    """
    Route to start the login process.
    """
    redirect_url = "http://localhost:5000/callback"
    return oauth.entra.authorize_redirect(redirect_url)


@app.route("/callback")
def callback():
    """
    Route called by Microsoft Entra ID after user login.
    Retrieve access token to retrieve user profile then return it.
    """
    resp = oauth.entra.authorize_access_token()
    resp = oauth.entra.get('https://graph.microsoft.com/v1.0/me')
    resp.raise_for_status()
    profile = resp.json()
    return profile