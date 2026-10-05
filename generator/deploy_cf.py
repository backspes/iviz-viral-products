import os
import subprocess
import sys


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
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env()

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dist_dir = os.path.join(project_dir, "dist")
project_name = "store-iviztrading"

wrangler_bin = "/root/node_modules/.bin/wrangler"

cmd = [
    wrangler_bin, "pages", "deploy", dist_dir,
    f"--project-name={project_name}",
    "--branch=main",
    "--commit-dirty=true"
]

print(f"Deploying {dist_dir} to Cloudflare Pages ({project_name})...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr, file=sys.stderr)

if res.returncode != 0:
    sys.exit(res.returncode)
