#!/usr/bin/env bash
set -e
PROJECT_DIR="/root/projects/iviz-viral-products"
LOG_FILE="$PROJECT_DIR/logs/auto_update.log"
mkdir -p "$PROJECT_DIR/logs"

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Starting Build & Deploy ===" >> "$LOG_FILE"

# 0.5 Refresh affiliate links (auto-heal — langkau senyap kalau API IA down)
echo "--- Refreshing Affiliate Links ---" >> "$LOG_FILE"
python3 "$PROJECT_DIR/generator/refresh_affiliate_links.py" >> "$LOG_FILE" 2>&1 || true

# 1. Build Pages
echo "--- Building Pages ---" >> "$LOG_FILE"
python3 "$PROJECT_DIR/generator/build_microsites.py" >> "$LOG_FILE" 2>&1

# 2. Deploy
echo "--- Deploying to Cloudflare ---" >> "$LOG_FILE"
python3 "$PROJECT_DIR/generator/deploy_cf.py" >> "$LOG_FILE" 2>&1

# 3. Purge
echo "--- Purging Cache ---" >> "$LOG_FILE"
# Source .env for ZONE_ID
if [ -f "$PROJECT_DIR/.env" ]; then
  source <(grep "CLOUDFLARE_ZONE_ID" "$PROJECT_DIR/.env" | sed 's/ //g')
  source <(grep "CLOUDFLARE_API_TOKEN" "$PROJECT_DIR/.env" | sed 's/ //g')
fi

curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${CLOUDFLARE_ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}' >> "$LOG_FILE" 2>&1

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Done ===" >> "$LOG_FILE"
