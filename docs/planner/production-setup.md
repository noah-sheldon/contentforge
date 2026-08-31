# Production Setup Guide — Noah's filming kit (all free)

Hardware: Mac (M1 Pro) + iPad + Apple Pencil + iPhone.

## 1. OBS Studio (Mac) — base configuration

- Install OBS (obsproject.com, free).
- **Canvas 1920×1080** for long-form; a separate **1080×1920** profile for camera-led shorts.
- Encoder: **Apple VT H.264 hardware encoder**, CBR ~20-40 Mbps (1080p), "High Quality" preset.
- Record to **MKV**, remux to MP4 after (File → Remux Recordings). MKV survives crashes.
- **DUAL-TRACK AUDIO (mandatory):** Settings → Output → Recording → Audio Tracks:
  - Track 1 = Microphone (your voice)
  - Track 2 = Desktop Audio (code execution, system sound)
  - Advanced Audio Properties: untick the wrong track per source. Editing pauses later never destroys background audio.

## 2. Scenes (presets, so filming = scene-switching)

| Scene | Content | Source |
|---|---|---|
| Code | VSCode fullscreen (font ≥ 20pt, high-contrast theme) | Display Capture (Mac) |
| Whiteboard | Excalidraw in Safari | Window Capture — or iPad via QuickTime wired (below) |
| Camera | Talking head | iPhone via Continuity Camera |
| Camera+Code | PiP: camera top-left, code/whiteboard below | both sources |
| Camera Offline / Code Only | Fallback — keep recording when the feed drops | no camera source |

## 3. Whiteboard — iPad + Excalidraw

- Open `excalidraw.com` on iPad Safari. Apple Pencil pressure + palm rejection work (toggles in settings).
- Diagrams: the pipeline generates each video's diagrams into its workspace folder (`workspace/<form>/<date>/<video>/03_diagrams/*.excalidraw`). Sync the whole `workspace/` folder to iCloud Drive — on the iPad, open the file from there, trace/animate on camera — never draw from scratch.
- iPad screen into OBS: **QuickTime (free)** → New Movie Recording → select iPad (USB-C cable required). Add that capture as a window source in OBS. Use the Mac/iPhone mic — QuickTime doesn't carry iPad audio.

## 4. Camera — iPhone

- **Continuity Camera:** macOS 13+/iOS 16+, same Apple Account, Wi-Fi + Bluetooth. In OBS add it as a Video Capture Device.
- It WILL drop eventually (wireless). **Protocol:** on drop → switch to "Camera Offline / Code Only" scene → keep recording → re-add the feed → continue. Never restart the recording.
- Framing: eye level, rule of thirds, window light facing you.

## 5. Shorts (9:16)

- Code-led shorts: record 16:9 and crop in edit (code is wide).
- Camera-led shorts (diagram/talking head): use the 1080×1920 OBS profile.
- Upload natively per platform — **no watermarks** (a TikTok watermark costs ~5-15% of IG reach).

## 6. Teleprompter

- `teleprompter.txt` (breath-broken lines) → open on iPad/iPhone in any scrollable reader (Notes, a web teleprompter). Phone screen just below the lens — read lines, keep eye contact.

## 7. Batch filming day checklist

1. `workspace/` synced to iPad — every video's `03_diagrams/*.excalidraw` present
2. `teleprompter.txt` files on the phone
3. OBS: dual-track verified (level meters on both tracks)
4. Camera scene test + "Camera Offline" fallback confirmed
5. Record long-form top-to-bottom (Batch A), then immediately the 3-5 shorts from the same topic (Batch B) — lighting, mic, canvas already warm
6. Remux MKV → MP4; edit only when you must; captions from the recording's own transcription later

## 8. First-session sanity targets

- One 10-15 min long-form + 3-5 shorts recorded in one sitting
- Dual-track verified by listening to Track 2 alone in edit
- 16:9 raw for everything; crop to 9:16 for shorts
