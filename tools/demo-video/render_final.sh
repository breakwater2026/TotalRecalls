#!/bin/bash
# Final CRF10 renders — locked spec: scale 2292x1440 lanczos, 30fps,
# libx264 High preset slow CRF10 aq-mode=0, yuv420p, +faststart, no audio.
set -e
cd /c/Users/break/demo-shoot
OUT="C:/Users/break/OneDrive/TotalRecalls-LS-demo"
mkdir -p renders
log(){ echo "[$(date +%H:%M:%S)] $*"; }

X264=( -c:v libx264 -preset slow -crf 10 -x264-params aq-mode=0 -pix_fmt yuv420p -movflags +faststart -an )
VF="scale=2292:1440:flags=lanczos,fps=30"

log "STEP 1/6: logo card -> h264 (180 frames, fast)"
ffmpeg -y -loglevel error -i logo/logo_master.mkv -vf "$VF" "${X264[@]}" renders/logo_h264.mp4
log "  done: $(du -h renders/logo_h264.mp4 | cut -f1)"

log "STEP 2/6: minis body (1.5x + 1.5x-speed badge)"
ffmpeg -y -loglevel error -i masters/seg2_minis_cut.mkv -i logo/badge_1.5x_speed.png \
  -filter_complex "[0:v]scale=2292:1440:flags=lanczos,setpts=PTS/1.5,fps=30[v0];[v0][1:v]overlay=40:40[v]" \
  -map "[v]" "${X264[@]}" renders/minis_body.mp4
log "  done: $(du -h renders/minis_body.mp4 | cut -f1)"

log "STEP 3/6: claude body (hero master -> locked spec, TRIM t=0-5s static white logo card)"
# NOTE: the hero master opens with a static WHITE logo card (t=0..5s, the
# shoot's placeholder intro). The animated dark convergence card (logo_h264)
# replaces it, so trim the body to the demo start (frame 150 = t=5.0s).
ffmpeg -y -loglevel error -ss 5.0 -i masters/seg1_claude_hero.mkv -vf "$VF" "${X264[@]}" renders/claude_body.mp4
log "  done: $(du -h renders/claude_body.mp4 | cut -f1)"

log "STEP 4/6: chatgpt body (re-encode at locked spec)"
ffmpeg -y -loglevel error -i masters/seg3_chatgpt_cut.mkv -vf "$VF" "${X264[@]}" renders/chatgpt_body.mp4
log "  done: $(du -h renders/chatgpt_body.mp4 | cut -f1)"

log "STEP 5/6: final concats (stream copy, identical codec params)"
# Claude = logo intro + hero body
printf "file 'renders/logo_h264.mp4'\nfile 'renders/claude_body.mp4'\n" > renders/claude_list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i renders/claude_list.txt -c copy "$OUT/totalrecalls_demo_claude_hero.mp4"
# ChatGPT = chatgpt body + logo outro
printf "file 'renders/chatgpt_body.mp4'\nfile 'renders/logo_h264.mp4'\n" > renders/chatgpt_list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i renders/chatgpt_list.txt -c copy "$OUT/totalrecalls_demo_chatgpt.mp4"
# minis = single segment (badge already baked in), direct copy
cp -f renders/minis_body.mp4 "$OUT/totalrecalls_demo_minis_6providers.mp4"
log "  done"

log "STEP 6/6: verify"
for f in "$OUT/totalrecalls_demo_claude_hero.mp4" \
         "$OUT/totalrecalls_demo_chatgpt.mp4" \
         "$OUT/totalrecalls_demo_minis_6providers.mp4"; do
  echo "--- $f"
  ffprobe -v error -show_entries stream=codec_name,profile,width,height,r_frame_rate,pix_fmt -show_entries format=duration -of default=noprint_wrappers=1 "$f"
  ls -la "$f" | awk '{print "size:", $5}'
done
log "ALL RENDERS COMPLETE"
