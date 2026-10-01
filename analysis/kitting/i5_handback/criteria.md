# I5 — results carried forward, asserted at HEAD (from metrics.csv, variant `base`)

| result | holds | measured |
|---|---|---|
| next-task reveals prior-on: s00 81, s20 57, s30 77, all pre-grasp | yes | d(item_2):81(pre-grasp,grasp d(item_2):57(pre-grasp,grasp d(item_7):77(pre-grasp,grasp |
| coffee crossing at 135 (prior-on) / 143 (prior-off) | yes | coffee:135(no-grasp,grasp coffee:143(no-grasp,grasp |
| the 63 wrong-task ticks gone: no ac range in s40; only item_6 203–213 (11) prior-on, none prior-off | yes | on: d(item_6):203-213(11); off: - |
| segment 3b retraction visible: item_6 0.790 → 0.083 (prior-on) | yes | 0.790->0.083 |
| s30's first reveal pre-grasp: 28 (off) / 21 (on), grasp 39 | yes | d(item_3):28(pre-grasp,grasp d(item_3):21(pre-grasp,grasp |
| TODO-53 closed: ac_activation most_likely on the 3 post-boundary prior ticks only in 184–271; ac 0.001 at 272 | yes | ac most_likely ticks 3, at 272: unknown 0.520 (item_6 0.474) |
| s20_off's first-task reveal at 20 (pre-grasp, grasp 22) | yes | d(item_3):20(pre-grasp,grasp |
| TODO-60 closed: invariant max |Δ log odds| ≤ 1e-9 in every condition | yes | max 7.1e-15 |
| no wrong crossing prior-on except item_6's aligned walk (203); none prior-off | yes | s00_off:0 s00_on:0 s20_off:0 s20_on:0 s30_off:0 s30_on:0 s40_off:0 s40_on:1 |
| prior-off repeated crossings, recorded not tuned: s00_off 109/113/115, s20_off 20/24/30 and 87/91/95 | yes | s00_off: 39:d(item_3) 109:d(item_2) 113:d(item_2) 115:d(item_2) 166:unknown; s20_off: 20:d(item_3) 24:d(item_3) 30:d(item_3) 87:d(item_2) 91:d(item_2) 95:d(item_2) |

ALL CARRIED FORWARD: yes
