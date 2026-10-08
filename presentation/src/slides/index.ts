/**
 * The deck's slides, in the talk's order (handoff_T-pres.md, section 5, as the overall revision of 8 October 2026 left
 * it, and the merge of the same day, the old talk stages 6 and 7 one talk stage 6): talk stages 0 to 11, each of 1 to 6
 * opened by its transition slide, and the question that leads from talk stage 2 to 3. Each entry is one slide; a slide may have several steps.
 */

import type { ComponentType } from "react";

import * as later from "./later";
import * as opening from "./opening";
import * as stage1 from "./stage1";
import * as stage2 from "./stage2";

export const SLIDES: ComponentType[] = [
  // 0 Opening
  opening.TitleSlide,
  opening.AntonSlide,
  opening.ActorsSlide,
  opening.DonnySlide,
  opening.ProblemSlide,
  opening.TeamSlide,
  opening.QuestionsSlide,
  opening.ArchitectureFrameSlide,
  // 1 The robot alone
  stage1.Stage1Transition,
  stage1.DecompositionSlide,
  stage1.PlanExecuteSlide,
  stage1.Stage1Architecture,
  // 2 A human in the shared space; the question that leads to talk stage 3
  stage2.Stage2Transition,
  stage2.AudienceQuestionSlide,
  stage2.ProjectionSlide,
  stage2.ReactiveRunSlide,
  stage2.Stage2Architecture,
  stage2.TurningPointSlide,
  // 3 Assigned tasks
  later.Stage3Transition,
  later.Stage3Replay,
  later.Stage3Architecture,
  // 4 Foreseeable behaviours
  later.Stage4Transition,
  later.Stage4Replay,
  later.Stage4Architecture,
  // 5 Context
  later.Stage5Transition,
  later.Stage5Replay,
  later.Stage5Architecture,
  // 6 Unmodelled behaviour
  later.Stage6Transition,
  later.Stage6Replay,
  later.Stage6Architecture,
  // 7 to 11
  later.Stage7Recap,
  later.Stage8,
  later.Stage9,
  later.Stage10,
  later.Stage11,
];
