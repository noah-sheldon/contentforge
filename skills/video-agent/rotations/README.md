# Rotation System — Every Video Must Be Different

No two videos should share the same combination of creative choices.

## What Rotates

| Element | Options | How to Pick |
|---|---|---|
| Template | Vox, Fireship, Documentary, Authority | Check post-tracker last used. Never repeat. |
| Color Palette | 5 palettes | Rotate to next unused palette |
| Font Pairing | 4 pairings | Never use same pairing twice in a row |
| Music Mood | 5 moods | Different from last video |
| Title Animation | 6 styles | Rotate per video |
| Transition Style | 5 types | Rotate per video |
| VFX Combo | 4 combos | Never repeat same combo |
| Layout Frame | 5 layouts | Rotate per video |

## How to Check

```bash
# Check last video's choices
tail -20 docs/post-tracker.md | grep -E "Date|Font|Music|Template"
```

## Rotation Rules

1. Check post-tracker for last video's creative choices
2. Pick different choices for every category
3. If post-tracker is empty (first video), choose randomly
4. Log choices to post-tracker after render
