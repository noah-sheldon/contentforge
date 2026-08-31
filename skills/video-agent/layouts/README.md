# Layout Templates

5 frame layouts that rotate per video.

## Layouts

| # | Name | Video Position | Graphics Position | Best For |
|---|---|---|---|---|
| 1 | Bottom Window | Bottom 18% | Top 82% | Default Vox (educational, data viz) |
| 2 | Corner Circle | Top-right circle 120px | Full frame | Fireship (code, tutorials) |
| 3 | Split Vertical | Left 40% | Right 55% | Comparison, before/after |
| 4 | Full Frame | 100% cinematic | Overlays only | Documentary, storytelling |
| 5 | Center Head | Center 30% circle | Full frame behind | Authority, LinkedIn, talking-head |

## Implementation

```tsx
// Layout 1: Bottom Window (default for Vox)
<div style={{position:"absolute",bottom:"10%",left:"4%",right:"4%",height:"16%",...}}>
  <Video ... />
</div>

// Layout 2: Corner Circle (Fireship style)
<div style={{position:"absolute",top:30,right:30,width:120,height:120,borderRadius:"50%",...}}>
  <Video ... />
</div>
```
