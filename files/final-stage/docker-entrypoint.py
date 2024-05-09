#!/usr/bin/python3
import os
import sys
import json
import uuid
from shlex import join

with open('/etc/realm-export.json', 'r') as f:
  realm = json.load(f)

for client in realm.get('clients', []):
  if os.environ.get('KC_WEBGATE_REALM_FRONTEND_URL') and client['webOrigins'] == []:
    client['webOrigins'] = [os.environ['KC_WEBGATE_REALM_FRONTEND_URL']]
  if client.get('clientId') == 'webgate-web':
    client['secret'] = os.environ['OIDC_CLIENT_SECRET']
    if os.environ.get('KC_WEBGATE_REALM_RP_URL'):
      client['rootUrl'] = os.environ['KC_WEBGATE_REALM_RP_URL']
      client['baseUrl'] = os.environ['KC_WEBGATE_REALM_RP_URL']
    if os.environ.get('KC_WEBGATE_MAPPERS'):
      client['protocolMappers'] = list(map(
        lambda name: {
          "id": str(uuid.uuid4()),
          "name": name,
          "protocol": "openid-connect",
          "protocolMapper": "oidc-usermodel-attribute-mapper",
          "consentRequired": "false",
          "config": {
            "userinfo.token.claim": "false",
            "user.attribute": name,
            "id.token.claim": "true",
            "access.token.claim": "true",
            "claim.name": name,
            "jsonType.label": "String"
          }
        },
        os.environ['KC_WEBGATE_MAPPERS'].split(' ')
      ))


if os.environ.get('OIDC_WEB_AUTHN_POLICY_PASSWORD_RP_ID'):
  realm['webAuthnPolicyPasswordlessRpId'] = os.environ['OIDC_WEB_AUTHN_POLICY_PASSWORD_RP_ID']
if os.environ.get('OIDC_DISPLAY_NAME'):
  realm['displayName'] = os.environ['OIDC_DISPLAY_NAME']
if os.environ.get('OIDC_DISPLAY_NAME_HTML'):
  realm['displayNameHtml'] = os.environ['OIDC_DISPLAY_NAME_HTML']
if os.environ.get('OIDC_ACCESS_TOKEN_LIFESPAN'):
  realm['accessTokenLifespan'] = int(os.environ['OIDC_ACCESS_TOKEN_LIFESPAN'])
if os.environ.get('OIDC_SSO_SESSION_IDLE_TIMEOUT'):
  realm['ssoSessionIdleTimeout'] = int(os.environ['OIDC_SSO_SESSION_IDLE_TIMEOUT'])
if os.environ.get('OIDC_SSO_SESSION_MAX_LIFESPAN'):
  realm['ssoSessionMaxLifespan'] = int(os.environ['OIDC_SSO_SESSION_MAX_LIFESPAN'])
if os.environ.get('KC_WEBGATE_REALM_FRONTEND_URL'):
  realm['attributes']['frontendUrl'] = os.environ['KC_WEBGATE_REALM_FRONTEND_URL']
if os.environ.get('KC_WEBGATE_REALM_SMTP_SERVER'):
  realm['smtpServer']['host'] = os.environ['KC_WEBGATE_REALM_SMTP_SERVER']
  if os.environ.get('KC_WEBGATE_REALM_SMTP_PORT'):
    realm['smtpServer']['port'] = int(os.environ['KC_WEBGATE_REALM_SMTP_PORT'])
  if os.environ.get('KC_WEBGATE_REALM_SMTP_FROM'):
    realm['smtpServer']['from'] = os.environ['KC_WEBGATE_REALM_SMTP_FROM']
  if os.environ.get('KC_WEBGATE_REALM_SMTP_USER'):
    realm['smtpServer']['user'] = os.environ['KC_WEBGATE_REALM_SMTP_USER']
  if os.environ.get('KC_WEBGATE_REALM_SMTP_PASSWORD'):
    realm['smtpServer']['password'] = os.environ['KC_WEBGATE_REALM_SMTP_PASSWORD']
  if os.environ.get('KC_WEBGATE_REALM_SMTP_STARTTLS'):
    realm['smtpServer']['starttls'] = os.environ['KC_WEBGATE_REALM_SMTP_STARTTLS']
  if os.environ.get('KC_WEBGATE_REALM_SMTP_SSL'):
    realm['smtpServer']['ssl'] = os.environ['KC_WEBGATE_REALM_SMTP_SSL']
with open('/opt/keycloak/data/import/realm.json', 'w') as f:
    json.dump(realm, f, indent=2)

with open('/usr/local/etc/supervisor.d/keycloak.ini', 'r') as f:
    file_data = f.read()

command = join(['command=/opt/keycloak/bin/kc.sh'] + sys.argv[1:])
file_data = file_data.replace('command=', command)

with open('/usr/local/etc/supervisor.d/keycloak.ini', 'w') as f:
    f.write(file_data)

path='/usr/local/bin/supervisord'
os.execv(path, [path, "-c", "/usr/local/etc/supervisord.conf"])
