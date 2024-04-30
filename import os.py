import os
import secrets

# Using os
secret_key_os = os.urandom(16)
print("Secret Key (os):", secret_key_os)

# Using secrets
secret_key_secrets = secrets.token_urlsafe(16)
print("Secret Key (secrets):", secret_key_secrets)
