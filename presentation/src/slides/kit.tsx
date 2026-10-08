/**
 * The parts every slide is made of: the slide itself (its section, its 16:9 stage, its footer and its speaker notes),
 * a step, a TODO box, a talk stage's card with the three questions as columns, a level's title, and the architecture
 * at a talk stage. Text and keywords come from talk.ts.
 */

import { createContext, type ReactNode, type RefObject, useContext, useRef } from "react";

import { Architecture, type Colouring } from "../architecture/Architecture";
import { useNear, useShown } from "../Deck";
import { footerText, LEVELS, QUESTION_HEADER, QUESTIONS, STAGES, type TalkStage } from "../talk";

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
          {footer && <div className="footer">{stage === 0 ? "Opening" : footerText(stage)}</div>}
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

export function StageTitle({ stage }: { stage: TalkStage }) {
  return (
    <h1 className="stage-title"><span className="stage-n">{stage}</span>{STAGES[stage].title}</h1>
  );
}

/** A talk stage's card: its title and the three questions as columns, with the keywords of section 5; a column the
 * talk stage leaves empty shows a dash. `children` go below the columns (a scene, a TODO box). */
export function StageCard({ stage, children }: { stage: TalkStage; children?: ReactNode }) {
  const row = STAGES[stage];
  return (
    <>
      <StageTitle stage={stage} />
      <div className="columns">
        {QUESTIONS.map((q) => (
          <div key={q} className={`column column-${q}`}>
            <h2 className="column-head">{QUESTION_HEADER[q]}</h2>
            {(row.columns[q] ?? []).length === 0 ? <p className="column-empty">–</p> : (
              <ul>{row.columns[q]!.map((k) => <li key={k}>{k}</li>)}</ul>
            )}
          </div>
        ))}
      </div>
      {children}
    </>
  );
}

/** A level's title and its sub-line. */
export function LevelTitle({ level }: { level: 1 | 2 | 3 }) {
  const l = LEVELS[level];
  return (
    <div className="level">
      <div className="level-n">Level {l.n}</div>
      <h1 className="level-title">{l.title}</h1>
      <p className="level-sub">{l.sub}</p>
    </div>
  );
}

/** The architecture at a talk stage. With `step`, the slide opens on the state before the talk stage and a click adds
 * what it adds (at talk stage 0, the three questions over the empty frames); without, it shows the talk stage's state
 * at once. */
export function ArchitectureView({ stage, step = true, colouring = "new", questionTags = false, title }: {
  stage: TalkStage; step?: boolean; colouring?: Colouring; questionTags?: boolean; title: string;
}) {
  const [marker, shown] = useStep();
  const near = useSlideNear();
  return (
    <>
      {title !== "" && <h1 className="arch-title">{title}</h1>}
      <div className="arch-box">
        {near && <Architecture stage={stage} revealed={step && stage > 0 ? shown : true} colouring={colouring}
                               questionTags={questionTags} tagsShown={step ? shown : true} />}
      </div>
      {step && <StepMarker r={marker} />}
    </>
  );
}
