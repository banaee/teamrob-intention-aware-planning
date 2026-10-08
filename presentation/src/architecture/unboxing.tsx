/**
 * What a block of the architecture does, opened from its place in the diagram (Hadi, 8 October 2026, preferred:
 * "unboxing the blocks"; it replaces the handoff's "at most one formula"). A block is opened when it first appears, and
 * again at each later talk stage that extends it: then the earlier content recedes and the addition is drawn at full
 * strength, the language the diagram uses for old and new.
 *
 * One source per block: its parts, in the order they are shown, each with the talk stage that brings it. A part is a
 * line in the audience's words, with the formal line beside it where there is one. Abstract, not as implemented: no
 * flowchart, no if-then branch. Every formulation is taken from the code and the records:
 * - belief update: shared/recognizer.py, shared/likelihood_functions.py (L(x) = 2 / (1 + e^(βx)), x = v·D, one factor
 *   per phase of the episode); docs/context_knowledge_method.md, sections 6 and 7 (the prior, the belief);
 * - support: the observation warrant (glossary; context_knowledge_method.md, section 8, condition 3);
 * - confidence check: MetaPlanner._clears_gate (θ = 0.75, adequacy, observation warrant, evidence rank);
 * - projection: the admitted task's projection (Projector.project) and the fallback projection (T-D P4);
 * - realizer: realize(), one minimal-shift search per entry, F1 (realization is total), min_separation 50 cm;
 * - task choice: single_task and full_reorder, only the first hold executed;
 * - fit: the adequacy test, D = e/v + (s − s_exp), S(v·D) against α = 0.05 (glossary §5, §7).
 */

import type { ReactNode } from "react";

import type { TalkStage } from "../talk";

export type Unboxable = "B41" | "B43" | "B44" | "B51" | "B53" | "B54" | "B42";

export interface Line {
  stage: TalkStage;
  words: ReactNode;
  formal?: ReactNode;
  /** A line that states the block's output, set apart below the others. */
  output?: boolean;
}

export interface Box {
  name: string;
  code: string;
  lines: Line[];
}

const V = ({ children }: { children: ReactNode }) => <i className="mv">{children}</i>;

function Frac({ num, den }: { num: ReactNode; den: ReactNode }) {
  return <span className="frac"><span className="frac-num">{num}</span><span className="frac-den">{den}</span></span>;
}

export const BOXES: Record<Unboxable, Box> = {
  B41: {
    name: "belief update", code: "B4.1",
    lines: [
      { stage: 3, words: <>For each task <V>h</V> she may be doing: how likely it was before watching her, times how
          well her movement fits it, normalised over all of them.</>,
        formal: <><V>belief</V>(<V>h</V>) = <Frac num={<><V>prior</V>(<V>h</V>) · <V>evidence</V>(<V>h</V>)</>}
          den={<>Σ<sub><V>h′</V> ∈ <V>H</V></sub> <V>prior</V>(<V>h′</V>) · <V>evidence</V>(<V>h′</V>)</>} /></> },
      { stage: 3, words: <>What she may be doing: her assigned tasks.</>,
        formal: <><V>H</V> = {"{"}her assigned tasks{"}"}</> },
      { stage: 4, words: <>What she may be doing grows by what people foreseeably do besides their tasks.</>,
        formal: <><V>H</V> = {"{"}her assigned tasks + foreseeable behaviours{"}"}</> },
      { stage: 3, words: <>Evidence: her movement in each step of <V>h</V>. Path walked beyond the shortest way to the
          step's target, or standing longer than the step takes, lowers it.</>,
        formal: <><V>evidence</V>(<V>h</V>) = Π<sub>steps</sub> <V>L</V>(<V>x</V>), &nbsp;<V>L</V>(<V>x</V>) =
          <Frac num="2" den={<>1 + <V>e</V><sup>β<V>x</V></sup></>} /><br /><V>x</V> = extra path + extra standing</> },
      { stage: 3, words: <>Prior: equal over <V>H</V>, for now.</>,
        formal: <><V>prior</V>(<V>h</V>) = 1 / |<V>H</V>|</> },
      { stage: 5, words: <>Prior from the situation: her assigned tasks together weigh 1, shared equally; each
          foreseeable behaviour weighs its strength, which the situation sets: ordinary, raised when the situation
          favours it (break time raises the coffee break), lowered just after it happened.</>,
        formal: <><V>prior</V>(<V>h</V>) ∝ 1 / |<V>A</V>| for an assigned task, &nbsp;<V>s</V><sub><V>f</V></sub> /
          |<V>H</V><sub><V>f</V></sub>| for a behaviour <V>f</V>; &nbsp;<V>s</V> ∈ {"{"}0.005, 0.02, raised{"}"}</> },
      { stage: 5, words: <>The evidence is untouched: it holds no context.</> },
    ],
  },
  B43: {
    name: "support", code: "B4.3",
    lines: [
      { stage: 3, words: <>A hypothesis has support when her movement in its current step has brought her closer to
          the step's target,</>,
        formal: <><V>cost</V>(start of step → target) − <V>cost</V>(now → target) &gt; 0</> },
      { stage: 3, words: <>or when Anton saw her complete the step before it. A wait has only this source.</> },
      { stage: 3, words: <>Without support no belief is trusted, however strong: knowing what is probable does not say
          when she starts.</>, output: true },
    ],
  },
  B44: {
    name: "confidence check", code: "B4.4",
    lines: [
      { stage: 3, words: <>The leading hypothesis <V>h*</V>, the one with the highest belief, is trusted when all of
          these hold:</> },
      { stage: 3, words: <>strong enough</>, formal: <><V>belief</V>(<V>h*</V>) ≥ θ = 0.75</> },
      { stage: 3, words: <>supported</>, formal: <><V>h*</V> has support</> },
      { stage: 5, words: <>observations still decide: context may make the trust come earlier, never against what her
          movement shows</>, formal: <>no <V>h</V> with <V>evidence</V>(<V>h</V>) &gt; <V>evidence</V>(<V>h*</V>)</> },
      { stage: 6, words: <>it fits what she does now</>, formal: <><V>h*</V> fits</> },
      { stage: 3, words: <>Out: the trusted intention <V>h*</V>, or none.</>, output: true },
    ],
  },
  B51: {
    name: "projection", code: "B5.1",
    lines: [
      { stage: 2, words: <>From her motion: her last motion continued, for as long as Anton has seen it.</> },
      { stage: 3, words: <>From her intention: the plan of the trusted task, decomposed down to actions from where she
          is now: where she will be, and when.</>,
        formal: <><V>her path</V> = <V>plan</V>(<V>h*</V>, world state)</> },
      { stage: 3, words: <>One knowledge, two uses: the task knowledge Anton plans its own work with is the knowledge
          that turns her trusted task into her path.</>, output: true },
      { stage: 7, words: <>No trusted intention, because nothing fits: the projection from her motion, now a
          deliberate fallback. When a belief is trusted again, the projection from her intention returns.</> },
    ],
  },
  B53: {
    name: "realizer", code: "B5.3",
    lines: [
      { stage: 3, words: <>For each task of Anton's plan, in order: the smallest hold before it, in whole ticks, such
          that Anton's moving path never comes closer than the minimum separation to her projected path.</>,
        formal: <><V>δ</V><sub><V>k</V></sub> = min {"{"} <V>δ</V> ≥ <V>δ</V><sub><V>k</V>−1</sub> : Anton's moves keep
          ≥ <V>d</V><sub>min</sub> from her path {"}"}, &nbsp;<V>d</V><sub>min</sub> = 50 cm</> },
      { stage: 3, words: <>Standing still never comes too close, so a hold always exists and every plan has a cost.</> },
      { stage: 3, words: <>The cost of a plan: its duration plus its holds.</>,
        formal: <><V>cost</V> = <V>T</V> + <V>δ</V><sub>last</sub></>, output: true },
    ],
  },
  B54: {
    name: "task choice", code: "B5.4",
    lines: [
      { stage: 3, words: <>A candidate: one remaining task, or an ordering of all remaining tasks.</> },
      { stage: 3, words: <>Each candidate is realized against her projected path; the cheapest is chosen.</>,
        formal: <><V>next</V> = argmin<sub><V>c</V></sub> <V>cost</V>(<V>realize</V>(<V>c</V>, her path))</> },
      { stage: 3, words: <>A switch: another task is now cheaper. A reorder: another order is cheaper. Only the first
          hold is carried out; the rest is decided again later.</>, output: true },
    ],
  },
  B42: {
    name: "fit", code: "B4.2",
    lines: [
      { stage: 6, words: <>For each hypothesis, in its current step: how much later than its plan she would finish,
          from extra path walked and extra standing.</>,
        formal: <><V>D</V> = extra path / <V>v</V> + (standing − expected standing)</> },
      { stage: 6, words: <>It fits unless that delay is surprising: at 5 %, about 334 cm walked off the way, or 17
          ticks of standing beyond the step.</>,
        formal: <>fits ⇔ <V>S</V>(<V>v</V>·<V>D</V>) ≥ <V>α</V> = 0.05</> },
      { stage: 6, words: <>When the trusted hypothesis stops fitting, Anton stops trusting it and replans.</>,
        output: true },
      { stage: 7, words: <>No hypothesis fits: her behaviour is unexplained. Anton knows that it does not know.</>,
        formal: <><V>S</V>(<V>v</V>·<V>D</V><sub><V>h</V></sub>) &lt; <V>α</V> for every observed <V>h</V></>,
        output: true },
    ],
  },
};

/** A block opened at a talk stage: its parts up to that talk stage; the earlier ones recede when the talk stage adds
 * any. */
export function Unboxed({ block, stage, side }: { block: Unboxable; stage: TalkStage; side: "left" | "right" }) {
  const box = BOXES[block];
  const shown = box.lines.filter((l) => l.stage <= stage);
  const adds = shown.some((l) => l.stage === stage) && shown.some((l) => l.stage < stage);
  const lines = shown.filter((l) => !l.output);
  const outputs = shown.filter((l) => l.output);
  // At an extension an earlier line recedes and shrinks to its formal line, so that the addition has the room.
  const line = (l: Line, i: number) => {
    const old = adds && l.stage < stage;
    return (
      <div key={i} className={`ub-line${adds ? (old ? " ub-old" : " ub-new") : ""}`}>
        {(!old || l.formal === undefined) && <p className="ub-words">{l.words}</p>}
        {l.formal !== undefined && <p className="ub-formal">{l.formal}</p>}
      </div>
    );
  };
  return (
    <div className={`unboxed unboxed-${side}`}>
      <div className="ub-head"><span className="ub-name">{box.name}</span><span className="ub-code">{box.code}</span></div>
      {lines.map(line)}
      {outputs.length > 0 && <div className="ub-out">{outputs.map(line)}</div>}
    </div>
  );
}
