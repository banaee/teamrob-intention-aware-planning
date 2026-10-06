# Task tree

6 October 2026, commit be3c200

? = the records disagree (docs/task_tree_elaborative.md)

```text
T-A   records .......................................... done
T-B   B3.B (full_reorder) .............................. done
T-C   human action script .............................. closed
T-H   human behaviour model ............................ closed
T-L   layouts, setups, scenarios ....................... done
T-D   robustness in kitting ............................ closed except tail
├─ tracks 1, L, P, 2.5, G, X, 3 ........................ done
├─ track 3b   activation under conflict ................ open
├─ track 4    boundary and departure ................... moved to T-G
└─ 4D detour strategy .................................. FW

T-G   second domain, dock_loading ...................... paused
├─ stage 1    basic domain ............................. closed
├─ stage 2    full domain .............................. open ◀ next
├─ track 4    human outside monitored areas ............ ruled
└─ stage 3    check-in and check-out ................... ruled in outline

T-K   context knowledge ................................ ruled
├─ part 1     crisp context knowledge .................. ongoing
│  ├─ step 1   A/C switch layouts ...................... done
│  ├─ step 2   plan of the build ....................... done
│  ├─ step 3   the build ............................... done
│  ├─ step 4   kitting, idle robot ..................... done
│  ├─ step 5   kitting, planning cases ................. done
│  ├─ step 5b  existing kitting sets ................... done
│  ├─ step 5c  the gate after step 5b .................. done
│  ├─ step 5d  measurements after the gate ............. done
│  ├─ step 5e  kitting rooms 02 to 07, 19, 20 .......... done
│  ├─ step 6   dock_loading stage 1 measured ........... done ?
│  └─ step 7   close of part 1 ......................... on hold ?
├─ part 2     degrees of context facts ................. not started
└─ later directions .................................... FW

T-F   evaluation ....................................... open
├─ part 1     human-/intention-unaware ................. closed
└─ part 2 .............................................. parked

T-viz web-ui (T-V) ..................................... asked for
├─ stage 0    foundation ............................... done
│  ├─ 0.1      recording ............................... done
│  ├─ 0.2      code structure .......................... done
│  ├─ 0.3      style trial ............................. built
│  └─ 0.4      messages ................................ built
├─ stage 1    first web-ui (T-V track 1) ............... open
│  ├─ 1a       sim-run in the browser .................. asked for ? ◀ now
│  ├─ 1b       robot's mind ............................ open
│  └─ 1c       plots over ticks ........................ open
├─ stage 2    editing and comparison ................... FW
│  ├─ 2.1      editing layouts ......................... FW
│  ├─ 2.2      editing setups .......................... FW
│  ├─ 2.3      editing scenarios ....................... FW
│  └─ 2.4      sim-runs side by side ................... FW
├─ stage 3    changes during a sim-run (T-V track 2) ... FW
│  └─ 3.1      events in the human's script ............ FW
└─ items with no stage ................................. open

T-S   ROS/PRIEST ....................................... FW
D3    task_committed not a trigger ..................... done
T-E   demonstration .................................... superseded
other two-table re-examination ......................... not scheduled
other oracle-IR evaluation ............................. open
other Alternative 1 .................................... not scheduled
other belief-aware planning ............................ not scheduled
```
