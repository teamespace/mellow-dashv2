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

## Cloudflare demo deployment

The demo at `https://dev.elx.onl/mellowdashv2/` is deployed through the
path-isolated Worker in `cloudflare/`. Its routes match only `/mellowdashv2`
and `/mellowdashv2/*`; the existing `dev-elx` Worker remains responsible for
authentication and every other path on the hostname.

Generate the private deployment artifact with the current live/approved CSV:

```bash
python3 build_dashboard.py path/to/inquiries-export.csv cloudflare/public/mellowdashv2/index.html
```

Then validate and deploy it with the checked-in configuration:

```bash
npx wrangler deploy --dry-run --config cloudflare/wrangler.jsonc
npx wrangler deploy --config cloudflare/wrangler.jsonc
```

`cloudflare/public/` is ignored because the generated HTML embeds applicant
data. Never commit that directory, a CSV export, login credentials, or API
tokens.

## What's in it

### Inquiries

- Search, and filters for application status, payment, **email state**, event and archive
- Table / list / card views; 10 rows per page by default, with a Rows selector (10/20/50/100)
- Bulk-select submissions in the table (including the current page), then apply
  an application status or delete only the selected records after confirmation
- Inline status editing and internal notes. `Withdrawn` is part of the application
  status flow rather than a separate dashboard flag
- Accepted submissions unlock `Assign stall`; `Send invoice` appears in Payment
  only after an available stall is selected. Other statuses expose `Send email`
  directly in Payment
- Copy emails, export the filtered set as CSV, and a full ZIP backup
  (CSV + browsable HTML + one image per record), written in-browser

**Columns are user-controlled.** The table shows eight columns by default and
fits a 1280px window with no horizontal scrolling. The *Columns* button opens a
picker for seven more (insurance, applied-before, secondary category, Instagram,
invoice, decided date, sharing); the choice is saved per browser. Reference is
always shown. Everything else lives in the centered submission modal.

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

## Status, stall and send flow

Status changes and send actions are separate and intentionally visible in the
table rather than hidden in the submission modal. Closed Application and Payment
controls remain colour-coded badges, while their opened option panels use one
neutral white treatment. Rejected is red while Withdrawn is violet so they remain
distinguishable.

1. **Pending, Waitlisted, Rejected or Withdrawn.** Payment shows *Send email*.
   Changing to one of these statuses prepares the matching status email, and the
   button opens a compact confirmation before recording it as sent.
2. **Accepted, no stall.** Stall shows *Assign stall* and Payment says
   *Assign stall first*. Every configured stall option remains available because
   capacity and duplicate-assignment rules have not been formally defined yet.
3. **Accepted, stall assigned.** Payment shows *Send invoice*. Confirming it
   changes payment to *Awaiting payment* and records the Approval / invoice email
   as sent.
4. **Leaving Accepted.** If a stall is assigned, a confirmation explains that it
   will be released. Existing invoice and payment history is preserved.

Bulk email and invoice sending are deliberately not included. Email and invoice
actions remain explicit per-row actions with confirmation.

The centered submission modal is informational only; it contains no email queue,
reason editor or template preview.

Four columns carry this workflow and are included in CSV exports:
`Email state`, `Email template`, `Email reason`, `Email sent at`.

Existing records with no email tracking can still use the direct *Send email*
button. A matching sent state prevents an accidental duplicate until the status
changes again.

## Known limits

This is a front-end prototype. It is convincing, and it does not persist.

- **No backend.** Every edit — status, stall, payment, notes, email state — lives
  in memory and is lost on reload. Use *Backup data* before closing the tab.
- **Sending is simulated.** *Send email* and *Send invoice* update in-memory state;
  they deliver nothing. Each send confirmation states this before the action is recorded.
- **Stall capacity is not enforced.** Every configured option is shown for every
  accepted submission, so multiple submissions can choose the same stall type.
  Add capacity or inventory rules only after the operational mechanism is confirmed.
- **Stall prices are event-scoped upstream.** The values in `PRICES` come from the
  production `stall_options` table (Mini $250 / Mini–Debut $200, Standard $450 /
  Standard–Debut $400, Flagship $570 / Flagship–Debut $520). Stalls are priced
  per event there, and neither seeded event is MEL.01 — the tier names match
  exactly, but one Xero invoice line would confirm it outright.
- **Form placeholders are stored as answers.** Some records have values like
  `Select booth type...` where the applicant skipped a dropdown. The table renders
  these as `—`; the underlying data still holds the string.
