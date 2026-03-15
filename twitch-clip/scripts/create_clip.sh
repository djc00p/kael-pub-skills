#!/bin/bash
# Usage: create_clip.sh [duration_seconds]
# Duration defaults to 30, max 60

DURATION=${1:-30}
CLIENT_ID="${TWITCH_CLIENT_ID}"
TOKEN="${TWITCH_ACCESS_TOKEN}"
BROADCASTER_ID="${TWITCH_BROADCASTER_ID}"

if [ -z "$TOKEN" ] || [ -z "$CLIENT_ID" ] || [ -z "$BROADCASTER_ID" ]; then
  echo "ERROR: Missing Twitch credentials in environment" >&2
  exit 1
fi

RESPONSE=$(curl -s -X POST \
  "https://api.twitch.tv/helix/clips?broadcaster_id=${BROADCASTER_ID}&has_delay=false" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Client-Id: ${CLIENT_ID}")

CLIP_ID=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['data'][0]['id'])" 2>/dev/null)
EDIT_URL=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['data'][0]['edit_url'])" 2>/dev/null)

if [ -z "$CLIP_ID" ]; then
  echo "ERROR: Failed to create clip. Response: $RESPONSE" >&2
  exit 1
fi

echo "clip_id=$CLIP_ID"
echo "edit_url=$EDIT_URL"
echo "url=https://clips.twitch.tv/$CLIP_ID"
