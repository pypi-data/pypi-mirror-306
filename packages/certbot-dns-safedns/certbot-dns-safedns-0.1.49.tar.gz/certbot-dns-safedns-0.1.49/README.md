# SafeDNS Authenticator plugin for Certbot

## `ans-group/certbot-dns-safedns` - Docker image

### About
This container uses the SafeDNS Authenticator plugin for Certbot. It utilizes API calls to create and remove DNS TXT records for domain ownership validation.

### How to use this image

1, Create the `/etc/letsencrypt` to house your configuration and your certificates
```bash
mkdir -p /etc/letsencrypt
```

2, Create the `/etc/letsencrypt/safedns.ini` configuration file with the below content
```
dns_safedns_auth_token = <YOUR API KEY HERE>
dns_safedns_propagation_seconds = 60
```

3, Set permissions for the newly created configuration file
```bash
chmod 0600 /etc/letsencrypt/safedns.ini
```

4, Test run the container
```bash
docker run -it \
  -v /etc/letsencrypt:/etc/letsencrypt \
  ans-group/certbot-dns-safedns:latest \
    certonly \
      -d yourdomain.com \
      --agree-tos \
      --no-eff-email \
      --email email@yourdomain.com \
      --test-cert
```

### Usage examples

#### Verify current certificates
```bash
docker run -it \
  -v /etc/letsencrypt:/etc/letsencrypt \
  ans-group/certbot-dns-safedns:latest \
    certificates
```

#### Delete a certificate
```bash
docker run -it \
  -v /etc/letsencrypt:/etc/letsencrypt \
  ans-group/certbot-dns-safedns:latest \
    delete --cert-name yourdomain.com
```

#### Renew all certificates
```bash
docker run -it \
  -v /etc/letsencrypt:/etc/letsencrypt \
  ans-group/certbot-dns-safedns:latest \
    renew
```

## The `certbot-dns-safedns` Plugin

### Setup

```bash
apt install certbot python3-pip
pip3 install --upgrade certbot-dns-safedns
```

### Execution

```bash
certbot certonly --authenticator dns_safedns
```

> **Warning**: Certbot might tell you that it doesn't have permissions to write to its log file. However, if you run `certbot` as `sudo`, you won't have access to the SafeDNS plugin if you didn't install the plugin as sudo.

This will result in the following error from Certbot:

```bash
Could not choose appropriate plugin: The requested dns_safedns plugin does not appear to be installed
```

To get around this just do:

```bash
sudo pip3 install --upgrade certbot-dns-safedns
sudo certbot certonly --authenticator dns_safedns
```

If you get any Python `cryptography` errors, such as:

```bash
ContextualVersionConflict: ...
```

Just make sure to upgrade your `pyopenssl`.

```bash
sudo pip install --upgrade pyopenssl
```

#### Credentials and Config Options

Use of this plugin can be simplified by using a configuration file containing SafeDNS API credentials, obtained from your ANS Portal [account page](https://portal.ans.co.uk/applications/index.php). See also the [SafeDNS API](https://developers.ukfast.io/documentation/safedns) documentation.

An example `safedns.ini` file:

```ini
dns_safedns_auth_token = 0123456789abcdef0123456789abcdef01234567
dns_safedns_propagation_seconds = 20
```

The path to this file can be provided interactively or using the `--dns_safedns-credentials` command-line argument. Certbot records the path to this file for use during renewal, but does not store the file's contents.

> **CAUTION:** You should protect these API credentials as you would the password to your ANS Portal account. Users who can read this file can use these credentials to issue arbitrary API calls on your behalf. Users who can cause Certbot to run using these credentials can complete a `dns-01` challenge to acquire new certificates or revoke existing certificates for associated domains, even if those domains aren't being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be accessed by other users on your system. The warning reads "Unsafe permissions on credentials configuration file", followed by the path to the credentials file. This warning will be emitted each time Certbot uses the credentials file, including for renewal, and cannot be silenced except by addressing the issue (e.g., by using a command like `chmod 600` to restrict access to the file).

#### Examples

To acquire a single certificate for both `example.com` and `*.example.com`, waiting 900 seconds for DNS propagation:

```bash
certbot certonly \
  --authenticator dns_safedns \
  --dns_safedns-credentials ~/.secrets/certbot/safedns.ini \
  --dns_safedns-propagation-seconds 900 \
  -d 'example.com' \
  -d '*.example.com'
```

### Build

The package for the SafeDNS plugin is hosted on PyPI here: <https://pypi.org/project/certbot-dns-safedns/>

To build and upload the package from source, first ensure you've increased the version number in `setup.py`.

Delete the `build`, `dist` and `.egg-info` directories if they are present from a previous build.

Then run:

```bash
python3 setup.py sdist bdist_wheel
```

### Deployment

```bash
python3 -m twine upload dist/*
```

> **Warning**: Use the username: `__token__`, along with the token registered on PyPI.
