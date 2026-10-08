/**
 * The deck: reveal.js over the slides React renders. reveal's own layout is off (`disableLayout`): it scales a slide
 * with CSS zoom or a transform, under which a WebGL canvas is measured and drawn at the wrong size. The stage is sized
 * by deck.css instead, in the unit --u (1/1920 of a 16:9 stage that fits the screen).
 *
 * A step of a slide is a reveal fragment; a slide reads whether its fragment is shown (useShown). A mouse click
 * advances, as the clicker's key does. Speaker notes are reveal's (`aside.notes`, the key S opens the speaker view);
 * they never show on the projected screen.
 *
 * A slide's heavy content (a 3D scene, the architecture diagram) is mounted only while the slide is the current one
 * or next to it (useNear), so that the browser holds a few WebGL contexts at a time, never one per slide.
 */

import Reveal from "reveal.js";
import RevealNotes from "reveal.js/plugin/notes";
import { createContext, type RefObject, useContext, useEffect, useRef, useState } from "react";

import { SLIDES } from "./slides";

type RevealApi = InstanceType<typeof Reveal>;

declare global {
  interface Window { deck?: RevealApi }     // for the click-through script (scripts/shots.mjs)
}

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
      transitionSpeed: "fast",
      plugins: [RevealNotes],
    });
    let live = true;      // StrictMode's second run: the first deck may resolve after its own destroy
    d.initialize().then(() => { if (live) { setDeck(d); window.deck = d; } });
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
          {SLIDES.map((S, i) => <S key={i} />)}
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

/** Whether a slide (its section) is the current one or next to it. */
export function useNear(section: RefObject<HTMLElement | null>): boolean {
  const deck = useContext(DeckContext);
  const [near, setNear] = useState(false);
  useEffect(() => {
    if (deck === null) return;
    const update = () => {
      const el = section.current;
      if (el === null) return;
      setNear(Math.abs(deck.getIndices(el).h - deck.getIndices().h) <= 1);
    };
    deck.on("slidechanged", update);
    deck.on("ready", update);
    update();
    return () => { deck.off("slidechanged", update); deck.off("ready", update); };
  }, [deck, section]);
  return near;
}

/** Whether a slide (its section) is the current one. */
export function useCurrent(section: RefObject<HTMLElement | null>): boolean {
  const deck = useContext(DeckContext);
  const [current, setCurrent] = useState(false);
  useEffect(() => {
    if (deck === null) return;
    const update = () => setCurrent(section.current !== null && deck.getCurrentSlide() === section.current);
    deck.on("slidechanged", update);
    deck.on("ready", update);
    update();
    return () => { deck.off("slidechanged", update); deck.off("ready", update); };
  }, [deck, section]);
  return current;
}

/** How many of a slide's elements matching `selector` are shown fragments now (the steps a slide has taken). */
export function useVisibleCount(section: RefObject<HTMLElement | null>, selector: string): number {
  const deck = useContext(DeckContext);
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (deck === null) return;
    const update = () => setCount(section.current?.querySelectorAll(`${selector}.visible`).length ?? 0);
    const events = ["fragmentshown", "fragmenthidden", "slidechanged"];
    for (const e of events) deck.on(e, update);
    update();
    return () => { for (const e of events) deck.off(e, update); };
  }, [deck, section, selector]);
  return count;
}
