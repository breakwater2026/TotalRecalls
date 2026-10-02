#!/usr/bin/env bash
# Night encode batch: master @1.5x, 6 provider minis @1.5x, ChatGPT standalone (3-part)
set -u
cd "$(dirname "$0")"
mkdir -p videos
LOG=videos/encodes.log
: > "$LOG"

run() {
  local name="$1"; shift
  echo "=== $name ===" >> "$LOG"
  ffmpeg -y -loglevel warning "$@" >> "$LOG" 2>&1
  echo "=== $name EXIT=$? ===" >> "$LOG"
}

HERO="C:/Users/break/OneDrive/TotalRecalls-LS-demo/totalrecalls_demo_claude_hero.mp4"
CG="C:/Users/break/OneDrive/TotalRecalls-LS-demo/totalrecalls_demo_chatgpt.mp4"
SHOT="C:/Users/break/demo-shoot"

ENC="-c:v libx264 -crf 20 -preset medium -c:a aac -b:a 128k -movflags +faststart"

# A. Master: Claude hero @1.5x  (258.9s -> 172.6s)
run master -i "$HERO" -f lavfi -i anullsrc=r=44100:cl=stereo \
  -filter_complex "[0:v]setpts=PTS/1.5[v]" -map "[v]" -map 1:a:0 -shortest $ENC videos/TR_yt_master_chatgpt_placeholder.mp4

# B. Six provider minis @1.5x
for p in pplx gemini grok mistral qwen deepseek; do
  run mini_$p -i "$SHOT/cutM_$p.mkv" -f lavfi -i anullsrc=r=44100:cl=stereo \
    -filter_complex "[0:v]setpts=PTS/1.5[v]" -map "[v]" -map 1:a:0 -shortest $ENC videos/TR_yt_provider_$p.mp4
done

# C. ChatGPT standalone: 30s open + 245s download @25x + 22s website outro  (~69.5s)
run chatgpt -i "$CG" -f lavfi -i anullsrc=r=44100:cl=stereo \
  -filter_complex "[0:v]trim=5:35,setpts=PTS-STARTPTS[s0];[0:v]trim=35:280,setpts=(PTS-STARTPTS)/25[s1];[0:v]trim=470:492,setpts=PTS-STARTPTS[s2];[s0][s1][s2]concat=n=3:v=1:a=0[v]" \
  -map "[v]" -map 1:a:0 -shortest $ENC videos/TR_yt_provider_chatgpt.mp4

echo "=== BATCH DONE ===" >> "$LOG"
