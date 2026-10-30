"""
Import all flow definitions from the flows directory into a running NiFi as process groups.

Used by the seed service of compose.yaml. Groups that already exist are skipped.
"""

import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

BASE_URL = os.environ.get("NIFI_URL", "https://nifi:8443/nifi-api")
USERNAME = os.environ["NIFI_USERNAME"]
PASSWORD = os.environ["NIFI_PASSWORD"]
FLOWS_DIR = Path(os.environ.get("FLOWS_DIR", "/flows"))
TIMEOUT = 300

# NiFi uses a self-signed certificate locally
CONTEXT = ssl.create_default_context()
CONTEXT.check_hostname = False
CONTEXT.verify_mode = ssl.CERT_NONE


def request(path, token=None, data=None, headers=None):
    """
    Send a request to the NiFi API and return the response body.
    """
    headers = dict(headers or {})
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=headers)

    with urllib.request.urlopen(req, context=CONTEXT, timeout=30) as response:
        return response.read()


def login():
    """
    Wait until NiFi accepts the credentials and return an access token.
    """
    body = urllib.parse.urlencode({"username": USERNAME, "password": PASSWORD}).encode()
    deadline = time.monotonic() + TIMEOUT

    while True:
        try:
            return request("/access/token", data=body).decode()
        except (urllib.error.URLError, ConnectionError, TimeoutError) as error:
            if time.monotonic() > deadline:
                raise SystemExit(f"NiFi not reachable: {error}") from error
            print("Waiting for NiFi ...", flush=True)
            time.sleep(10)


def multipart(fields, file_name, file_content):
    """
    Encode form fields and one file as multipart/form-data.
    """
    boundary = uuid.uuid4().hex
    parts = []

    for name, value in fields.items():
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode()
        )

    parts.append(
        (
            f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
            "Content-Type: application/json\r\n\r\n"
        ).encode()
        + file_content
        + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())

    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def main():
    """
    Import every flow definition that does not exist as process group yet.
    """
    token = login()

    root = json.loads(request("/flow/process-groups/root", token))["processGroupFlow"]
    root_id = root["id"]
    existing = {group["component"]["name"] for group in root["flow"]["processGroups"]}

    for index, path in enumerate(sorted(FLOWS_DIR.glob("*.json"))):
        name = path.stem

        if name in existing:
            print(f"Skip {name}, already exists")
            continue

        body, content_type = multipart(
            {
                "groupName": name,
                "positionX": 100 + index * 450,
                "positionY": 100,
                "clientId": uuid.uuid4(),
            },
            path.name,
            path.read_bytes(),
        )

        request(
            f"/process-groups/{root_id}/process-groups/upload",
            token,
            data=body,
            headers={"Content-Type": content_type},
        )
        print(f"Imported {name}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        sys.exit(f"{error}: {error.read().decode(errors='replace')}")
