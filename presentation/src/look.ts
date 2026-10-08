/**
 * The deck's own colours, beside the web-ui's theme (webui/page/src/theme.ts), which holds every other colour, the
 * font and the weights. The web-ui reserves blue for the robot and orange for the human; the three questions get
 * three further hues, kept apart from those two and from each other in lightness as well as hue (no red and green
 * pair). They mark a column's header on every talk stage and colour the architecture by question at the recap.
 */

import type { Question } from "./talk";

export const QUESTION_COLOUR: Record<Question, { ink: string; tint: string }> = {
  know: { ink: "#6A55A3", tint: "#EEEAF6" },      // violet
  believe: { ink: "#23767D", tint: "#E3F0F0" },   // teal
  decide: { ink: "#9C7424", tint: "#F5EEDD" },    // ochre
};

/** The look's values as CSS variables on the document, beside applyTheme's. */
export function applyLook(): void {
  const root = document.documentElement.style;
  for (const [q, c] of Object.entries(QUESTION_COLOUR)) {
    root.setProperty(`--q-${q}`, c.ink);
    root.setProperty(`--q-${q}-tint`, c.tint);
  }
}
