# Shared UI primitives

**OWNER: UI/UX track** — GRP6 builds the components, MINIONS owns the tokens in
`src/styles/theme.css`, ASTERIX owns mobile layout and the handoff to FE.

This directory is empty on purpose. Fill it deliberately.

## Install only what gets used

shadcn/ui components are copied into your repo rather than installed as a
dependency, which makes it very easy to accumulate files nobody imports. The
reference implementation vendors **49** of them and imports **6** — all from a
single screen. Its three main screens ignore the design system entirely and
hardcode Tailwind utility strings, and each one re-implements its own header
inline.

Add a component when a screen needs it. Not before.

## The six that are actually needed

These are the pieces the reference app copy-pasted two or three times instead of
extracting. Building them is your Sprint 1:

| Component | Why |
|---|---|
| `AppHeader` | Re-implemented inline on every screen there |
| `PhotoModal` | Full-screen photo view, duplicated twice |
| `MonthCalendar` | The 7-column grid plus its legend, duplicated twice |
| `AttendanceRow` | One record in a list, duplicated three times |
| `StatCard` | The count-with-a-label tile on the dashboard |
| `EmptyState` | Nothing to show yet — and nobody ever designs this one |

## The rule

Components read from tokens; they do not hardcode colour. The test: change one
value in `theme.css` and watch it move on every screen. If you have to edit a
component to change a colour, the design system is not doing its job.
