# ECK v2 UI Design Spec

This document defines the approved Premium Dark UI layout for Exile Creator Kit.

## Window

- Base size: 900 x 780.
- Background: matte black.
- Main content is centered.
- Vertical scrolling is allowed when the screen is small.
- The lower content must remain reachable on small screens.

## Header

- Positioned at the top center.
- Contains:
  - ECK logo
  - Exile Creator Kit title
  - Short description
  - Settings button
  - About button
- Keep the approved header ratio and spacing.
- Do not make the header oversized.

## Selected Video

- Full-width card.
- Contains:
  - Selected Video heading
  - Large Drag & Drop area
  - Choose Video button
  - Media information
- Use the approved dark wine red as the accent color.

## Center Columns

The middle area uses two columns.

Left column:

- Export card
- Export for X
- Export for YouTube

Right column:

- Status card
- Status text
- Progress
- Message
- Open Output Folder
- Open Log Folder

## Recent Exports

- Full-width card at the bottom.
- Displays export history.
- If empty, use the existing empty state text.

## Colors

- Matte black background.
- Dark charcoal cards.
- White to silver text.
- Dark wine red accent.
- Bright red is not allowed.
- Keep the currently approved dark red values.

## Typography

- Prefer Segoe UI Semibold for headings.
- Avoid excessive bold weight.
- Use readable font sizes and spacing on Windows.
- Reduce blurry text by using moderate size and weight.

## Cards

- Cards must have a visible border.
- Cards must have enough internal padding.
- Spacing between cards should be consistent.
- Excessive glow and heavy shadows are not allowed.

## Buttons

- Use dark wine red or dark gray.
- Hover states must not use bright red.
- Export should stand out through size and placement.
- Do not change processing callbacks.

## Protected Behavior

Do not change:

- Export processing logic.
- History processing.
- Drag & Drop behavior.
- Status update behavior.
- Settings / About callbacks.
- Save paths or AppData behavior.
