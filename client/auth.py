import requests
import time
import os
import sys
from pathlib import Path

client_id = "Iv1.479cca827e65c19d"

def token_file_path():
    return Path().home() / ".inven" / ".token"

def get_token():
    p = token_file_path()
    if not p.exists():
        print("You are not logged in. Run `inven login` to log in.")
        sys.exit(1)
    with p.open(mode='r') as f:
        token = f.read().rstrip()
    return token

def login():
    r = request_device_code()
    verification_uri, user_code, device_code, interval = r['verification_uri'], r['user_code'], r['device_code'], r['interval']
    print(f"Copy this code: {user_code}")
    print(f"Enter the code at this URL: {verification_uri}")

    token = poll_for_token(device_code, interval)
    p = token_file_path()
    os.makedirs(p.parent, exist_ok=True)
    with p.open(mode='w') as f:
        f.write(token)
    # Make only the user be able to read/write the token file.
    p.chmod(0o600)
    # print(f"Token saved to {p}.")
    print(f"Successfully authenticated with GitHub!")

    pass

def request_device_code():
    r = requests.post("https://github.com/login/device/code", params={'client_id': client_id}, headers={"Accept": "application/json"})
    return r.json()

def request_token(device_code):
    r = requests.post("https://github.com/login/oauth/access_token", params={'client_id': client_id, 'device_code': device_code, 'grant_type': "urn:ietf:params:oauth:grant-type:device_code"}, headers={"Accept": "application/json"})
    return r.json()


def poll_for_token(device_code, interval):
    while True:
        r = request_token(device_code)
        if "error" in r:
            error = r['error']
            if error == "authorization_pending":
                time.sleep(interval)
            elif error == "slow_down":
                time.sleep(interval + 5)
            elif error == "expired_token":
                print("Your GitHub code has expired. Please re-run `inven login`.")
                sys.exit(1)
            elif error == "access_denied":
                print("Login cancelled by user.")
                sys.exit(1)
            else:
                print("Unexpected error from GitHub while trying to log in:")
                print(error)
                sys.exit(1)
        else:
            return r['access_token']

def github_username():
    tok = get_token()
    r = requests.get("https://api.github.com/user", data={'access_token': tok}, headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {tok}"})
    r.raise_for_status()
    r = r.json()
    return r['login']
