# mellow-dashv2

Admin dashboard for the **Mellow Art & Stationery Fair** artist application system.
One self-contained HTML file: no server, no build toolchain, no dependencies.

It merges what used to be two separate prototypes — the inquiries dashboard and
the email-template studio — into a single app with working sidebar routing.

```
dashboard.template.html   the whole app; __COLS__ / __ROWS__ are data placeholders
build_dashboard.py        injects a CSV export into the template
mellow-dashv2.html        build output (gitignored)
```

## Build

```bash
python3 build_dashboard.py path/to/inquiries-export.csv
```

Writes `mellow-dashv2.html` next to the script. With no argument it looks for
`./inquiries.csv`. A third argument sets the output path.

Serve it over HTTP rather than opening the file directly — under `file://` the
browser blocks the `assets/manifest.json` fetch, so **Backup data** silently
falls back to generated placeholder images instead of real uploads:

```bash
python3 -m http.server 8000
```

## What's in it

### Inquiries

- Search, and filters for application status, payment, **email state**, event and archive
- Table / list / card views; 10 rows per page by default, with a Rows selector (10/20/50/100)
- Inline editing of status and payment; internal notes. Stall assignment unlocks
  only once an application is accepted, and locks again once an invoice exists
- Copy emails, export the filtered set as CSV, and a full ZIP backup
  (CSV + browsable HTML + one image per record), written in-browser

**Columns are user-controlled.** The table shows eight columns by default and
fits a 1280px window with no horizontal scrolling. The *Columns* button opens a
picker for seven more (insurance, applied-before, secondary category, Instagram,
invoice, decided date, sharing); the choice is saved per browser. Reference is
always shown. Everything else lives in the detail panel.

**Rows open on click.** Hovering a row highlights it and shows a `›` affordance;
clicking anywhere that isn't an inline control opens the full record. Rows are
focusable, so Enter and Space work too. This replaces the old kebab menu, which
was the only way to reach a record and was easy to miss.

### Email templates

The block editor, moved in whole from the previous standalone PoC. Seven block
types (hero, text, image, button, invoice summary, divider, spacer), drag-and-drop
ordering, merge tags, image upload, and desktop/mobile preview. Branding — logo,
colours, footer, social links — is shared across every template and edited in the
same workspace under the *Branding* tab.

Templates persist to `localStorage` under `mellowDashV2.email`.

## Status changes no longer send email

Previously, moving an application to **Waitlist** or **Rejected** was coupled to
sending the corresponding email. These are now two separate steps.

1. **Change the status.** The record is updated immediately and an email is
   *queued*, not sent. A banner reports how many are waiting.
2. **Review it.** Open the record. The panel shows the exact template that will
   go out, the merged subject line, and a live preview rendered with that
   applicant's real details — the same template you edit under *Email templates*.
3. **Send, or don't.** *Send* records it as sent, with a timestamp. *Don't send*
   marks it skipped. Reverting the status before sending cancels the queued email.

The review step also captures the **reason** shown to the applicant, filling the
`{{reason}}` merge tag that the Rejection template has always referenced but that
the data never populated. Presets are offered per template; leaving it blank drops
the paragraph rather than sending an empty gap.

Accepted applications are unchanged — that email stays tied to invoice sending.

Four columns carry this workflow and are included in CSV exports:
`Email state`, `Email template`, `Email reason`, `Email sent at`.

**Existing records are not backfilled.** Every application decided before this
flow existed shows *Not tracked* and never enters the send queue — the app makes
no assumption about whether those artists were already emailed. Any single record
can be queued by hand from its detail panel.

## Known limits

This is a front-end prototype. It is convincing, and it does not persist.

- **No backend.** Every edit — status, stall, payment, notes, email state — lives
  in memory and is lost on reload. Use *Backup data* before closing the tab.
- **Sending is simulated.** *Send* records the email as sent; it delivers nothing.
  Wiring this to a real provider is the remaining work, and the review step is
  where that call belongs.
- **Stall prices are event-scoped upstream.** The values in `PRICES` come from the
  production `stall_options` table (Mini $250 / Mini–Debut $200, Standard $450 /
  Standard–Debut $400, Flagship $570 / Flagship–Debut $520). Stalls are priced
  per event there, and neither seeded event is MEL.01 — the tier names match
  exactly, but one Xero invoice line would confirm it outright.
- **Form placeholders are stored as answers.** Some records have values like
  `Select booth type...` where the applicant skipped a dropdown. The table renders
  these as `—`; the underlying data still holds the string.
