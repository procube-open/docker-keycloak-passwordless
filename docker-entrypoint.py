#!/usr/bin/python3
import os
import sys
import json

with open('/etc/realm-export.json', 'r') as f:
  realm = json.load(f)

for client in realm.get('clients', []):
  if client.get('clientId') == 'webgate-web':
    client['secret'] = os.environ['OIDC_CLIENT_SECRET']

if os.environ.get('OIDC_WEB_AUTHN_POLICY_PASSWORD_RP_ID'):
  realm['webAuthnPolicyPasswordlessRpId'] = int(os.environ['OIDC_WEB_AUTHN_POLICY_PASSWORD_RP_ID'])
if os.environ.get('OIDC_ACCESS_TOKEN_LIFESPAN'):
  realm['accessTokenLifespan'] = int(os.environ['OIDC_ACCESS_TOKEN_LIFESPAN'])
if os.environ.get('OIDC_SSO_SESSION_IDLE_TIMEOUT'):
  realm['ssoSessionIdleTimeout'] = int(os.environ['OIDC_SSO_SESSION_IDLE_TIMEOUT'])
if os.environ.get('OIDC_SSO_SESSION_MAX_LIFESPAN'):
  realm['ssoSessionMaxLifespan'] = int(os.environ['SSO_SESSION_MAX_LIFESPAN'])
if os.environ.get('KC_WEBGATE_REALM_FRONTEND_URL'):
  realm['attributes']['frontendUrl'] = int(os.environ['KC_WEBGATE_REALM_FRONTEND_URL'])
if os.environ.get('KC_WEBGATE_REALM_SMTP_SERVER'):
  realm['smtpServer']['host'] = int(os.environ['KC_WEBGATE_REALM_SMTP_SERVER'])
  if os.environ.get('KC_WEBGATE_REALM_SMTP_PORT'):
    realm['smtpServer']['port'] = int(os.environ['KC_WEBGATE_REALM_SMTP_PORT'])
  if os.environ.get('KC_WEBGATE_REALM_SMTP_FROM'):
    realm['smtpServer']['from'] = int(os.environ['KC_WEBGATE_REALM_SMTP_FROM'])
  if os.environ.get('KC_WEBGATE_REALM_SMTP_USER'):
    realm['smtpServer']['user'] = int(os.environ['KC_WEBGATE_REALM_SMTP_USER'])
  if os.environ.get('KC_WEBGATE_REALM_SMTP_PASSWORD'):
    realm['smtpServer']['password'] = int(os.environ['KC_WEBGATE_REALM_SMTP_PASSWORD'])
  if os.environ.get('KC_WEBGATE_REALM_SMTP_STARTTLS'):
    realm['smtpServer']['starttls'] = int(os.environ['KC_WEBGATE_REALM_SMTP_STARTTLS'])
  if os.environ.get('KC_WEBGATE_REALM_SMTP_SSL'):
    realm['smtpServer']['ssl'] = int(os.environ['KC_WEBGATE_REALM_SMTP_SSL'])


with open('/opt/keycloak/data/import/realm.json', 'w') as f:
    json.dump(realm, f, indent=2)

path='/opt/keycloak/bin/kc.sh'
os.execv(path, [path] + sys.argv[1:])
