# Custom Fonts

Use @fontsource packages for reliable server-side rendering. Never rely on external Google Fonts links for production.

## Install

```bash
npm install @fontsource/inter @fontsource/jetbrains-mono @fontsource/playfair-display
```

## Usage

```tsx
import "@fontsource/inter/700.css";
import "@fontsource/jetbrains-mono/400.css";
import "@fontsource/playfair-display/700.css";

// Font available globally via font-family name
<div style={{ fontFamily: "Inter, sans-serif", fontSize: 60 }}>Text</div>
```

## Font Pairings

| Style | Headline | Body | Mono |
|---|---|---|---|
| Editorial | Playfair Display | Inter | JetBrains Mono |
| Tech | Inter 800 | Inter 400 | JetBrains Mono |
| Modern | Syne | Space Grotesk | JetBrains Mono |

## 3K Sizing

All sizes ×1.6 from 1080p reference:
- Hook: 150-170px
- Titles: 96px
- Body: 60px
- Captions: 60px
- Tags: 22px
