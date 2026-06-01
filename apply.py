import os
import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone


B12_ENDPOINT = "https://b12.io/apply/submission"


def main():
    signing_secret = os.environ["B12_SIGNING_SECRET"].encode("utf-8")

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "name": os.environ["APPLICANT_NAME"],
        "email": os.environ["APPLICANT_EMAIL"],
        "resume_link": os.environ["RESUME_LINK"],
        "repository_link": os.environ["REPOSITORY_LINK"],
        "action_run_link": os.environ["ACTION_RUN_LINK"],
    }

    body = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    digest = hmac.new(
        signing_secret,
        body,
        hashlib.sha256,
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={digest}",
    }

    response = requests.post(
        B12_ENDPOINT,
        data=body,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()
    result = response.json()

    print(f"Receipt: {result['receipt']}")


if __name__ == "__main__":
    main()
