/**
 * The parts every slide is made of: the slide itself (its section, its 16:9 stage, its footer and its speaker notes),
 * a step, a TODO box, a mark for what is not settled, a talk stage's transition (the seven talk stages as a list, the
 * starting one with its three columns), and the architecture at a talk stage. Text and keywords come from talk.ts.
 */

import { createContext, type ReactNode, type RefObject, useContext, useRef } from "react";

import { Architecture, type Colouring } from "../architecture/Architecture";
import { type Unboxable, Unboxed } from "../architecture/unboxing";
import { ELEMENTS } from "../architecture/model";
import { useCurrent, useNear, useShown, useVisibleCount } from "../Deck";
import { BUILT_STAGES, footerText, QUESTION_HEADER, QUESTIONS, STAGES, type TalkStage } from "../talk";

const SlideContext = createContext<RefObject<HTMLElement | null> | null>(null);

/** One slide. `notes` are the speaker notes (never projected); `footer` false for a slide that stands outside the
 * talk stages' flow (the title slide). */
export function Slide({ stage, notes, children, className = "", footer = true }: {
  stage: TalkStage; notes: ReactNode; children: ReactNode; className?: string; footer?: boolean;
}) {
  const section = useRef<HTMLElement>(null);
  return (
    <section ref={section} data-talk-stage={stage}>
      <SlideContext.Provider value={section}>
        <div className={`stage ${className}`}>
          {children}
          {footer && <div className="footer">{footerText(stage)}</div>}
        </div>
      </SlideContext.Provider>
      <aside className="notes">{notes}</aside>
    </section>
  );
}

/** Whether the slide this is called in is the current one or next to it: heavy content mounts only then. */
export function useSlideNear(): boolean {
  const section = useContext(SlideContext);
  if (section === null) throw new Error("useSlideNear outside a Slide");
  return useNear(section);
}

/** Whether the slide this is called in is the current one: a canvas renders only then. */
export function useSlideCurrent(): boolean {
  const section = useContext(SlideContext);
  if (section === null) throw new Error("useSlideCurrent outside a Slide");
  return useCurrent(section);
}

/** How many of the slide's elements matching `selector` are shown steps now. */
export function useSlideSteps(selector: string): number {
  const section = useContext(SlideContext);
  if (section === null) throw new Error("useSlideSteps outside a Slide");
  return useVisibleCount(section, selector);
}

/** A step of a slide: a hidden marker that a click shows; `shown` tells the slide. */
export function useStep(): [RefObject<HTMLSpanElement | null>, boolean] {
  const ref = useRef<HTMLSpanElement>(null);
  return [ref, useShown(ref)];
}

export function StepMarker({ r }: { r: RefObject<HTMLSpanElement | null> }) {
  return <span className="fragment step-marker" ref={r} aria-hidden />;
}

/** A place on a slide still to be filled: what is to be shown there and why. `by`: the part of T-pres that fills it,
 * or Hadi for material he supplies. */
export function Todo({ by, children, className = "" }: { by: string; children: ReactNode; className?: string }) {
  return (
    <div className={`todo ${className}`}>
      <div className="todo-head">TODO · {by}</div>
      <div className="todo-body">{children}</div>
    </div>
  );
}

/** A mark on a slide whose content is not settled: Hadi's word is needed (listed in the report of the revision that
 * set it). Small, in a corner, never in the way of the content. */
export function Unsettled({ children }: { children: ReactNode }) {
  return <div className="unsettled"><span className="unsettled-head">not settled</span> {children}</div>;
}

export function StageTitle({ stage }: { stage: TalkStage }) {
  return (
    <h1 className="stage-title"><span className="stage-n">{stage}</span>{STAGES[stage].title}</h1>
  );
}

/** The transition into a talk stage 1 to 7 (the overall revision, point B): the seven talk stages as numbered circles
 * joined by a line, the starting one larger and bold, the finished ones marked done (a check and a quiet colour), the
 * coming ones plain; beside them the starting talk stage's three columns (what I know, believe, decide). */
export function Transition({ stage }: { stage: TalkStage }) {
  const row = STAGES[stage];
  return (
    <div className="transition">
      <ol className="steps">
        {BUILT_STAGES.map((n) => {
          const state = n < stage ? "done" : n === stage ? "now" : "coming";
          return (
            <li key={n} className={`step step-${state}`}>
              <span className="step-circle" aria-label={state === "done" ? `${n}, done` : `${n}`}>
                {state === "done" ? "✓" : n}
              </span>
              <span className="step-text">
                <span className="step-label">{STAGES[n].title}</span>
                <span className="step-line">{STAGES[n].line}</span>
              </span>
            </li>
          );
        })}
      </ol>
      <div className="transition-columns">
        {QUESTIONS.map((q) => (
          <div key={q} className={`tcol column-${q}`}>
            <h2 className="tcol-head">{QUESTION_HEADER[q]}</h2>
            {(row.columns[q] ?? []).length === 0 ? <p className="tcol-empty">–</p> : (
              <ul>{row.columns[q]!.map((k) => <li key={k}>{k}</li>)}</ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/** The slide that opens a talk stage 1 to 7. */
export function TransitionSlide({ stage, notes }: { stage: TalkStage; notes: ReactNode }) {
  return (
    <Slide stage={stage} className="transition-slide" notes={notes}>
      <Transition stage={stage} />
    </Slide>
  );
}

/** The architecture at a talk stage. With `step`, the slide opens on the state before the talk stage and a click adds
 * what it adds (at talk stage 0, the three questions over the empty frames); without, it shows the talk stage's state
 * at once. Then, one click each: a `caption`, and the blocks of `opens` in their order, each opened from its place into
 * a panel (unboxing.tsx) while the rest of the diagram recedes. */
export function ArchitectureView({ stage, step = true, colouring = "new", questionTags = false, title, caption, opens = [] }: {
  stage: TalkStage; step?: boolean; colouring?: Colouring; questionTags?: boolean; title: string; caption?: string;
  opens?: Unboxable[];
}) {
  const [marker, shown] = useStep();
  const near = useSlideNear();
  const section = useContext(SlideContext)!;
  const opened = useVisibleCount(section, ".step-open");
  const focus = opened === 0 ? null : opens[opened - 1];
  const x = focus === null ? 0 : ELEMENTS.find((e) => e.id === focus)!.box.x;
  return (
    <>
      {title !== "" && <h1 className="arch-title">{title}</h1>}
      <div className="arch-box">
        {near && <Architecture stage={stage} revealed={step && stage > 0 ? shown : true} colouring={colouring}
                               questionTags={questionTags} tagsShown={step ? shown : true} focus={focus} />}
        {near && opens.map((b) => (
          <div key={b} className={`ub-slot${b === focus ? " ub-on" : ""}`}>
            <Unboxed block={b} stage={stage} side={x < 1000 ? "right" : "left"} />
          </div>
        ))}
      </div>
      {step && <StepMarker r={marker} />}
      {caption !== undefined && <p className="arch-caption fragment">{caption}</p>}
      {opens.map((b) => <span key={b} className="fragment step-marker step-open" aria-hidden />)}
    </>
  );
}
