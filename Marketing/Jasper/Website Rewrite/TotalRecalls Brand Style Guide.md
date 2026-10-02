# TotalRecalls Brand Style Guide

**Version 1.0 · Visual Identity: Private Archive + Calm Utility**

This guide defines how TotalRecalls looks everywhere: website, desktop app, email, social, and video. It is a working reference, so every rule is meant to be applied as written. When a situation isn't covered here, choose the option that feels quieter, more orderly, and more honest.

---

## 1. Brand Essence

### The One-Line Essence

> **TotalRecalls is a private local archive for valuable AI work.**

Every design decision should support this sentence. If a visual doesn't make TotalRecalls feel more private, more permanent, or more organized, it doesn't belong.

### Identity Blend

TotalRecalls blends three design directions in fixed proportions:

| Direction                     | Weight | What It Contributes                         |
| ----------------------------- | ------ | ------------------------------------------- |
| **Private Archive**           | 70%    | Trust, permanence, warmth, seriousness      |
| **Practical Desktop Utility** | 20%    | Clarity, approachability, easy scanning     |
| **Local Command Center**      | 10%    | Technical proof, status, file-flow diagrams |

The Archive leads. Utility keeps it usable. Command Center adds evidence without turning the brand into a dashboard.

### Core Attributes

| Attribute     | What It Means                      | How It Shows Up Visually                                              |
| ------------- | ---------------------------------- | --------------------------------------------------------------------- |
| **Private**   | Your data stays with you           | Dark, contained surfaces. No cloud imagery. Restrained lock icon use. |
| **Durable**   | Built to last, not to trend        | Stable grids, timeless type, no trend effects like glassmorphism      |
| **Orderly**   | Everything has a place             | Clear hierarchy, consistent spacing, indexed layouts                  |
| **Local**     | Lives on your PC as ordinary files | File paths, folder structures, Markdown and JSON evidence             |
| **Technical** | Competent and precise              | Mono metadata, exact labels, clean diagrams                           |
| **Calm**      | Relief, not alarm                  | Muted palette, slow motion, generous whitespace                       |

### What TotalRecalls Is Not

Avoid anything that reads as:

- Flashy or futuristic
- Playful or cartoonish
- Chaotic or alarmist
- Overtly "AI" (glowing brains, sparkles, neural meshes, robot imagery)
- Generic SaaS gloss (purple gradients, floating 3D blobs)
- Security software (shields everywhere, red alert banners)
- Cyberpunk or gamer aesthetics (neon, scanlines, glitch effects)

---

## 2. Color System

### 2.1 Core Palette

#### Backgrounds (Dark Neutrals)

| Swatch | Name         | Hex       | RGB        | Primary Role                                   |
| ------ | ------------ | --------- | ---------- | ---------------------------------------------- |
| ⬛      | **Obsidian** | `#111315` | 17, 19, 21 | Base background for site, app, and video       |
| ⬛      | **Graphite** | `#1A1D21` | 26, 29, 33 | Raised surfaces: cards, panels, sidebars       |
| ⬛      | **Slate**    | `#2A2F36` | 42, 47, 54 | Borders, dividers, input fills, hover surfaces |

#### Light Neutrals

| Swatch | Name      | Hex       | RGB           | Primary Role                                    |
| ------ | --------- | --------- | ------------- | ----------------------------------------------- |
| ⬜      | **Paper** | `#F3EFE7` | 243, 239, 231 | Primary text on dark; light section backgrounds |
| ⬜      | **Mist**  | `#D9D4CB` | 217, 212, 203 | Secondary text on dark; borders on light        |
| ⬜      | **Dust**  | `#B5AEA3` | 181, 174, 163 | Tertiary text, captions, placeholders on dark   |

#### Accents

| Swatch | Name              | Hex       | RGB           | Primary Role                                    |
| ------ | ----------------- | --------- | ------------- | ----------------------------------------------- |
| 🟧     | **Archive Amber** | `#C88A2B` | 200, 138, 43  | Primary CTA, pricing emphasis, key highlights   |
| 🟩     | **Local Green**   | `#5E8A68` | 94, 138, 104  | Local, saved, complete, and success states      |
| 🟦     | **Steel Blue**    | `#7A8FA6` | 122, 143, 166 | Metadata, secondary UI accents, diagrams, links |

### 2.2 Usage Rules by Color

**Obsidian `#111315`**

- Default background for the website, app window, video end cards, and thumbnails.
- Use as text color on Archive Amber buttons and on Paper sections.
- Never place Obsidian cards on an Obsidian background. Step up to Graphite for elevation.

**Graphite `#1A1D21`**

- Cards, panels, app sidebars, modals, table rows, and code blocks.
- Creates depth through tone instead of shadow.
- Never use Graphite as a text color.

**Slate `#2A2F36`**

- 1px borders and dividers on dark surfaces.
- Input field fills, hover states on Graphite cards, and disabled button fills.
- Use as text color on Paper backgrounds when you need a softer tone than Obsidian.

**Paper `#F3EFE7`**

- Primary text on all dark backgrounds.
- Background for occasional "relief" sections on the website, such as pricing tables or long-form docs.
- Never use pure white `#FFFFFF`. Paper is the brand's white.

**Mist `#D9D4CB`**

- Secondary text on dark: subheads, descriptions, and body copy in dense layouts.
- Borders and dividers on Paper backgrounds.

**Dust `#B5AEA3`**

- Tertiary text on dark: timestamps, helper text, captions, and input placeholders.
- Never use Dust on Paper or Mist. The contrast fails.

**Archive Amber `#C88A2B`**

- Primary CTA button fills, pricing figures, active tab indicators, and single-word highlights.
- Always pair with Obsidian text when used as a fill.
- Limit to **one dominant Amber element per screen or frame**.
- Never use Amber as text on Paper or Mist. The contrast fails.

**Local Green `#5E8A68`**

- Reserved for state, not decoration: "Saved locally," "Download complete," "Offline ready," and success toasts.
- Status dots, check icons, and completion chips.
- Use as text on Obsidian only. On Graphite or Slate, use it for icons, dots, and large text (18px+) only.

**Steel Blue `#7A8FA6`**

- Metadata labels, diagram lines, provider node connectors, inline links, and secondary icons.
- File-type badges such as `.md` and `.json`.
- On Slate, use for large text or icons only.

### 2.3 Functional Extension Colors

These support UI states only. They are not brand colors and must never appear in marketing graphics.

| Name              | Hex                      | Use                                                                |
| ----------------- | ------------------------ | ------------------------------------------------------------------ |
| **Error Rust**    | `#C8664A`                | Error messages, failed downloads, destructive action confirmations |
| **Amber Hover**   | `#D69A3D`                | Hover state for Archive Amber buttons                              |
| **Amber Pressed** | `#AE7722`                | Pressed state for Archive Amber buttons                            |
| **Amber Tint**    | `#C88A2B` at 12% opacity | Subtle highlight backgrounds, such as a selected row               |
| **Green Tint**    | `#5E8A68` at 12% opacity | Background for success banners and "local" chips                   |

### 2.4 Contrast Reference

Approximate WCAG 2.1 contrast ratios. **AA** requires 4.5:1 for body text and 3:1 for large text (18px+ regular or 14px+ bold).

| Text          | Background    | Ratio   | Approved For              |
| ------------- | ------------- | ------- | ------------------------- |
| Paper         | Obsidian      | ≈16:1   | All text                  |
| Paper         | Graphite      | ≈15:1   | All text                  |
| Mist          | Obsidian      | ≈12.6:1 | All text                  |
| Mist          | Graphite      | ≈11.4:1 | All text                  |
| Dust          | Obsidian      | ≈8.4:1  | All text                  |
| Dust          | Slate         | ≈6.1:1  | All text                  |
| Obsidian      | Archive Amber | ≈6.3:1  | Button labels, all text   |
| Archive Amber | Obsidian      | ≈6.3:1  | All text                  |
| Steel Blue    | Obsidian      | ≈5.6:1  | All text                  |
| Steel Blue    | Graphite      | ≈5.1:1  | All text                  |
| Local Green   | Obsidian      | ≈4.7:1  | All text                  |
| Local Green   | Graphite      | ≈4.3:1  | Large text and icons only |
| Obsidian      | Paper         | ≈16:1   | All text                  |
| Slate         | Paper         | ≈11.7:1 | All text                  |
| Archive Amber | Paper         | ≈2.6:1  | ❌ Not approved            |
| Dust          | Paper         | ≈1.9:1  | ❌ Not approved            |
| Steel Blue    | Paper         | ≈2.9:1  | ❌ Not approved            |

### 2.5 Color Proportions

In any layout, aim for roughly this balance:

- **70%** dark neutrals (Obsidian, Graphite, Slate)
- **20%** light neutrals (Paper, Mist, Dust), mostly as text
- **10%** accents combined, with Archive Amber as the largest share

### 2.6 Colors to Avoid

- Bright electric blues
- Neon greens
- Harsh reds as a dominant color
- Rainbow or multi-stop "AI" gradients
- Pure black `#000000` or pure white `#FFFFFF`
- Official provider brand colors used as design accents

### 2.7 Developer Tokens

```
:root {
  /* Backgrounds */
  --tr-obsidian: #111315;
  --tr-graphite: #1A1D21;
  --tr-slate:    #2A2F36;

  /* Light neutrals */
  --tr-paper: #F3EFE7;
  --tr-mist:  #D9D4CB;
  --tr-dust:  #B5AEA3;

  /* Accents */
  --tr-amber:       #C88A2B;
  --tr-amber-hover: #D69A3D;
  --tr-amber-press: #AE7722;
  --tr-green:       #5E8A68;
  --tr-steel:       #7A8FA6;

  /* Functional */
  --tr-error: #C8664A;

  /* Semantic aliases */
  --tr-bg:             var(--tr-obsidian);
  --tr-surface:        var(--tr-graphite);
  --tr-border:         var(--tr-slate);
  --tr-text-primary:   var(--tr-paper);
  --tr-text-secondary: var(--tr-mist);
  --tr-text-tertiary:  var(--tr-dust);
  --tr-cta:            var(--tr-amber);
  --tr-success:        var(--tr-green);
  --tr-meta:           var(--tr-steel);
}
```

---

## 3. Typography System

### 3.1 Typefaces

| Role        | Typeface      | Source                               | Weights Used                                    |
| ----------- | ------------- | ------------------------------------ | ----------------------------------------------- |
| **Primary** | Inter         | Google Fonts / rsms.me (open source) | 400 Regular, 500 Medium, 600 Semibold, 700 Bold |
| **Accent**  | IBM Plex Mono | Google Fonts (open source)           | 400 Regular, 500 Medium                         |

Use no more than these six weights in total. Do not add italics except for rare editorial emphasis in long-form content.

### 3.2 The Governing Rule

> **Sans for meaning. Mono for evidence.**

- **Inter** carries the message: headlines, body copy, buttons, navigation, and captions.
- **IBM Plex Mono** carries proof: file paths, file names, timestamps, provider IDs, metadata labels, and diagram notation.

If a piece of text is something a user could find on their own hard drive, set it in mono. Everything else is Inter.

### 3.3 Web Type Scale

Base size: 16px. Scale ratio: roughly 1.25, adjusted for display sizes.

| Token     | Use                              | Font / Weight           | Desktop | Mobile | Line Height | Tracking |
| --------- | -------------------------------- | ----------------------- | ------- | ------ | ----------- | -------- |
| `display` | Homepage hero only               | Inter Bold              | 64px    | 40px   | 1.05        | −0.02em  |
| `h1`      | Page titles                      | Inter Bold              | 48px    | 34px   | 1.1         | −0.02em  |
| `h2`      | Section headings                 | Inter Semibold          | 36px    | 28px   | 1.15        | −0.01em  |
| `h3`      | Subsections, card titles         | Inter Semibold          | 24px    | 20px   | 1.25        | −0.005em |
| `h4`      | Small headings, list titles      | Inter Semibold          | 18px    | 17px   | 1.35        | 0        |
| `body-lg` | Lead paragraphs, hero subhead    | Inter Regular           | 20px    | 18px   | 1.55        | 0        |
| `body`    | Default paragraph text           | Inter Regular           | 16px    | 16px   | 1.6         | 0        |
| `body-sm` | Dense UI, table cells, footnotes | Inter Regular           | 14px    | 14px   | 1.5         | 0        |
| `eyebrow` | Section labels above headings    | Inter Medium, uppercase | 12px    | 12px   | 1.3         | +0.12em  |
| `button`  | Button labels                    | Inter Semibold          | 15px    | 15px   | 1           | +0.01em  |
| `mono`    | File paths, metadata             | IBM Plex Mono Regular   | 14px    | 13px   | 1.5         | 0        |
| `mono-sm` | Timestamps, badges, chips        | IBM Plex Mono Medium    | 12px    | 12px   | 1.3         | +0.02em  |

### 3.4 App Type Scale

The desktop app uses a tighter scale for density.

| Token         | Use                               | Font / Weight         | Size | Line Height |
| ------------- | --------------------------------- | --------------------- | ---- | ----------- |
| `app-title`   | Window and view titles            | Inter Semibold        | 20px | 1.3         |
| `app-heading` | Panel headings                    | Inter Semibold        | 15px | 1.35        |
| `app-body`    | Default UI text                   | Inter Regular         | 14px | 1.45        |
| `app-label`   | Field labels, list secondary text | Inter Medium          | 13px | 1.4         |
| `app-caption` | Helper text, hints                | Inter Regular         | 12px | 1.4         |
| `app-mono`    | Paths, file names, counts         | IBM Plex Mono Regular | 13px | 1.4         |

### 3.5 Typography Rules

- **Measure:** Keep body text between 60 and 75 characters per line. Cap paragraph containers at 680px.
- **Alignment:** Left-align all text. Center only short hero headlines, single-line CTAs, and video captions.
- **Headline length:** Aim for under 10 words. Break lines by meaning, not by available width.
- **Case:** Sentence case for headings and buttons. Uppercase only for eyebrows, mono chips, and short video text overlays.
- **Color pairing:** Headings in Paper, body in Mist, captions in Dust (on dark backgrounds).
- **Mono limit:** Never set more than two consecutive lines of
