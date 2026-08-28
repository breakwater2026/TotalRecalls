"""Assemble TotalRecalls demo v3 (fixed): trim each input to its real duration so no
anullsrc padding leaks, then concat. Silent logo cards get exact-duration silence."""
import os
import subprocess

E = r"C:\Users\break\Videos\TR-demo-shoot\edit"
D = r"C:\Users\break\Videos\TR-demo-shoot"
files = [
    os.path.join(E, "scene1_logo_from_v3.mp4"),    # 3s logo clip, lifted from reference demo
    os.path.join(D, "Complete Process Perplexity.mp4"),
    os.path.join(D, "Claude.mp4"),
    os.path.join(D, "ChatGPT.mp4"),
    os.path.join(D, "Grok+Gemini.mp4"),              # combined Grok+Gemini take (7:47)
    os.path.join(E, "scene7_endcard_v3.mp4"),        # 4s endcard, silent
]
final = os.path.join(D, "TotalRecalls_demo_v3.mp4")

def probe_duration(f):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", f], capture_output=True, text=True)
    return float(r.stdout.strip())

def has_audio(f):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-select_streams", "a",
         "-show_entries", "stream=codec_type", "-of", "csv=p=0", f],
        capture_output=True, text=True)
    return bool(r.stdout.strip())

durs = [probe_duration(f) for f in files]
audio = [has_audio(f) for f in files]
print("durations:", [round(d, 1) for d in durs])
print("audio:", audio)

cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
for f in files:
    cmd += ["-i", f]
n_silent = sum(1 for a in audio if not a)
for _ in range(n_silent):
    cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]

si = len(files)
fc = ""
pairs = []
total = 0.0
for i, (f, has_a, dur) in enumerate(zip(files, audio, durs)):
    total += dur
    fc += (f"[{i}:v]scale=2560:1440:force_original_aspect_ratio=decrease,"
           f"pad=2560:1440:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,"
           f"trim=duration={dur:.3f},setpts=PTS-STARTPTS[v{i}];")
    if has_a:
        fc += (f"[{i}:a]aresample=44100,aformat=sample_rates=44100:channel_layouts=stereo,"
               f"atrim=duration={dur:.3f},asetpts=PTS-STARTPTS[a{i}];")
    else:
        fc += f"[{si}:a]atrim=duration={dur:.3f},asetpts=PTS-STARTPTS[a{i}];"
        si += 1
    pairs.append(f"[v{i}][a{i}]")
fc += "".join(pairs) + f"concat=n={len(files)}:v=1:a=1[vout][aout]"
cmd += ["-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k", "-r", "30",
        "-movflags", "+faststart", final]

if os.path.exists(final):
    try:
        os.remove(final)
    except PermissionError:
        pass

logf = os.path.join(E, "concat_v4_log.txt")
proc = subprocess.Popen(cmd, stdout=open(logf, "w"), stderr=subprocess.STDOUT,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
print(f"encoding started pid={proc.pid} | expected duration ~ {total/60:.1f} min "
      f"({total:.0f}s)")
