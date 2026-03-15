---
name: twitch-clip
description: Create Twitch clips for djc00p23's stream. Use when Deonte says "clip that", "clip the last X seconds", or any variation of clipping the current stream moment.
---

# Twitch Clip Skill

Creates a clip of the last ~30 seconds (or specified duration up to 60s) of the live stream.

## Credentials
Stored in environment:
- `TWITCH_CLIENT_ID`
- `TWITCH_ACCESS_TOKEN`
- `TWITCH_BROADCASTER_ID` (50699927)
- `TWITCH_CHANNEL` (djc00p23)

## Usage

Run the script:
```bash
bash /home/djc00p23/.openclaw/workspace/skills/twitch-clip/scripts/create_clip.sh [duration]
```

- Duration is optional, defaults to 30 seconds, max 60
- Stream must be live or this will fail

## Trigger phrases
- "clip that"
- "clip the last X seconds"
- "make a clip"
- "clip it"

## Response format
After clipping, reply with the clip URL:
"Clipped! 🎬 https://clips.twitch.tv/CLIP_ID"

## Token refresh
If the access token expires (401 error), notify Deonte to re-authorize at:
https://id.twitch.tv/oauth2/authorize?client_id=lkmqheqz0mtwj5csmqqbr4ntlaneh0&redirect_uri=http://localhost&response_type=token&scope=clips:edit
