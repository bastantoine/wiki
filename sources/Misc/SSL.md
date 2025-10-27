## Decrypting an encrypted private key

Sometimes you have a private key that is encrypted using a pass phrase:

```
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBvTBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIpZHwLtkYRb4CAggA
MAwGCCqGSIb3DQIJBQAwHQYJYIZIAWUDBAECBBCCGsoP7F4bd8O5I1poTn8PBIIB
...
QwinX0cR9Hx84rSMrFndxZi52o9EOLJ7cithncoW1KOAf7lIJIUzP0oIKkskAndQ
o2UiZsxgoMYuq02T07DOknc=
-----END ENCRYPTED PRIVATE KEY-----
```

To decrypt it, using the passphrase, you can use the openssl CLI, and its rsa module.
- `encrypted.key` is where the encrypted private key is
- `decrypted.key` is where to write the decrypted private key
- You will get an interactive prompt to provide the pass phrase.

```bash
> openssl rsa -in encrypted.key -out decrypted.key
Enter pass phrase for encrypted.key: ****
writing RSA key
```
