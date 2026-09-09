# Mellow Admin — design specification

Everything needed to rebuild this dashboard's look in any stack. Written to be
self-contained: no file in this repo needs to be read alongside it.

The system is **shadcn/ui in the `radix-nova` style on the `neutral` base
colour**, with the **Geist** typeface. Values below were measured from the
running application, not inferred — where a number looks oddly specific
(`12.8px`, `oklch(55.6% 0 0)`), it is specific on purpose.

If your target stack is React + Tailwind, the fastest faithful route is
`npx shadcn@latest init` with style `radix-nova`, base colour `neutral`, then
follow §7. Everything else here is for hand-written CSS or any other stack.

---

## 1. Design tokens

Copy this block verbatim. Every value in the rest of the document refers to it.

```css
:root{
  /* surfaces */
  --background:oklch(100% 0 0);          /* #ffffff */
  --foreground:oklch(14.5% 0 0);         /* #0a0a0a */
  --card:oklch(100% 0 0);
  --popover:oklch(100% 0 0);
  --sidebar:oklch(98.5% 0 0);            /* #fafafa — one step off the page */

  /* accents */
  --primary:oklch(20.5% 0 0);            /* #171717 — near-black, not blue */
  --primary-foreground:oklch(98.5% 0 0);
  --secondary:oklch(97% 0 0);            /* #f5f5f5 */
  --muted:oklch(97% 0 0);
  --muted-foreground:oklch(55.6% 0 0);   /* #737373 — all secondary text */
  --accent:oklch(97% 0 0);               /* every hover fill */
  --accent-foreground:oklch(20.5% 0 0);
  --destructive:oklch(57.7% .245 27.325);/* #e7000b */

  /* lines */
  --border:oklch(92.2% 0 0);             /* #e5e5e5 — every rule and outline */
  --input:oklch(92.2% 0 0);
  --ring:oklch(70.8% 0 0);               /* #a1a1a1 — focus only */
  --sidebar-border:oklch(92.2% 0 0);
  --sidebar-accent:oklch(97% 0 0);

  /* status tints — Tailwind 100/700-ish pairs, the only colour in the UI */
  --ok-bg:#dcfce7;   --ok-fg:#008236;    /* green-100  / green-700  */
  --warn-bg:#fef9c2; --warn-fg:#894b00;  /* yellow-100 / yellow-800 */
  --bad-bg:#ffe2e2;  --bad-fg:#c10007;   /* red-100    / red-700    */

  /* radius — multiplicative, NOT shadcn's default ±2px steps */
  --radius:.625rem;                      /* 10px  default control */
  --radius-sm:calc(var(--radius) * .6);  /*  6px  */
  --radius-md:calc(var(--radius) * .8);  /*  8px  small controls, badges, table box */
  --radius-xl:calc(var(--radius) * 1.4); /* 14px  dialogs, cards */

  --shadow-pop:0 4px 6px -1px rgb(0 0 0/.1), 0 2px 4px -2px rgb(0 0 0/.1);
  --sidebar-w:256px;
}
```

**Dark mode** (apply on `.dark`, swapping only these):

```css
--background:oklch(14.5% 0 0);  --foreground:oklch(98.5% 0 0);
--card:oklch(20.5% 0 0);        --popover:oklch(20.5% 0 0);
--primary:oklch(92.2% 0 0);     --primary-foreground:oklch(20.5% 0 0);
--secondary:oklch(26.9% 0 0);   --muted:oklch(26.9% 0 0);
--muted-foreground:oklch(70.8% 0 0);
--accent:oklch(26.9% 0 0);      --accent-foreground:oklch(98.5% 0 0);
--destructive:oklch(70.4% .191 22.216);
--border:oklch(100% 0 0 / 10%); --input:oklch(100% 0 0 / 15%);
--ring:oklch(55.6% 0 0);        --sidebar:oklch(20.5% 0 0);
```

The palette is **fully achromatic** apart from the three status tints and
destructive. There is no brand hue. Resist adding one — the colour that does
appear carries meaning precisely because nothing else is coloured.

---

## 2. Typography

```css
font-family:"Geist", ui-sans-serif, system-ui, -apple-system,
            "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

Geist is on Google Fonts (`family=Geist:wght@100..900`) and npm
(`@fontsource-variable/geist`). Always ship the fallback chain.

Body base is **14px / 20px**. Not 16 — the whole UI is one step down from
browser default, which is a large part of why it reads as a dense tool.

| Role | Size / line | Weight | Other |
|---|---|---|---|
| Page title (`h1`) | 24 / 32 | 600 | `letter-spacing:-0.025em` |
| Page subtitle | 14 / 20 | 400 | `--muted-foreground` |
| Dialog / sheet title | 16 / 24 | 500 | |
| Section heading | 14 / 20 | 500 | |
| Body, table cells, menu items | 14 / 20 | 400 | |
| Table header cell | 14 / 20 | **500** | same size as the body |
| Badge, static pill, small print | 12 / 16 | 500 | |
| Button (small — the default here) | **12.8** | 500 | |
| Drawer section label | 12 | 500 | uppercase, `letter-spacing:.06em` |

Only two weights in practice: **400** and **500**. 600 is reserved for the page
title and the brand name. Never bold body text — use `--foreground` against
`--muted-foreground` for emphasis instead.

---

## 3. Layout shell

```
┌──────────┬──────────────────────────────────────┐
│ sidebar  │ topbar  64px, border-bottom          │
│ 256px    ├──────────────────────────────────────┤
│ bg:      │ page   padding 24px 24px 64px        │
│ sidebar  │   h1 + subtitle                      │
│ border-  │   toolbar   (margin-top 20px)        │
│ right    │   table box (margin-top 16px)        │
│          │   footer / pagination                │
└──────────┴──────────────────────────────────────┘
```

```css
.app{display:flex;height:100vh;overflow:hidden}
.sidebar{width:256px;flex:0 0 256px;background:var(--sidebar);
         border-right:1px solid var(--sidebar-border);padding:8px;
         display:flex;flex-direction:column}
.main{flex:1;min-width:0;display:flex;flex-direction:column;overflow:hidden}
.topbar{height:64px;flex:0 0 64px;display:flex;align-items:center;gap:8px;
        padding:0 16px;border-bottom:1px solid var(--border)}
.scroll{flex:1;overflow:auto}          /* only this scrolls */
.page{padding:24px 24px 64px}
```

`min-width:0` on `.main` is load-bearing — without it a wide table forces the
flex parent open and the sidebar gets squeezed.

**Sidebar nav item** — 32px tall, 8px radius, 8px gap, 16px icon:

```css
.nav a{display:flex;align-items:center;gap:8px;height:32px;padding:0 8px;
       border-radius:var(--radius-md);font-size:14px;
       color:var(--foreground);text-decoration:none}
.nav a:hover{background:var(--sidebar-accent)}
.nav a.on{background:var(--sidebar-accent);font-weight:500}      /* active */
.nav a.stub{color:var(--muted-foreground);cursor:default}        /* disabled */
```

The active item is marked by a **fill only** — no left bar, no colour, no bold
beyond weight 500. Brand mark at the top is a 32×32 `--primary` square with
`--radius-md` and a 16px glyph.

---

## 4. Controls

Two heights only. **32px** for the primary input; **28px** for everything
secondary. Mixing them in one row is intentional, not an accident.

```css
/* text input — 32px, the larger radius */
.input{height:32px;border:1px solid var(--input);border-radius:var(--radius);
       background:var(--background);padding:0 10px;font-size:14px;outline:none}
.input:focus{border-color:var(--ring);
             box-shadow:0 0 0 3px color-mix(in oklab,var(--ring) 50%,transparent)}

/* search variant: 320px wide, 16px icon at left:10px, padding-left:32px */

/* select — 28px, smaller radius, custom caret */
select{appearance:none;height:28px;border:1px solid var(--input);
       border-radius:var(--radius-md);padding:0 28px 0 10px;font-size:14px}

/* button — 28px "sm" is the default in this UI */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:4px;
     height:28px;padding:0 10px;border:1px solid var(--border);
     border-radius:var(--radius-md);background:var(--background);
     font-size:12.8px;font-weight:500;white-space:nowrap;
     transition:background-color .15s,border-color .15s,color .15s}
.btn svg{width:14px;height:14px}
.btn:hover{background:var(--accent)}
.btn:active{transform:translateY(1px)}      /* signature press */
.btn:disabled{opacity:.5;pointer-events:none}

.btn.primary{background:var(--primary);color:var(--primary-foreground);
             border-color:var(--primary)}
.btn.danger{color:var(--destructive)}       /* never a solid red fill */
```

Three details that carry most of the character:

1. **The 1px press.** `:active{transform:translateY(1px)}` on every button.
2. **The focus ring is two parts** — the border turns `--ring` *and* a 3px
   50%-alpha halo appears. Not an `outline`.
3. **Destructive is a tint, never a fill.** Red text, transparent or 10%-red
   background. A solid red button reads as a different design system.

---

## 5. The data table

The centrepiece. A bordered rounded box wrapping a borderless table.

```css
.tablewrap{margin-top:16px;border:1px solid var(--border);
           border-radius:var(--radius-md);overflow:hidden}
.tablescroll{width:100%;overflow-x:auto}     /* scroll lives INSIDE the box */
table{width:100%;border-collapse:collapse;table-layout:fixed}

thead th{height:40px;padding:0 8px;text-align:left;
         font-size:14px;font-weight:500;color:var(--foreground);
         white-space:nowrap;overflow:hidden;
         border-bottom:1px solid var(--border)}

tbody td{padding:8px;font-size:14px;vertical-align:middle;
         white-space:nowrap;overflow:hidden;
         border-bottom:1px solid var(--border)}
tbody tr:last-child td{border-bottom:0}      /* no double line at the box edge */

tbody tr:hover{background:color-mix(in oklab,var(--muted) 60%,transparent)}
```

Rules that matter:

- **No zebra striping.** Separation is a 1px bottom rule plus the hover tint. Adding stripes breaks the look immediately.
- **Header is the same size as the body**, distinguished only by weight 500. No uppercase, no letter-spacing, no grey.
- **`table-layout:fixed` with an explicit `<colgroup>`.** Auto layout will size to the longest string and overflow. Give every column a pixel width.
- **Rows are 48–51px** as a consequence of 8px padding plus a 28px control, not a set height.
- **Everything is left-aligned**, including numbers. Only a trailing actions cell right-aligns.
- The scroll container is **inside** the bordered box, so the border never scrolls away.

**Clickable rows** (this UI opens a record on row click):

```css
tbody tr{cursor:pointer;transition:background-color .12s}
tbody tr:focus-visible{outline:2px solid var(--ring);outline-offset:-2px}
tbody tr .chev{opacity:0;color:var(--muted-foreground);transition:opacity .12s}
tbody tr:hover .chev{opacity:1}              /* "›" in a 24px trailing cell */
```

Give rows `tabindex="0"` and handle Enter/Space. Guard the click handler so
`select`, `button` and `a` inside a row do not trigger it.

**Cell composition** — two lines in one cell instead of two columns:

```css
.stack{display:flex;flex-direction:column;line-height:18px}
.stack .sub{font-size:13px;line-height:16px;color:var(--muted-foreground)}
/* both lines: overflow:hidden; text-overflow:ellipsis; white-space:nowrap */
```

**Empty cell** is an em dash `—` in `--muted-foreground`, never blank.

---

## 6. Status colour system

Two shapes, one palette. This is the only colour in the interface.

| Tone | Background | Text | Used for |
|---|---|---|---|
| grey | `var(--muted)` | `var(--muted-foreground)` | pending, not-sent, voided, untracked |
| green | `#dcfce7` | `#008236` | accepted, paid, sent |
| yellow | `#fef9c2` | `#894b00` | waitlisted, invoicing, awaiting payment |
| red | `#ffe2e2` | `#c10007` | rejected, overdue |

**Interactive pill** — a `<select>` styled as a badge, for states a user changes:

```css
.pill{appearance:none;border:0;border-radius:var(--radius-md);height:28px;
      padding:0 26px 0 10px;font-size:14px;font-weight:400;cursor:pointer}
/* + tone background/text, and a 11px chevron absolutely positioned at right:8px */
```

**Static pill** — for states the system owns and the user cannot set:

```css
.tagp{display:inline-flex;align-items:center;padding:2px 8px;
      border-radius:var(--radius-md);
      font-size:12px;line-height:16px;font-weight:500}
```

The distinction is the useful part: **if it is a dropdown you may change it; if
it is a small flat pill you may not.** Shape encodes affordance, so a user never
has to click to discover a control is inert.

A dot variant adds state without another colour:

```css
.em::before{content:"";width:5px;height:5px;border-radius:50%;
            background:currentColor;margin-right:5px}
```

---

## 7. Overlays

**Sheet / drawer** — right-hand panel for record detail:

```css
.drawer-veil{position:fixed;inset:0;background:rgb(0 0 0/.10)}
@supports (backdrop-filter:blur(1px)){.drawer-veil{backdrop-filter:blur(4px)}}
.drawer{position:fixed;inset-block:0;right:0;width:480px;max-width:92vw;
        background:var(--popover);border-left:1px solid var(--border);
        box-shadow:0 10px 15px -3px rgb(0 0 0/.1),0 4px 6px -4px rgb(0 0 0/.1);
        overflow-y:auto;padding:16px}
```

**Dialog**:

```css
.veil{position:fixed;inset:0;background:rgb(0 0 0/.10);backdrop-filter:blur(4px);
      display:grid;place-items:center;padding:16px}
.modal{width:100%;max-width:480px;background:var(--popover);
       border-radius:var(--radius-xl);padding:16px;font-size:14px;
       box-shadow:0 0 0 1px color-mix(in oklab,var(--foreground) 10%,transparent)}
/* full-bleed footer bar */
.modal-actions{display:flex;justify-content:flex-end;gap:8px;
  margin:16px -16px -16px;padding:16px;border-top:1px solid var(--border);
  background:color-mix(in oklab,var(--muted) 50%,transparent);
  border-radius:0 0 var(--radius-xl) var(--radius-xl)}
```

Three things people get wrong here:

- **The scrim is `black/10` with a 4px blur**, not `black/50`. The page stays legible behind it. A heavy scrim is the single fastest way to look like a different system.
- **Dialogs and popovers use a 1px `foreground/10` ring, not a border and not a drop shadow.** `box-shadow:0 0 0 1px …`.
- **The dialog footer is full-bleed** — negative margins to the panel edge, muted fill, top border, bottom corners rounded.

**Popover / menu**: `--radius` (10px), 4px padding, `--shadow-pop` plus the same
1px ring, items 14px at `padding:6px 8px` with `--radius-sm` and `--accent` on
hover. Anchor it so it opens **into** the viewport — a menu anchored `right:0` on
a left-aligned trigger will be clipped by any `overflow:hidden` ancestor.

**Toast**: bottom-right, `--popover` on a 1px border, `--radius`, `--shadow-pop`,
13px text, max-width 380px.

---

## 8. Spacing and motion

Everything is a multiple of **4px**. In practice only these appear:

`4 · 6 · 8 · 10 · 12 · 14 · 16 · 20 · 24 · 32 · 64`

- Between toolbar controls: **8px**
- Page title → toolbar: **20px**; toolbar → table: **16px**
- Inside a card or dialog: **16px**
- Page padding: **24px**

Transitions are **120–150ms** on `background-color`, `border-color`, `color`,
`opacity` only. Never animate layout. No entrance animations on table rows. The
only transform in the system is the 1px button press.

---

## 9. Fingerprints

If a rebuild feels wrong, it is almost always one of these:

1. **10px base radius with a multiplicative scale** — 6 / 8 / 10 / 14, not 4 / 6 / 8.
2. **14px body text**, not 16.
3. **Achromatic everything** except three status tints. No brand hue anywhere.
4. **Cards, dialogs and popovers use a 1px ring, not a border.**
5. **Buttons nudge 1px down on press.**
6. **Focus = `--ring` border + 3px 50%-alpha halo**, never a browser outline.
7. **Destructive is a 10% tint with coloured text**, never a solid red fill.
8. **The table has no stripes** — one 1px rule and a hover tint.
9. **28px controls next to a 32px search field**, deliberately.
10. **Muted-filled footers** on dialogs and cards.
11. **Two weights, 400 and 500.** Emphasis comes from colour, not bold.
12. **Em dash for empty**, never an empty cell.

## 10. Anti-patterns

Do **not**: add a brand colour or gradient · use `border-radius` above 14px on
anything but a pill · stripe the table · bold table headers or make them
uppercase-grey · use a dark modal scrim · put drop shadows on cards · animate
row entry · centre-align numeric columns · use 16px body text · put a coloured
left border on the active nav item · use solid-fill destructive buttons.

---

## 11. Reference implementation

`dashboard.template.html` in this repo is a complete working implementation —
one file, no dependencies, no build step. Its `<style>` block is the source of
truth for everything above; read it if a value here is ambiguous.

Provenance: token values and component metrics were measured from the running
production dashboard via `getComputedStyle`, then cross-checked against the
`shadcn/ui` component sources it is built from.
