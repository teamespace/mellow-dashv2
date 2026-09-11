# Changelog

## 2026-09-11

- Added dashboard table multi-selection, including select-current-page and
  selection-aware controls.
- Added bulk application status updates using the existing Pending, Accepted,
  Waitlisted and Rejected workflow.
- Changed the dashboard Delete action so it removes only selected submissions;
  selecting every submission retains the stronger typed `DELETE` safeguard.
- Added a path-isolated Cloudflare Worker deployment for
  `https://dev.elx.onl/mellowdashv2/`. Authentication and all other
  `dev.elx.onl` routes continue to be handled by the existing `dev-elx` Worker.
