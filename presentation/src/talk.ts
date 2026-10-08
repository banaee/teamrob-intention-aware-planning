/**
 * The talk's skeleton (docs/handoffs/handoff_T-pres.md, section 5; preferred, 8 October 2026): the talk stages 0 to 12
 * as rows, the robot's three questions as columns, three level titles and one turning point. A "talk stage" is a row of
 * the talk; a "part" is a unit of work on the deck (design_records.md, "T-pres, the talk"). The slides read their
 * titles, keywords and footers from here, so that a change of wording is made once.
 */

export type Question = "know" | "believe" | "decide";

export const QUESTIONS: readonly Question[] = ["know", "believe", "decide"];

/** The three questions as the talk asks them, and the field each answers. */
export const QUESTION_TEXT: Record<Question, { ask: string; field: string }> = {
  know: { ask: "What do I know?", field: "knowledge representation" },
  believe: { ask: "What do I believe?", field: "intention recognition" },
  decide: { ask: "What do I decide?", field: "adaptive planning" },
};

/** A column's short header on a talk stage's card. */
export const QUESTION_HEADER: Record<Question, string> = {
  know: "What I know",
  believe: "What I believe",
  decide: "What I decide",
};

export type TalkStage = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;

export interface Level {
  n: 1 | 2 | 3;
  title: string;
  sub: string;
}

export const LEVELS: Record<1 | 2 | 3, Level> = {
  1: { n: 1, title: "Anton works around her", sub: "It sees where she moves, and keeps clear" },
  2: { n: 2, title: "Anton works with her", sub: "What Anton knows grows" },
  3: { n: 3, title: "Anton keeps up with her", sub: "Anton checks whether its belief still fits" },
};

export interface StageRow {
  stage: TalkStage;
  title: string;
  level: 1 | 2 | 3 | null;
  /** The keywords of the three columns, as section 5 gives them; a missing column has none. */
  columns: Partial<Record<Question, string[]>>;
}

export const STAGES: Record<TalkStage, StageRow> = {
  0: { stage: 0, title: "Opening", level: null, columns: {} },
  1: {
    stage: 1, title: "Anton works alone", level: null,
    columns: {
      know: ["Its own tasks, decomposed down to actions"],
      decide: ["Plan, then execute"],
    },
  },
  2: {
    stage: 2, title: "Donny enters", level: 1,
    columns: {
      know: ["Nothing about her intentions"],
      believe: ["Empty"],
      decide: ["Projection from her motion", "Hold near her"],
    },
  },
  3: {
    stage: 3, title: "She does her assigned tasks", level: 2,
    columns: {
      know: ["Her task list"],
      believe: ["H = {assigned tasks}", "Belief update", "Support from her movement",
        "The confidence check admits a belief when it is strong enough"],
      decide: ["Projection from her intention", "Realizer (holds)", "Task choice (switch, reorder)"],
    },
  },
  4: {
    stage: 4, title: "She takes a coffee break", level: 2,
    columns: {
      know: ["Foreseeable behaviours"],
      believe: ["H = {assigned tasks + foreseeable behaviours}"],
      decide: ["Anton plans around her break"],
    },
  },
  5: {
    stage: 5, title: "The situation gives hints", level: 2,
    columns: {
      know: ["Context"],
      believe: ["The prior favours what the situation makes likely", "Observations still decide"],
      decide: ["Anton adapts earlier"],
    },
  },
  6: {
    stage: 6, title: "She switches mid-way, and resumes", level: 3,
    columns: {
      believe: ["The trusted belief stops fitting (fit, for one hypothesis)"],
      decide: ["Anton stops trusting it, replans", "Resumption"],
    },
  },
  7: {
    stage: 7, title: "She does something nobody modelled", level: 3,
    columns: {
      know: ["Anton knows where its model ends"],
      believe: ["No hypothesis fits (fit, for all)", "Anton knows that it does not know"],
      decide: ["Projection from motion, now as a deliberate fallback",
        "Recognition resumes when she returns to modelled behaviour"],
    },
  },
  8: { stage: 8, title: "Recap: the complete architecture", level: null, columns: {} },
  9: { stage: 9, title: "The lift truck's turn", level: null, columns: {} },
  10: { stage: 10, title: "Results", level: null, columns: {} },
  11: { stage: 11, title: "Limits and outlook", level: null, columns: {} },
  12: { stage: 12, title: "The afternoon: the web-ui station", level: null, columns: {} },
};

/** The footer of a slide: where in the talk it stands. */
export function footerText(stage: TalkStage): string {
  const row = STAGES[stage];
  const level = row.level === null ? "" : `Level ${row.level} · `;
  return `${level}${stage} ${row.title}`;
}
