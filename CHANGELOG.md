# Changelog

## 2026-09-22

- Integrated the Nova-inspired Email Templates library and focused block editor
  into the dashboard shell, with persistent sidebar/hash routing so refreshing
  the page keeps the current Email Templates view.
- Added Global and event filtering while retaining the five protected
  status-linked templates: Application received, Approval / invoice, Rejection,
  Waitlist and Withdrawal confirmation.
- Added drag-and-drop outline reordering and keyboard controls for selected
  blocks: `Ctrl/Cmd+D` to duplicate, Arrow Up/Down to move and Delete to remove.
- Replaced the header-logo URL field with an image upload, including an optional
  custom-width control, and added editable social-account links to shared branding.
- Added a recipient-address confirmation modal for Send test. This remains a
  local simulation and does not deliver email.
- Refined the template cards, editor top bar and create-template dialog; the
  latter now closes from its top-right icon, backdrop click or Escape.

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
