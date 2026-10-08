/**
 * Mathematical typesetting on the slides (Hadi, 8 October 2026, preferred, tpres-v5): every formal line in TeX style,
 * with a mathematical font, typeset by KaTeX (pinned; its fonts are bundled into the build by Vite, so the deck loads
 * nothing from outside). `trust` allows \htmlClass, with which a formal line marks the part a talk stage adds (the
 * class "add", deck.css); the strings are the deck's own.
 */

import katex from "katex";
import "katex/dist/katex.min.css";
import { useMemo } from "react";

export function Tex({ children, display = false }: { children: string; display?: boolean }) {
  const html = useMemo(() => katex.renderToString(children, {
    displayMode: display, throwOnError: true, trust: true, strict: "ignore",
  }), [children, display]);
  return <span className={display ? "tex tex-display" : "tex"} dangerouslySetInnerHTML={{ __html: html }} />;
}
