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
 * Formal lines and pseudocode are typeset in TeX style by KaTeX (../tex.tsx; Hadi, tpres-v5). The codes of the blocks
 * (B4.1 and so on) stay here as internal labels; no slide shows them (Hadi, tpres-v5).
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
import { Tex } from "../tex";

export type Unboxable = "B41" | "B43" | "B44" | "B51" | "B53" | "B54" | "B42";

/** One item of a panel. `words`: a short sentence (its symbols typeset, `T`); `formal`: the formal line, a TeX string
 * (its new part in \htmlClass{add} where an extension changes it); `lead` and `cond`: a condition's lead and its parts;
 * `code`: pseudocode, one TeX string per line, typeset as an algorithm; `options`: a block's options side by side, each
 * a bold name and a short gloss; `out`: the block's output, set apart below the rest. `until`: the talk stage from which
 * a later item replaces it. */
export interface Item {
  stage: TalkStage;
  until?: TalkStage;
  kind: "words" | "formal" | "lead" | "cond" | "code" | "options" | "out";
  content: ReactNode;
}

export interface Box {
  name: string;
  /** The name of the block's approach, under its name (the realizer's, Hadi, tpres-v6). */
  approach?: string;
  code: string;
  items: Item[];
}

const T = ({ children }: { children: string }) => <Tex>{children}</Tex>;

/** The belief update's formal line; `add` marks the part a talk stage adds (\htmlClass{add}). */
const BAYES = String.raw`P(h \mid o) \;\propto\; P(o \mid h)\,`;

export const BOXES: Record<Unboxable, Box> = {
  B41: {
    name: "belief update", code: "B4.1",
    items: [
      { stage: 3, until: 4, kind: "formal", content: String.raw`${BAYES} P(h), \qquad h \in H` },
      { stage: 4, until: 5, kind: "formal", content: String.raw`${BAYES} P(h), \qquad h \in \htmlClass{add}{H}` },
      { stage: 5, kind: "formal",
        content: String.raw`${BAYES} \htmlClass{add}{P(h \mid \text{context})}, \qquad h \in H` },
      { stage: 3, until: 4, kind: "words", content: <><T>H</T>: the hypotheses, her assigned tasks.</> },
      { stage: 4, kind: "words", content: <><T>H</T> grows: her assigned tasks and the foreseeable behaviours.</> },
      { stage: 3, until: 5, kind: "words", content: <><T>o</T>: her observed movement. The prior <T>P(h)</T> is
          equal, for now.</> },
      { stage: 5, kind: "words", content: <>The context sets the prior: break time makes a coffee break more likely.</> },
    ],
  },
  B43: {
    name: "support", code: "B4.3",
    items: [
      { stage: 3, kind: "cond", content: <>She moves toward its next target,</> },
      { stage: 3, kind: "cond", content: <>or robot saw her finish the step before.</> },
    ],
  },
  B44: {
    name: "confidence check", code: "B4.4",
    items: [
      { stage: 3, kind: "lead", content: <>The leading hypothesis is recognised when</> },
      { stage: 3, kind: "cond", content: <>its belief is at least <T>{String.raw`\theta = 0.75`}</T>,</> },
      { stage: 3, kind: "cond", content: <>it has support,</> },
      { stage: 5, kind: "cond", content: <>her movement alone ranks no other hypothesis above it,</> },
      { stage: 6, kind: "cond", content: <>it fits.</> },
      { stage: 3, kind: "out", content: <>Out: the recognised intention, or none.</> },
    ],
  },
  B51: {
    name: "projection", code: "B5.1",
    items: [
      { stage: 2, kind: "words", content: <>From her motion: her present motion, continued.</> },
      { stage: 3, kind: "words", content: <>From her intention: robot plans her task with its own task knowledge.</> },
      { stage: 3, kind: "formal", content: String.raw`\text{her path} = \operatorname{plan}(\text{recognised intention})` },
      { stage: 6, kind: "words", content: <>No hypothesis fits, so no recognised intention: the projection from her motion
          is the fallback.</> },
    ],
  },
  B53: {
    name: "realizer", approach: "Spatio-temporal conflict resolution", code: "B5.3",
    items: [
      { stage: 3, kind: "code", content: [
        String.raw`\textbf{for each}\ \text{task } k \text{ of the plan:}`,
        String.raw`\quad \delta_k \leftarrow \min\,\{\delta \ge 0 : \operatorname{dist}(\text{robot},\ \text{her path}) \ge d_{\min}\}`,
        String.raw`\mathit{cost} \leftarrow T + \textstyle\sum_k \delta_k`,
      ] },
      { stage: 3, kind: "words", content: <><T>{String.raw`\delta_k`}</T>: a hold in ticks; <T>{String.raw`d_{\min}`}</T>: the
          minimum separation; <T>T</T>: the plan's duration.</> },
    ],
  },
  B54: {
    name: "task choice", code: "B5.4",
    items: [
      { stage: 3, kind: "words", content: <>Against her projected path, robot takes the cheapest of its options:</> },
      { stage: 3, kind: "options", content: [
        ["hold", "wait, then go on"],
        ["switch", "take another task"],
        ["reorder", "change the order"],
      ] },
      { stage: 3, kind: "words", content: <>It decides again at the next change.</> },
    ],
  },
  B42: {
    name: "fit", code: "B4.2",
    items: [
      { stage: 6, kind: "cond", content: <>A hypothesis fits while her detours and her standing stay plausible for it.</> },
      { stage: 6, kind: "cond", content: <>No hypothesis fits: her behaviour is unexplained.</> },
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
        return <p key={k} className={`ub-item ub-formal${cls}`}><Tex>{i.content as string}</Tex></p>;
      case "code":
        return (
          <div key={k} className={`ub-item ub-code${cls}`}>
            {(i.content as string[]).map((line, j) => <div key={j} className="ub-code-line"><Tex>{line}</Tex></div>)}
          </div>
        );
      case "options":
        return (
          <div key={k} className={`ub-item ub-options${cls}`}>
            {(i.content as [string, string][]).map(([name, gloss]) => (
              <div key={name} className="ub-option"><strong>{name}</strong><span>{gloss}</span></div>
            ))}
          </div>
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
      <div className="ub-head"><span className="ub-name">{box.name}</span></div>
      {box.approach !== undefined && <p className="ub-approach">{box.approach}</p>}
      {body.map(item)}
      {outs.length > 0 && <div className="ub-out">{outs.map(item)}</div>}
    </div>
  );
}
