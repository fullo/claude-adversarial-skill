# UX verification targets (Step 3)

Part of the adversarial-verify skill. Step numbers and section names with no file name are in `SKILL.md`; paths are relative to the skill's folder. Read this file when UX is in the target.

**UX:** adapt each point to the kind of interface (web, native app, game, command-line or terminal); WCAG 2.2 is the reference where it applies. Check, in every target format (sizes, input methods, themes):
- **Render**: the layout holds in each format; nothing is cut off or off screen; navigation stays reachable.
- **Contrast**: text at least 4.5:1 (3:1 for large text), graphics and the boundaries of controls at least 3:1, in every theme including dark mode. Compute the ratio from the actual colours; do not estimate it. A computed failure is a demonstrated defect when the artifact shows those values apply (no later rule, theme or fallback overrides them); otherwise it is a preventive measure until the rendered check.
- **Legibility**: text size for the viewing distance, line length, heading hierarchy; zoom to 200% and reflow at 320 px wide without loss of content, where the platform has them.
- **Targets**: the size of what is touched or clicked, against the project's threshold or WCAG 2.5.8.
- **Keyboard, controller and focus**: everything reachable with each supported input, the focus visible from the viewing distance, the order logical.
- **Real content**: long names, translations longer than the original, empty values, many items.
- **States**: empty, loading, error, success; error messages shown where they are seen, next to what caused them (their wording is Documentation).
- **Basic accessibility**: labels on fields, text alternatives for images, an accessible name for icon-only buttons.
- **Motion and perceived speed**: reduced-motion preferences respected; time to the first useful content on a slow network or device.
- **Sensitive data**: no secrets or personal data visible on screen, in screenshots or recordings.

**UX check round.** Suggest a check of the main screens in the project's target formats, using its interface tests if it has any. It is a run, so it is proposed under Execution and consent, with the screens, formats and inputs it covers. A measured fact (a width, a colour pair) can be computed by reasoning; how the screen really renders cannot.

**Alternative interfaces.** For each weak point found, suggest one or two alternatives with a short comparison: what each improves, what it makes worse, and its cost. The verifier describes the alternatives in the Fix of the FAIL row; when a choice between them is open, it suggests a mock-up as in Step 1c (`references/pre-code.md`), listed in the same Fix.
