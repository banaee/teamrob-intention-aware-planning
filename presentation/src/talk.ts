/**
 * The talk's skeleton (docs/handoffs/handoff_T-pres.md, section 5; preferred, 8 October 2026; revised 8 October 2026,
 * the overall revision: the levels removed, each talk stage opened by a transition slide, the names Hadi gave; and the
 * merge of the same day: the old talk stages 6, switch and resumption, and 7, unmodelled behaviour, are one talk stage
 * 6, since both rest on fit): the talk stages 0 to 11 as rows, the robot's three questions as columns. A "talk stage" is a row of the talk; a
 * "part" is a unit of work on the deck (design_records.md, "T-pres, the talk"). The slides read their titles, keywords
 * and footers from here, so that a change of wording is made once.
 *
 * One concept, one term in the whole deck (the overall revision, point A): the terms used here are the deck's, listed
 * with their meaning and their repo term in the report of that revision.
 */

export type Question = "know" | "believe" | "decide";

export const QUESTIONS: readonly Question[] = ["know", "believe", "decide"];

/** The three questions as the talk asks them, and the field each answers. */
export const QUESTION_TEXT: Record<Question, { ask: string; field: string }> = {
  know: { ask: "What do I know?", field: "knowledge representation" },
  believe: { ask: "What do I believe?", field: "intention recognition" },
  decide: { ask: "What do I decide?", field: "adaptive planning" },
};

/** A column's short header. */
export const QUESTION_HEADER: Record<Question, string> = {
  know: "What I know",
  believe: "What I believe",
  decide: "What I decide",
};

/** The talk's title (Hadi, 8 October 2026, preferred, a first version). */
export const TALK_TITLE = "Intention-aware adaptive planning in human-robot teams";

export type TalkStage = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11;

/** The talk stages a transition slide lists: the six that build the architecture. */
export const BUILT_STAGES = [1, 2, 3, 4, 5, 6] as const;

export interface StageRow {
  stage: TalkStage;
  /** The short label: in the transition slides' list and in the footer. */
  title: string;
  /** The line after the colon (Hadi's names): under the label in the transition slides' list. */
  line: string;
  /** The keywords of the three columns; a missing column has none. */
  columns: Partial<Record<Question, string[]>>;
}

export const STAGES: Record<TalkStage, StageRow> = {
  0: { stage: 0, title: "Opening", line: "", columns: {} },
  1: {
    stage: 1, title: "The robot alone", line: "it plans and executes its own tasks",
    columns: {
      know: ["Its own tasks, broken down into actions"],
      decide: ["Plan, then execute"],
    },
  },
  2: {
    stage: 2, title: "A human in the shared space",
    line: "the robot knows nothing about her; it reacts to her motion",
    columns: {
      know: ["Nothing about her intentions"],
      believe: ["Nothing"],
      decide: ["Projection from her motion", "A hold to keep the minimum separation"],
    },
  },
  3: {
    stage: 3, title: "Assigned tasks",
    line: "the robot knows her task list and recognises which task she does",
    columns: {
      know: ["Her task list"],
      believe: ["Hypotheses: her assigned tasks", "Belief update", "Support from her movement",
        "Confidence check: a trusted intention, or none"],
      decide: ["Projection from her intention", "Realizer: the holds", "Task choice: a switch or a reorder"],
    },
  },
  4: {
    stage: 4, title: "Foreseeable behaviours",
    line: "she does something expected that is not a task, such as a coffee break",
    columns: {
      know: ["Foreseeable behaviours"],
      believe: ["More hypotheses: her assigned tasks and the foreseeable behaviours"],
      decide: ["Anton adapts its plan to her coffee break"],
    },
  },
  5: {
    stage: 5, title: "Context", line: "the situation makes some behaviours more likely",
    columns: {
      know: ["Context"],
      believe: ["The prior depends on the context", "Her observed movement still decides"],
      decide: ["Anton adapts its plan earlier"],
    },
  },
  6: {
    stage: 6, title: "Unmodelled behaviour", line: "she does something the robot has no model of",
    columns: {
      know: ["Where its model ends"],
      believe: ["Fit: does the trusted intention still fit what she does?", "No hypothesis fits: Anton knows that it does not know"],
      decide: ["Anton stops trusting it", "Projection from her motion, now as the fallback",
        "When she returns to a modelled behaviour, her task is trusted again"],
    },
  },
  7: { stage: 7, title: "Recap: the complete architecture", line: "", columns: {} },
  8: { stage: 8, title: "The lift truck's turn", line: "", columns: {} },
  9: { stage: 9, title: "Results", line: "", columns: {} },
  10: { stage: 10, title: "Limits and outlook", line: "", columns: {} },
  11: { stage: 11, title: "The afternoon: the web-ui station", line: "", columns: {} },
};

/** The footer of a slide: where in the talk it stands. */
export function footerText(stage: TalkStage): string {
  return stage === 0 ? "Opening" : `${stage} ${STAGES[stage].title}`;
}
