/**
 * The page's layout the screen-user sets by dragging the borders (T-viz 1c, point 9): the widths of the two side panels
 * and the height of panel 4c, each kept within its bounds, remembered in this browser (a convenience; a fresh browser
 * opens with the defaults).
 */

export interface Layout {
  left: number;     // px: panel 4a's width
  right: number;    // px: panel 4b's width
  bottom: number | null;   // px: panel 4c's height; null: fitted to its lanes (up to FIT of the window)
}

export const BOUNDS = {
  left: { min: 240, max: 640 },
  right: { min: 260, max: 640 },
  bottom: { min: 120 },
} as const;

/** Panel 4c's height while it is fitted to its lanes, at most this share of the window. */
export const FIT = 0.55;

/** The defaults: the side panels as before; panel 4c fitted to its lanes until its border is dragged. */
export function defaults(): Layout {
  return { left: 360, right: 340, bottom: null };
}

/** A size kept within its bounds. */
export function bounded(value: number, min: number, max: number): number {
  return Math.round(Math.min(max, Math.max(min, value)));
}

const KEY = "tviz.layout";

export function remembered(): Layout {
  const d = defaults();
  try {
    const saved = JSON.parse(window.localStorage.getItem(KEY) ?? "null") as Partial<Layout> | null;
    if (saved === null) return d;
    return {
      left: typeof saved.left === "number" ? bounded(saved.left, BOUNDS.left.min, BOUNDS.left.max) : d.left,
      right: typeof saved.right === "number" ? bounded(saved.right, BOUNDS.right.min, BOUNDS.right.max) : d.right,
      bottom: typeof saved.bottom === "number" ? Math.max(BOUNDS.bottom.min, Math.round(saved.bottom)) : d.bottom,
    };
  } catch {
    return d;
  }
}

export function remember(layout: Layout): void {
  try { window.localStorage.setItem(KEY, JSON.stringify(layout)); } catch { /* kept for the page's life only */ }
}
