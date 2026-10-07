/**
 * A border between two panels that the screen-user drags to change their sizes (T-viz 1c; Hadi, 7 October 2026,
 * preferred, point 9): between the upper row and panel 4c, and between the side panels and the env-pane. A thin line that
 * shows a handle under the pointer; a drag moves it, a double click returns its panel to the default size. The sizes are
 * the page's layout, remembered in this browser (src/frame/layout.ts).
 */

import { useRef } from "react";

export function Splitter({ axis, size, onSize, onReset, label }: {
  /** "x": a vertical border dragged left and right; "y": a horizontal border dragged up and down. */
  axis: "x" | "y";
  /** The size the drag changes, read at the drag's start, and how a pointer's movement changes it (+1 or −1). */
  size: { value: () => number; sign: 1 | -1 };
  onSize: (value: number) => void;
  onReset: () => void;
  label: string;
}) {
  const start = useRef<{ at: number; value: number } | null>(null);
  return (
    <div className={`splitter splitter-${axis}`} role="separator" aria-orientation={axis === "x" ? "vertical" : "horizontal"}
         aria-label={label} title={`${label}: drag; double click resets`}
         onPointerDown={(e) => {
           e.currentTarget.setPointerCapture(e.pointerId);
           start.current = { at: axis === "x" ? e.clientX : e.clientY, value: size.value() };
           document.body.classList.add(`is-resizing-${axis}`);
         }}
         onPointerMove={(e) => {
           if (start.current === null) return;
           const moved = (axis === "x" ? e.clientX : e.clientY) - start.current.at;
           onSize(start.current.value + size.sign * moved);
         }}
         onPointerUp={(e) => {
           e.currentTarget.releasePointerCapture(e.pointerId);
           start.current = null;
           document.body.classList.remove(`is-resizing-${axis}`);
         }}
         onDoubleClick={onReset}>
      <i />
    </div>
  );
}
