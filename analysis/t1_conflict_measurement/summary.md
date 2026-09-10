# Auto-generated summary tables (analyze.py)

rows: total 93, primary 43, counterfactual 44 (of which degenerate 8), none 6


## Primary rows

| condition | step | trigger | confidence | most_likely | human_actual_task | hypothesis_matches_actual | robot_holding | candidate | is_current_task | cost | is_winner | min_d | argmin_t | min_at_window_end | robot_action_at_min | human_action_at_min | T_r | T_h |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 41 | theta_crossed | 0.80 | item_3 | item_3 | True |  | item_6 | True | 1025 | True | 136.39 | 259.00 | False | approach_shelf | carry_to_table | 1025.49 | 699.18 |
| s00_off | 41 | theta_crossed | 0.80 | item_3 | item_3 | True |  | item_4 | False | 1387 | False | 226.31 | 282.00 | False | approach_shelf | carry_to_table | 1386.99 | 699.18 |
| s00_off | 63 | task_committed | 0.80 | item_3 | item_3 | True | item_6 | item_6 | True | 582 | True | 301.67 | 279.00 | True | carry_to_table | placement | 581.67 | 279.18 |
| s00_off | 63 | task_committed | 0.80 | item_3 | item_3 | True | item_6 | item_4 | False | 1468 | False | 326.65 | 0.00 | False | return_held_item | carry_to_table | 1468.31 | 279.18 |
| s00_off | 111 | theta_crossed | 0.97 | item_2 | item_2 | True |  | item_4 | True | 1106 | True | 140.68 | 131.00 | False | approach_shelf | carry_to_table | 1105.77 | 588.27 |
| s00_off | 131 | task_committed | 0.97 | item_2 | item_2 | True | item_4 | item_4 | True | 689 | True | 480.02 | 208.00 | True | carry_to_table | placement | 689.02 | 208.27 |
| s00_on | 41 | theta_crossed | 0.80 | item_3 | item_3 | True |  | item_6 | True | 1025 | True | 136.39 | 259.00 | False | approach_shelf | carry_to_table | 1025.49 | 699.18 |
| s00_on | 41 | theta_crossed | 0.80 | item_3 | item_3 | True |  | item_4 | False | 1387 | False | 226.31 | 282.00 | False | approach_shelf | carry_to_table | 1386.99 | 699.18 |
| s00_on | 63 | task_committed | 0.80 | item_3 | item_3 | True | item_6 | item_6 | True | 582 | True | 301.67 | 279.00 | True | carry_to_table | placement | 581.67 | 279.18 |
| s00_on | 63 | task_committed | 0.80 | item_3 | item_3 | True | item_6 | item_4 | False | 1468 | False | 326.65 | 0.00 | False | return_held_item | carry_to_table | 1468.31 | 279.18 |
| s00_on | 81 | theta_crossed | 0.86 | item_2 | item_2 | True | item_6 | item_6 | True | 222 | True | 154.79 | 89.00 | False | carry_to_table | approach_shelf | 221.67 | 1178.89 |
| s00_on | 81 | theta_crossed | 0.86 | item_2 | item_2 | True | item_6 | item_4 | False | 1828 | False | 203.16 | 0.00 | False | return_held_item | approach_shelf | 1828.31 | 1178.89 |
| s00_on | 95 | no_current_task | 0.86 | item_2 | item_2 | True |  | item_4 | False | 1426 | True | 139.75 | 446.00 | False | approach_shelf | carry_to_table | 1425.77 | 898.89 |
| s00_on | 131 | task_committed | 0.97 | item_2 | item_2 | True | item_4 | item_4 | True | 689 | True | 480.02 | 208.00 | True | carry_to_table | placement | 689.02 | 208.27 |
| s10_off | 257 | theta_crossed | 0.77 | item_4 | item_4 | True |  | item_5 | True | 1308 | True | 24.49 | 1308.00 | True | placement | carry_to_table | 1308.30 | 1333.49 |
| s10_off | 262 | task_committed | 0.77 | item_4 | item_4 | True | item_5 | item_5 | True | 1190 | True | 63.49 | 1189.00 | True | placement | carry_to_table | 1189.86 | 1253.49 |
| s10_on | 107 | theta_crossed | 0.85 | item_6 | coffee_break | False |  | item_1 | True | 1820 | True | 89.56 | 159.00 | False | approach_shelf | approach_shelf | 1820.45 | 1379.62 |
| s10_on | 107 | theta_crossed | 0.85 | item_6 | coffee_break | False |  | item_5 | False | 2655 | False | 189.08 | 0.00 | False | approach_shelf | approach_shelf | 2654.59 | 1379.62 |
| s10_on | 142 | task_committed | 0.85 | item_6 | coffee_break | False | item_1 | item_1 | True | 1110 | True | 6.96 | 146.00 | False | carry_to_table | approach_shelf | 1109.72 | 1403.83 |
| s10_on | 142 | task_committed | 0.85 | item_6 | coffee_break | False | item_1 | item_5 | False | 3198 | False | 4.01 | 317.00 | False | approach_shelf | approach_shelf | 3198.01 | 1403.83 |
| s10_on | 200 | no_current_task | 0.88 | item_6 | item_4 | False |  | item_5 | False | 2448 | True | 661.30 | 1.00 | False | approach_shelf | approach_shelf | 2448.30 | 1277.97 |
| s10_on | 257 | theta_crossed | 0.77 | item_4 | item_4 | True |  | item_5 | True | 1308 | True | 24.49 | 1308.00 | True | placement | carry_to_table | 1308.30 | 1333.49 |
| s10_on | 262 | task_committed | 0.77 | item_4 | item_4 | True | item_5 | item_5 | True | 1190 | True | 63.49 | 1189.00 | True | placement | carry_to_table | 1189.86 | 1253.49 |
| s20_off | 22 | theta_crossed | 0.80 | item_3 | item_3 | True |  | item_4 | True | 612 | True | 16.31 | 595.00 | True | carry_to_table | placement | 612.31 | 595.85 |
| s20_off | 22 | theta_crossed | 0.80 | item_3 | item_3 | True |  | item_6 | False | 1078 | False | 185.43 | 2.00 | False | approach_shelf | carry_to_table | 1078.33 | 595.85 |
| s20_off | 22 | theta_crossed | 0.80 | item_3 | item_3 | True |  | item_7 | False | 1687 | False | 93.66 | 109.00 | False | approach_shelf | carry_to_table | 1686.68 | 595.85 |
| s20_off | 24 | task_committed | 0.80 | item_3 | item_3 | True | item_4 | item_4 | True | 570 | True | 5.85 | 569.00 | True | placement | carry_to_table | 569.95 | 575.85 |
| s20_off | 24 | task_committed | 0.80 | item_3 | item_3 | True | item_4 | item_6 | False | 1100 | False | 159.87 | 28.00 | False | return_placement | carry_to_table | 1100.27 | 575.85 |
| s20_off | 24 | task_committed | 0.80 | item_3 | item_3 | True | item_4 | item_7 | False | 1695 | False | 125.63 | 96.00 | False | approach_shelf | carry_to_table | 1695.43 | 575.85 |
| s20_off | 89 | theta_crossed | 0.93 | item_2 | item_2 | True |  | item_6 | True | 933 | True | 303.26 | 629.00 | True | carry_to_table | placement | 933.26 | 629.67 |
| s20_off | 89 | theta_crossed | 0.93 | item_2 | item_2 | True |  | item_7 | False | 1778 | False | 493.61 | 353.00 | False | approach_shelf | carry_to_table | 1778.41 | 629.67 |
| s20_off | 96 | task_committed | 0.93 | item_2 | item_2 | True | item_6 | item_6 | True | 810 | True | 299.86 | 509.00 | True | carry_to_table | placement | 809.86 | 509.67 |
| s20_off | 96 | task_committed | 0.93 | item_2 | item_2 | True | item_6 | item_7 | False | 1844 | False | 618.83 | 329.00 | False | approach_shelf | carry_to_table | 1844.09 | 509.67 |
| s20_on | 11 | theta_crossed | 0.78 | item_3 | item_3 | True |  | item_4 | True | 812 | True | 15.29 | 812.00 | True | placement | carry_to_table | 812.31 | 828.29 |
| s20_on | 11 | theta_crossed | 0.78 | item_3 | item_3 | True |  | item_6 | False | 1189 | False | 292.30 | 215.00 | False | approach_shelf | carry_to_table | 1188.73 | 828.29 |
| s20_on | 11 | theta_crossed | 0.78 | item_3 | item_3 | True |  | item_7 | False | 1841 | False | 41.29 | 336.00 | False | approach_shelf | carry_to_table | 1841.35 | 828.29 |
| s20_on | 23 | task_committed | 0.80 | item_3 | item_3 | True | item_4 | item_4 | True | 570 | True | 25.85 | 569.00 | True | placement | carry_to_table | 569.95 | 595.85 |
| s20_on | 23 | task_committed | 0.80 | item_3 | item_3 | True | item_4 | item_6 | False | 1100 | False | 159.36 | 28.00 | False | return_placement | carry_to_table | 1100.27 | 595.85 |
| s20_on | 23 | task_committed | 0.80 | item_3 | item_3 | True | item_4 | item_7 | False | 1695 | False | 111.90 | 106.00 | False | approach_shelf | carry_to_table | 1695.43 | 595.85 |
| s20_on | 82 | theta_crossed | 0.85 | item_2 | item_2 | True |  | item_6 | True | 1053 | True | 299.26 | 753.00 | True | carry_to_table | placement | 1053.26 | 753.96 |
| s20_on | 82 | theta_crossed | 0.85 | item_2 | item_2 | True |  | item_7 | False | 1733 | False | 380.52 | 388.00 | False | approach_shelf | carry_to_table | 1733.23 | 753.96 |
| s20_on | 95 | task_committed | 0.93 | item_2 | item_2 | True | item_6 | item_6 | True | 810 | True | 279.86 | 529.00 | True | carry_to_table | placement | 809.86 | 529.67 |
| s20_on | 95 | task_committed | 0.93 | item_2 | item_2 | True | item_6 | item_7 | False | 1844 | False | 611.12 | 339.00 | False | approach_shelf | carry_to_table | 1844.09 | 529.67 |


## Counterfactual rows (below-θ triggers, projection of that tick's most_likely) — NOT pooled with primary

| condition | step | trigger | confidence | most_likely | human_actual_task | hypothesis_matches_actual | robot_holding | candidate | is_current_task | cost | is_winner | min_d | argmin_t | min_at_window_end | robot_action_at_min | human_action_at_min | T_r | T_h |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 0 | no_current_task | 0.17 | item_3 | item_3 | True |  | item_4 | False | 1538 | False | 12.21 | 432.00 | False | approach_shelf | approach_shelf | 1537.95 | 1517.95 |
| s00_off | 0 | no_current_task | 0.17 | item_3 | item_3 | True |  | item_6 | False | 908 | False | 261.07 | 521.00 | False | carry_to_table | approach_shelf | 908.22 | 1517.95 |
| s00_off | 0 | no_current_task | 0.17 | item_3 | item_3 | True |  | item_7 | False | 586 | True | 352.21 | 383.00 | False | carry_to_table | approach_shelf | 585.50 | 1517.95 |
| s00_off | 7 | task_committed | 0.21 | item_3 | item_3 | True | item_7 | item_7 | True | 463 | True | 355.83 | 253.00 | False | carry_to_table | approach_shelf | 462.67 | 1377.95 |
| s00_off | 7 | task_committed | 0.21 | item_3 | item_3 | True | item_7 | item_4 | False | 1537 | False | 47.17 | 380.00 | False | approach_shelf | approach_shelf | 1536.92 | 1377.95 |
| s00_off | 7 | task_committed | 0.21 | item_3 | item_3 | True | item_7 | item_6 | False | 817 | False | 256.50 | 405.00 | False | carry_to_table | approach_shelf | 816.88 | 1377.95 |
| s00_off | 33 | no_current_task | 0.31 | item_3 | item_3 | True |  | item_4 | False | 1432 | False | 352.12 | 422.00 | False | approach_shelf | carry_to_table | 1431.67 | 857.95 |
| s00_off | 33 | no_current_task | 0.31 | item_3 | item_3 | True |  | item_6 | False | 1185 | True | 130.42 | 419.00 | False | approach_shelf | carry_to_table | 1185.49 | 857.95 |
| s00_off | 95 | no_current_task | 0.33 | item_2 | item_2 | True |  | item_4 | False | 1426 | True | 139.75 | 446.00 | False | approach_shelf | carry_to_table | 1425.77 | 898.89 |
| s00_on | 7 | task_committed | 0.51 | item_3 | item_3 | True | item_7 | item_7 | True | 463 | True | 355.83 | 253.00 | False | carry_to_table | approach_shelf | 462.67 | 1377.95 |
| s00_on | 7 | task_committed | 0.51 | item_3 | item_3 | True | item_7 | item_4 | False | 1537 | False | 47.17 | 380.00 | False | approach_shelf | approach_shelf | 1536.92 | 1377.95 |
| s00_on | 7 | task_committed | 0.51 | item_3 | item_3 | True | item_7 | item_6 | False | 817 | False | 256.50 | 405.00 | False | carry_to_table | approach_shelf | 816.88 | 1377.95 |
| s00_on | 33 | no_current_task | 0.67 | item_3 | item_3 | True |  | item_4 | False | 1432 | False | 352.12 | 422.00 | False | approach_shelf | carry_to_table | 1431.67 | 857.95 |
| s00_on | 33 | no_current_task | 0.67 | item_3 | item_3 | True |  | item_6 | False | 1185 | True | 130.42 | 419.00 | False | approach_shelf | carry_to_table | 1185.49 | 857.95 |
| s10_off | 0 | no_current_task | 0.15 | item_1 | item_2 | False |  | item_5 | False | 1996 | False | 303.79 | 1691.00 | True | carry_to_table | placement | 1995.79 | 1691.42 |
| s10_off | 0 | no_current_task | 0.15 | item_1 | item_2 | False |  | item_1 | False | 2457 | False | 126.78 | 939.00 | False | approach_shelf | carry_to_table | 2456.56 | 1691.42 |
| s10_off | 0 | no_current_task | 0.15 | item_1 | item_2 | False |  | item_7 | False | 1646 | True | 45.42 | 1645.00 | True | placement | carry_to_table | 1645.80 | 1691.42 |
| s10_off | 34 | task_committed | 0.66 | item_2 | item_2 | True | item_7 | item_7 | True | 971 | True | 173.78 | 796.00 | True | carry_to_table | placement | 970.78 | 796.74 |
| s10_off | 34 | task_committed | 0.66 | item_2 | item_2 | True | item_7 | item_5 | False | 2029 | False | 1209.73 | 795.00 | False | approach_shelf | carry_to_table | 2028.80 | 796.74 |
| s10_off | 34 | task_committed | 0.66 | item_2 | item_2 | True | item_7 | item_1 | False | 2404 | False | 751.06 | 545.00 | False | approach_shelf | carry_to_table | 2404.23 | 796.74 |
| s10_off | 85 | no_current_task | 0.65 | item_0 | coffee_break | False |  | item_5 | False | 2414 | False | 173.12 | 0.00 | False | approach_shelf | approach_shelf | 2414.49 | 1378.31 |
| s10_off | 85 | no_current_task | 0.65 | item_0 | coffee_break | False |  | item_1 | False | 2260 | True | 169.30 | 38.00 | False | approach_shelf | approach_shelf | 2260.45 | 1378.31 |
| s10_off | 142 | task_committed | 0.39 | item_0 | coffee_break | False | item_1 | item_1 | True | 1110 | True | 168.10 | 0.00 | False | carry_to_table | approach_shelf | 1109.72 | 1419.07 |
| s10_off | 142 | task_committed | 0.39 | item_0 | coffee_break | False | item_1 | item_5 | False | 3198 | False | 168.10 | 0.00 | False | return_held_item | approach_shelf | 3198.01 | 1419.07 |
| s10_off | 200 | no_current_task | 0.48 | item_6 | item_4 | False |  | item_5 | False | 2448 | True | 661.30 | 1.00 | False | approach_shelf | approach_shelf | 2448.30 | 1277.97 |
| s10_on | 0 | no_current_task | 0.25 | item_6 | item_2 | False |  | item_5 | False | 1996 | False | 788.60 | 0.00 | False | approach_shelf | approach_shelf | 1995.79 | 1083.00 |
| s10_on | 0 | no_current_task | 0.25 | item_6 | item_2 | False |  | item_1 | False | 2457 | False | 55.34 | 596.00 | False | approach_shelf | carry_to_table | 2456.56 | 1083.00 |
| s10_on | 0 | no_current_task | 0.25 | item_6 | item_2 | False |  | item_7 | False | 1646 | True | 561.80 | 1083.00 | True | carry_to_table | placement | 1645.80 | 1083.00 |
| s10_on | 34 | task_committed | 0.66 | item_2 | item_2 | True | item_7 | item_7 | True | 971 | True | 173.78 | 796.00 | True | carry_to_table | placement | 970.78 | 796.74 |
| s10_on | 34 | task_committed | 0.66 | item_2 | item_2 | True | item_7 | item_5 | False | 2029 | False | 1209.73 | 795.00 | False | approach_shelf | carry_to_table | 2028.80 | 796.74 |
| s10_on | 34 | task_committed | 0.66 | item_2 | item_2 | True | item_7 | item_1 | False | 2404 | False | 751.06 | 545.00 | False | approach_shelf | carry_to_table | 2404.23 | 796.74 |
| s10_on | 85 | no_current_task | 0.73 | item_6 | coffee_break | False |  | item_5 | False | 2414 | False | 173.12 | 0.00 | False | approach_shelf | approach_shelf | 2414.49 | 1658.62 |
| s10_on | 85 | no_current_task | 0.73 | item_6 | coffee_break | False |  | item_1 | False | 2260 | True | 147.14 | 175.00 | False | approach_shelf | approach_shelf | 2260.45 | 1658.62 |
| s20_off | 0 | no_current_task | 0.17 | item_4 | item_3 | False |  | item_4 | False | 1032 | True | 20.00 | 475.00 | False | carry_to_table | approach_shelf | 1032.31 | 1087.87 |
| s20_off | 0 | no_current_task | 0.17 | item_4 | item_3 | False |  | item_6 | False | 1372 | False | 224.96 | 503.00 | False | approach_shelf | pick_up | 1372.06 | 1087.87 |
| s20_off | 0 | no_current_task | 0.17 | item_4 | item_3 | False |  | item_7 | False | 2028 | False | 148.78 | 396.00 | False | approach_shelf | approach_shelf | 2027.73 | 1087.87 |


## Degenerate counterfactual rows (human finished, or hypothesis projects an item already at the table) — excluded from (d) and (e)

| condition | step | trigger | confidence | most_likely | human_actual_task | hypothesis_matches_actual | robot_holding | candidate | is_current_task | cost | is_winner | min_d | argmin_t | min_at_window_end | robot_action_at_min | human_action_at_min | T_r | T_h | human_actual_action | human_longest_leg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s20_off | 55 | no_current_task | 0.60 | item_4 | item_3 | False |  | item_6 | False | 1613 | True | 15.54 | 0.00 | False | approach_shelf | approach_shelf | 1613.26 | 16.85 | place | 14.90 |
| s20_off | 55 | no_current_task | 0.60 | item_4 | item_3 | False |  | item_7 | False | 1739 | False | 15.54 | 0.00 | False | approach_shelf | approach_shelf | 1739.10 | 16.85 | place | 14.90 |
| s20_off | 139 | no_current_task | 0.43 | item_4 |  | False |  | item_7 | False | 1741 | True | 29.12 | 10.00 | False | approach_shelf | approach_shelf | 1741.14 | 30.67 |  | 28.70 |
| s20_off | 183 | task_committed | 0.43 | item_4 |  | False | item_7 | item_7 | True | 851 | True | 820.16 | 30.00 | True | carry_to_table | placement | 851.16 | 30.67 |  | 28.70 |
| s20_on | 54 | no_current_task | 0.64 | item_3 | item_3 | True |  | item_6 | False | 1613 | True | 15.54 | 0.00 | False | approach_shelf | approach_shelf | 1613.26 | 16.85 | place | 14.90 |
| s20_on | 54 | no_current_task | 0.64 | item_3 | item_3 | True |  | item_7 | False | 1739 | False | 15.54 | 0.00 | False | approach_shelf | approach_shelf | 1739.10 | 16.85 | place | 14.90 |
| s20_on | 138 | no_current_task | 0.50 | item_3 |  | False |  | item_7 | False | 1741 | True | 29.12 | 10.00 | False | approach_shelf | approach_shelf | 1741.14 | 30.67 |  | 28.70 |
| s20_on | 182 | task_committed | 0.50 | item_3 |  | False | item_7 | item_7 | True | 851 | True | 820.16 | 30.00 | True | carry_to_table | placement | 851.16 | 30.67 |  | 28.70 |


## Rows with no projection

| condition | step | trigger | confidence | projection_reason | most_likely | candidate | cost | is_winner |
|---|---|---|---|---|---|---|---|---|
| s00_on | 0 | no_current_task | 0.33 | none(below_theta) | unknown | item_4 | 1538 | False |
| s00_on | 0 | no_current_task | 0.33 | none(below_theta) | unknown | item_6 | 908 | False |
| s00_on | 0 | no_current_task | 0.33 | none(below_theta) | unknown | item_7 | 586 | True |
| s20_on | 0 | no_current_task | 0.33 | none(below_theta) | unknown | item_4 | 1032 | True |
| s20_on | 0 | no_current_task | 0.33 | none(below_theta) | unknown | item_6 | 1372 | False |
| s20_on | 0 | no_current_task | 0.33 | none(below_theta) | unknown | item_7 | 2028 | False |


## (a) Conflict profile, primary rows, steps with d(t) < s

| condition | step | candidate | cost | min_d | n_intervals@10 | n_intervals@25 | n_intervals@50 | n_intervals@100 | steps_below@10 | steps_below@25 | steps_below@50 | steps_below@100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 41 | item_4 | 1387 | 226.31 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_off | 41 | item_6 | 1025 | 136.39 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_off | 63 | item_4 | 1468 | 326.65 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_off | 63 | item_6 | 582 | 301.67 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_off | 111 | item_4 | 1106 | 140.68 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_off | 131 | item_4 | 689 | 480.02 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | 41 | item_4 | 1387 | 226.31 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | 41 | item_6 | 1025 | 136.39 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | 63 | item_4 | 1468 | 326.65 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | 63 | item_6 | 582 | 301.67 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | 81 | item_4 | 1828 | 203.16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | 81 | item_6 | 222 | 154.79 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | 95 | item_4 | 1426 | 139.75 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s00_on | 131 | item_4 | 689 | 480.02 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s10_off | 257 | item_5 | 1308 | 24.49 | 0 | 1 | 1 | 1 | 0 | 1 | 187 | 433 |
| s10_off | 262 | item_5 | 1190 | 63.49 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 325 |
| s10_on | 107 | item_1 | 1820 | 89.56 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 85 |
| s10_on | 107 | item_5 | 2655 | 189.08 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s10_on | 142 | item_1 | 1110 | 6.96 | 1 | 1 | 1 | 1 | 12 | 42 | 86 | 174 |
| s10_on | 142 | item_5 | 3198 | 4.01 | 1 | 1 | 1 | 2 | 30 | 82 | 166 | 451 |
| s10_on | 200 | item_5 | 2448 | 661.30 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s10_on | 257 | item_5 | 1308 | 24.49 | 0 | 1 | 1 | 1 | 0 | 1 | 187 | 433 |
| s10_on | 262 | item_5 | 1190 | 63.49 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 325 |
| s20_off | 22 | item_4 | 612 | 16.31 | 0 | 1 | 1 | 1 | 0 | 61 | 164 | 350 |
| s20_off | 22 | item_6 | 1078 | 185.43 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_off | 22 | item_7 | 1687 | 93.66 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 47 |
| s20_off | 24 | item_4 | 570 | 5.85 | 1 | 1 | 1 | 1 | 23 | 75 | 155 | 314 |
| s20_off | 24 | item_6 | 1100 | 159.87 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_off | 24 | item_7 | 1695 | 125.63 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_off | 89 | item_6 | 933 | 303.26 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_off | 89 | item_7 | 1778 | 493.61 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_off | 96 | item_6 | 810 | 299.86 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_off | 96 | item_7 | 1844 | 618.83 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_on | 11 | item_4 | 812 | 15.29 | 0 | 1 | 1 | 1 | 0 | 72 | 188 | 398 |
| s20_on | 11 | item_6 | 1189 | 292.30 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_on | 11 | item_7 | 1841 | 41.29 | 0 | 0 | 1 | 1 | 0 | 0 | 36 | 118 |
| s20_on | 23 | item_4 | 570 | 25.85 | 0 | 0 | 1 | 1 | 0 | 0 | 124 | 294 |
| s20_on | 23 | item_6 | 1100 | 159.36 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_on | 23 | item_7 | 1695 | 111.90 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_on | 82 | item_6 | 1053 | 299.26 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_on | 82 | item_7 | 1733 | 380.52 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_on | 95 | item_6 | 810 | 279.86 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| s20_on | 95 | item_7 | 1844 | 611.12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


## (a) Where the close steps fall (primary rows with any step below 100)

| condition | step | candidate | s | steps_below | n_intervals | first_step | last_step | robot_phase_steps | human_phase_steps |
|---|---|---|---|---|---|---|---|---|---|
| s10_off | 257 | item_5 | 25 | 1 | 1 | 1308.00 | 1308.00 | placement:1 | carry_to_table:1 |
| s10_off | 257 | item_5 | 50 | 187 | 1 | 1122.00 | 1308.00 | carry_to_table:186;placement:1 | carry_to_table:187 |
| s10_off | 257 | item_5 | 100 | 433 | 1 | 876.00 | 1308.00 | carry_to_table:432;placement:1 | carry_to_table:433 |
| s10_off | 262 | item_5 | 100 | 325 | 1 | 865.00 | 1189.00 | carry_to_table:324;placement:1 | carry_to_table:325 |
| s10_on | 107 | item_1 | 100 | 85 | 1 | 117.00 | 201.00 | approach_shelf:85 | approach_shelf:85 |
| s10_on | 142 | item_1 | 10 | 12 | 1 | 141.00 | 152.00 | carry_to_table:12 | approach_shelf:12 |
| s10_on | 142 | item_1 | 25 | 42 | 1 | 126.00 | 167.00 | carry_to_table:42 | approach_shelf:42 |
| s10_on | 142 | item_1 | 50 | 86 | 1 | 104.00 | 189.00 | carry_to_table:86 | approach_shelf:86 |
| s10_on | 142 | item_1 | 100 | 174 | 1 | 60.00 | 233.00 | carry_to_table:174 | approach_shelf:174 |
| s10_on | 142 | item_5 | 10 | 30 | 1 | 302.00 | 331.00 | approach_shelf:30 | approach_shelf:30 |
| s10_on | 142 | item_5 | 25 | 82 | 1 | 276.00 | 357.00 | approach_shelf:82 | approach_shelf:82 |
| s10_on | 142 | item_5 | 50 | 166 | 1 | 234.00 | 399.00 | approach_shelf:166 | approach_shelf:166 |
| s10_on | 142 | item_5 | 100 | 451 | 2 | 150.00 | 636.00 | approach_shelf:451 | approach_shelf:334;carry_to_table:117 |
| s10_on | 257 | item_5 | 25 | 1 | 1 | 1308.00 | 1308.00 | placement:1 | carry_to_table:1 |
| s10_on | 257 | item_5 | 50 | 187 | 1 | 1122.00 | 1308.00 | carry_to_table:186;placement:1 | carry_to_table:187 |
| s10_on | 257 | item_5 | 100 | 433 | 1 | 876.00 | 1308.00 | carry_to_table:432;placement:1 | carry_to_table:433 |
| s10_on | 262 | item_5 | 100 | 325 | 1 | 865.00 | 1189.00 | carry_to_table:324;placement:1 | carry_to_table:325 |
| s20_off | 22 | item_4 | 25 | 61 | 1 | 535.00 | 595.00 | carry_to_table:61 | carry_to_table:60;placement:1 |
| s20_off | 22 | item_4 | 50 | 164 | 1 | 432.00 | 595.00 | carry_to_table:164 | carry_to_table:163;placement:1 |
| s20_off | 22 | item_4 | 100 | 350 | 1 | 246.00 | 595.00 | carry_to_table:350 | carry_to_table:349;placement:1 |
| s20_off | 22 | item_7 | 100 | 47 | 1 | 86.00 | 132.00 | approach_shelf:47 | carry_to_table:47 |
| s20_off | 24 | item_4 | 10 | 23 | 1 | 547.00 | 569.00 | carry_to_table:22;placement:1 | carry_to_table:23 |
| s20_off | 24 | item_4 | 25 | 75 | 1 | 495.00 | 569.00 | carry_to_table:74;placement:1 | carry_to_table:75 |
| s20_off | 24 | item_4 | 50 | 155 | 1 | 415.00 | 569.00 | carry_to_table:154;placement:1 | carry_to_table:155 |
| s20_off | 24 | item_4 | 100 | 314 | 1 | 256.00 | 569.00 | carry_to_table:313;placement:1 | carry_to_table:314 |
| s20_on | 11 | item_4 | 25 | 72 | 1 | 741.00 | 812.00 | carry_to_table:71;placement:1 | carry_to_table:72 |
| s20_on | 11 | item_4 | 50 | 188 | 1 | 625.00 | 812.00 | carry_to_table:187;placement:1 | carry_to_table:188 |
| s20_on | 11 | item_4 | 100 | 398 | 1 | 415.00 | 812.00 | carry_to_table:397;placement:1 | carry_to_table:398 |
| s20_on | 11 | item_7 | 50 | 36 | 1 | 318.00 | 353.00 | approach_shelf:36 | carry_to_table:36 |
| s20_on | 11 | item_7 | 100 | 118 | 1 | 277.00 | 394.00 | approach_shelf:118 | carry_to_table:118 |
| s20_on | 23 | item_4 | 50 | 124 | 1 | 446.00 | 569.00 | carry_to_table:123;placement:1 | carry_to_table:124 |
| s20_on | 23 | item_4 | 100 | 294 | 1 | 276.00 | 569.00 | carry_to_table:293;placement:1 | carry_to_table:294 |


## (c) Pause delay, primary rows

| condition | step | candidate | is_winner | cost | T_r | T_h | min_d | s | status | delta | delta_over_cost | clears_via_tail | clears_via_tail_only | unchecked_share_at_delta | hold_first_conflict_t | delta_ext_human_held_at_end |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 41 | item_6 | True | 1025 | 1025.500 | 699.200 | 136.390 | 10 | cleared | 0 | 0.000 | False | False | 0.318 |  | unresolvable |
| s00_off | 41 | item_6 | True | 1025 | 1025.500 | 699.200 | 136.390 | 25 | cleared | 0 | 0.000 | False | False | 0.318 |  | unresolvable |
| s00_off | 41 | item_6 | True | 1025 | 1025.500 | 699.200 | 136.390 | 50 | cleared | 0 | 0.000 | False | False | 0.318 |  | unresolvable |
| s00_off | 41 | item_6 | True | 1025 | 1025.500 | 699.200 | 136.390 | 100 | cleared | 0 | 0.000 | False | False | 0.318 | 447.000 | unresolvable |
| s00_off | 41 | item_4 | False | 1387 | 1387.000 | 699.200 | 226.310 | 10 | cleared | 0 | 0.000 | False | False | 0.496 |  | unresolvable |
| s00_off | 41 | item_4 | False | 1387 | 1387.000 | 699.200 | 226.310 | 25 | cleared | 0 | 0.000 | False | False | 0.496 |  | unresolvable |
| s00_off | 41 | item_4 | False | 1387 | 1387.000 | 699.200 | 226.310 | 50 | cleared | 0 | 0.000 | False | False | 0.496 |  | unresolvable |
| s00_off | 41 | item_4 | False | 1387 | 1387.000 | 699.200 | 226.310 | 100 | cleared | 0 | 0.000 | False | False | 0.496 | 447.000 | unresolvable |
| s00_off | 63 | item_6 | True | 582 | 581.700 | 279.200 | 301.670 | 10 | cleared | 0 | 0.000 | False | False | 0.520 |  | unresolvable |
| s00_off | 63 | item_6 | True | 582 | 581.700 | 279.200 | 301.670 | 25 | cleared | 0 | 0.000 | False | False | 0.520 |  | unresolvable |
| s00_off | 63 | item_6 | True | 582 | 581.700 | 279.200 | 301.670 | 50 | cleared | 0 | 0.000 | False | False | 0.520 |  | unresolvable |
| s00_off | 63 | item_6 | True | 582 | 581.700 | 279.200 | 301.670 | 100 | cleared | 0 | 0.000 | False | False | 0.520 |  | unresolvable |
| s00_off | 63 | item_4 | False | 1468 | 1468.300 | 279.200 | 326.650 | 10 | cleared | 0 | 0.000 | False | False | 0.810 |  | unresolvable |
| s00_off | 63 | item_4 | False | 1468 | 1468.300 | 279.200 | 326.650 | 25 | cleared | 0 | 0.000 | False | False | 0.810 |  | unresolvable |
| s00_off | 63 | item_4 | False | 1468 | 1468.300 | 279.200 | 326.650 | 50 | cleared | 0 | 0.000 | False | False | 0.810 |  | unresolvable |
| s00_off | 63 | item_4 | False | 1468 | 1468.300 | 279.200 | 326.650 | 100 | cleared | 0 | 0.000 | False | False | 0.810 |  | unresolvable |
| s00_off | 111 | item_4 | True | 1106 | 1105.800 | 588.300 | 140.680 | 10 | cleared | 0 | 0.000 | False | False | 0.468 |  | unresolvable |
| s00_off | 111 | item_4 | True | 1106 | 1105.800 | 588.300 | 140.680 | 25 | cleared | 0 | 0.000 | False | False | 0.468 |  | unresolvable |
| s00_off | 111 | item_4 | True | 1106 | 1105.800 | 588.300 | 140.680 | 50 | cleared | 0 | 0.000 | False | False | 0.468 |  | unresolvable |
| s00_off | 111 | item_4 | True | 1106 | 1105.800 | 588.300 | 140.680 | 100 | cleared | 0 | 0.000 | False | False | 0.468 |  | unresolvable |
| s00_off | 131 | item_4 | True | 689 | 689.000 | 208.300 | 480.020 | 10 | cleared | 0 | 0.000 | False | False | 0.698 |  | unresolvable |
| s00_off | 131 | item_4 | True | 689 | 689.000 | 208.300 | 480.020 | 25 | cleared | 0 | 0.000 | False | False | 0.698 |  | unresolvable |
| s00_off | 131 | item_4 | True | 689 | 689.000 | 208.300 | 480.020 | 50 | cleared | 0 | 0.000 | False | False | 0.698 |  | unresolvable |
| s00_off | 131 | item_4 | True | 689 | 689.000 | 208.300 | 480.020 | 100 | cleared | 0 | 0.000 | False | False | 0.698 |  | unresolvable |
| s00_on | 41 | item_6 | True | 1025 | 1025.500 | 699.200 | 136.390 | 10 | cleared | 0 | 0.000 | False | False | 0.318 |  | unresolvable |
| s00_on | 41 | item_6 | True | 1025 | 1025.500 | 699.200 | 136.390 | 25 | cleared | 0 | 0.000 | False | False | 0.318 |  | unresolvable |
| s00_on | 41 | item_6 | True | 1025 | 1025.500 | 699.200 | 136.390 | 50 | cleared | 0 | 0.000 | False | False | 0.318 |  | unresolvable |
| s00_on | 41 | item_6 | True | 1025 | 1025.500 | 699.200 | 136.390 | 100 | cleared | 0 | 0.000 | False | False | 0.318 | 447.000 | unresolvable |
| s00_on | 41 | item_4 | False | 1387 | 1387.000 | 699.200 | 226.310 | 10 | cleared | 0 | 0.000 | False | False | 0.496 |  | unresolvable |
| s00_on | 41 | item_4 | False | 1387 | 1387.000 | 699.200 | 226.310 | 25 | cleared | 0 | 0.000 | False | False | 0.496 |  | unresolvable |
| s00_on | 41 | item_4 | False | 1387 | 1387.000 | 699.200 | 226.310 | 50 | cleared | 0 | 0.000 | False | False | 0.496 |  | unresolvable |
| s00_on | 41 | item_4 | False | 1387 | 1387.000 | 699.200 | 226.310 | 100 | cleared | 0 | 0.000 | False | False | 0.496 | 447.000 | unresolvable |
| s00_on | 63 | item_6 | True | 582 | 581.700 | 279.200 | 301.670 | 10 | cleared | 0 | 0.000 | False | False | 0.520 |  | unresolvable |
| s00_on | 63 | item_6 | True | 582 | 581.700 | 279.200 | 301.670 | 25 | cleared | 0 | 0.000 | False | False | 0.520 |  | unresolvable |
| s00_on | 63 | item_6 | True | 582 | 581.700 | 279.200 | 301.670 | 50 | cleared | 0 | 0.000 | False | False | 0.520 |  | unresolvable |
| s00_on | 63 | item_6 | True | 582 | 581.700 | 279.200 | 301.670 | 100 | cleared | 0 | 0.000 | False | False | 0.520 |  | unresolvable |
| s00_on | 63 | item_4 | False | 1468 | 1468.300 | 279.200 | 326.650 | 10 | cleared | 0 | 0.000 | False | False | 0.810 |  | unresolvable |
| s00_on | 63 | item_4 | False | 1468 | 1468.300 | 279.200 | 326.650 | 25 | cleared | 0 | 0.000 | False | False | 0.810 |  | unresolvable |
| s00_on | 63 | item_4 | False | 1468 | 1468.300 | 279.200 | 326.650 | 50 | cleared | 0 | 0.000 | False | False | 0.810 |  | unresolvable |
| s00_on | 63 | item_4 | False | 1468 | 1468.300 | 279.200 | 326.650 | 100 | cleared | 0 | 0.000 | False | False | 0.810 |  | unresolvable |
| s00_on | 81 | item_6 | True | 222 | 221.700 | 1178.900 | 154.790 | 10 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s00_on | 81 | item_6 | True | 222 | 221.700 | 1178.900 | 154.790 | 25 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s00_on | 81 | item_6 | True | 222 | 221.700 | 1178.900 | 154.790 | 50 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s00_on | 81 | item_6 | True | 222 | 221.700 | 1178.900 | 154.790 | 100 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s00_on | 81 | item_4 | False | 1828 | 1828.300 | 1178.900 | 203.160 | 10 | cleared | 0 | 0.000 | False | False | 0.355 |  | unresolvable |
| s00_on | 81 | item_4 | False | 1828 | 1828.300 | 1178.900 | 203.160 | 25 | cleared | 0 | 0.000 | False | False | 0.355 |  | unresolvable |
| s00_on | 81 | item_4 | False | 1828 | 1828.300 | 1178.900 | 203.160 | 50 | cleared | 0 | 0.000 | False | False | 0.355 |  | unresolvable |
| s00_on | 81 | item_4 | False | 1828 | 1828.300 | 1178.900 | 203.160 | 100 | cleared | 0 | 0.000 | False | False | 0.355 |  | unresolvable |
| s00_on | 95 | item_4 | True | 1426 | 1425.800 | 898.900 | 139.750 | 10 | cleared | 0 | 0.000 | False | False | 0.370 |  | unresolvable |
| s00_on | 95 | item_4 | True | 1426 | 1425.800 | 898.900 | 139.750 | 25 | cleared | 0 | 0.000 | False | False | 0.370 | 882.000 | unresolvable |
| s00_on | 95 | item_4 | True | 1426 | 1425.800 | 898.900 | 139.750 | 50 | cleared | 0 | 0.000 | False | False | 0.370 | 850.000 | unresolvable |
| s00_on | 95 | item_4 | True | 1426 | 1425.800 | 898.900 | 139.750 | 100 | cleared | 0 | 0.000 | False | False | 0.370 | 798.000 | unresolvable |
| s00_on | 131 | item_4 | True | 689 | 689.000 | 208.300 | 480.020 | 10 | cleared | 0 | 0.000 | False | False | 0.698 |  | unresolvable |
| s00_on | 131 | item_4 | True | 689 | 689.000 | 208.300 | 480.020 | 25 | cleared | 0 | 0.000 | False | False | 0.698 |  | unresolvable |
| s00_on | 131 | item_4 | True | 689 | 689.000 | 208.300 | 480.020 | 50 | cleared | 0 | 0.000 | False | False | 0.698 |  | unresolvable |
| s00_on | 131 | item_4 | True | 689 | 689.000 | 208.300 | 480.020 | 100 | cleared | 0 | 0.000 | False | False | 0.698 |  | unresolvable |
| s10_off | 257 | item_5 | True | 1308 | 1308.300 | 1333.500 | 24.490 | 10 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s10_off | 257 | item_5 | True | 1308 | 1308.300 | 1333.500 | 24.490 | 25 | cleared | 51 | 0.039 | True | False | 0.020 |  | unresolvable |
| s10_off | 257 | item_5 | True | 1308 | 1308.300 | 1333.500 | 24.490 | 50 | cleared | 76 | 0.058 | True | False | 0.039 |  | unresolvable |
| s10_off | 257 | item_5 | True | 1308 | 1308.300 | 1333.500 | 24.490 | 100 | cleared | 126 | 0.096 | True | False | 0.077 |  | unresolvable |
| s10_off | 262 | item_5 | True | 1190 | 1189.900 | 1253.500 | 63.490 | 10 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s10_off | 262 | item_5 | True | 1190 | 1189.900 | 1253.500 | 63.490 | 25 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s10_off | 262 | item_5 | True | 1190 | 1189.900 | 1253.500 | 63.490 | 50 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s10_off | 262 | item_5 | True | 1190 | 1189.900 | 1253.500 | 63.490 | 100 | cleared | 165 | 0.139 | True | True | 0.085 |  | unresolvable |
| s10_on | 107 | item_1 | True | 1820 | 1820.400 | 1379.600 | 89.560 | 10 | cleared | 0 | 0.000 | False | False | 0.242 |  | unresolvable |
| s10_on | 107 | item_1 | True | 1820 | 1820.400 | 1379.600 | 89.560 | 25 | cleared | 0 | 0.000 | False | False | 0.242 |  | unresolvable |
| s10_on | 107 | item_1 | True | 1820 | 1820.400 | 1379.600 | 89.560 | 50 | cleared | 0 | 0.000 | False | False | 0.242 |  | unresolvable |
| s10_on | 107 | item_1 | True | 1820 | 1820.400 | 1379.600 | 89.560 | 100 | cleared | 13 | 0.007 | False | False | 0.249 |  | unresolvable |
| s10_on | 107 | item_5 | False | 2655 | 2654.600 | 1379.600 | 189.080 | 10 | cleared | 0 | 0.000 | False | False | 0.480 |  | unresolvable |
| s10_on | 107 | item_5 | False | 2655 | 2654.600 | 1379.600 | 189.080 | 25 | cleared | 0 | 0.000 | False | False | 0.480 |  | unresolvable |
| s10_on | 107 | item_5 | False | 2655 | 2654.600 | 1379.600 | 189.080 | 50 | cleared | 0 | 0.000 | False | False | 0.480 |  | unresolvable |
| s10_on | 107 | item_5 | False | 2655 | 2654.600 | 1379.600 | 189.080 | 100 | cleared | 0 | 0.000 | False | False | 0.480 |  | unresolvable |
| s10_on | 142 | item_1 | True | 1110 | 1109.700 | 1403.800 | 6.960 | 10 | cleared | 4 | 0.004 | False | False | 0.000 |  | 4 |
| s10_on | 142 | item_1 | True | 1110 | 1109.700 | 1403.800 | 6.960 | 25 | cleared | 23 | 0.021 | False | False | 0.000 |  | 23 |
| s10_on | 142 | item_1 | True | 1110 | 1109.700 | 1403.800 | 6.960 | 50 | cleared | 53 | 0.048 | False | False | 0.000 |  | 53 |
| s10_on | 142 | item_1 | True | 1110 | 1109.700 | 1403.800 | 6.960 | 100 | cleared | 114 | 0.103 | False | False | 0.000 |  | 114 |
| s10_on | 142 | item_5 | False | 3198 | 3198.000 | 1403.800 | 4.010 | 10 | cleared | 15 | 0.005 | False | False | 0.566 |  | unresolvable |
| s10_on | 142 | item_5 | False | 3198 | 3198.000 | 1403.800 | 4.010 | 25 | cleared | 31 | 0.010 | False | False | 0.571 |  | unresolvable |
| s10_on | 142 | item_5 | False | 3198 | 3198.000 | 1403.800 | 4.010 | 50 | cleared | 152 | 0.048 | False | False | 0.609 |  | unresolvable |
| s10_on | 142 | item_5 | False | 3198 | 3198.000 | 1403.800 | 4.010 | 100 | cleared | 209 | 0.065 | False | False | 0.626 |  | unresolvable |
| s10_on | 200 | item_5 | True | 2448 | 2448.300 | 1278.000 | 661.300 | 10 | cleared | 0 | 0.000 | False | False | 0.478 |  | unresolvable |
| s10_on | 200 | item_5 | True | 2448 | 2448.300 | 1278.000 | 661.300 | 25 | cleared | 0 | 0.000 | False | False | 0.478 | 1228.000 | unresolvable |
| s10_on | 200 | item_5 | True | 2448 | 2448.300 | 1278.000 | 661.300 | 50 | cleared | 0 | 0.000 | False | False | 0.478 | 1202.000 | unresolvable |
| s10_on | 200 | item_5 | True | 2448 | 2448.300 | 1278.000 | 661.300 | 100 | cleared | 0 | 0.000 | False | False | 0.478 | 1151.000 | unresolvable |
| s10_on | 257 | item_5 | True | 1308 | 1308.300 | 1333.500 | 24.490 | 10 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s10_on | 257 | item_5 | True | 1308 | 1308.300 | 1333.500 | 24.490 | 25 | cleared | 51 | 0.039 | True | False | 0.020 |  | unresolvable |
| s10_on | 257 | item_5 | True | 1308 | 1308.300 | 1333.500 | 24.490 | 50 | cleared | 76 | 0.058 | True | False | 0.039 |  | unresolvable |
| s10_on | 257 | item_5 | True | 1308 | 1308.300 | 1333.500 | 24.490 | 100 | cleared | 126 | 0.096 | True | False | 0.077 |  | unresolvable |
| s10_on | 262 | item_5 | True | 1190 | 1189.900 | 1253.500 | 63.490 | 10 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s10_on | 262 | item_5 | True | 1190 | 1189.900 | 1253.500 | 63.490 | 25 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s10_on | 262 | item_5 | True | 1190 | 1189.900 | 1253.500 | 63.490 | 50 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s10_on | 262 | item_5 | True | 1190 | 1189.900 | 1253.500 | 63.490 | 100 | cleared | 165 | 0.139 | True | True | 0.085 |  | unresolvable |
| s20_off | 22 | item_4 | True | 612 | 612.300 | 595.900 | 16.310 | 10 | cleared | 0 | 0.000 | False | False | 0.027 |  | unresolvable |
| s20_off | 22 | item_4 | True | 612 | 612.300 | 595.900 | 16.310 | 25 | cleared | 9 | 0.015 | True | False | 0.042 |  | unresolvable |
| s20_off | 22 | item_4 | True | 612 | 612.300 | 595.900 | 16.310 | 50 | cleared | 34 | 0.056 | True | False | 0.082 |  | unresolvable |
| s20_off | 22 | item_4 | True | 612 | 612.300 | 595.900 | 16.310 | 100 | cleared | 84 | 0.137 | True | False | 0.164 |  | unresolvable |
| s20_off | 22 | item_6 | False | 1078 | 1078.300 | 595.900 | 185.430 | 10 | cleared | 0 | 0.000 | False | False | 0.447 |  | unresolvable |
| s20_off | 22 | item_6 | False | 1078 | 1078.300 | 595.900 | 185.430 | 25 | cleared | 0 | 0.000 | False | False | 0.447 |  | unresolvable |
| s20_off | 22 | item_6 | False | 1078 | 1078.300 | 595.900 | 185.430 | 50 | cleared | 0 | 0.000 | False | False | 0.447 |  | unresolvable |
| s20_off | 22 | item_6 | False | 1078 | 1078.300 | 595.900 | 185.430 | 100 | cleared | 0 | 0.000 | False | False | 0.447 |  | unresolvable |
| s20_off | 22 | item_7 | False | 1687 | 1686.700 | 595.900 | 93.660 | 10 | cleared | 0 | 0.000 | False | False | 0.647 |  | unresolvable |
| s20_off | 22 | item_7 | False | 1687 | 1686.700 | 595.900 | 93.660 | 25 | cleared | 0 | 0.000 | False | False | 0.647 |  | unresolvable |
| s20_off | 22 | item_7 | False | 1687 | 1686.700 | 595.900 | 93.660 | 50 | cleared | 0 | 0.000 | False | False | 0.647 |  | unresolvable |
| s20_off | 22 | item_7 | False | 1687 | 1686.700 | 595.900 | 93.660 | 100 | cleared | 10 | 0.006 | False | False | 0.653 |  | unresolvable |
| s20_off | 24 | item_4 | True | 570 | 569.900 | 575.900 | 5.850 | 10 | cleared | 17 | 0.030 | True | True | 0.019 |  | unresolvable |
| s20_off | 24 | item_4 | True | 570 | 569.900 | 575.900 | 5.850 | 25 | cleared | 32 | 0.056 | True | True | 0.046 |  | unresolvable |
| s20_off | 24 | item_4 | True | 570 | 569.900 | 575.900 | 5.850 | 50 | cleared | 57 | 0.100 | True | True | 0.090 |  | unresolvable |
| s20_off | 24 | item_4 | True | 570 | 569.900 | 575.900 | 5.850 | 100 | cleared | 107 | 0.188 | True | True | 0.177 |  | unresolvable |
| s20_off | 24 | item_6 | False | 1100 | 1100.300 | 575.900 | 159.870 | 10 | cleared | 0 | 0.000 | False | False | 0.477 |  | unresolvable |
| s20_off | 24 | item_6 | False | 1100 | 1100.300 | 575.900 | 159.870 | 25 | cleared | 0 | 0.000 | False | False | 0.477 |  | unresolvable |
| s20_off | 24 | item_6 | False | 1100 | 1100.300 | 575.900 | 159.870 | 50 | cleared | 0 | 0.000 | False | False | 0.477 |  | unresolvable |
| s20_off | 24 | item_6 | False | 1100 | 1100.300 | 575.900 | 159.870 | 100 | cleared | 0 | 0.000 | False | False | 0.477 |  | unresolvable |
| s20_off | 24 | item_7 | False | 1695 | 1695.400 | 575.900 | 125.630 | 10 | cleared | 0 | 0.000 | False | False | 0.660 |  | unresolvable |
| s20_off | 24 | item_7 | False | 1695 | 1695.400 | 575.900 | 125.630 | 25 | cleared | 0 | 0.000 | False | False | 0.660 |  | unresolvable |
| s20_off | 24 | item_7 | False | 1695 | 1695.400 | 575.900 | 125.630 | 50 | cleared | 0 | 0.000 | False | False | 0.660 |  | unresolvable |
| s20_off | 24 | item_7 | False | 1695 | 1695.400 | 575.900 | 125.630 | 100 | cleared | 0 | 0.000 | False | False | 0.660 |  | unresolvable |
| s20_off | 89 | item_6 | True | 933 | 933.300 | 629.700 | 303.260 | 10 | cleared | 0 | 0.000 | False | False | 0.325 |  | unresolvable |
| s20_off | 89 | item_6 | True | 933 | 933.300 | 629.700 | 303.260 | 25 | cleared | 0 | 0.000 | False | False | 0.325 |  | unresolvable |
| s20_off | 89 | item_6 | True | 933 | 933.300 | 629.700 | 303.260 | 50 | cleared | 0 | 0.000 | False | False | 0.325 |  | unresolvable |
| s20_off | 89 | item_6 | True | 933 | 933.300 | 629.700 | 303.260 | 100 | cleared | 0 | 0.000 | False | False | 0.325 |  | unresolvable |
| s20_off | 89 | item_7 | False | 1778 | 1778.400 | 629.700 | 493.610 | 10 | cleared | 0 | 0.000 | False | False | 0.646 |  | unresolvable |
| s20_off | 89 | item_7 | False | 1778 | 1778.400 | 629.700 | 493.610 | 25 | cleared | 0 | 0.000 | False | False | 0.646 |  | unresolvable |
| s20_off | 89 | item_7 | False | 1778 | 1778.400 | 629.700 | 493.610 | 50 | cleared | 0 | 0.000 | False | False | 0.646 |  | unresolvable |
| s20_off | 89 | item_7 | False | 1778 | 1778.400 | 629.700 | 493.610 | 100 | cleared | 0 | 0.000 | False | False | 0.646 |  | unresolvable |
| s20_off | 96 | item_6 | True | 810 | 809.900 | 509.700 | 299.860 | 10 | cleared | 0 | 0.000 | False | False | 0.371 |  | unresolvable |
| s20_off | 96 | item_6 | True | 810 | 809.900 | 509.700 | 299.860 | 25 | cleared | 0 | 0.000 | False | False | 0.371 |  | unresolvable |
| s20_off | 96 | item_6 | True | 810 | 809.900 | 509.700 | 299.860 | 50 | cleared | 0 | 0.000 | False | False | 0.371 |  | unresolvable |
| s20_off | 96 | item_6 | True | 810 | 809.900 | 509.700 | 299.860 | 100 | cleared | 0 | 0.000 | False | False | 0.371 |  | unresolvable |
| s20_off | 96 | item_7 | False | 1844 | 1844.100 | 509.700 | 618.830 | 10 | cleared | 0 | 0.000 | False | False | 0.724 |  | unresolvable |
| s20_off | 96 | item_7 | False | 1844 | 1844.100 | 509.700 | 618.830 | 25 | cleared | 0 | 0.000 | False | False | 0.724 |  | unresolvable |
| s20_off | 96 | item_7 | False | 1844 | 1844.100 | 509.700 | 618.830 | 50 | cleared | 0 | 0.000 | False | False | 0.724 |  | unresolvable |
| s20_off | 96 | item_7 | False | 1844 | 1844.100 | 509.700 | 618.830 | 100 | cleared | 0 | 0.000 | False | False | 0.724 |  | unresolvable |
| s20_on | 11 | item_4 | True | 812 | 812.300 | 828.300 | 15.290 | 10 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s20_on | 11 | item_4 | True | 812 | 812.300 | 828.300 | 15.290 | 25 | cleared | 42 | 0.052 | True | True | 0.032 |  | unresolvable |
| s20_on | 11 | item_4 | True | 812 | 812.300 | 828.300 | 15.290 | 50 | cleared | 67 | 0.083 | True | True | 0.063 |  | unresolvable |
| s20_on | 11 | item_4 | True | 812 | 812.300 | 828.300 | 15.290 | 100 | cleared | 117 | 0.144 | True | True | 0.124 |  | unresolvable |
| s20_on | 11 | item_6 | False | 1189 | 1188.700 | 828.300 | 292.300 | 10 | cleared | 0 | 0.000 | False | False | 0.303 |  | unresolvable |
| s20_on | 11 | item_6 | False | 1189 | 1188.700 | 828.300 | 292.300 | 25 | cleared | 0 | 0.000 | False | False | 0.303 |  | unresolvable |
| s20_on | 11 | item_6 | False | 1189 | 1188.700 | 828.300 | 292.300 | 50 | cleared | 0 | 0.000 | False | False | 0.303 |  | unresolvable |
| s20_on | 11 | item_6 | False | 1189 | 1188.700 | 828.300 | 292.300 | 100 | cleared | 0 | 0.000 | False | False | 0.303 |  | unresolvable |
| s20_on | 11 | item_7 | False | 1841 | 1841.300 | 828.300 | 41.290 | 10 | cleared | 0 | 0.000 | False | False | 0.550 |  | unresolvable |
| s20_on | 11 | item_7 | False | 1841 | 1841.300 | 828.300 | 41.290 | 25 | cleared | 0 | 0.000 | False | False | 0.550 |  | unresolvable |
| s20_on | 11 | item_7 | False | 1841 | 1841.300 | 828.300 | 41.290 | 50 | cleared | 144 | 0.078 | False | False | 0.628 |  | unresolvable |
| s20_on | 11 | item_7 | False | 1841 | 1841.300 | 828.300 | 41.290 | 100 | cleared | 223 | 0.121 | False | False | 0.671 |  | unresolvable |
| s20_on | 23 | item_4 | True | 570 | 569.900 | 595.900 | 25.850 | 10 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s20_on | 23 | item_4 | True | 570 | 569.900 | 595.900 | 25.850 | 25 | cleared | 0 | 0.000 | False | False | 0.000 |  | 0 |
| s20_on | 23 | item_4 | True | 570 | 569.900 | 595.900 | 25.850 | 50 | cleared | 77 | 0.135 | True | True | 0.090 |  | unresolvable |
| s20_on | 23 | item_4 | True | 570 | 569.900 | 595.900 | 25.850 | 100 | cleared | 127 | 0.223 | True | True | 0.177 |  | unresolvable |
| s20_on | 23 | item_6 | False | 1100 | 1100.300 | 595.900 | 159.360 | 10 | cleared | 0 | 0.000 | False | False | 0.458 |  | unresolvable |
| s20_on | 23 | item_6 | False | 1100 | 1100.300 | 595.900 | 159.360 | 25 | cleared | 0 | 0.000 | False | False | 0.458 |  | unresolvable |
| s20_on | 23 | item_6 | False | 1100 | 1100.300 | 595.900 | 159.360 | 50 | cleared | 0 | 0.000 | False | False | 0.458 |  | unresolvable |
| s20_on | 23 | item_6 | False | 1100 | 1100.300 | 595.900 | 159.360 | 100 | cleared | 0 | 0.000 | False | False | 0.458 |  | unresolvable |
| s20_on | 23 | item_7 | False | 1695 | 1695.400 | 595.900 | 111.900 | 10 | cleared | 0 | 0.000 | False | False | 0.649 |  | unresolvable |
| s20_on | 23 | item_7 | False | 1695 | 1695.400 | 595.900 | 111.900 | 25 | cleared | 0 | 0.000 | False | False | 0.649 |  | unresolvable |
| s20_on | 23 | item_7 | False | 1695 | 1695.400 | 595.900 | 111.900 | 50 | cleared | 0 | 0.000 | False | False | 0.649 |  | unresolvable |
| s20_on | 23 | item_7 | False | 1695 | 1695.400 | 595.900 | 111.900 | 100 | cleared | 0 | 0.000 | False | False | 0.649 |  | unresolvable |
| s20_on | 82 | item_6 | True | 1053 | 1053.300 | 754.000 | 299.260 | 10 | cleared | 0 | 0.000 | False | False | 0.284 |  | unresolvable |
| s20_on | 82 | item_6 | True | 1053 | 1053.300 | 754.000 | 299.260 | 25 | cleared | 0 | 0.000 | False | False | 0.284 |  | unresolvable |
| s20_on | 82 | item_6 | True | 1053 | 1053.300 | 754.000 | 299.260 | 50 | cleared | 0 | 0.000 | False | False | 0.284 |  | unresolvable |
| s20_on | 82 | item_6 | True | 1053 | 1053.300 | 754.000 | 299.260 | 100 | cleared | 0 | 0.000 | False | False | 0.284 |  | unresolvable |
| s20_on | 82 | item_7 | False | 1733 | 1733.200 | 754.000 | 380.520 | 10 | cleared | 0 | 0.000 | False | False | 0.565 |  | unresolvable |
| s20_on | 82 | item_7 | False | 1733 | 1733.200 | 754.000 | 380.520 | 25 | cleared | 0 | 0.000 | False | False | 0.565 |  | unresolvable |
| s20_on | 82 | item_7 | False | 1733 | 1733.200 | 754.000 | 380.520 | 50 | cleared | 0 | 0.000 | False | False | 0.565 |  | unresolvable |
| s20_on | 82 | item_7 | False | 1733 | 1733.200 | 754.000 | 380.520 | 100 | cleared | 0 | 0.000 | False | False | 0.565 |  | unresolvable |
| s20_on | 95 | item_6 | True | 810 | 809.900 | 529.700 | 279.860 | 10 | cleared | 0 | 0.000 | False | False | 0.346 |  | unresolvable |
| s20_on | 95 | item_6 | True | 810 | 809.900 | 529.700 | 279.860 | 25 | cleared | 0 | 0.000 | False | False | 0.346 |  | unresolvable |
| s20_on | 95 | item_6 | True | 810 | 809.900 | 529.700 | 279.860 | 50 | cleared | 0 | 0.000 | False | False | 0.346 |  | unresolvable |
| s20_on | 95 | item_6 | True | 810 | 809.900 | 529.700 | 279.860 | 100 | cleared | 0 | 0.000 | False | False | 0.346 |  | unresolvable |
| s20_on | 95 | item_7 | False | 1844 | 1844.100 | 529.700 | 611.120 | 10 | cleared | 0 | 0.000 | False | False | 0.713 |  | unresolvable |
| s20_on | 95 | item_7 | False | 1844 | 1844.100 | 529.700 | 611.120 | 25 | cleared | 0 | 0.000 | False | False | 0.713 |  | unresolvable |
| s20_on | 95 | item_7 | False | 1844 | 1844.100 | 529.700 | 611.120 | 50 | cleared | 0 | 0.000 | False | False | 0.713 |  | unresolvable |
| s20_on | 95 | item_7 | False | 1844 | 1844.100 | 529.700 | 611.120 | 100 | cleared | 0 | 0.000 | False | False | 0.713 |  | unresolvable |


## (d) min d sorted, primary rows

| condition | step | trigger | candidate | is_winner | is_current_task | hypothesis_matches_actual | cost | min_d | argmin_t | min_at_window_end |
|---|---|---|---|---|---|---|---|---|---|---|
| s10_on | 142 | task_committed | item_5 | False | False | False | 3198 | 4.01 | 317 | False |
| s20_off | 24 | task_committed | item_4 | True | True | True | 570 | 5.85 | 569 | True |
| s10_on | 142 | task_committed | item_1 | True | True | False | 1110 | 6.96 | 146 | False |
| s20_on | 11 | theta_crossed | item_4 | True | True | True | 812 | 15.29 | 812 | True |
| s20_off | 22 | theta_crossed | item_4 | True | True | True | 612 | 16.31 | 595 | True |
| s10_off | 257 | theta_crossed | item_5 | True | True | True | 1308 | 24.49 | 1308 | True |
| s10_on | 257 | theta_crossed | item_5 | True | True | True | 1308 | 24.49 | 1308 | True |
| s20_on | 23 | task_committed | item_4 | True | True | True | 570 | 25.85 | 569 | True |
| s20_on | 11 | theta_crossed | item_7 | False | False | True | 1841 | 41.29 | 336 | False |
| s10_off | 262 | task_committed | item_5 | True | True | True | 1190 | 63.49 | 1189 | True |
| s10_on | 262 | task_committed | item_5 | True | True | True | 1190 | 63.49 | 1189 | True |
| s10_on | 107 | theta_crossed | item_1 | True | True | False | 1820 | 89.56 | 159 | False |
| s20_off | 22 | theta_crossed | item_7 | False | False | True | 1687 | 93.66 | 109 | False |
| s20_on | 23 | task_committed | item_7 | False | False | True | 1695 | 111.90 | 106 | False |
| s20_off | 24 | task_committed | item_7 | False | False | True | 1695 | 125.63 | 96 | False |
| s00_off | 41 | theta_crossed | item_6 | True | True | True | 1025 | 136.39 | 259 | False |
| s00_on | 41 | theta_crossed | item_6 | True | True | True | 1025 | 136.39 | 259 | False |
| s00_on | 95 | no_current_task | item_4 | True | False | True | 1426 | 139.75 | 446 | False |
| s00_off | 111 | theta_crossed | item_4 | True | True | True | 1106 | 140.68 | 131 | False |
| s00_on | 81 | theta_crossed | item_6 | True | True | True | 222 | 154.79 | 89 | False |
| s20_on | 23 | task_committed | item_6 | False | False | True | 1100 | 159.36 | 28 | False |
| s20_off | 24 | task_committed | item_6 | False | False | True | 1100 | 159.87 | 28 | False |
| s20_off | 22 | theta_crossed | item_6 | False | False | True | 1078 | 185.43 | 2 | False |
| s10_on | 107 | theta_crossed | item_5 | False | False | False | 2655 | 189.08 | 0 | False |
| s00_on | 81 | theta_crossed | item_4 | False | False | True | 1828 | 203.16 | 0 | False |
| s00_off | 41 | theta_crossed | item_4 | False | False | True | 1387 | 226.31 | 282 | False |
| s00_on | 41 | theta_crossed | item_4 | False | False | True | 1387 | 226.31 | 282 | False |
| s20_on | 95 | task_committed | item_6 | True | True | True | 810 | 279.86 | 529 | True |
| s20_on | 11 | theta_crossed | item_6 | False | False | True | 1189 | 292.30 | 215 | False |
| s20_on | 82 | theta_crossed | item_6 | True | True | True | 1053 | 299.26 | 753 | True |
| s20_off | 96 | task_committed | item_6 | True | True | True | 810 | 299.86 | 509 | True |
| s00_off | 63 | task_committed | item_6 | True | True | True | 582 | 301.67 | 279 | True |
| s00_on | 63 | task_committed | item_6 | True | True | True | 582 | 301.67 | 279 | True |
| s20_off | 89 | theta_crossed | item_6 | True | True | True | 933 | 303.26 | 629 | True |
| s00_off | 63 | task_committed | item_4 | False | False | True | 1468 | 326.65 | 0 | False |
| s00_on | 63 | task_committed | item_4 | False | False | True | 1468 | 326.65 | 0 | False |
| s20_on | 82 | theta_crossed | item_7 | False | False | True | 1733 | 380.52 | 388 | False |
| s00_off | 131 | task_committed | item_4 | True | True | True | 689 | 480.02 | 208 | True |
| s00_on | 131 | task_committed | item_4 | True | True | True | 689 | 480.02 | 208 | True |
| s20_off | 89 | theta_crossed | item_7 | False | False | True | 1778 | 493.61 | 353 | False |
| s20_on | 95 | task_committed | item_7 | False | False | True | 1844 | 611.12 | 339 | False |
| s20_off | 96 | task_committed | item_7 | False | False | True | 1844 | 618.83 | 329 | False |
| s10_on | 200 | no_current_task | item_5 | True | False | False | 2448 | 661.30 | 1 | False |


## (d) scale context

| field | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| condition | s00_off | s00_on | s10_off | s10_on | s20_off | s20_on |
| layout | env_layout0 | env_layout0 | env_layout1 | env_layout1 | env_layout2 | env_layout2 |
| space_w_x_h | 1000x800 | 1000x800 | 2000x1000 | 2000x1000 | 1200x900 | 1200x900 |
| space_diagonal | 1280.6 | 1280.6 | 2236.1 | 2236.1 | 1500.0 | 1500.0 |
| task_object_bbox | x[-400,400] y[-300,350] | x[-400,400] y[-300,350] | x[-975,950] y[-450,400] | x[-975,950] y[-450,400] | x[-500,450] y[-350,400] | x[-500,450] y[-350,400] |
| assumed_speed | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| default_action_cost | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| mesa_step_size | 20 | 20 | 20 | 20 | 20 | 20 |
| min_safe_distance | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| theta | 0.75 | 0.75 | 0.75 | 0.75 | 0.75 | 0.75 |
| full_task_costs_at_t0 | {'item_4': 1538, 'item_6': 908, 'item_7': 586} | {'item_4': 1538, 'item_6': 908, 'item_7': 586} | {'item_5': 1996, 'item_1': 2457, 'item_7': 1646} | {'item_5': 1996, 'item_1': 2457, 'item_7': 1646} | {'item_4': 1032, 'item_6': 1372, 'item_7': 2028} | {'item_4': 1032, 'item_6': 1372, 'item_7': 2028} |
| candidate_cost_min_med_max | 463/1106/1538 | 222/1105/1828 | 971/2029/3198 | 971/2029/3198 | 570/1372/2028 | 570/1372/2028 |
| n_projected_legs | 44 | 45 | 37 | 43 | 46 | 46 |
| leg_len_min_med_max | 0/602/820 | 0/602/820 | 18/1125/1953 | 18/1109/1953 | 0/612/1151 | 0/629/1151 |
| approach_leg_med | 581.0 | 581.0 | 783.0 | 776.0 | 526.0 | 447.0 |
| carry_leg_med | 645.0 | 602.0 | 1134.0 | 1134.0 | 820.0 | 820.0 |


## (e) pairs, primary triggers

| condition | step | A_cheaper | B | A_is_winner | d_cost | min_d_A | min_d_B | d_min_d | disagree_min_d | d_below10 | disagree_below10 | d_below25 | disagree_below25 | d_below50 | disagree_below50 | d_below100 | disagree_below100 | delta10_A | delta10_B | d_delta10 | disagree_delta10 | delta25_A | delta25_B | d_delta25 | disagree_delta25 | delta50_A | delta50_B | d_delta50 | disagree_delta50 | delta100_A | delta100_B | d_delta100 | disagree_delta100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 41 | item_6 | item_4 | True | 362 | 136.40 | 226.30 | 89.90 | True | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |
| s00_off | 63 | item_6 | item_4 | True | 886 | 301.70 | 326.70 | 25.00 | True | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |
| s00_on | 41 | item_6 | item_4 | True | 362 | 136.40 | 226.30 | 89.90 | True | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |
| s00_on | 63 | item_6 | item_4 | True | 886 | 301.70 | 326.70 | 25.00 | True | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |
| s00_on | 81 | item_6 | item_4 | True | 1606 | 154.80 | 203.20 | 48.40 | True | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |
| s10_on | 107 | item_1 | item_5 | True | 835 | 89.60 | 189.10 | 99.50 | True | 0 | False | 0 | False | 0 | False | -85 | True | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 13.00 | 0.00 | -13.00 | True |
| s10_on | 142 | item_1 | item_5 | True | 2088 | 7.00 | 4.00 | -2.90 | False | 18 | False | 40 | False | 80 | False | 277 | False | 4.00 | 15.00 | 11.00 | False | 23.00 | 31.00 | 8.00 | False | 53.00 | 152.00 | 99.00 | False | 114.00 | 209.00 | 95.00 | False |
| s20_off | 22 | item_4 | item_6 | True | 466 | 16.30 | 185.40 | 169.10 | True | 0 | False | -61 | True | -164 | True | -350 | True | 0.00 | 0.00 | 0.00 | False | 9.00 | 0.00 | -9.00 | True | 34.00 | 0.00 | -34.00 | True | 84.00 | 0.00 | -84.00 | True |
| s20_off | 22 | item_4 | item_7 | True | 1075 | 16.30 | 93.70 | 77.30 | True | 0 | False | -61 | True | -164 | True | -303 | True | 0.00 | 0.00 | 0.00 | False | 9.00 | 0.00 | -9.00 | True | 34.00 | 0.00 | -34.00 | True | 84.00 | 10.00 | -74.00 | True |
| s20_off | 22 | item_6 | item_7 | False | 609 | 185.40 | 93.70 | -91.80 | False | 0 | False | 0 | False | 0 | False | 47 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 10.00 | 10.00 | False |
| s20_off | 24 | item_4 | item_6 | True | 530 | 5.90 | 159.90 | 154.00 | True | -23 | True | -75 | True | -155 | True | -314 | True | 17.00 | 0.00 | -17.00 | True | 32.00 | 0.00 | -32.00 | True | 57.00 | 0.00 | -57.00 | True | 107.00 | 0.00 | -107.00 | True |
| s20_off | 24 | item_4 | item_7 | True | 1125 | 5.90 | 125.60 | 119.80 | True | -23 | True | -75 | True | -155 | True | -314 | True | 17.00 | 0.00 | -17.00 | True | 32.00 | 0.00 | -32.00 | True | 57.00 | 0.00 | -57.00 | True | 107.00 | 0.00 | -107.00 | True |
| s20_off | 24 | item_6 | item_7 | False | 595 | 159.90 | 125.60 | -34.20 | False | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |
| s20_off | 89 | item_6 | item_7 | True | 845 | 303.30 | 493.60 | 190.40 | True | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |
| s20_off | 96 | item_6 | item_7 | True | 1034 | 299.90 | 618.80 | 319.00 | True | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |
| s20_on | 11 | item_4 | item_6 | True | 377 | 15.30 | 292.30 | 277.00 | True | 0 | False | -72 | True | -188 | True | -398 | True | 0.00 | 0.00 | 0.00 | False | 42.00 | 0.00 | -42.00 | True | 67.00 | 0.00 | -67.00 | True | 117.00 | 0.00 | -117.00 | True |
| s20_on | 11 | item_4 | item_7 | True | 1029 | 15.30 | 41.30 | 26.00 | True | 0 | False | -72 | True | -152 | True | -280 | True | 0.00 | 0.00 | 0.00 | False | 42.00 | 0.00 | -42.00 | True | 67.00 | 144.00 | 77.00 | False | 117.00 | 223.00 | 106.00 | False |
| s20_on | 11 | item_6 | item_7 | False | 652 | 292.30 | 41.30 | -251.00 | False | 0 | False | 0 | False | 36 | False | 118 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 144.00 | 144.00 | False | 0.00 | 223.00 | 223.00 | False |
| s20_on | 23 | item_4 | item_6 | True | 530 | 25.90 | 159.40 | 133.50 | True | 0 | False | 0 | False | -124 | True | -294 | True | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 77.00 | 0.00 | -77.00 | True | 127.00 | 0.00 | -127.00 | True |
| s20_on | 23 | item_4 | item_7 | True | 1125 | 25.90 | 111.90 | 86.00 | True | 0 | False | 0 | False | -124 | True | -294 | True | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 77.00 | 0.00 | -77.00 | True | 127.00 | 0.00 | -127.00 | True |
| s20_on | 23 | item_6 | item_7 | False | 595 | 159.40 | 111.90 | -47.50 | False | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |
| s20_on | 82 | item_6 | item_7 | True | 680 | 299.30 | 380.50 | 81.30 | True | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |
| s20_on | 95 | item_6 | item_7 | True | 1034 | 279.90 | 611.10 | 331.30 | True | 0 | False | 0 | False | 0 | False | 0 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False | 0.00 | 0.00 | 0.00 | False |


## (e) pairs, counterfactual triggers

| condition | step | A_cheaper | B | A_is_winner | d_cost | min_d_A | min_d_B | d_min_d | disagree_min_d | d_below10 | disagree_below10 | d_below25 | disagree_below25 | d_below50 | disagree_below50 | d_below100 | disagree_below100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 0 | item_7 | item_6 | True | 322 | 352.20 | 261.10 | -91.10 | False | 0 | False | 0 | False | 0 | False | 0 | False |
| s00_off | 0 | item_7 | item_4 | True | 952 | 352.20 | 12.20 | -340.00 | False | 0 | False | 39 | False | 108 | False | 234 | False |
| s00_off | 0 | item_6 | item_4 | False | 630 | 261.10 | 12.20 | -248.90 | False | 0 | False | 39 | False | 108 | False | 234 | False |
| s00_off | 7 | item_7 | item_6 | True | 354 | 355.80 | 256.50 | -99.30 | False | 0 | False | 0 | False | 0 | False | 0 | False |
| s00_off | 7 | item_7 | item_4 | True | 1074 | 355.80 | 47.20 | -308.70 | False | 0 | False | 0 | False | 19 | False | 105 | False |
| s00_off | 7 | item_6 | item_4 | False | 720 | 256.50 | 47.20 | -209.30 | False | 0 | False | 0 | False | 19 | False | 105 | False |
| s00_off | 33 | item_6 | item_4 | True | 247 | 130.40 | 352.10 | 221.70 | True | 0 | False | 0 | False | 0 | False | 0 | False |
| s00_on | 7 | item_7 | item_6 | True | 354 | 355.80 | 256.50 | -99.30 | False | 0 | False | 0 | False | 0 | False | 0 | False |
| s00_on | 7 | item_7 | item_4 | True | 1074 | 355.80 | 47.20 | -308.70 | False | 0 | False | 0 | False | 19 | False | 105 | False |
| s00_on | 7 | item_6 | item_4 | False | 720 | 256.50 | 47.20 | -209.30 | False | 0 | False | 0 | False | 19 | False | 105 | False |
| s00_on | 33 | item_6 | item_4 | True | 247 | 130.40 | 352.10 | 221.70 | True | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_off | 0 | item_7 | item_5 | True | 350 | 45.40 | 303.80 | 258.40 | True | 0 | False | 0 | False | -7 | True | -57 | True |
| s10_off | 0 | item_7 | item_1 | True | 811 | 45.40 | 126.80 | 81.40 | True | 0 | False | 0 | False | -7 | True | -57 | True |
| s10_off | 0 | item_5 | item_1 | False | 461 | 303.80 | 126.80 | -177.00 | False | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_off | 34 | item_7 | item_5 | True | 1058 | 173.80 | 1209.70 | 1036.00 | True | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_off | 34 | item_7 | item_1 | True | 1433 | 173.80 | 751.10 | 577.30 | True | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_off | 34 | item_5 | item_1 | False | 375 | 1209.70 | 751.10 | -458.70 | False | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_off | 85 | item_1 | item_5 | True | 154 | 169.30 | 173.10 | 3.80 | True | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_off | 142 | item_1 | item_5 | True | 2088 | 168.10 | 168.10 | 0.00 | False | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_on | 0 | item_7 | item_5 | True | 350 | 561.80 | 788.60 | 226.80 | True | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_on | 0 | item_7 | item_1 | True | 811 | 561.80 | 55.30 | -506.50 | False | 0 | False | 0 | False | 0 | False | 89 | False |
| s10_on | 0 | item_5 | item_1 | False | 461 | 788.60 | 55.30 | -733.30 | False | 0 | False | 0 | False | 0 | False | 89 | False |
| s10_on | 34 | item_7 | item_5 | True | 1058 | 173.80 | 1209.70 | 1036.00 | True | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_on | 34 | item_7 | item_1 | True | 1433 | 173.80 | 751.10 | 577.30 | True | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_on | 34 | item_5 | item_1 | False | 375 | 1209.70 | 751.10 | -458.70 | False | 0 | False | 0 | False | 0 | False | 0 | False |
| s10_on | 85 | item_1 | item_5 | True | 154 | 147.10 | 173.10 | 26.00 | True | 0 | False | 0 | False | 0 | False | 0 | False |
| s20_off | 0 | item_4 | item_6 | True | 340 | 20.00 | 225.00 | 205.00 | True | 0 | False | -16 | True | -50 | True | -618 | True |
| s20_off | 0 | item_4 | item_7 | True | 996 | 20.00 | 148.80 | 128.80 | True | 0 | False | -16 | True | -50 | True | -618 | True |
| s20_off | 0 | item_6 | item_7 | False | 656 | 225.00 | 148.80 | -76.20 | False | 0 | False | 0 | False | 0 | False | 0 | False |


## (5.6) most_likely changes with both confidences ≥ θ

(none)


## (5.6) all most_likely changes

| condition | step | old | new | conf_prev | conf_now | both_above_theta | robot_task_at_tick | robot_holding_at_tick | trigger_this_tick | next_fired_trigger_step | human_actual_task |
|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 16 | item_3 | item_4 | 0.214 | 0.269 | False | item_7 | item_7 | none | 33 | item_3 |
| s00_off | 22 | item_4 | item_3 | 0.270 | 0.303 | False | item_7 | item_7 | none | 33 | item_3 |
| s00_off | 78 | item_3 | item_7 | 0.797 | 0.351 | False | item_6 | item_6 | none | 95 | item_3 |
| s00_off | 81 | item_7 | item_2 | 0.351 | 0.291 | False | item_6 | item_6 | none | 95 | item_2 |
| s00_off | 142 | item_2 | item_4 | 0.970 | 0.366 | False | item_4 | item_4 | none | 168 | item_2 |
| s00_on | 1 | unknown | item_3 | 0.332 | 0.507 | False | item_7 |  | none | 7 | item_3 |
| s00_on | 16 | item_3 | item_2 | 0.507 | 0.532 | False | item_7 | item_7 | none | 33 | item_3 |
| s00_on | 22 | item_2 | item_3 | 0.532 | 0.672 | False | item_7 | item_7 | none | 33 | item_3 |
| s00_on | 78 | item_3 | item_2 | 0.797 | 0.510 | False | item_6 | item_6 | none | 81 | item_3 |
| s10_off | 1 | item_1 | item_2 | 0.154 | 0.300 | False | item_7 |  | none | 34 | item_2 |
| s10_off | 75 | item_2 | item_0 | 0.662 | 0.460 | False | item_7 | item_7 | none | 85 | item_2 |
| s10_off | 161 | item_0 | item_6 | 0.393 | 0.478 | False | item_1 | item_1 | none | 200 | item_4 |
| s10_off | 209 | item_6 | item_0 | 0.485 | 0.327 | False | item_5 |  | none | 257 | item_4 |
| s10_off | 257 | item_0 | item_4 | 0.327 | 0.769 | False | item_5 |  | theta_crossed | 257 | item_4 |
| s10_on | 1 | item_6 | item_2 | 0.249 | 0.521 | False | item_7 |  | none | 34 | item_2 |
| s10_on | 78 | item_2 | item_6 | 0.399 | 0.730 | False | item_7 | item_7 | none | 85 | coffee_break |
| s10_on | 257 | item_6 | item_4 | 0.738 | 0.769 | False | item_5 |  | theta_crossed | 257 | item_4 |
| s20_off | 1 | item_4 | item_3 | 0.167 | 0.248 | False | item_4 |  | none | 22 | item_3 |
| s20_off | 54 | item_3 | item_4 | 0.797 | 0.599 | False | item_4 |  | none | 55 | item_3 |
| s20_off | 57 | item_4 | item_7 | 0.599 | 0.264 | False | item_6 |  | none | 89 | item_2 |
| s20_off | 89 | item_7 | item_2 | 0.353 | 0.928 | False | item_6 |  | theta_crossed | 89 | item_2 |
| s20_off | 122 | item_2 | item_4 | 0.928 | 0.432 | False | item_6 | item_6 | none | 139 | item_2 |
| s20_on | 1 | unknown | item_3 | 0.332 | 0.641 | False | item_4 |  | none | 11 | item_3 |
| s20_on | 57 | item_3 | item_2 | 0.641 | 0.743 | False | item_6 |  | none | 82 | item_2 |
| s20_on | 122 | item_2 | item_3 | 0.928 | 0.500 | False | item_6 | item_6 | none | 138 | item_2 |


## (5.7) tail beyond the human projection, primary rows

| condition | step | trigger | candidate | is_winner | cost | T_r | T_h | T_r_minus_T_h | unchecked_steps | share_of_cost | robot_phases_in_tail | min_at_window_end |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s00_off | 41 | theta_crossed | item_6 | True | 1025 | 1025.500 | 699.200 | 326.300 | 326.300 | 0.318 | carry_to_table|placement | False |
| s00_off | 41 | theta_crossed | item_4 | False | 1387 | 1387.000 | 699.200 | 687.800 | 687.800 | 0.496 | carry_to_table|placement | False |
| s00_off | 63 | task_committed | item_6 | True | 582 | 581.700 | 279.200 | 302.500 | 302.500 | 0.520 | carry_to_table|placement | True |
| s00_off | 63 | task_committed | item_4 | False | 1468 | 1468.300 | 279.200 | 1189.100 | 1189.100 | 0.810 | approach_shelf|pick_up|carry_to_table|placement | False |
| s00_off | 111 | theta_crossed | item_4 | True | 1106 | 1105.800 | 588.300 | 517.500 | 517.500 | 0.468 | carry_to_table|placement | False |
| s00_off | 131 | task_committed | item_4 | True | 689 | 689.000 | 208.300 | 480.700 | 480.700 | 0.698 | carry_to_table|placement | True |
| s00_on | 41 | theta_crossed | item_6 | True | 1025 | 1025.500 | 699.200 | 326.300 | 326.300 | 0.318 | carry_to_table|placement | False |
| s00_on | 41 | theta_crossed | item_4 | False | 1387 | 1387.000 | 699.200 | 687.800 | 687.800 | 0.496 | carry_to_table|placement | False |
| s00_on | 63 | task_committed | item_6 | True | 582 | 581.700 | 279.200 | 302.500 | 302.500 | 0.520 | carry_to_table|placement | True |
| s00_on | 63 | task_committed | item_4 | False | 1468 | 1468.300 | 279.200 | 1189.100 | 1189.100 | 0.810 | approach_shelf|pick_up|carry_to_table|placement | False |
| s00_on | 81 | theta_crossed | item_6 | True | 222 | 221.700 | 1178.900 | -957.200 | 0.000 | 0.000 |  | False |
| s00_on | 81 | theta_crossed | item_4 | False | 1828 | 1828.300 | 1178.900 | 649.400 | 649.400 | 0.355 | carry_to_table|placement | False |
| s00_on | 95 | no_current_task | item_4 | True | 1426 | 1425.800 | 898.900 | 526.900 | 526.900 | 0.370 | carry_to_table|placement | False |
| s00_on | 131 | task_committed | item_4 | True | 689 | 689.000 | 208.300 | 480.700 | 480.700 | 0.698 | carry_to_table|placement | True |
| s10_off | 257 | theta_crossed | item_5 | True | 1308 | 1308.300 | 1333.500 | -25.200 | 0.000 | 0.000 |  | True |
| s10_off | 262 | task_committed | item_5 | True | 1190 | 1189.900 | 1253.500 | -63.600 | 0.000 | 0.000 |  | True |
| s10_on | 107 | theta_crossed | item_1 | True | 1820 | 1820.400 | 1379.600 | 440.800 | 440.800 | 0.242 | carry_to_table|placement | False |
| s10_on | 107 | theta_crossed | item_5 | False | 2655 | 2654.600 | 1379.600 | 1275.000 | 1275.000 | 0.480 | approach_shelf|pick_up|carry_to_table|placement | False |
| s10_on | 142 | task_committed | item_1 | True | 1110 | 1109.700 | 1403.800 | -294.100 | 0.000 | 0.000 |  | False |
| s10_on | 142 | task_committed | item_5 | False | 3198 | 3198.000 | 1403.800 | 1794.200 | 1794.200 | 0.561 | approach_shelf|pick_up|carry_to_table|placement | False |
| s10_on | 200 | no_current_task | item_5 | True | 2448 | 2448.300 | 1278.000 | 1170.300 | 1170.300 | 0.478 | carry_to_table|placement | False |
| s10_on | 257 | theta_crossed | item_5 | True | 1308 | 1308.300 | 1333.500 | -25.200 | 0.000 | 0.000 |  | True |
| s10_on | 262 | task_committed | item_5 | True | 1190 | 1189.900 | 1253.500 | -63.600 | 0.000 | 0.000 |  | True |
| s20_off | 22 | theta_crossed | item_4 | True | 612 | 612.300 | 595.900 | 16.500 | 16.500 | 0.027 | carry_to_table|placement | True |
| s20_off | 22 | theta_crossed | item_6 | False | 1078 | 1078.300 | 595.900 | 482.500 | 482.500 | 0.447 | carry_to_table|placement | False |
| s20_off | 22 | theta_crossed | item_7 | False | 1687 | 1686.700 | 595.900 | 1090.800 | 1090.800 | 0.647 | approach_shelf|pick_up|carry_to_table|placement | False |
| s20_off | 24 | task_committed | item_4 | True | 570 | 569.900 | 575.900 | -5.900 | 0.000 | 0.000 |  | True |
| s20_off | 24 | task_committed | item_6 | False | 1100 | 1100.300 | 575.900 | 524.400 | 524.400 | 0.477 | carry_to_table|placement | False |
| s20_off | 24 | task_committed | item_7 | False | 1695 | 1695.400 | 575.900 | 1119.600 | 1119.600 | 0.660 | approach_shelf|pick_up|carry_to_table|placement | False |
| s20_off | 89 | theta_crossed | item_6 | True | 933 | 933.300 | 629.700 | 303.600 | 303.600 | 0.325 | carry_to_table|placement | True |
| s20_off | 89 | theta_crossed | item_7 | False | 1778 | 1778.400 | 629.700 | 1148.700 | 1148.700 | 0.646 | approach_shelf|pick_up|carry_to_table|placement | False |
| s20_off | 96 | task_committed | item_6 | True | 810 | 809.900 | 509.700 | 300.200 | 300.200 | 0.371 | carry_to_table|placement | True |
| s20_off | 96 | task_committed | item_7 | False | 1844 | 1844.100 | 509.700 | 1334.400 | 1334.400 | 0.724 | approach_shelf|pick_up|carry_to_table|placement | False |
| s20_on | 11 | theta_crossed | item_4 | True | 812 | 812.300 | 828.300 | -16.000 | 0.000 | 0.000 |  | True |
| s20_on | 11 | theta_crossed | item_6 | False | 1189 | 1188.700 | 828.300 | 360.400 | 360.400 | 0.303 | carry_to_table|placement | False |
| s20_on | 11 | theta_crossed | item_7 | False | 1841 | 1841.300 | 828.300 | 1013.100 | 1013.100 | 0.550 | approach_shelf|pick_up|carry_to_table|placement | False |
| s20_on | 23 | task_committed | item_4 | True | 570 | 569.900 | 595.900 | -25.900 | 0.000 | 0.000 |  | True |
| s20_on | 23 | task_committed | item_6 | False | 1100 | 1100.300 | 595.900 | 504.400 | 504.400 | 0.458 | carry_to_table|placement | False |
| s20_on | 23 | task_committed | item_7 | False | 1695 | 1695.400 | 595.900 | 1099.600 | 1099.600 | 0.649 | approach_shelf|pick_up|carry_to_table|placement | False |
| s20_on | 82 | theta_crossed | item_6 | True | 1053 | 1053.300 | 754.000 | 299.300 | 299.300 | 0.284 | carry_to_table|placement | True |
| s20_on | 82 | theta_crossed | item_7 | False | 1733 | 1733.200 | 754.000 | 979.300 | 979.300 | 0.565 | approach_shelf|pick_up|carry_to_table|placement | False |
| s20_on | 95 | task_committed | item_6 | True | 810 | 809.900 | 529.700 | 280.200 | 280.200 | 0.346 | carry_to_table|placement | True |
| s20_on | 95 | task_committed | item_7 | False | 1844 | 1844.100 | 529.700 | 1314.400 | 1314.400 | 0.713 | approach_shelf|pick_up|carry_to_table|placement | False |
