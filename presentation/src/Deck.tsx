/**
 * The deck: reveal.js over the slides React renders. reveal's own layout is off (`disableLayout`): it scales a slide
 * with CSS zoom or a transform, under which a WebGL canvas is measured and drawn at the wrong size. The stage is sized
 * by deck.css instead, in the unit --u (1/1920 of a 16:9 stage that fits the screen).
 */

import Reveal from "reveal.js";
import { useEffect, useRef } from "react";

import { S01Robot } from "./slides/S01Robot";

export function Deck() {
  const root = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const deck = new Reveal(root.current!, {
      disableLayout: true,
      hash: true,           // a reload stays on its slide
      controls: false,      // a clicker or the keyboard
      progress: false,
      transition: "fade",
    });
    deck.initialize();
    return () => deck.destroy();
  }, []);
  return (
    <div className="reveal" ref={root}>
      <div className="slides">
        <S01Robot />
      </div>
    </div>
  );
}
