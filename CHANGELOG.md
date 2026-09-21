# Changelog

## 2026-09-21

- Moved Withdrawn into the application status flow and removed its separate
  dashboard column/filter treatment.
- Added the Accepted → Assign stall → Send invoice sequence in the Stall and
  Payment columns, with all stall options always available and release confirmation.
- Added direct Send email actions for Pending, Waitlisted, Rejected and Withdrawn
  submissions; bulk email sending is intentionally excluded for now.
- Replaced the detail drawer with a centered, read-only submission modal and
  removed the queue/reason/template-preview workflow from submission details.
- Clarified the bulk toolbar hierarchy with a dynamic primary `Apply <status>`
  action and secondary `Clear selection`.
- Kept editable Application and Payment triggers as colour-coded badges while
  making both opened option panels neutral; Rejected remains red and Withdrawn violet.
- Expanded inquiry search to include internal notes.

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
