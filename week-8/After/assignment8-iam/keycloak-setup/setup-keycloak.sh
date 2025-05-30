#!/usr/bin/env bash
set -eo pipefail

REALM_NAME="CyberArchRealm"
KEYCLOAK_URL_FROM_HOST="http://localhost:8080"
KEYCLOAK_INTERNAL_URL="http://keycloak-server:8080"
KEYCLOAK_ADMIN_USER="admin"
KEYCLOAK_ADMIN_PASSWORD="admin"
OIDC_CLIENT_ID="my-flask-api-client"
OIDC_CLIENT_SECRET="supersecret"
FLASK_APP_BASE_URL="http://localhost:5001"
OIDC_REDIRECT_URIS="[\"${FLASK_APP_BASE_URL}/authorize\", \"${FLASK_APP_BASE_URL}/*\"]"
TEST_USER_USERNAME="testuser"
TEST_USER_PASSWORD="password"
KEYCLOAK_CONTAINER_NAME= ""

########################################
# A) Start Keycloak
########################################
echo "[*] Starting Keycloak..."
docker compose up -d --build keycloak 


########################################
# B) Checking that keycloak container is running
########################################
KEYCLOAK_CONTAINER_NAME=$(docker ps --filter "ancestor=quay.io/keycloak/keycloak:latest" --format "{{.Names}}" | head -n 1)
if [ -z "$KEYCLOAK_CONTAINER_NAME" ]; then
  echo "[!] failed to find ruinning keycloak container in docker."
  exit 1
fi
echo "[*] found keycloak container: $KEYCLOAK_CONTAINER_NAME"



########################################
# C) Wait for Keycloak to be ready
########################################
echo "[*] waiting for keycloak to ready on $KEYCLOAK_URL_HOST..."
for i in {20..1}; do
  if curl -s -f "$KEYCLOAK_URL_FROM_HOST/admin/master/console/" > /dev/null; then
  echo "[*] keycloak ui is responseive."
  if curl -s -f -o /dev/null -w "%{http_code}" "$KEYCLOAK_URL_FROM_HOST/realms/master" | grep -q "200"; then
    echo "[*] keycloak master realm is available."
    return 0
  fi
  fi
  echo " waiting for keycloak... ($i)"
  sleep 3
done

########################################
# D) Authenticate kcadm.sh
########################################
echo "[*] Logging into Keycloak CLI…"
docker exec "$KEYCLOAK_CONTAINER_NAME" /opt/keycloak/bin/kcadm.sh config credentials \
  --server "$KEYCLOAK_URL_FROM_HOST" --realm master \
  --user "$KEYCLOAK_ADMIN_USER" --password "$KEYCLOAK_ADMIN_PASSWORD"
  echo "[*] kcadm.sh aunthinicated with master realm."


########################################
# E) Delete & (re)create Cyber Arch Realm
########################################
echo "[*] Deleting any existing realm '$REALM_NAME'…"
docker exec "$KEYCLOAK_CONTAINER_NAME" /opt/keycloak/bin/kcadm.sh delete realms/$REALM_NAME || true

echo "[*] Creating realm '$REALM_NAME'…"
docker exec "$KEYCLOAK_CONTAINER_NAME" /opt/keycloak/bin/kcadm.sh create realms \
  -s realm="$REALM_NAME" -s enabled=true

########################################
# F) Wait for Realm to be available through OIDC discovery endpoint
########################################
REALM_OIDC_DISCOVERY_URL="$KEYCLOAK_URL_FROM_HOST/realms/$REALM_NAME/.well-known/openid-configuration"
echo "[*] Waiting for OIDC Discovery Endpoint…"
for i in {30..1}; do
  if curl -s -f "$REALM_OIDC_DISCOVERY_URL" > /dev/null; then
    echo "[*] OIDC Discovery Endpoint is now available."
    break
  fi
  echo "  still waiting for OIDC Discovery… ($i)"
  sleep 2
done
curl -sf "$REALM_OIDC_DISCOVERY_URL" >/dev/null || {
  echo "[!] OIDC Discovery Endpoint never appeared. Exiting."
  exit 1
}


########################################
# G) Create OIDC Client for FLASK App
########################################
echo "[*] Creating OIDC Client '$OIDC_CLIENT_ID' In Realm '$REALM_NAME'..."
CLIENT_CONFIG_JSON=$(cat <<EOF
{
  "clientId": "${OIDC_CLIENT_ID}",
  "secret": "${OIDC_CLIENT_SECRET}",
  "enabled": true,
  "protocol": "openid-connect",
  "clientAuthenticatorType": "client-secret",
  "redirectUris": ${OIDC_REDIRECT_URIS},
  "baseUrl": "${FLASK_APP_BASE_URL}",
  "adminUrl": "${FLASK_APP_BASE_URL}",
  "rootUrl": "${FLASK_APP_BASE_URL}",
  "publicClient": false,
  "standardFlowEnabled": true,        департа
  "directAccessGrantsEnabled": true, 
  "implicitFlowEnabled": false,
  "serviceAccountsEnabled": false,
  "fullScopeAllowed": true,
  "defaultClientScopes": ["email", "profile", "roles", "web-origins"],
  "optionalClientScopes": ["address", "phone", "offline_access", "microprofile-jwt"]
}
EOF
)

TEMP_CLIENT_CONFIG_FILE="/tmp/oidc-client-config-$$.json"

echo "$CLIENT_CONFIG_JSON" | docker exec -i "$KEYCLOAK_CONTAINER_NAME" sh -c "cat > $TEMP_CLIENT_CONFIG_FILE"

docker exec "$KEYCLOAK_CONTAINER_NAME" \
  /opt/keycloak/bin/kcadm.sh create clients \
  -r "$REALM_NAME"
  -f "$TEMP_CLIENT_CONFIG_FILE"
echo "[*] OIDC client '$OIDC_CLIENT_ID' created."


########################################
# H) Create a Test User
########################################
echo "[*] Creating Test User '$TEST_USER_NAME' In Realm '$REALM_NAME'..."
docker exec "$KEYCLOAK_CONTAINER_NAME" \
  /opt/keycloak/bin/kcadm.sh create users \
  -r "$REALM_NAME" \
  -s username="$TEST_USER_USERNAME" \
  -s enabled=true \
  -s emailVerified=true \
  -s email="$TEST_USER_USERNAME@example.com" \
  -s firstName="Test" \
  -s lastName="User"
echo "[*] User '$TEST_USER_USERNAME' created."

echo "[*] Setting password for user '$TEST_USER_USERNAME'..."
docker exec "$KEYCLOAK_CONTAINER_NAME" \
  /opt/keycloak/bin/kcadm.sh set-password \
  -r "$REALM_NAME" \
  --username "$TEST_USER_USERNAME" \
  --new-password "$TEST_USER_PASSWORD"
echo "[*] Password set for user '$TEST_USER_USERNAME'."