/**
 * The robot's architecture as the talk shows it (docs/handoffs/handoff_T-pres.md, section 6; preferred, 8 October
 * 2026): the elements (6.2) with their kinds (6.1), the talk stage at which each appears (6.5), the arrows with their
 * keywords and the talk stage at which each appears or gives way (6.4), and the arrangement (6.3). One diagram: its
 * state is a talk stage, and each state holds everything of the earlier states except the two direct arrows into
 * "execute" that give way at talk stages 2 and 3. Fit appears at talk stage 6 (unmodelled behaviour, since the merge of
 * 8 October 2026 the last talk stage that adds to the diagram).
 *
 * The codes (L1, C4, B4.1, BL2.1 and so on) are internal labels: no slide shows them (Hadi, tpres-v5). The world strip
 * names no communication (Hadi, tpres-v5).
 *
 * Positions are in the diagram's own unit, a canvas of DESIGN.w x DESIGN.h that the page scales to the slide. The
 * arrangement: knowledge in a left column (C1, C2, C3, the AAAI order); the mind beside it, recognition (C4) left and
 * adaptive planning (C5) right, the arrow "recognised intention" between them at the centre; the body below; the world a
 * strip at the bottom, reached only through the body (sense, act).
 */

import type { Question, TalkStage } from "../talk";

export const DESIGN = { w: 1760, h: 960 };

/** The element kinds, one shape each (6.1): given information, sensed information, a function (a component, which
 * holds blocks), a mechanism (a block); and the frames that hold them: a layer, the knowledge column, the world. */
export type Kind = "knowledge" | "sensed" | "component" | "mechanism" | "layer" | "column" | "world";

export interface Box { x: number; y: number; w: number; h: number }

/** A piece of text that appears at a talk stage; `who` colours it as the web-ui does (the human's orange). */
export interface Part { text: string; stage: TalkStage; who?: "human" }

export interface Element {
  id: string;
  code: string | null;
  label: string;
  /** A second line, its parts joined by ", ", each appearing at its own talk stage. */
  sub: Part[];
  kind: Kind;
  stage: TalkStage;
  parent: string | null;
  question: Question | null;
  box: Box;
}

export type Side = "top" | "bottom" | "left" | "right";

/** An arrow's end: an element's side, at a share of that side's length (0.5 its middle). */
export interface End { el: string; side: Side; at: number }

export interface Arrow {
  id: string;
  from: End;
  to: End;
  /** The keyword, its parts appearing at their talk stages; none for an arrow without one ("fills"). */
  label: Part[];
  stage: TalkStage;
  /** The talk stage at which the arrow gives way; null if it stays. */
  leaves: TalkStage | null;
  /** Where the keyword sits, as an offset from the arrow's centre, in the diagram's unit. */
  labelOffset: { dx: number; dy: number };
  /** The visual centre of the diagram: the one arrow from recognition to planning. */
  centre: boolean;
  /** A width at which the keyword wraps, for a keyword longer than its arrow; null: one line. */
  labelWidth: number | null;
}

const el = (e: Omit<Element, "sub" | "parent" | "question" | "code"> & Partial<Pick<Element, "sub" | "parent" |
  "question" | "code">>): Element => ({ sub: [], parent: null, question: null, code: null, ...e });

export const ELEMENTS: Element[] = [
  // The frames, present from talk stage 0: the empty architecture the opening shows.
  el({ id: "K", label: "Knowledge", sub: [{ text: "given", stage: 0 }], kind: "column", stage: 0,
       question: "know", box: { x: 0, y: 0, w: 290, h: 640 } }),
  el({ id: "L1", code: "L1", label: "Mind", kind: "layer", stage: 0, box: { x: 340, y: 0, w: 1420, h: 640 } }),
  el({ id: "L2", code: "L2", label: "Body", kind: "layer", stage: 0, box: { x: 340, y: 680, w: 1420, h: 170 } }),
  el({ id: "W", label: "World", kind: "world", stage: 0, box: { x: 0, y: 890, w: 1760, h: 70 },
       sub: [{ text: "the room, objects", stage: 0 }, { text: "the human", stage: 2, who: "human" }] }),

  // Knowledge (given).
  el({ id: "C1", code: "C1", label: "team task knowledge", kind: "knowledge", stage: 1, parent: "K", question: "know",
       sub: [{ text: "robot's tasks", stage: 1 }, { text: "her task list", stage: 3 }],
       box: { x: 20, y: 60, w: 250, h: 110 } }),
  el({ id: "C2", code: "C2", label: "knowledge about the human", kind: "knowledge", stage: 4, parent: "K",
       question: "know", sub: [{ text: "foreseeable behaviours", stage: 4 }], box: { x: 20, y: 205, w: 250, h: 110 } }),
  el({ id: "C3", code: "C3", label: "context", kind: "knowledge", stage: 5, parent: "K", question: "know",
       box: { x: 20, y: 440, w: 250, h: 90 } }),

  // L1, the mind.
  el({ id: "C4", code: "C4", label: "Recognition", kind: "component", stage: 3, parent: "L1", question: "believe",
       box: { x: 380, y: 70, w: 590, h: 540 } }),
  el({ id: "B43", code: "B4.3", label: "support", kind: "mechanism", stage: 3, parent: "C4", question: "believe",
       box: { x: 410, y: 150, w: 230, h: 70 } }),
  el({ id: "B42", code: "B4.2", label: "fit", kind: "mechanism", stage: 6, parent: "C4", question: "believe",
       box: { x: 410, y: 300, w: 230, h: 70 } }),
  el({ id: "B41", code: "B4.1", label: "belief update", kind: "mechanism", stage: 3, parent: "C4", question: "believe",
       box: { x: 410, y: 450, w: 230, h: 70 } }),
  el({ id: "B44", code: "B4.4", label: "confidence check", kind: "mechanism", stage: 3, parent: "C4",
       question: "believe", box: { x: 705, y: 300, w: 235, h: 70 } }),

  el({ id: "C5", code: "C5", label: "Adaptive planning", kind: "component", stage: 1, parent: "L1", question: "decide",
       box: { x: 1100, y: 70, w: 640, h: 540 } }),
  el({ id: "B51", code: "B5.1", label: "projection", kind: "mechanism", stage: 2, parent: "C5", question: "decide",
       box: { x: 1130, y: 300, w: 220, h: 70 } }),
  el({ id: "B52", code: "B5.2", label: "planner", kind: "mechanism", stage: 1, parent: "C5", question: "decide",
       box: { x: 1490, y: 150, w: 220, h: 70 } }),
  el({ id: "B53", code: "B5.3", label: "realizer", kind: "mechanism", stage: 2, parent: "C5", question: "decide",
       box: { x: 1490, y: 300, w: 220, h: 70 } }),
  el({ id: "B54", code: "B5.4", label: "task choice", kind: "mechanism", stage: 3, parent: "C5", question: "decide",
       box: { x: 1490, y: 450, w: 220, h: 70 } }),

  // L2, the body: two free blocks and the sensed world state.
  el({ id: "BL21", code: "BL2.1", label: "observe", kind: "mechanism", stage: 1, parent: "L2",
       box: { x: 400, y: 740, w: 220, h: 70 } }),
  el({ id: "WS", label: "world state", kind: "sensed", stage: 1, parent: "L2", sub: [{ text: "sensed", stage: 1 }],
       box: { x: 820, y: 722, w: 260, h: 104 } }),
  el({ id: "BL22", code: "BL2.2", label: "execute", kind: "mechanism", stage: 1, parent: "L2",
       sub: [{ text: "with the safety stop", stage: 1 }], box: { x: 1480, y: 728, w: 240, h: 94 } }),
];

const end = (el: string, side: Side, at = 0.5): End => ({ el, side, at });
const kw = (text: string, stage: TalkStage): Part[] => [{ text, stage }];
const arrow = (a: Omit<Arrow, "leaves" | "labelOffset" | "centre" | "labelWidth"> & Partial<Pick<Arrow, "leaves" |
  "labelOffset" | "centre" | "labelWidth">>): Arrow =>
  ({ leaves: null, labelOffset: { dx: 0, dy: 0 }, centre: false, labelWidth: null, ...a });

// x on the world strip's and the world state's top side, as a share of their widths.
const onWorld = (x: number) => x / 1760;
const onWorldState = (x: number) => (x - 820) / 260;

export const ARROWS: Arrow[] = [
  // Talk stage 1: the robot alone.
  arrow({ id: "sense", from: end("W", "top", onWorld(510)), to: end("BL21", "bottom"), label: kw("sense", 1), stage: 1,
          labelOffset: { dx: 50, dy: 0 } }),
  arrow({ id: "fills", from: end("BL21", "right"), to: end("WS", "left"), label: [], stage: 1 }),
  arrow({ id: "tasks", from: end("C1", "right"), to: end("L1", "left", 40 / 640),
          label: [{ text: "robot's tasks", stage: 1 }, { text: "her task list", stage: 3 }], stage: 1,
          labelOffset: { dx: 200, dy: -38 } }),
  arrow({ id: "room", from: end("WS", "top", onWorldState(950)), to: end("C5", "bottom", 0.5), label: kw("room", 1),
          stage: 1, labelOffset: { dx: 150, dy: 0 } }),
  arrow({ id: "next-action", from: end("B52", "bottom"), to: end("BL22", "top"), label: kw("next action", 1), stage: 1,
          leaves: 2 }),
  arrow({ id: "act", from: end("BL22", "bottom"), to: end("W", "top", onWorld(1600)), label: kw("act", 1), stage: 1,
          labelOffset: { dx: 40, dy: 0 } }),
  // Talk stage 2: a human in the shared space.
  arrow({ id: "her-motion", from: end("WS", "top", onWorldState(1050)), to: end("B51", "bottom"),
          label: kw("her motion", 2), stage: 2, labelOffset: { dx: 0, dy: -60 } }),
  arrow({ id: "her-path", from: end("B51", "right"), to: end("B53", "left"), label: kw("her path", 2), stage: 2,
          labelOffset: { dx: 0, dy: -26 } }),
  arrow({ id: "plan", from: end("B52", "bottom"), to: end("B53", "top"), label: kw("plan", 2), stage: 2,
          labelOffset: { dx: 46, dy: 0 } }),
  arrow({ id: "next-action-hold", from: end("B53", "bottom"), to: end("BL22", "top"), label: kw("next action, hold", 2),
          stage: 2, leaves: 3 }),
  // Talk stage 3: her assigned tasks.
  arrow({ id: "her-actions", from: end("WS", "top", onWorldState(850)), to: end("C4", "bottom", (850 - 380) / 590),
          label: kw("her actions", 3), stage: 3, labelOffset: { dx: -76, dy: 0 } }),
  arrow({ id: "belief", from: end("B41", "right"), to: end("B44", "bottom"), label: kw("belief", 3), stage: 3,
          labelOffset: { dx: 0, dy: 26 } }),
  arrow({ id: "support", from: end("B43", "right"), to: end("B44", "top"), label: kw("support", 3), stage: 3,
          labelOffset: { dx: 0, dy: -26 } }),
  arrow({ id: "trusted", from: end("B44", "right"), to: end("B51", "left"), label: kw("recognised intention, or none", 3),
          stage: 3, centre: true, labelOffset: { dx: 0, dy: -46 }, labelWidth: 190 }),
  arrow({ id: "cost", from: end("B53", "bottom"), to: end("B54", "top"), label: kw("cost", 3), stage: 3,
          labelOffset: { dx: 46, dy: 0 } }),
  arrow({ id: "next-task-hold", from: end("B54", "bottom"), to: end("BL22", "top"), label: kw("next task, hold", 3),
          stage: 3, labelOffset: { dx: 0, dy: -20 } }),
  // Talk stages 4, 5, 6.
  arrow({ id: "foreseeable", from: end("C2", "right"), to: end("C4", "left", (260 - 70) / 540),
          label: kw("foreseeable behaviours", 4), stage: 4, labelOffset: { dx: 0, dy: -40 }, labelWidth: 130 }),
  arrow({ id: "prior", from: end("C3", "right"), to: end("B41", "left"), label: kw("prior", 5), stage: 5,
          labelOffset: { dx: -20, dy: -24 } }),
  arrow({ id: "fit", from: end("B42", "right"), to: end("B44", "left"), label: kw("fit", 6), stage: 6,
          labelOffset: { dx: 0, dy: -24 } }),
];

/** An element's or an arrow's state at a talk stage: absent, present since an earlier talk stage, new at this one,
 * or leaving at this one (an arrow that gives way). */
export type Presence = "absent" | "old" | "new" | "leaving";

/** `revealed`: whether the talk stage's additions are shown yet (a slide shows the state before them, then a click
 * adds them). */
export function presence(appears: TalkStage, leaves: TalkStage | null, stage: TalkStage, revealed: boolean): Presence {
  const shown = revealed ? stage : stage - 1;
  if (leaves !== null && leaves <= shown) return leaves === stage ? "leaving" : "absent";
  if (appears > shown) return "absent";
  return appears === stage ? "new" : "old";
}
