/**
 * The deck: reveal.js over the slides React renders. reveal's own layout is off (`disableLayout`): it scales a slide
 * with CSS zoom or a transform, under which a WebGL canvas is measured and drawn at the wrong size. The stage is sized
 * by deck.css instead, in the unit --u (1/1920 of a 16:9 stage that fits the screen).
 *
 * A step of a slide is a reveal fragment; a slide reads whether its fragment is shown (useShown). A mouse click
 * advances, as the clicker's key does.
 */

import Reveal from "reveal.js";
import { createContext, type RefObject, useContext, useEffect, useRef, useState } from "react";

import { S01Robot } from "./slides/S01Robot";

type RevealApi = InstanceType<typeof Reveal>;

const DeckContext = createContext<RevealApi | null>(null);

export function Deck() {
  const root = useRef<HTMLDivElement>(null);
  const [deck, setDeck] = useState<RevealApi | null>(null);
  useEffect(() => {
    const el = root.current!;
    const d = new Reveal(el, {
      disableLayout: true,
      hash: true,           // a reload stays on its slide and step
      controls: false,      // a clicker or the keyboard
      progress: false,
      transition: "fade",
    });
    let live = true;      // StrictMode's second run: the first deck may resolve after its own destroy
    d.initialize().then(() => { if (live) setDeck(d); });
    const next = () => d.next();
    el.addEventListener("click", next);
    return () => {
      live = false;
      el.removeEventListener("click", next);
      d.destroy();
      setDeck(null);
    };
  }, []);
  return (
    <DeckContext.Provider value={deck}>
      <div className="reveal" ref={root}>
        <div className="slides">
          <S01Robot />
        </div>
      </div>
    </DeckContext.Provider>
  );
}

/** Whether a fragment of the deck is shown now. */
export function useShown(fragment: RefObject<HTMLElement | null>): boolean {
  const deck = useContext(DeckContext);
  const [shown, setShown] = useState(false);
  useEffect(() => {
    if (deck === null) return;
    const update = () => setShown(fragment.current?.classList.contains("visible") ?? false);
    const events = ["fragmentshown", "fragmenthidden", "slidechanged"];
    for (const e of events) deck.on(e, update);
    update();
    return () => { for (const e of events) deck.off(e, update); };
  }, [deck, fragment]);
  return shown;
}
