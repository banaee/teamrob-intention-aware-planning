/**
 * The deck's slides, in the talk's order (handoff_T-pres.md, section 5): talk stages 0 to 12, the three level titles
 * and the turning point after talk stage 2. Each entry is one slide; a slide may have several steps.
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
  // 1 Anton works alone
  stage1.Stage1Card,
  stage1.DecompositionSlide,
  stage1.PlanExecuteSlide,
  stage1.Stage1Architecture,
  // Level 1; 2 Donny enters; the turning point
  stage2.Level1Slide,
  stage2.DonnyEntersSlide,
  stage2.AudienceQuestionSlide,
  stage2.Stage2Card,
  stage2.ProjectionSlide,
  stage2.ReactiveRunSlide,
  stage2.Stage2Architecture,
  stage2.TurningPointSlide,
  // Level 2: 3, 4, 5
  later.Level2Slide,
  later.Stage3Card,
  later.Stage3Architecture,
  later.Stage4Card,
  later.Stage4Architecture,
  later.Stage5Card,
  later.Stage5Architecture,
  // Level 3: 6, 7
  later.Level3Slide,
  later.Stage6Card,
  later.Stage6Architecture,
  later.Stage7Card,
  later.Stage7Architecture,
  // 8 to 12
  later.Stage8Recap,
  later.Stage9,
  later.Stage10,
  later.Stage11,
  later.Stage12,
];
