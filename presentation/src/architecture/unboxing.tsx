/**
 * What a block of the architecture does, opened from its place in the diagram (Hadi, 8 October 2026, preferred:
 * "unboxing the blocks"; simplified in the overall revision of the same day, points D and E). A block is opened when it
 * first appears, and again at each later talk stage that extends it: then the earlier content recedes and the addition
 * is drawn at full strength, the language the diagram uses for old and new.
 *
 * A panel says what the block does in the time of one sentence of speech: an abstract formalisation, at most one
 * formal line and two short sentences, readable from the back of a hall; what was taken out is in the speaker notes.
 * The belief is classic Bayes over the hypotheses H, H growing at talk stage 4 and the prior depending on the context
 * at talk stage 5; support, fit and the confidence check are short conditions in plain words; the realizer and task
 * choice are algorithms, shown as a few lines of high-level pseudocode (Hadi, preferred: this sets aside the
 * handoff's "no if-then" for these two blocks). No likelihood formula, no survival function, no figures in
 * centimetres.
 *
 * Every formulation is an abstraction of the code and the records:
 * - belief update: shared/recognizer.py (belief = normalise(prior × evidence) over the live hypotheses);
 *   docs/context_knowledge_method.md, sections 6 and 7 (the prior from the context facts);
 * - support: the observation warrant (glossary; context_knowledge_method.md, section 8, condition 3);
 * - confidence check: MetaPlanner._clears_gate (θ = 0.75, hypothesis adequacy, observation warrant, evidence rank);
 * - projection: the admitted task's projection (Projector.project) and the fallback projection (T-D P4);
 * - realizer: realize(), one minimal-shift search per entry, F1 (realization is total); cost = T_r + the cumulative
 *   shift, which is the sum of the holds;
 * - task choice: single_task and full_reorder, only the first hold executed;
 * - fit: hypothesis adequacy and the adequacy finding (glossary §5, §7).
 */

import type { ReactNode } from "react";

import type { TalkStage } from "../talk";

export type Unboxable = "B41" | "B43" | "B44" | "B51" | "B53" | "B54" | "B42";

/** One item of a panel. `words`: a short sentence; `formal`: the formal line (its new part in an `Add` where an
 * extension changes it); `lead` and `cond`: a condition's lead and its parts; `code`: pseudocode, one string per line;
 * `out`: the block's output, set apart below the rest. `until`: the talk stage from which a later item replaces it. */
export interface Item {
  stage: TalkStage;
  until?: TalkStage;
  kind: "words" | "formal" | "lead" | "cond" | "code" | "out";
  content: ReactNode;
}

export interface Box {
  name: string;
  code: string;
  items: Item[];
}

const V = ({ children }: { children: ReactNode }) => <i className="mv">{children}</i>;
/** The part of a formal line a talk stage adds. */
const Add = ({ children }: { children: ReactNode }) => <span className="add">{children}</span>;

const P = (a: ReactNode, b?: ReactNode) => <><V>P</V>({a}{b !== undefined && <> | {b}</>})</>;

export const BOXES: Record<Unboxable, Box> = {
  B41: {
    name: "belief update", code: "B4.1",
    items: [
      { stage: 3, until: 4, kind: "formal",
        content: <>{P(<V>h</V>, <V>o</V>)} ∝ {P(<V>o</V>, <V>h</V>)} · {P(<V>h</V>)}, &nbsp;<V>h</V> ∈ <V>H</V></> },
      { stage: 4, until: 5, kind: "formal",
        content: <>{P(<V>h</V>, <V>o</V>)} ∝ {P(<V>o</V>, <V>h</V>)} · {P(<V>h</V>)}, &nbsp;<V>h</V> ∈ <Add><V>H</V></Add></> },
      { stage: 5, kind: "formal",
        content: <>{P(<V>h</V>, <V>o</V>)} ∝ {P(<V>o</V>, <V>h</V>)} · <Add>{P(<V>h</V>, "context")}</Add>, &nbsp;<V>h</V> ∈ <V>H</V></> },
      { stage: 3, until: 4, kind: "words", content: <><V>H</V>: the hypotheses, her assigned tasks.</> },
      { stage: 4, kind: "words", content: <><V>H</V> grows: her assigned tasks and the foreseeable behaviours.</> },
      { stage: 3, until: 5, kind: "words", content: <><V>o</V>: her observed movement. The prior <V>P</V>(<V>h</V>) is
          equal, for now.</> },
      { stage: 5, kind: "words", content: <>The context sets the prior: break time makes a coffee break more likely.</> },
    ],
  },
  B43: {
    name: "support", code: "B4.3",
    items: [
      { stage: 3, kind: "lead", content: <>A hypothesis has support when</> },
      { stage: 3, kind: "cond", content: <>she moves toward the target of its current action,</> },
      { stage: 3, kind: "cond", content: <>or Anton has just seen her finish the action before it.</> },
    ],
  },
  B44: {
    name: "confidence check", code: "B4.4",
    items: [
      { stage: 3, kind: "lead", content: <>The leading hypothesis is trusted when</> },
      { stage: 3, kind: "cond", content: <>its belief is at least θ = 0.75,</> },
      { stage: 3, kind: "cond", content: <>it has support,</> },
      { stage: 5, kind: "cond", content: <>her movement alone ranks no other hypothesis above it,</> },
      { stage: 6, kind: "cond", content: <>it fits.</> },
      { stage: 3, kind: "out", content: <>Out: the trusted intention, or none.</> },
    ],
  },
  B51: {
    name: "projection", code: "B5.1",
    items: [
      { stage: 2, kind: "words", content: <>From her motion: her present motion, continued.</> },
      { stage: 3, kind: "words", content: <>From her intention: Anton plans her trusted task with the same task knowledge
          it plans its own work with.</> },
      { stage: 3, kind: "formal", content: <><V>her path</V> = <V>plan</V>(trusted intention)</> },
      { stage: 6, kind: "words", content: <>No trusted intention: the projection from her motion is the fallback, until a
          hypothesis is trusted again.</> },
    ],
  },
  B53: {
    name: "realizer", code: "B5.3",
    items: [
      { stage: 3, kind: "code", content: [
        "for each task of Anton's plan, in order:",
        "    hold ← the smallest hold, in ticks, such that",
        "           Anton's path keeps the minimum separation",
        "           from her projected path",
        "cost ← the plan's duration + its holds",
      ] },
      { stage: 3, kind: "words", content: <>Standing still never comes too close: a hold always exists.</> },
    ],
  },
  B54: {
    name: "task choice", code: "B5.4",
    items: [
      { stage: 3, kind: "code", content: [
        "for each candidate (a task, or an order of tasks):",
        "    cost ← realizer(candidate, her projected path)",
        "take the cheapest candidate",
        "carry out its first hold and its first task",
      ] },
      { stage: 3, kind: "words", content: <>A switch or a reorder comes from here. Anton decides again at the next
          change.</> },
    ],
  },
  B42: {
    name: "fit", code: "B4.2",
    items: [
      { stage: 6, kind: "words", content: <>A hypothesis fits while her detours and her standing delay its current action
          no more than is plausible.</> },
      { stage: 6, kind: "out", content: <>When the trusted intention stops fitting, Anton stops trusting it.</> },
      { stage: 6, kind: "out", content: <>No hypothesis fits: her behaviour is unexplained.</> },
    ],
  },
};

/** A block opened at a talk stage: its items up to that talk stage; at an extension the earlier ones recede (a
 * receded sentence keeps its words, a formal line stays with the sentence it belongs to). */
export function Unboxed({ block, stage, side }: { block: Unboxable; stage: TalkStage; side: "left" | "right" }) {
  const box = BOXES[block];
  const shown = box.items.filter((i) => i.stage <= stage && (i.until === undefined || i.until > stage));
  const adds = shown.some((i) => i.stage === stage) && box.items.some((i) => i.stage < stage);
  const state = (i: Item) => (adds ? (i.stage < stage ? " ub-old" : " ub-new") : "");
  const item = (i: Item, k: number) => {
    const cls = state(i);
    switch (i.kind) {
      case "formal":
        return <p key={k} className={`ub-item ub-formal${cls}`}>{i.content}</p>;
      case "code":
        return (
          <pre key={k} className={`ub-item ub-code${cls}`}>
            {(i.content as string[]).map((line, j) => <span key={j}>{line}{"\n"}</span>)}
          </pre>
        );
      case "cond":
        return <p key={k} className={`ub-item ub-cond${cls}`}>{i.content}</p>;
      case "lead":
        return <p key={k} className={`ub-item ub-lead${cls}`}>{i.content}</p>;
      default:
        return <p key={k} className={`ub-item ub-words${cls}`}>{i.content}</p>;
    }
  };
  const body = shown.filter((i) => i.kind !== "out");
  const outs = shown.filter((i) => i.kind === "out");
  return (
    <div className={`unboxed unboxed-${side}`}>
      <div className="ub-head"><span className="ub-name">{box.name}</span><span className="ub-code-name">{box.code}</span></div>
      {body.map(item)}
      {outs.length > 0 && <div className="ub-out">{outs.map(item)}</div>}
    </div>
  );
}
