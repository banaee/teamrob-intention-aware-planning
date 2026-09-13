# Auto-generated summary tables (analyze.py)

## (a) Evidence paths per condition — counts over (tick × hypothesis) likelihood calls

| condition | ticks | crash_step | n_hyp | n_inadmissible | moving_ticks | discrete_ticks | stationary_ticks | likelihood_calls | branch_progress | branch_completion | branch_completion_unresolved | branch_fallthrough | resolve_term_value_calls | chord_scored | at_target_HIGH | zero_move_NEUTRAL | target_none_phase2_var | target_none_no_item_binding | target_none_other | origin_none | zone_boost_pairs | temp_boost_pairs | fatigue_boost_pairs | held_refutation_ticks | held_refutation_pairs | floor_clamps_evidence | floor_clamps_output |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 169 |  | 5 | 0 | 130 | 4 | 35 | 670 | 670 | 0 | 0 | 0 | 0 | 588 | 0 | 18 | 64 | 0 | 0 | 0 | 72 | 0 | 0 | 68 | 272 | 0 | 0 |
| s00_on | 169 |  | 5 | 3 | 130 | 4 | 35 | 268 | 268 | 0 | 0 | 0 | 0 | 198 | 0 | 6 | 64 | 0 | 0 | 0 | 36 | 0 | 0 | 68 | 272 | 0 | 0 |
| s10_off | 258 | 257 | 9 | 0 | 215 | 3 | 40 | 1962 | 1962 | 0 | 0 | 0 | 0 | 1679 | 0 | 22 | 43 | 218 | 0 | 0 | 414 | 0 | 0 | 45 | 315 | 0 | 54 |
| s10_on | 258 | 257 | 9 | 4 | 215 | 3 | 40 | 1090 | 1090 | 0 | 0 | 0 | 0 | 819 | 0 | 10 | 43 | 218 | 0 | 0 | 244 | 0 | 0 | 45 | 315 | 0 | 0 |
| s20_off | 200 |  | 5 | 0 | 110 | 4 | 86 | 570 | 570 | 0 | 0 | 0 | 0 | 491 | 0 | 18 | 61 | 0 | 0 | 0 | 64 | 0 | 0 | 65 | 260 | 0 | 0 |
| s20_on | 200 |  | 5 | 3 | 110 | 4 | 86 | 228 | 228 | 0 | 0 | 0 | 0 | 161 | 0 | 6 | 61 | 0 | 0 | 0 | 28 | 0 | 0 | 65 | 260 | 0 | 0 |
| s30_off | 168 |  | 5 | 0 | 109 | 4 | 55 | 565 | 565 | 0 | 0 | 0 | 0 | 493 | 0 | 18 | 54 | 0 | 0 | 0 | 223 | 0 | 0 | 58 | 232 | 0 | 0 |
| s30_on | 168 |  | 5 | 3 | 109 | 4 | 55 | 226 | 226 | 0 | 0 | 0 | 0 | 166 | 0 | 6 | 54 | 0 | 0 | 0 | 158 | 0 | 0 | 58 | 232 | 0 | 0 |

## (b) _get_expected_position outcome per hypothesis (likelihood calls, moving+discrete ticks only)

| condition | hyp | task | inadmissible | calls | phase1_shelf | phase1_table_delivered_decoy | phase1_container_is_agent_fallback_item_pos | phase2_var_target_NEUTRAL | no_item_binding_NEUTRAL | phase1_item_pos |
|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | item_3 | deliver_item | False | 134 | 39 | 60 | 0 | 35 | 0 | 0 |
| s00_off | item_4 | deliver_item | False | 134 | 123 | 0 | 11 | 0 | 0 | 0 |
| s00_off | item_6 | deliver_item | False | 134 | 60 | 47 | 27 | 0 | 0 | 0 |
| s00_off | item_7 | deliver_item | False | 134 | 6 | 104 | 24 | 0 | 0 | 0 |
| s00_off | item_2 | deliver_item | False | 134 | 104 | 1 | 0 | 29 | 0 | 0 |
| s00_on | item_3 | deliver_item | False | 134 | 39 | 60 | 0 | 35 | 0 | 0 |
| s00_on | item_4 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | item_6 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | item_7 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | item_2 | deliver_item | False | 134 | 104 | 1 | 0 | 29 | 0 | 0 |
| s10_off | item_0 | deliver_item | False | 218 | 218 | 0 | 0 | 0 | 0 | 0 |
| s10_off | item_1 | deliver_item | False | 218 | 122 | 59 | 37 | 0 | 0 | 0 |
| s10_off | item_2 | deliver_item | False | 218 | 29 | 147 | 0 | 42 | 0 | 0 |
| s10_off | item_3 | deliver_item | False | 218 | 218 | 0 | 0 | 0 | 0 | 0 |
| s10_off | item_4 | deliver_item | False | 218 | 217 | 0 | 0 | 1 | 0 | 0 |
| s10_off | item_5 | deliver_item | False | 218 | 218 | 0 | 0 | 0 | 0 | 0 |
| s10_off | item_6 | deliver_item | False | 218 | 218 | 0 | 0 | 0 | 0 | 0 |
| s10_off | item_7 | deliver_item | False | 218 | 31 | 141 | 46 | 0 | 0 | 0 |
| s10_off | coffee_break | coffee_break | False | 218 | 0 | 0 | 0 | 0 | 218 | 0 |
| s10_on | item_0 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s10_on | item_1 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s10_on | item_2 | deliver_item | False | 218 | 29 | 147 | 0 | 42 | 0 | 0 |
| s10_on | item_3 | deliver_item | False | 218 | 218 | 0 | 0 | 0 | 0 | 0 |
| s10_on | item_4 | deliver_item | False | 218 | 217 | 0 | 0 | 1 | 0 | 0 |
| s10_on | item_5 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s10_on | item_6 | deliver_item | False | 218 | 218 | 0 | 0 | 0 | 0 | 0 |
| s10_on | item_7 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s10_on | coffee_break | coffee_break | False | 218 | 0 | 0 | 0 | 0 | 218 | 0 |
| s20_off | item_4 | deliver_item | False | 114 | 103 | 0 | 11 | 0 | 0 | 0 |
| s20_off | item_3 | deliver_item | False | 114 | 20 | 64 | 0 | 30 | 0 | 0 |
| s20_off | item_6 | deliver_item | False | 114 | 38 | 38 | 38 | 0 | 0 | 0 |
| s20_off | item_7 | deliver_item | False | 114 | 114 | 0 | 0 | 0 | 0 | 0 |
| s20_off | item_2 | deliver_item | False | 114 | 82 | 1 | 0 | 31 | 0 | 0 |
| s20_on | item_4 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_on | item_3 | deliver_item | False | 114 | 20 | 64 | 0 | 30 | 0 | 0 |
| s20_on | item_6 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_on | item_7 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_on | item_2 | deliver_item | False | 114 | 82 | 1 | 0 | 31 | 0 | 0 |
| s30_off | item_3 | deliver_item | False | 113 | 37 | 43 | 0 | 33 | 0 | 0 |
| s30_off | item_4 | deliver_item | False | 113 | 111 | 0 | 2 | 0 | 0 | 0 |
| s30_off | item_6 | deliver_item | False | 113 | 113 | 0 | 0 | 0 | 0 | 0 |
| s30_off | item_7 | deliver_item | False | 113 | 91 | 1 | 0 | 21 | 0 | 0 |
| s30_off | item_2 | deliver_item | False | 113 | 53 | 24 | 36 | 0 | 0 | 0 |
| s30_on | item_3 | deliver_item | False | 113 | 37 | 43 | 0 | 33 | 0 | 0 |
| s30_on | item_4 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s30_on | item_6 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s30_on | item_7 | deliver_item | False | 113 | 91 | 1 | 0 | 21 | 0 | 0 |
| s30_on | item_2 | deliver_item | True | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## (c) ZONE_BOOST episodes — maximal step ranges where ω_context carried ×2 for a hypothesis

| condition | hyp | zone | first_step | last_step | human_task_at_start | human_action_at_start | hyp_is_human_task |
|---|---|---|---|---|---|---|---|
| s00_off | item_2 | zone_SE | 16 | 21 | item_3 | move_to | False |
| s00_off | item_4 | zone_SE | 16 | 21 | item_3 | move_to | False |
| s00_off | item_3 | zone_SW | 22 | 40 | item_3 | move_to | True |
| s00_off | item_6 | zone_SW | 22 | 77 | item_3 | move_to | False |
| s00_off | item_3 | zone_NW | 78 | 80 | item_3 | place | True |
| s00_off | item_7 | zone_NW | 78 | 80 | item_3 | place | False |
| s00_off | item_2 | zone_SE | 103 | 110 | item_2 | move_to | True |
| s00_off | item_4 | zone_SE | 103 | 141 | item_2 | move_to | False |
| s00_on | item_2 | zone_SE | 16 | 21 | item_3 | move_to | False |
| s00_on | item_3 | zone_SW | 22 | 40 | item_3 | move_to | True |
| s00_on | item_3 | zone_NW | 78 | 80 | item_3 | place | True |
| s00_on | item_2 | zone_SE | 103 | 110 | item_2 | move_to | True |
| s10_off | item_1 | zone_SW | 0 | 74 | item_2 | move_to | False |
| s10_off | item_2 | zone_SW | 0 | 30 | item_2 | move_to | True |
| s10_off | item_6 | zone_SW | 0 | 74 | item_2 | move_to | False |
| s10_off | item_0 | zone_NW | 75 | 106 | item_2 | place | False |
| s10_off | item_2 | zone_NW | 75 | 106 | item_2 | place | True |
| s10_off | item_7 | zone_NW | 83 | 106 | coffee_break | move_to | False |
| s10_off | item_1 | zone_SW | 107 | 141 | coffee_break | move_to | False |
| s10_off | item_6 | zone_SW | 107 | 208 | coffee_break | move_to | False |
| s10_off | item_4 | zone_SE | 209 | 256 | item_4 | move_to | True |
| s10_off | item_5 | zone_SE | 209 | 257 | item_4 | move_to | False |
| s10_on | item_2 | zone_SW | 0 | 30 | item_2 | move_to | True |
| s10_on | item_6 | zone_SW | 0 | 74 | item_2 | move_to | False |
| s10_on | item_2 | zone_NW | 75 | 106 | item_2 | place | True |
| s10_on | item_6 | zone_SW | 107 | 208 | coffee_break | move_to | False |
| s10_on | item_4 | zone_SE | 209 | 256 | item_4 | move_to | True |
| s20_off | item_2 | zone_SE | 4 | 10 | item_3 | move_to | False |
| s20_off | item_7 | zone_SE | 4 | 10 | item_3 | move_to | False |
| s20_off | item_3 | zone_SW | 11 | 21 | item_3 | move_to | True |
| s20_off | item_4 | zone_SW | 11 | 53 | item_3 | move_to | False |
| s20_off | item_6 | zone_SW | 11 | 53 | item_3 | move_to | False |
| s20_off | item_3 | zone_NW | 54 | 56 | item_3 | place | True |
| s20_off | item_2 | zone_SE | 82 | 88 | item_2 | move_to | True |
| s20_off | item_7 | zone_SE | 82 | 121 | item_2 | move_to | False |
| s20_on | item_2 | zone_SE | 4 | 10 | item_3 | move_to | False |
| s20_on | item_3 | zone_SW | 11 | 21 | item_3 | move_to | True |
| s20_on | item_3 | zone_NW | 54 | 56 | item_3 | place | True |
| s20_on | item_2 | zone_SE | 82 | 88 | item_2 | move_to | True |
| s30_off | item_2 | zone_SE | 19 | 22 | item_3 | move_to | False |
| s30_off | item_4 | zone_SE | 19 | 22 | item_3 | move_to | False |
| s30_off | item_6 | zone_SE | 19 | 22 | item_3 | move_to | False |
| s30_off | item_3 | zone_SW | 23 | 38 | item_3 | move_to | True |
| s30_off | item_3 | zone_NW | 74 | 167 | item_3 | place | True |
| s30_off | item_7 | zone_NW | 74 | 97 | item_3 | place | False |
| s30_off | item_2 | zone_NW | 95 | 167 | item_7 | move_to | False |
| s30_off | item_7 | zone_NW | 121 | 167 | item_7 | place | True |
| s30_off | item_4 | zone_NW | 165 | 167 | - |  | False |
| s30_on | item_3 | zone_SW | 23 | 38 | item_3 | move_to | True |
| s30_on | item_3 | zone_NW | 74 | 167 | item_3 | place | True |
| s30_on | item_7 | zone_NW | 74 | 97 | item_3 | place | False |
| s30_on | item_7 | zone_NW | 121 | 167 | item_7 | place | True |

## (d) Held-item refutation episodes — while holding(human, X) is in the world

| condition | first_step | last_step | held_item | n_refuted | human_task | most_likely_tick_before | most_likely_at_start | confidence_at_start | most_likely_after_release | confidence_after_release |
|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 41 | 77 | item_3 | 4 | item_3 | item_3 | item_3 | 0.797 | item_7 | 0.351 |
| s00_off | 111 | 141 | item_2 | 4 | item_2 | item_2 | item_2 | 0.970 | item_4 | 0.366 |
| s00_on | 41 | 77 | item_3 | 4 | item_3 | item_3 | item_3 | 0.797 | item_2 | 0.510 |
| s00_on | 111 | 141 | item_2 | 4 | item_2 | item_2 | item_2 | 0.970 | item_2 | 0.632 |
| s10_off | 31 | 74 | item_2 | 7 | item_2 | item_2 | item_2 | 0.662 | item_0 | 0.460 |
| s10_off | 257 | 257 | item_4 | 7 | item_4 | item_0 | item_4 | 0.769 |  |  |
| s10_on | 31 | 74 | item_2 | 7 | item_2 | item_2 | item_2 | 0.662 | item_2 | 0.399 |
| s10_on | 257 | 257 | item_4 | 7 | item_4 | item_6 | item_4 | 0.769 |  |  |
| s20_off | 22 | 53 | item_3 | 4 | item_3 | item_3 | item_3 | 0.797 | item_6 | 0.277 |
| s20_off | 89 | 121 | item_2 | 4 | item_2 | item_7 | item_2 | 0.928 | item_4 | 0.562 |
| s20_on | 22 | 53 | item_3 | 4 | item_3 | item_3 | item_3 | 0.797 | item_3 | 0.641 |
| s20_on | 89 | 121 | item_2 | 4 | item_2 | item_2 | item_2 | 0.928 | item_3 | 0.500 |
| s30_off | 39 | 73 | item_3 | 4 | item_3 | item_3 | item_3 | 0.797 | item_7 | 0.382 |
| s30_off | 98 | 120 | item_7 | 4 | item_7 | item_7 | item_7 | 0.976 | item_7 | 0.311 |
| s30_on | 39 | 73 | item_3 | 4 | item_3 | item_3 | item_3 | 0.797 | item_7 | 0.730 |
| s30_on | 98 | 120 | item_7 | 4 | item_7 | item_7 | item_7 | 0.976 | item_7 | 0.757 |

## (e) Movement legs (one global leg for all hypotheses) against the human's actual action boundaries

| condition | first_moving_step | last_moving_step | n_moving_ticks | human_task_at_start | human_action_at_start | distinct_human_actions_spanned | distinct_human_tasks_spanned | closed_by | closing_microaction |
|---|---|---|---|---|---|---|---|---|---|
| s00_off | 1 | 39 | 39 | item_3 | move_to | 1 | 1 | stationary | stand |
| s00_off | 43 | 76 | 34 | item_3 | move_to | 1 | 1 | stationary | stand |
| s00_off | 81 | 109 | 29 | item_2 | move_to | 1 | 1 | stationary | stand |
| s00_off | 113 | 140 | 28 | item_2 | move_to | 1 | 1 | stationary | stand |
| s00_on | 1 | 39 | 39 | item_3 | move_to | 1 | 1 | stationary | stand |
| s00_on | 43 | 76 | 34 | item_3 | move_to | 1 | 1 | stationary | stand |
| s00_on | 81 | 109 | 29 | item_2 | move_to | 1 | 1 | stationary | stand |
| s00_on | 113 | 140 | 28 | item_2 | move_to | 1 | 1 | stationary | stand |
| s10_off | 1 | 29 | 29 | item_2 | move_to | 1 | 1 | stationary | stand |
| s10_off | 33 | 73 | 41 | item_2 | move_to | 1 | 1 | stationary | stand |
| s10_off | 78 | 127 | 50 | coffee_break | move_to | 1 | 1 | stationary | stand |
| s10_off | 161 | 255 | 95 | item_4 | move_to | 1 | 1 | stationary | stand |
| s10_on | 1 | 29 | 29 | item_2 | move_to | 1 | 1 | stationary | stand |
| s10_on | 33 | 73 | 41 | item_2 | move_to | 1 | 1 | stationary | stand |
| s10_on | 78 | 127 | 50 | coffee_break | move_to | 1 | 1 | stationary | stand |
| s10_on | 161 | 255 | 95 | item_4 | move_to | 1 | 1 | stationary | stand |
| s20_off | 1 | 20 | 20 | item_3 | move_to | 1 | 1 | stationary | stand |
| s20_off | 24 | 52 | 29 | item_3 | move_to | 1 | 1 | stationary | stand |
| s20_off | 57 | 87 | 31 | item_2 | move_to | 1 | 1 | stationary | stand |
| s20_off | 91 | 120 | 30 | item_2 | move_to | 1 | 1 | stationary | stand |
| s20_on | 1 | 20 | 20 | item_3 | move_to | 1 | 1 | stationary | stand |
| s20_on | 24 | 52 | 29 | item_3 | move_to | 1 | 1 | stationary | stand |
| s20_on | 57 | 87 | 31 | item_2 | move_to | 1 | 1 | stationary | stand |
| s20_on | 91 | 120 | 30 | item_2 | move_to | 1 | 1 | stationary | stand |
| s30_off | 1 | 37 | 37 | item_3 | move_to | 1 | 1 | stationary | stand |
| s30_off | 41 | 72 | 32 | item_3 | move_to | 1 | 1 | stationary | stand |
| s30_off | 77 | 96 | 20 | item_7 | move_to | 1 | 1 | stationary | stand |
| s30_off | 100 | 119 | 20 | item_7 | move_to | 1 | 1 | stationary | stand |
| s30_on | 1 | 37 | 37 | item_3 | move_to | 1 | 1 | stationary | stand |
| s30_on | 41 | 72 | 32 | item_3 | move_to | 1 | 1 | stationary | stand |
| s30_on | 77 | 96 | 20 | item_7 | move_to | 1 | 1 | stationary | stand |
| s30_on | 100 | 119 | 20 | item_7 | move_to | 1 | 1 | stationary | stand |

## (f) Completion predicates of the human's LIVE plan, evaluated externally against the WorldState the recognizer saw

| condition | human_task | action_index | action | completion_predicate | first_tick_executing | last_tick_executing | first_tick_predicate_true | ticks_predicate_true |
|---|---|---|---|---|---|---|---|---|
| s00_off | item_3 | 0 | move_to | at(human_0, item_3) | 0 | 39 | 39 | 4 |
| s00_off | item_3 | 1 | pick_up | holding(human_0, item_3) | 40 | 41 | 41 | 37 |
| s00_off | item_3 | 2 | move_to | at(human_0, kitting_table_0) | 42 | 76 | 76 | 4 |
| s00_off | item_3 | 3 | place | obj_at(item_3, kitting_table_0) | 77 | 78 | 78 | 2 |
| s00_off | item_2 | 0 | move_to | at(human_0, item_2) | 81 | 109 | 109 | 4 |
| s00_off | item_2 | 1 | pick_up | holding(human_0, item_2) | 110 | 111 | 111 | 31 |
| s00_off | item_2 | 2 | move_to | at(human_0, kitting_table_0) | 112 | 140 | 140 | 4 |
| s00_off | item_2 | 3 | place | obj_at(item_2, kitting_table_0) | 141 | 142 | 142 | 2 |
| s00_on | item_3 | 0 | move_to | at(human_0, item_3) | 0 | 39 | 39 | 4 |
| s00_on | item_3 | 1 | pick_up | holding(human_0, item_3) | 40 | 41 | 41 | 37 |
| s00_on | item_3 | 2 | move_to | at(human_0, kitting_table_0) | 42 | 76 | 76 | 4 |
| s00_on | item_3 | 3 | place | obj_at(item_3, kitting_table_0) | 77 | 78 | 78 | 2 |
| s00_on | item_2 | 0 | move_to | at(human_0, item_2) | 81 | 109 | 109 | 4 |
| s00_on | item_2 | 1 | pick_up | holding(human_0, item_2) | 110 | 111 | 111 | 31 |
| s00_on | item_2 | 2 | move_to | at(human_0, kitting_table_0) | 112 | 140 | 140 | 4 |
| s00_on | item_2 | 3 | place | obj_at(item_2, kitting_table_0) | 141 | 142 | 142 | 2 |
| s10_off | item_2 | 0 | move_to | at(human_0, item_2) | 0 | 29 | 29 | 4 |
| s10_off | item_2 | 1 | pick_up | holding(human_0, item_2) | 30 | 31 | 31 | 44 |
| s10_off | item_2 | 2 | move_to | at(human_0, kitting_table_0) | 32 | 73 | 73 | 4 |
| s10_off | item_2 | 3 | place | obj_at(item_2, kitting_table_0) | 74 | 75 | 75 | 2 |
| s10_off | coffee_break | 0 | move_to | at(human_0, coffee_machine_0) | 78 | 127 | 127 | 33 |
| s10_off | coffee_break | 1 | wait_at | ProcessCompletion | 128 | 158 |  | 0 |
| s10_off | item_4 | 0 | move_to | at(human_0, item_4) | 161 | 255 | 255 | 2 |
| s10_off | item_4 | 1 | pick_up | holding(human_0, item_4) | 256 | 257 | 257 | 1 |
| s10_off | item_4 | 2 | move_to | at(human_0, kitting_table_0) |  |  |  | 0 |
| s10_off | item_4 | 3 | place | obj_at(item_4, kitting_table_0) |  |  |  | 0 |
| s10_on | item_2 | 0 | move_to | at(human_0, item_2) | 0 | 29 | 29 | 4 |
| s10_on | item_2 | 1 | pick_up | holding(human_0, item_2) | 30 | 31 | 31 | 44 |
| s10_on | item_2 | 2 | move_to | at(human_0, kitting_table_0) | 32 | 73 | 73 | 4 |
| s10_on | item_2 | 3 | place | obj_at(item_2, kitting_table_0) | 74 | 75 | 75 | 2 |
| s10_on | coffee_break | 0 | move_to | at(human_0, coffee_machine_0) | 78 | 127 | 127 | 33 |
| s10_on | coffee_break | 1 | wait_at | ProcessCompletion | 128 | 158 |  | 0 |
| s10_on | item_4 | 0 | move_to | at(human_0, item_4) | 161 | 255 | 255 | 2 |
| s10_on | item_4 | 1 | pick_up | holding(human_0, item_4) | 256 | 257 | 257 | 1 |
| s10_on | item_4 | 2 | move_to | at(human_0, kitting_table_0) |  |  |  | 0 |
| s10_on | item_4 | 3 | place | obj_at(item_4, kitting_table_0) |  |  |  | 0 |
| s20_off | item_3 | 0 | move_to | at(human_0, item_3) | 0 | 20 | 20 | 4 |
| s20_off | item_3 | 1 | pick_up | holding(human_0, item_3) | 21 | 22 | 22 | 32 |
| s20_off | item_3 | 2 | move_to | at(human_0, kitting_table_0) | 23 | 52 | 52 | 4 |
| s20_off | item_3 | 3 | place | obj_at(item_3, kitting_table_0) | 53 | 54 | 54 | 2 |
| s20_off | item_2 | 0 | move_to | at(human_0, item_2) | 57 | 87 | 87 | 4 |
| s20_off | item_2 | 1 | pick_up | holding(human_0, item_2) | 88 | 89 | 89 | 33 |
| s20_off | item_2 | 2 | move_to | at(human_0, kitting_table_0) | 90 | 120 | 120 | 4 |
| s20_off | item_2 | 3 | place | obj_at(item_2, kitting_table_0) | 121 | 122 | 122 | 2 |
| s20_on | item_3 | 0 | move_to | at(human_0, item_3) | 0 | 20 | 20 | 4 |
| s20_on | item_3 | 1 | pick_up | holding(human_0, item_3) | 21 | 22 | 22 | 32 |
| s20_on | item_3 | 2 | move_to | at(human_0, kitting_table_0) | 23 | 52 | 52 | 4 |
| s20_on | item_3 | 3 | place | obj_at(item_3, kitting_table_0) | 53 | 54 | 54 | 2 |
| s20_on | item_2 | 0 | move_to | at(human_0, item_2) | 57 | 87 | 87 | 4 |
| s20_on | item_2 | 1 | pick_up | holding(human_0, item_2) | 88 | 89 | 89 | 33 |
| s20_on | item_2 | 2 | move_to | at(human_0, kitting_table_0) | 90 | 120 | 120 | 4 |
| s20_on | item_2 | 3 | place | obj_at(item_2, kitting_table_0) | 121 | 122 | 122 | 2 |
| s30_off | item_3 | 0 | move_to | at(human_0, item_3) | 0 | 37 | 37 | 4 |
| s30_off | item_3 | 1 | pick_up | holding(human_0, item_3) | 38 | 39 | 39 | 35 |
| s30_off | item_3 | 2 | move_to | at(human_0, kitting_table_0) | 40 | 72 | 72 | 4 |
| s30_off | item_3 | 3 | place | obj_at(item_3, kitting_table_0) | 73 | 74 | 74 | 2 |
| s30_off | item_7 | 0 | move_to | at(human_0, item_7) | 77 | 96 | 96 | 4 |
| s30_off | item_7 | 1 | pick_up | holding(human_0, item_7) | 97 | 98 | 98 | 23 |
| s30_off | item_7 | 2 | move_to | at(human_0, kitting_table_0) | 99 | 119 | 119 | 4 |
| s30_off | item_7 | 3 | place | obj_at(item_7, kitting_table_0) | 120 | 121 | 121 | 2 |
| s30_on | item_3 | 0 | move_to | at(human_0, item_3) | 0 | 37 | 37 | 4 |
| s30_on | item_3 | 1 | pick_up | holding(human_0, item_3) | 38 | 39 | 39 | 35 |
| s30_on | item_3 | 2 | move_to | at(human_0, kitting_table_0) | 40 | 72 | 72 | 4 |
| s30_on | item_3 | 3 | place | obj_at(item_3, kitting_table_0) | 73 | 74 | 74 | 2 |
| s30_on | item_7 | 0 | move_to | at(human_0, item_7) | 77 | 96 | 96 | 4 |
| s30_on | item_7 | 1 | pick_up | holding(human_0, item_7) | 97 | 98 | 98 | 23 |
| s30_on | item_7 | 2 | move_to | at(human_0, kitting_table_0) | 99 | 119 | 119 | 4 |
| s30_on | item_7 | 3 | place | obj_at(item_7, kitting_table_0) | 120 | 121 | 121 | 2 |

## (f2) Every action of every method, grounded from hypothesis bindings only (analysis-side); ticks (summed over hypotheses of that task) where the grounded predicate held

| condition | task | method_index | method | guards | step_index | action | microactions | completion_type | groundable_from_hyp_bindings | example_grounding | hyp_ticks_true_sum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | deliver_item | 0 | deliver_already_held | holding('?agent', '?item') | 0 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 170 |
| s00_off | deliver_item | 0 | deliver_already_held | holding('?agent', '?item') | 1 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_3, kitting_table_0) | 335 |
| s00_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 0 | move_to | STEP* | ConditionSchema | unbound:?target |  | 0 |
| s00_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 1 | place | ['RELEASE'] | ConditionSchema | unbound:?target |  | 0 |
| s00_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 2 | move_to | STEP* | ConditionSchema | grounded | at(human_0, item_3) | 129 |
| s00_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 3 | pick_up | ['GRASP'] | ConditionSchema | grounded | holding(human_0, item_3) | 68 |
| s00_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 4 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 170 |
| s00_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 5 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_3, kitting_table_0) | 335 |
| s00_off | deliver_item | 2 | deliver_default | - | 0 | move_to | STEP* | ConditionSchema | grounded | at(human_0, item_3) | 129 |
| s00_off | deliver_item | 2 | deliver_default | - | 1 | pick_up | ['GRASP'] | ConditionSchema | grounded | holding(human_0, item_3) | 68 |
| s00_off | deliver_item | 2 | deliver_default | - | 2 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 170 |
| s00_off | deliver_item | 2 | deliver_default | - | 3 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_3, kitting_table_0) | 335 |
| s10_off | deliver_item | 0 | deliver_already_held | holding('?agent', '?item') | 0 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 40 |
| s10_off | deliver_item | 0 | deliver_already_held | holding('?agent', '?item') | 1 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_0, kitting_table_0) | 418 |
| s10_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 0 | move_to | STEP* | ConditionSchema | unbound:?target |  | 0 |
| s10_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 1 | place | ['RELEASE'] | ConditionSchema | unbound:?target |  | 0 |
| s10_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 2 | move_to | STEP* | ConditionSchema | grounded | at(human_0, item_0) | 7 |
| s10_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 3 | pick_up | ['GRASP'] | ConditionSchema | grounded | holding(human_0, item_0) | 45 |
| s10_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 4 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 40 |
| s10_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 5 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_0, kitting_table_0) | 418 |
| s10_off | deliver_item | 2 | deliver_default | - | 0 | move_to | STEP* | ConditionSchema | grounded | at(human_0, item_0) | 7 |
| s10_off | deliver_item | 2 | deliver_default | - | 1 | pick_up | ['GRASP'] | ConditionSchema | grounded | holding(human_0, item_0) | 45 |
| s10_off | deliver_item | 2 | deliver_default | - | 2 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 40 |
| s10_off | deliver_item | 2 | deliver_default | - | 3 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_0, kitting_table_0) | 418 |
| s10_off | coffee_break | 0 | coffee_break_default | - | 0 | move_to | STEP* | ConditionSchema | grounded | at(human_0, coffee_machine_0) | 34 |
| s10_off | coffee_break | 0 | coffee_break_default | - | 1 | wait_at | STAND* | ProcessCompletion | process_completion |  | 0 |
| s20_off | deliver_item | 0 | deliver_already_held | holding('?agent', '?item') | 0 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 425 |
| s20_off | deliver_item | 0 | deliver_already_held | holding('?agent', '?item') | 1 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_4, kitting_table_0) | 400 |
| s20_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 0 | move_to | STEP* | ConditionSchema | unbound:?target |  | 0 |
| s20_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 1 | place | ['RELEASE'] | ConditionSchema | unbound:?target |  | 0 |
| s20_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 2 | move_to | STEP* | ConditionSchema | grounded | at(human_0, item_4) | 303 |
| s20_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 3 | pick_up | ['GRASP'] | ConditionSchema | grounded | holding(human_0, item_4) | 65 |
| s20_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 4 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 425 |
| s20_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 5 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_4, kitting_table_0) | 400 |
| s20_off | deliver_item | 2 | deliver_default | - | 0 | move_to | STEP* | ConditionSchema | grounded | at(human_0, item_4) | 303 |
| s20_off | deliver_item | 2 | deliver_default | - | 1 | pick_up | ['GRASP'] | ConditionSchema | grounded | holding(human_0, item_4) | 65 |
| s20_off | deliver_item | 2 | deliver_default | - | 2 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 425 |
| s20_off | deliver_item | 2 | deliver_default | - | 3 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_4, kitting_table_0) | 400 |
| s30_off | deliver_item | 0 | deliver_already_held | holding('?agent', '?item') | 0 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 270 |
| s30_off | deliver_item | 0 | deliver_already_held | holding('?agent', '?item') | 1 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_3, kitting_table_0) | 217 |
| s30_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 0 | move_to | STEP* | ConditionSchema | unbound:?target |  | 0 |
| s30_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 1 | place | ['RELEASE'] | ConditionSchema | unbound:?target |  | 0 |
| s30_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 2 | move_to | STEP* | ConditionSchema | grounded | at(human_0, item_3) | 155 |
| s30_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 3 | pick_up | ['GRASP'] | ConditionSchema | grounded | holding(human_0, item_3) | 58 |
| s30_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 4 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 270 |
| s30_off | deliver_item | 1 | deliver_with_return | holding('?agent', '?other'); not_equal('?other', '?item') | 5 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_3, kitting_table_0) | 217 |
| s30_off | deliver_item | 2 | deliver_default | - | 0 | move_to | STEP* | ConditionSchema | grounded | at(human_0, item_3) | 155 |
| s30_off | deliver_item | 2 | deliver_default | - | 1 | pick_up | ['GRASP'] | ConditionSchema | grounded | holding(human_0, item_3) | 58 |
| s30_off | deliver_item | 2 | deliver_default | - | 2 | move_to | STEP* | ConditionSchema | grounded | at(human_0, kitting_table_0) | 270 |
| s30_off | deliver_item | 2 | deliver_default | - | 3 | place | ['RELEASE'] | ConditionSchema | grounded | obj_at(item_3, kitting_table_0) | 217 |

## (g) Belief events (most_likely changes, θ crossings) with the state factors active at that tick

| condition | step | event | kind | microaction | most_likely | confidence | prev_most_likely | prev_confidence | human_task | human_action | correct | leg_start | zone_boosted_now | zone_boosted_prev | n_refuted_now | n_refuted_prev | held_item |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 0 | first | stationary | step | item_3 | 0.167 |  |  | item_3 | move_to | True |  |  |  | 0 | 0 |  |
| s00_off | 16 | most_likely_change | moving | step | item_4 | 0.269 | item_3 | 0.214 | item_3 | move_to | False |  | item_2,item_4 |  | 0 | 0 |  |
| s00_off | 22 | most_likely_change | moving | step | item_3 | 0.303 | item_4 | 0.270 | item_3 | move_to | True |  | item_3,item_6 | item_2,item_4 | 0 | 0 |  |
| s00_off | 41 | theta_up | discrete | grasp | item_3 | 0.797 | item_3 | 0.308 | item_3 | pick_up | True |  |  | item_3,item_6 | 4 | 0 | item_3 |
| s00_off | 78 | most_likely_change+theta_down | discrete | release | item_7 | 0.351 | item_3 | 0.797 | item_3 | place | False |  | item_3,item_7 |  | 0 | 4 |  |
| s00_off | 81 | most_likely_change | moving | step | item_2 | 0.291 | item_7 | 0.351 | item_2 | move_to | True | leg_start |  | item_3,item_7 | 0 | 0 |  |
| s00_off | 111 | theta_up | discrete | grasp | item_2 | 0.970 | item_2 | 0.396 | item_2 | pick_up | True |  |  | item_2,item_4 | 4 | 0 | item_2 |
| s00_off | 142 | most_likely_change+theta_down | discrete | release | item_4 | 0.366 | item_2 | 0.970 | item_2 | place | False |  |  |  | 0 | 4 |  |
| s00_on | 0 | first | stationary | step | unknown | 0.332 |  |  | item_3 | move_to | False |  |  |  | 0 | 0 |  |
| s00_on | 1 | most_likely_change | moving | step | item_3 | 0.507 | unknown | 0.332 | item_3 | move_to | True | leg_start |  |  | 0 | 0 |  |
| s00_on | 16 | most_likely_change | moving | step | item_2 | 0.532 | item_3 | 0.507 | item_3 | move_to | False |  | item_2 |  | 0 | 0 |  |
| s00_on | 22 | most_likely_change | moving | step | item_3 | 0.672 | item_2 | 0.532 | item_3 | move_to | True |  | item_3 | item_2 | 0 | 0 |  |
| s00_on | 41 | theta_up | discrete | grasp | item_3 | 0.797 | item_3 | 0.672 | item_3 | pick_up | True |  |  | item_3 | 4 | 0 | item_3 |
| s00_on | 78 | most_likely_change+theta_down | discrete | release | item_2 | 0.510 | item_3 | 0.797 | item_3 | place | False |  | item_3 |  | 0 | 4 |  |
| s00_on | 81 | theta_up | moving | step | item_2 | 0.856 | item_2 | 0.510 | item_2 | move_to | True | leg_start |  | item_3 | 0 | 0 |  |
| s00_on | 142 | theta_down | discrete | release | item_2 | 0.632 | item_2 | 0.970 | item_2 | place | True |  |  |  | 0 | 4 |  |
| s10_off | 0 | first | stationary | step | item_1 | 0.154 |  |  | item_2 | move_to | False |  | item_1,item_2,item_6 |  | 0 | 0 |  |
| s10_off | 1 | most_likely_change | moving | step | item_2 | 0.300 | item_1 | 0.154 | item_2 | move_to | True | leg_start | item_1,item_2,item_6 | item_1,item_2,item_6 | 0 | 0 |  |
| s10_off | 75 | most_likely_change | discrete | release | item_0 | 0.460 | item_2 | 0.662 | item_2 | place | False |  | item_0,item_2 |  | 0 | 7 |  |
| s10_off | 161 | most_likely_change | moving | step | item_6 | 0.478 | item_0 | 0.393 | item_4 | move_to | False | leg_start | item_6 | item_6 | 0 | 0 |  |
| s10_off | 209 | most_likely_change | moving | step | item_0 | 0.327 | item_6 | 0.485 | item_4 | move_to | False |  | item_4,item_5 | item_6 | 0 | 0 |  |
| s10_off | 257 | most_likely_change+theta_up | discrete | grasp | item_4 | 0.769 | item_0 | 0.327 | item_4 | pick_up | True |  |  | item_4,item_5 | 7 | 0 | item_4 |
| s10_on | 0 | first | stationary | step | item_6 | 0.249 |  |  | item_2 | move_to | False |  | item_2,item_6 |  | 0 | 0 |  |
| s10_on | 1 | most_likely_change | moving | step | item_2 | 0.521 | item_6 | 0.249 | item_2 | move_to | True | leg_start | item_2,item_6 | item_2,item_6 | 0 | 0 |  |
| s10_on | 78 | most_likely_change | moving | step | item_6 | 0.730 | item_2 | 0.399 | coffee_break | move_to | False | leg_start | item_2 | item_2 | 0 | 0 |  |
| s10_on | 107 | theta_up | moving | step | item_6 | 0.853 | item_6 | 0.730 | coffee_break | move_to | False |  | item_6 | item_2 | 0 | 0 |  |
| s10_on | 209 | theta_down | moving | step | item_6 | 0.738 | item_6 | 0.882 | item_4 | move_to | False |  | item_4 | item_6 | 0 | 0 |  |
| s10_on | 257 | most_likely_change+theta_up | discrete | grasp | item_4 | 0.769 | item_6 | 0.738 | item_4 | pick_up | True |  |  | item_4 | 7 | 0 | item_4 |
| s20_off | 0 | first | stationary | step | item_4 | 0.167 |  |  | item_3 | move_to | False |  |  |  | 0 | 0 |  |
| s20_off | 1 | most_likely_change | moving | step | item_3 | 0.248 | item_4 | 0.167 | item_3 | move_to | True | leg_start |  |  | 0 | 0 |  |
| s20_off | 22 | theta_up | discrete | grasp | item_3 | 0.797 | item_3 | 0.286 | item_3 | pick_up | True |  |  | item_3,item_4,item_6 | 4 | 0 | item_3 |
| s20_off | 54 | most_likely_change+theta_down | discrete | release | item_6 | 0.277 | item_3 | 0.797 | item_3 | place | False |  | item_3 |  | 0 | 4 |  |
| s20_off | 57 | most_likely_change | moving | step | item_4 | 0.305 | item_6 | 0.277 | item_2 | move_to | False | leg_start |  | item_3 | 0 | 0 |  |
| s20_off | 82 | most_likely_change | moving | step | item_7 | 0.320 | item_4 | 0.343 | item_2 | move_to | False |  | item_2,item_7 |  | 0 | 0 |  |
| s20_off | 89 | most_likely_change+theta_up | discrete | grasp | item_2 | 0.928 | item_7 | 0.320 | item_2 | pick_up | True |  |  | item_2,item_7 | 4 | 0 | item_2 |
| s20_off | 122 | most_likely_change+theta_down | discrete | release | item_4 | 0.562 | item_2 | 0.928 | item_2 | place | False |  |  |  | 0 | 4 |  |
| s20_on | 0 | first | stationary | step | unknown | 0.332 |  |  | item_3 | move_to | False |  |  |  | 0 | 0 |  |
| s20_on | 1 | most_likely_change | moving | step | item_3 | 0.641 | unknown | 0.332 | item_3 | move_to | True | leg_start |  |  | 0 | 0 |  |
| s20_on | 11 | theta_up | moving | step | item_3 | 0.780 | item_3 | 0.535 | item_3 | move_to | True |  | item_3 | item_2 | 0 | 0 |  |
| s20_on | 54 | theta_down | discrete | release | item_3 | 0.641 | item_3 | 0.797 | item_3 | place | True |  | item_3 |  | 0 | 4 |  |
| s20_on | 57 | most_likely_change | moving | step | item_2 | 0.743 | item_3 | 0.641 | item_2 | move_to | True | leg_start |  | item_3 | 0 | 0 |  |
| s20_on | 82 | theta_up | moving | step | item_2 | 0.851 | item_2 | 0.743 | item_2 | move_to | True |  | item_2 |  | 0 | 0 |  |
| s20_on | 122 | most_likely_change+theta_down | discrete | release | item_3 | 0.500 | item_2 | 0.928 | item_2 | place | False |  |  |  | 0 | 4 |  |
| s30_off | 0 | first | stationary | step | item_3 | 0.167 |  |  | item_3 | move_to | True |  |  |  | 0 | 0 |  |
| s30_off | 19 | most_likely_change | moving | step | item_4 | 0.259 | item_3 | 0.215 | item_3 | move_to | False |  | item_2,item_4,item_6 |  | 0 | 0 |  |
| s30_off | 23 | most_likely_change | moving | step | item_3 | 0.354 | item_4 | 0.259 | item_3 | move_to | True |  | item_3 | item_2,item_4,item_6 | 0 | 0 |  |
| s30_off | 39 | theta_up | discrete | grasp | item_3 | 0.797 | item_3 | 0.354 | item_3 | pick_up | True |  |  | item_3 | 4 | 0 | item_3 |
| s30_off | 74 | most_likely_change+theta_down | discrete | release | item_7 | 0.382 | item_3 | 0.797 | item_3 | place | False |  | item_3,item_7 |  | 0 | 4 |  |
| s30_off | 98 | theta_up | discrete | grasp | item_7 | 0.976 | item_7 | 0.615 | item_7 | pick_up | True |  |  | item_2,item_3,item_7 | 4 | 0 | item_7 |
| s30_off | 121 | theta_down | discrete | release | item_7 | 0.311 | item_7 | 0.976 | item_7 | place | True |  | item_2,item_3,item_7 |  | 0 | 4 |  |
| s30_off | 165 | most_likely_change | stationary | stand | item_4 | 0.308 | item_7 | 0.311 | - |  | False |  | item_2,item_3,item_4,item_7 | item_2,item_3,item_7 | 0 | 0 |  |
| s30_on | 0 | first | stationary | step | unknown | 0.332 |  |  | item_3 | move_to | False |  |  |  | 0 | 0 |  |
| s30_on | 1 | most_likely_change | moving | step | item_3 | 0.471 | unknown | 0.332 | item_3 | move_to | True | leg_start |  |  | 0 | 0 |  |
| s30_on | 39 | theta_up | discrete | grasp | item_3 | 0.797 | item_3 | 0.640 | item_3 | pick_up | True |  |  | item_3 | 4 | 0 | item_3 |
| s30_on | 74 | most_likely_change+theta_down | discrete | release | item_7 | 0.730 | item_3 | 0.797 | item_3 | place | False |  | item_3,item_7 |  | 0 | 4 |  |
| s30_on | 77 | theta_up | moving | step | item_7 | 0.917 | item_7 | 0.730 | item_7 | move_to | True | leg_start | item_3,item_7 | item_3,item_7 | 0 | 0 |  |

## (h) Chord likelihood values actually produced by the linear cosine kernel

| condition | chords | cos_min | cos_mean | cos_max | L_min | L_mean | L_max | L_equals_HIGH | L_below_NEUTRAL | L_correct_min | L_correct_mean | L_correct_max | L_wrong_min | L_wrong_mean | L_wrong_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 588 | -0.805 | 0.579 | 1.000 | 0.480 | 3.179 | 4.000 | 186 | 2 | 4.000 | 4.000 | 4.000 | 0.480 | 3.072 | 4.000 |
| s00_on | 198 | -0.387 | 0.619 | 1.000 | 1.296 | 3.258 | 4.000 | 96 | 0 | 4.000 | 4.000 | 4.000 | 1.296 | 2.869 | 4.000 |
| s10_off | 1679 | -0.979 | 0.399 | 1.000 | 0.140 | 2.828 | 4.000 | 124 | 302 | 4.000 | 4.000 | 4.000 | 0.140 | 2.735 | 3.983 |
| s10_on | 819 | -0.979 | 0.431 | 1.000 | 0.140 | 2.890 | 4.000 | 124 | 158 | 4.000 | 4.000 | 4.000 | 0.140 | 2.692 | 3.913 |
| s20_off | 491 | -0.898 | 0.333 | 1.000 | 0.299 | 2.699 | 4.000 | 111 | 67 | 4.000 | 4.000 | 4.000 | 0.299 | 2.548 | 4.000 |
| s20_on | 161 | -0.576 | 0.409 | 1.000 | 0.928 | 2.848 | 4.000 | 81 | 31 | 4.000 | 4.000 | 4.000 | 0.928 | 2.314 | 4.000 |
| s30_off | 493 | -0.988 | 0.523 | 1.000 | 0.124 | 3.071 | 4.000 | 97 | 26 | 4.000 | 4.000 | 4.000 | 0.124 | 2.949 | 4.000 |
| s30_on | 166 | -0.569 | 0.705 | 1.000 | 0.941 | 3.425 | 4.000 | 77 | 20 | 4.000 | 4.000 | 4.000 | 0.941 | 3.124 | 4.000 |

## (j) Discrete (event) ticks — the likelihood every hypothesis received from the event itself

| condition | step | microaction | human_task | human_action | likelihood_values | origin_passed | confidence | most_likely |
|---|---|---|---|---|---|---|---|---|
| s00_off | 41 | grasp | item_3 | pick_up | {1.0: 5} | [-284.09919128368006, -287.7686086797539] | 0.797 | item_3 |
| s00_off | 78 | release | item_3 | place | {1.0: 5} | [-7.399352322317554, 333.38934153802757] | 0.351 | item_7 |
| s00_off | 111 | grasp | item_2 | pick_up | {1.0: 5} | [389.8553747310403, -89.20819966845187] | 0.970 | item_2 |
| s00_off | 142 | release | item_2 | place | {1.0: 5} | [18.10570867556487, 329.60224168615736] | 0.366 | item_4 |
| s00_on | 41 | grasp | item_3 | pick_up | {1.0: 2} | [-284.09919128368006, -287.7686086797539] | 0.797 | item_3 |
| s00_on | 78 | release | item_3 | place | {1.0: 2} | [-7.399352322317554, 333.38934153802757] | 0.510 | item_2 |
| s00_on | 111 | grasp | item_2 | pick_up | {1.0: 2} | [389.8553747310403, -89.20819966845187] | 0.970 | item_2 |
| s00_on | 142 | release | item_2 | place | {1.0: 2} | [18.10570867556487, 329.60224168615736] | 0.632 | item_2 |
| s10_off | 31 | grasp | item_2 | pick_up | {1.0: 9} | [-926.7373437486307, -12.68872159165602] | 0.662 | item_2 |
| s10_off | 75 | release | item_2 | place | {1.0: 9} | [-213.68596372913578, 392.2282198325006] | 0.460 | item_0 |
| s10_off | 257 | grasp | item_4 | pick_up | {1.0: 9} | [933.981637302747, -299.7230641533652] | 0.769 | item_4 |
| s10_on | 31 | grasp | item_2 | pick_up | {1.0: 5} | [-926.7373437486307, -12.68872159165602] | 0.662 | item_2 |
| s10_on | 75 | release | item_2 | place | {1.0: 5} | [-213.68596372913578, 392.2282198325006] | 0.399 | item_2 |
| s10_on | 257 | grasp | item_4 | pick_up | {1.0: 5} | [933.981637302747, -299.7230641533652] | 0.769 | item_4 |
| s20_off | 22 | grasp | item_3 | pick_up | {1.0: 5} | [-155.10533927300781, -174.2770563829523] | 0.797 | item_3 |
| s20_off | 54 | release | item_3 | place | {1.0: 5} | [-3.873221195299976, 385.65941006813546] | 0.277 | item_6 |
| s20_off | 89 | grasp | item_2 | pick_up | {1.0: 5} | [392.55259057061767, -91.04445583367698] | 0.928 | item_2 |
| s20_off | 122 | release | item_2 | place | {1.0: 5} | [17.90026237056196, 377.6085426356359] | 0.562 | item_4 |
| s20_on | 22 | grasp | item_3 | pick_up | {1.0: 2} | [-155.10533927300781, -174.2770563829523] | 0.797 | item_3 |
| s20_on | 54 | release | item_3 | place | {1.0: 2} | [-3.873221195299976, 385.65941006813546] | 0.641 | item_3 |
| s20_on | 89 | grasp | item_2 | pick_up | {1.0: 2} | [392.55259057061767, -91.04445583367698] | 0.928 | item_2 |
| s20_on | 122 | release | item_2 | place | {1.0: 2} | [17.90026237056196, 377.6085426356359] | 0.500 | item_3 |
| s30_off | 39 | grasp | item_3 | pick_up | {1.0: 5} | [-186.54014374500463, -283.84817249400555] | 0.797 | item_3 |
| s30_off | 74 | release | item_3 | place | {1.0: 5} | [-5.85187901941282, 330.11579305320356] | 0.382 | item_7 |
| s30_off | 98 | grasp | item_7 | pick_up | {1.0: 5} | [-385.6898823643436, 204.72404206879315] | 0.976 | item_7 |
| s30_off | 121 | release | item_7 | place | {1.0: 5} | [-11.363540249915332, 345.71974980215634] | 0.311 | item_7 |
| s30_on | 39 | grasp | item_3 | pick_up | {1.0: 2} | [-186.54014374500463, -283.84817249400555] | 0.797 | item_3 |
| s30_on | 74 | release | item_3 | place | {1.0: 2} | [-5.85187901941282, 330.11579305320356] | 0.730 | item_7 |
| s30_on | 98 | grasp | item_7 | pick_up | {1.0: 2} | [-385.6898823643436, 204.72404206879315] | 0.976 | item_7 |
| s30_on | 121 | release | item_7 | place | {1.0: 2} | [-11.363540249915332, 345.71974980215634] | 0.757 | item_7 |

