import os
import glob
import json
import hashlib
import requests


def load_env(path=None):
    """Muatkan kredensial daripada fail .env (tidak pernah hardcoded)."""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


load_env()

account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
token = os.environ["CLOUDFLARE_API_TOKEN"]
project_name = "coupon-iviztrading"
dist_dir = "/root/projects/study-programmatic-seo/prototype-arbitrage/dist"

headers = {
    "Authorization": f"Bearer {token}"
}

html_files = glob.glob(os.path.join(dist_dir, "*.html"))
manifest = {}
files = {}

for filepath in html_files:
    rel_path = "/" + os.path.basename(filepath)
    with open(filepath, "rb") as f:
        content = f.read()
    file_hash = hashlib.sha256(content).hexdigest()[:32]
    # In Cloudflare Pages, manifest is { "/path": "hash" } or { "/path": "file_hash" }
    manifest[rel_path] = file_hash
    files[file_hash] = (file_hash, content, "text/html")

data = {
    "manifest": json.dumps(manifest)
}

url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project_name}/deployments"

response = requests.post(url, headers=headers, data=data, files=files)
print("HTTP Status:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))
