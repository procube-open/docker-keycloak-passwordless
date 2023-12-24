# keycloak for WebAuthn passwordless

Web 認証サーバの keycloak のイメージを提供する

## 環境変数

|変数名|意味|例|必須|
|--|--|--|--|
|KC_DB_URL|keycloak が使用するデータベースのURL|○|jdbc:mysql://mysql/keycloak|
|KC_DB_USERNAME|データベースに接続する際のユーザID|○|keycloak|
|KC_DB_PASSWORD|データベースに接続する際のパスワード|○|j49dfb1!34|
|OIDC_WEB_AUTHN_POLICY_PASSWORD_RP_ID|WebAuthn認証を実施する際のRP ID|✗|example.com|
|OIDC_CLIENT_SECRET|webgate-web クライアントのClient Secret|◯|j49dfb1!34|
|OIDC_ACCESS_TOKEN_LIFESPAN|アクセストークンの有効期間（秒）|✗|300|
|OIDC_SSO_SESSION_IDLE_TIMEOUT|リフレッシュトークンの有効期間（秒）|✗|1800|
|OIDC_SSO_SESSION_MAX_LIFESPAN|OIDCセッションの最大有効期間（秒）|✗|64800|
|KC_WEBGATE_REALM_FRONTEND_URL|WEBGATEレルムのフロントエンドURL|✗|https://example.com/|
|KC_WEBGATE_REALM_SMTP_SERVER|SMTPサーバのホスト名|✗|smtp.gmail.com|
|KC_WEBGATE_REALM_SMTP_PORT|SMTPサーバのポート番号|✗|５８７|
|KC_WEBGATE_REALM_SMTP_FROM|メールのFROMのアドレス|✗|support@example.com|
|KC_WEBGATE_REALM_SMTP_USER|SMTPサーバへのログインユーザ|✗|root@example.com|
|KC_WEBGATE_REALM_SMTP_PASSWORD|SMTPサーバへのログインパスワード|✗|j49dfb1!34|
|KC_WEBGATE_REALM_SMTP_STARTTLS|SMTPサーバでStartTLSを使用するか否か|✗|false|
|KC_WEBGATE_REALM_SMTP_SSL|SMTPサーバでSSLを使用するか否か|✗|true|
