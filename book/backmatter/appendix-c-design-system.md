<span class="chapter-number">Appendix C</span>

# Design System Starter Kit {.chapter-title}

A design system is not a component library. It's a set of constraints that make every design decision faster and every interface more consistent. Without one, every page looks like it was designed by a different person on a different day — because, in an AI-assisted workflow, it probably was. Claude Code generates beautiful components, but without constraints, each one invents its own spacing, colors, and typography.

This starter kit gives you the foundation: color tokens, typography, spacing, and component patterns. Fork it, customize it, and use it on every project.

---

## Color Tokens

Colors are defined as CSS custom properties on `:root` (light mode) and `[data-theme="dark"]` (dark mode). Never use raw hex values in your components — always reference tokens. This way, switching themes means changing variables, not hunting through files.

```css
/* /styles/tokens.css */

:root {
  /* --- Brand --- */
  --color-brand-primary: #2563eb;       /* Blue 600 — primary actions, links */
  --color-brand-primary-hover: #1d4ed8; /* Blue 700 — hover state */
  --color-brand-secondary: #7c3aed;     /* Violet 600 — accents, highlights */

  /* --- Backgrounds --- */
  --color-bg-primary: #ffffff;          /* Main background */
  --color-bg-secondary: #f9fafb;       /* Cards, subtle sections */
  --color-bg-tertiary: #f3f4f6;        /* Input fields, code blocks */
  --color-bg-inverse: #111827;         /* Inverted sections (dark on light) */

  /* --- Text --- */
  --color-text-primary: #111827;       /* Headings, body text */
  --color-text-secondary: #4b5563;     /* Descriptions, labels */
  --color-text-tertiary: #9ca3af;      /* Placeholders, disabled text */
  --color-text-inverse: #f9fafb;       /* Text on dark backgrounds */
  --color-text-link: var(--color-brand-primary);

  /* --- Borders --- */
  --color-border-primary: #e5e7eb;     /* Card borders, dividers */
  --color-border-secondary: #d1d5db;   /* Input borders */
  --color-border-focus: var(--color-brand-primary);

  /* --- Semantic (status colors) --- */
  --color-success: #059669;            /* Green 600 */
  --color-success-bg: #ecfdf5;         /* Green 50 */
  --color-warning: #d97706;            /* Amber 600 */
  --color-warning-bg: #fffbeb;         /* Amber 50 */
  --color-error: #dc2626;              /* Red 600 */
  --color-error-bg: #fef2f2;           /* Red 50 */
  --color-info: #2563eb;               /* Blue 600 */
  --color-info-bg: #eff6ff;            /* Blue 50 */

  /* --- Shadows --- */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1),
               0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1),
               0 4px 6px -4px rgb(0 0 0 / 0.1);
}

[data-theme="dark"] {
  --color-brand-primary: #60a5fa;       /* Blue 400 — brighter on dark */
  --color-brand-primary-hover: #93bbfd;
  --color-brand-secondary: #a78bfa;     /* Violet 400 */

  --color-bg-primary: #0f172a;          /* Slate 900 */
  --color-bg-secondary: #1e293b;        /* Slate 800 */
  --color-bg-tertiary: #334155;         /* Slate 700 */
  --color-bg-inverse: #f8fafc;

  --color-text-primary: #f1f5f9;        /* Slate 100 */
  --color-text-secondary: #94a3b8;      /* Slate 400 */
  --color-text-tertiary: #64748b;       /* Slate 500 */
  --color-text-inverse: #0f172a;
  --color-text-link: var(--color-brand-primary);

  --color-border-primary: #334155;      /* Slate 700 */
  --color-border-secondary: #475569;    /* Slate 600 */
  --color-border-focus: var(--color-brand-primary);

  --color-success: #34d399;             /* Emerald 400 */
  --color-success-bg: #064e3b;          /* Emerald 900 */
  --color-warning: #fbbf24;             /* Amber 400 */
  --color-warning-bg: #78350f;          /* Amber 900 */
  --color-error: #f87171;               /* Red 400 */
  --color-error-bg: #7f1d1d;            /* Red 900 */
  --color-info: #60a5fa;
  --color-info-bg: #1e3a5f;

  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4),
               0 2px 4px -2px rgb(0 0 0 / 0.3);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.5),
               0 4px 6px -4px rgb(0 0 0 / 0.4);
}
```

**Design note:** Dark mode is not inverted light mode. Notice that the brand color shifts from Blue 600 to Blue 400 — lighter values on dark backgrounds maintain the same perceived vibrancy. Semantic colors shift similarly: Red 600 becomes Red 400, Green 600 becomes Emerald 400. Shadows get heavier because dark backgrounds absorb more light.

---

## Typography Scale

A modular scale based on a 1.25 ratio (major third). Each step is 1.25x the previous size. This creates visual harmony without arbitrary decisions.

```css
:root {
  /* --- Font Families --- */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont,
               'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

  /* --- Font Sizes --- */
  --text-xs:    0.75rem;    /* 12px — captions, badges */
  --text-sm:    0.875rem;   /* 14px — secondary text, labels */
  --text-base:  1rem;       /* 16px — body text (never go smaller) */
  --text-lg:    1.125rem;   /* 18px — lead paragraphs */
  --text-xl:    1.25rem;    /* 20px — card titles */
  --text-2xl:   1.5rem;     /* 24px — section headings */
  --text-3xl:   1.875rem;   /* 30px — page headings */
  --text-4xl:   2.25rem;    /* 36px — hero headings */
  --text-5xl:   3rem;       /* 48px — display headings */

  /* --- Line Heights --- */
  --leading-tight:   1.25;  /* Headings (tight for large text) */
  --leading-normal:  1.5;   /* Body text (comfortable reading) */
  --leading-relaxed: 1.75;  /* Long-form content */

  /* --- Font Weights --- */
  --weight-normal:   400;
  --weight-medium:   500;
  --weight-semibold: 600;
  --weight-bold:     700;

  /* --- Letter Spacing --- */
  --tracking-tight:  -0.025em;  /* Large headings */
  --tracking-normal:  0;        /* Body text */
  --tracking-wide:    0.025em;  /* Uppercase labels, small caps */
}
```

**Heading hierarchy applied:**

```css
h1 {
  font-size: var(--text-4xl);
  font-weight: var(--weight-bold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
}
h2 {
  font-size: var(--text-3xl);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
}
h3 {
  font-size: var(--text-2xl);
  font-weight: var(--weight-semibold);
  line-height: var(--leading-tight);
}
h4 {
  font-size: var(--text-xl);
  font-weight: var(--weight-medium);
  line-height: var(--leading-normal);
}
p {
  font-size: var(--text-base);
  font-weight: var(--weight-normal);
  line-height: var(--leading-normal);
}
```

**The rule of three weights:** Use at most three font weights on any page. Typically: `normal` for body, `medium` for labels, `bold` or `semibold` for headings. More than three weights creates visual noise.

---

## Spacing System

An 8px base grid. Every spacing value is a multiple of 4 or 8. This creates visual rhythm without thinking — elements snap to a grid the eye can feel even if it can't articulate.

```css
:root {
  --space-0:   0;
  --space-1:   0.25rem;   /* 4px  — tight gaps, icon padding */
  --space-2:   0.5rem;    /* 8px  — inline element spacing */
  --space-3:   0.75rem;   /* 12px — compact list items */
  --space-4:   1rem;      /* 16px — standard element gap */
  --space-5:   1.25rem;   /* 20px — form field spacing */
  --space-6:   1.5rem;    /* 24px — card internal padding */
  --space-8:   2rem;      /* 32px — section gap */
  --space-10:  2.5rem;    /* 40px — large section gap */
  --space-12:  3rem;      /* 48px — page section separation */
  --space-16:  4rem;      /* 64px — major section breaks */
  --space-20:  5rem;      /* 80px — hero-level spacing */
  --space-24:  6rem;      /* 96px — page-level breathing room */

  /* --- Container Widths --- */
  --container-sm:   640px;  /* Narrow content (blog posts, forms) */
  --container-md:   768px;  /* Medium content */
  --container-lg:  1024px;  /* Standard page width */
  --container-xl:  1280px;  /* Wide layouts (dashboards, tables) */

  /* --- Border Radius --- */
  --radius-sm:    0.25rem;  /* 4px  — buttons, badges */
  --radius-md:    0.5rem;   /* 8px  — cards, inputs */
  --radius-lg:    0.75rem;  /* 12px — modals, large cards */
  --radius-xl:    1rem;     /* 16px — hero sections */
  --radius-full:  9999px;   /* Circles, pill buttons */
}
```

**Spacing rules of thumb:**

- `--space-4` (16px) between sibling elements inside a component
- `--space-6` (24px) for container/card internal padding
- `--space-8` to `--space-12` between sections on a page
- `--space-16` or more for hero sections and major visual breaks
- When it feels cramped, go up one step. When it feels wasteful, go down one step. Never invent values outside the scale.

---

## Component Patterns

These are not full implementations — they're patterns showing how tokens compose into components. Adapt the selectors to your framework (Tailwind utility classes, CSS modules, styled-components).

### Button

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  line-height: var(--leading-normal);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 150ms ease;
  min-height: 44px;   /* Touch target — non-negotiable */
  min-width: 44px;
}
.btn-primary {
  background: var(--color-brand-primary);
  color: white;
  border: none;
}
.btn-primary:hover { background: var(--color-brand-primary-hover); }
.btn-secondary {
  background: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-secondary);
}
.btn-secondary:hover { background: var(--color-bg-tertiary); }
.btn-ghost {
  background: transparent;
  color: var(--color-text-secondary);
  border: none;
}
.btn-ghost:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-tertiary);
}
```

### Card

```css
.card {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
}
.card-title {
  font-size: var(--text-xl);
  font-weight: var(--weight-semibold);
  color: var(--color-text-primary);
}
.card-description {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-top: var(--space-1);
}
```

### Input

```css
.input {
  width: 100%;
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-base);
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border-secondary);
  border-radius: var(--radius-md);
  min-height: 44px;
  transition: border-color 150ms ease, box-shadow 150ms ease;
}
.input:focus {
  outline: none;
  border-color: var(--color-border-focus);
  box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1);
}
.input::placeholder { color: var(--color-text-tertiary); }
.input-error { border-color: var(--color-error); }
.input-error:focus { box-shadow: 0 0 0 3px rgb(220 38 38 / 0.1); }
```

### Alert / Toast

```css
.alert {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
}
.alert-success { background: var(--color-success-bg); color: var(--color-success); }
.alert-warning { background: var(--color-warning-bg); color: var(--color-warning); }
.alert-error   { background: var(--color-error-bg);   color: var(--color-error); }
.alert-info    { background: var(--color-info-bg);     color: var(--color-info); }
```

---

## Using This System

1. **Copy `tokens.css`** into your project's `/styles/` directory. Import it in your root layout.
2. **Customize the brand colors.** Change `--color-brand-primary` and its hover state. The structural tokens (background, text, border) work with any brand palette.
3. **Respect the scale.** Using values outside the system (random padding of 13px, font size of 17px) defeats the purpose. Constrain yourself to the tokens. Constraint creates speed.
4. **Extend, don't override.** Need a new token? Add it to the system with a comment explaining when to use it. Don't create one-off values in components.
5. **Audit periodically.** Run a search for raw color values (`#`, `rgb(`, `hsl(`) in your components. Every hit is a token that should exist but doesn't.

The goal is speed through constraint. When every color, size, and spacing value is pre-decided, you stop designing pixels and start designing experiences.
