from flask import Flask, jsonify, redirect, url_for, session, request, render_template_string
from functools import wraps
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt
from authlib.oidc.core.errors import OAuth2Error
from urllib.parse import urlencode
import os, json
import requests
app=Flask(__name__)
app.secret_key=os.environ.get("FLASK_SECRET_KEY", "dev_secret_key")

oauth=OAuth(app)


KEYCLOAK_REALM_URL = os.environ.get('KEYCLOAK_SERVER_URL')
KEYCLOAK_CLIENT_ID = os.environ.get('KEYCLOAK_CLIENT_ID')
KEYCLOAK_CLIENT_SECRET = os.environ.get('KEYCLOAK_CLIENT_SECRET')
OIDC_REDIRECT_URI = os.environ.get('OIDC_REDIRECT_URI')

if not all ([KEYCLOAK_REALM_URL, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET, OIDC_REDIRECT_URI]):
    raise ValueError("One or more Keycloak Oauth environment variables are not set")

oauth.register(
    name='keycloak',
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret=KEYCLOAK_CLIENT_SECRET,
    server_metadata_url=f"{KEYCLOAK_REALM_URL}/.well-known/openid-configuration",
    client_kwargs={
        'scope': 'openid email profile roles'
    }
)

def introspect_token(token_string):
    introspection_endpoint = oauth.keycloak.server_metadata.get('introspection_endpoint')
    if not introspection_endpoint:
        app.logger.error("Introspection endpoint not found in Keycloak metadata.")
        return None

    try:
        response = requests.post(
            introspection_endpoint,
            data={'token': token_string},
            auth=(KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET) # Client credentials for introspection
        )
        response.raise_for_status() # Raise an exception for HTTP errors
        token_info = response.json()
        if token_info.get('active'):
            return token_info # Return all claims for an active token
        else:
            app.logger.warning(f"Token introspection result: inactive. Info: {token_info}")
            return None
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Token introspection request failed: {e}")
        return None
    except ValueError as e: # Includes JSONDecodeError
        app.logger.error(f"Failed to decode introspection response: {e}")
        return None



def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify(message="Authentication required. Bearer token missing."), 401

        token_claims = introspect_token(token)

        if not token_claims:
            return jsonify(message="Invalid or expired token."), 401

@app.route("/")
def home():
    user=session.get('user')
    if user:
        return jsonify(logged_in_as=user,
                       message="You are logged in.",
                       logout_url=url_for('logout', _external=True),
                       protected_resource_url=url_for('protected_resource', _external=True))
    else:
        return jsonify(message="Hello! You are not logged in.",
                       login_url=url_for('login', _external=True),
                       public_resource_url=url_for('public_resource', _external=True))
    
@app.route("/login")
def login():
    redirect_uri=url_for('authorized', _external=True)
    return oauth.keycloak.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    try:
        token=oauth.keycloak.authorize_access_token()
        id_token_claims=token.get("userinfo")
        if not id_token_claims:
            id_token_claims=oauth.keycloak.parse_id_token(token)
        session['user'] = id_token_claims.get('preferred_username', id_token_claims.get('sub'))
        session['access_token'] = token['access_token']
        session['id_token_claims'] = id_token_claims # Store all ID token claims
        # In a real app, be selective about what you store in the session.
        return redirect(url_for('home'))
    except OAuth2Error as e:
        app.logger.error(f"Error during Keycloak authorization: {e.error} - {e.description}")
        return jsonify(error="Authorization failed", message=str(e.description)), 400
    except Exception as e:
        app.logger.error(f"An unexpected error occurred during Keycloak authorization: {e}")
        return jsonify(error="Authorization failed", message="An unexpected error occurred."), 500
    
@app.route("/logout")
def logout():
    id_token_str=session.get('id_token_claims', {}).get('raw_id_token')
    session.pop('user', None)
    session.pop('access_token', None)
    session.pop('id_token_claims', None)

    keycloak_logout_url=oauth.keycloak.server_metadata.get('end_session_endpoint')
    if keycloak_logout_url:
        post_logout_redirect=url_for('home', _external=True)
        logout_params={
            'post_logout_redirect_uri': post_logout_redirect, 
            'client_id': KEYCLOAK_CLIENT_ID

        }

        full_logout_url=f"{keycloak_logout_url}?{urlencode(logout_params)}"

        return redirect(full_logout_url)
    return redirect(url_for("home"))

@app.route('/profile')
def profile():
    if 'user' not in session or 'id_token_claims' not in session:
        return redirect(url_for('login'))
    return jsonify(session.get('id_token_claims'))


@app.route('/api/public')
def public_resource():
    return jsonify(message="This is a public resource, anyone can access it!")



@app.route('/api/protected-browser')
def protected_resource_browser():
    if 'user' not in session:
         return jsonify(message="Authentication required via login for browser access."), 401, {'WWW-Authenticate': 'Bearer realm="Browser session required"'}
    user_info = session.get('id_token_claims', {})
    return jsonify(message="This is a PROTECTED resource (accessed via browser session)!",
                   accessed_by=user_info.get('preferred_username', 'Unknown'),
                   method="Session Cookie")


@app.route('/api/protected')
@token_required 
def protected_resource_api():
    user_claims = request.current_user_claims
    return jsonify(message="This is a PROTECTED resource (accessed via API Bearer token)!",
                   accessed_by=user_claims.get('preferred_username', user_claims.get('sub')),
                   client_id_from_token=user_claims.get('azp', user_claims.get('client_id')), 
                   scopes_in_token=user_claims.get('scope'),
                   method="Bearer Token",
                   all_claims_from_token=user_claims) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # Debug set by FLASK_DEBUG env var