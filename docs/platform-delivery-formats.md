# Platform Delivery Formats (verified Aug 2026)

Which aspect ratio / file to upload per platform. Source: live Instagram uploads (2026-08-03).

## Instagram — Reels only

Noah posts via the Reels flow (found a Reel adder — feed/carousel composer not used).

| Post type | Accepted ratio | File to use |
|---|---|---|
| Reel | 9:16 fullscreen (also 4:5, 1:1) | `dayN-social.mp4` (9:16 CRF 14) |

9:16 only works in the Reels flow. The feed composer rejects it ("doesn't fit 4:5 to 16:9") — that flow is not used.

## Output set per video

| File | Ratio | CRF | Purpose |
|---|---|---|---|
| `dayN-master.mp4` | 9:16 1728x3072 | 10 | Archive |
| `dayN-lossless.mp4` | 9:16 | lossless (qp 0) | True lossless master, editing |
| `dayN-social.mp4` | 9:16 | 14 | Reels upload (avoids re-compression) |

## Other platforms

- TikTok / YouTube Shorts: 9:16 (`dayN-social.mp4`)
- Facebook: Reels flow accepts 9:16
