# b2a against none

Separation threshold 50 cm. Decision format step:trigger:winner.

## s00_off

B2 verdicts:

- 7: trigger=task_committed current=item_7 projection=none verdict=continue hold=0
- 39: trigger=theta_crossed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=54.67 remaining=40.41 rho=0.5 bound=20.20 verdict=continue hold=0
- 63: trigger=task_committed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=30.53 remaining=16.41 rho=0.5 bound=8.20 verdict=continue hold=0
- 109: trigger=theta_crossed current=item_4 projection=admitted realizable=True reason=realized delta=0 T_r=58.69 remaining=34.86 rho=0.5 bound=17.43 verdict=continue hold=0
- 113: trigger=theta_crossed current=item_4 projection=admitted realizable=True reason=realized delta=0 T_r=54.69 remaining=30.86 rho=0.5 bound=15.43 verdict=continue hold=0
- 115: trigger=theta_crossed current=item_4 projection=admitted realizable=True reason=realized delta=0 T_r=52.69 remaining=28.86 rho=0.5 bound=14.43 verdict=continue hold=0
- 131: trigger=task_committed current=item_4 projection=admitted realizable=True reason=realized delta=0 T_r=35.90 remaining=12.86 rho=0.5 bound=6.43 verdict=continue hold=0

Decisions none: 0:no_current_task:item_7 7:task_committed:item_7 33:no_current_task:item_6 39:theta_crossed:item_6 63:task_committed:item_6 95:no_current_task:item_4 109:theta_crossed:item_4 113:theta_crossed:item_4 115:theta_crossed:item_4 131:task_committed:item_4 166:done:-  
Decisions b2a: 0:no_current_task:item_7 7:task_committed:item_7 33:no_current_task:item_6 39:theta_crossed:item_6 63:task_committed:item_6 95:no_current_task:item_4 109:theta_crossed:item_4 113:theta_crossed:item_4 115:theta_crossed:item_4 131:task_committed:item_4 166:done:-  
Decision sequence: identical

[sep] < 50: none 161–299 (139 t, min 8.15 @163)  
[sep] < 50: b2a 161–299 (139 t, min 8.15 @163)

Counterfactual B3: continues 7, B3 would switch 0, single-task pool 4; cf log equals the run: yes

## s00_on

B2 verdicts:

- 7: trigger=task_committed current=item_7 projection=none verdict=continue hold=0
- 11: trigger=theta_crossed current=item_7 projection=admitted realizable=True reason=realized delta=0 T_r=20.58 remaining=67.48 rho=0.5 bound=33.74 verdict=continue hold=0
- 63: trigger=task_committed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=30.53 remaining=16.41 rho=0.5 bound=8.20 verdict=continue hold=0
- 81: trigger=theta_crossed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=12.53 remaining=61.35 rho=0.5 bound=30.67 verdict=continue hold=0
- 131: trigger=task_committed current=item_4 projection=admitted realizable=True reason=realized delta=0 T_r=35.90 remaining=12.86 rho=0.5 bound=6.43 verdict=continue hold=0

Decisions none: 0:no_current_task:item_7 7:task_committed:item_7 11:theta_crossed:item_7 33:no_current_task:item_6 63:task_committed:item_6 81:theta_crossed:item_6 95:no_current_task:item_4 131:task_committed:item_4 168:done:-  
Decisions b2a: 0:no_current_task:item_7 7:task_committed:item_7 11:theta_crossed:item_7 33:no_current_task:item_6 63:task_committed:item_6 81:theta_crossed:item_6 95:no_current_task:item_4 131:task_committed:item_4 168:done:-  
Decision sequence: identical

[sep] < 50: none 161–299 (139 t, min 8.15 @163)  
[sep] < 50: b2a 161–299 (139 t, min 8.15 @163)

Counterfactual B3: continues 5, B3 would switch 0, single-task pool 1; cf log equals the run: yes

## s10_off

B2 verdicts:

- 24: trigger=task_committed current=item_7 projection=none verdict=continue hold=0
- 29: trigger=theta_crossed current=item_7 projection=admitted realizable=True reason=realized delta=6 T_r=44.81 remaining=47.29 rho=0.5 bound=23.64 verdict=continue_hold hold=6
- 33: trigger=theta_crossed current=item_7 projection=admitted realizable=True reason=realized delta=2 T_r=44.81 remaining=43.29 rho=0.5 bound=21.64 verdict=continue_hold hold=2
- 35: trigger=theta_crossed current=item_7 projection=admitted realizable=True reason=realized delta=0 T_r=44.81 remaining=41.29 rho=0.5 bound=20.64 verdict=continue hold=0
- 123: trigger=theta_crossed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=48.81 remaining=4.00 rho=0.5 bound=2.00 verdict=continue hold=0
- 126: trigger=task_committed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=45.33 remaining=4.00 rho=0.5 bound=2.00 verdict=continue hold=0
- 230: trigger=task_committed current=item_1 projection=none verdict=continue hold=0
- 247: trigger=theta_crossed current=item_1 projection=admitted realizable=True reason=realized delta=0 T_r=40.27 remaining=65.93 rho=0.5 bound=32.97 verdict=continue hold=0
- 334: trigger=theta_crossed current=item_4 projection=admitted realizable=True reason=realized delta=0 T_r=91.27 remaining=32.52 rho=0.5 bound=16.26 verdict=continue hold=0
- 357: trigger=task_committed current=item_4 projection=admitted realizable=True reason=realized delta=0 T_r=67.36 remaining=9.52 rho=0.5 bound=4.76 verdict=continue hold=0

Decisions none: 0:no_current_task:item_7 24:task_committed:item_7 29:theta_crossed:item_7 33:theta_crossed:item_7 35:theta_crossed:item_7 75:no_current_task:item_6 120:task_committed:item_6 123:theta_crossed:item_6 167:no_current_task:item_1 224:task_committed:item_1 247:theta_crossed:item_1 283:no_current_task:item_4 334:theta_crossed:item_4 351:task_committed:item_4 420:done:-  
Decisions b2a: 0:no_current_task:item_7 24:task_committed:item_7 29:theta_crossed:item_7 33:theta_crossed:item_7 35:theta_crossed:item_7 81:no_current_task:item_6 123:theta_crossed:item_6 126:task_committed:item_6 173:no_current_task:item_1 230:task_committed:item_1 247:theta_crossed:item_1 289:no_current_task:item_4 334:theta_crossed:item_4 357:task_committed:item_4 426:done:-  
Decision sequence: differs from entry 5 (none (75, 'no_current_task', 'item_6'), b2a (81, 'no_current_task', 'item_6')); task order (consecutive repeats collapsed) identical

Holds:

- `[hold] step=29 robot_0 start planned=6 trigger=theta_crossed pos=(244.17, -343.67)`
- `[hold] step=33 robot_0 end planned=6 executed=4 interrupted=True by=theta_crossed`
- `[hold] step=33 robot_0 start planned=2 trigger=theta_crossed pos=(244.17, -343.67)`
- `[hold] step=34 robot_0 end planned=2 executed=2 interrupted=False`

[sep] < 50: none 72–75 (4 t, min 30.87 @73)  
[sep] < 50: b2a 75–78 (4 t, min 30.87 @76)

Counterfactual B3: continues 10, B3 would switch 0, single-task pool 2; cf log equals the run: yes

## s10_on

B2 verdicts:

- 24: trigger=task_committed current=item_7 projection=none verdict=continue hold=0
- 25: trigger=theta_crossed current=item_7 projection=admitted realizable=True reason=realized delta=6 T_r=48.81 remaining=51.02 rho=0.5 bound=25.51 verdict=continue_hold hold=6
- 123: trigger=theta_crossed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=48.81 remaining=4.00 rho=0.5 bound=2.00 verdict=continue hold=0
- 126: trigger=task_committed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=45.33 remaining=4.00 rho=0.5 bound=2.00 verdict=continue hold=0
- 163: trigger=theta_crossed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=8.33 remaining=148.05 rho=0.5 bound=74.03 verdict=continue hold=0
- 230: trigger=task_committed current=item_1 projection=admitted realizable=True reason=realized delta=0 T_r=57.27 remaining=81.05 rho=0.5 bound=40.53 verdict=continue hold=0
- 314: trigger=theta_crossed current=item_4 projection=admitted realizable=True reason=realized delta=0 T_r=111.27 remaining=52.52 rho=0.5 bound=26.26 verdict=continue hold=0
- 357: trigger=task_committed current=item_4 projection=admitted realizable=True reason=realized delta=0 T_r=67.36 remaining=9.52 rho=0.5 bound=4.76 verdict=continue hold=0

Decisions none: 0:no_current_task:item_7 24:task_committed:item_7 25:theta_crossed:item_7 75:no_current_task:item_6 120:task_committed:item_6 123:theta_crossed:item_6 163:theta_crossed:item_6 167:no_current_task:item_1 224:task_committed:item_1 283:no_current_task:item_4 314:theta_crossed:item_4 351:task_committed:item_4 420:done:-  
Decisions b2a: 0:no_current_task:item_7 24:task_committed:item_7 25:theta_crossed:item_7 81:no_current_task:item_6 123:theta_crossed:item_6 126:task_committed:item_6 163:theta_crossed:item_6 173:no_current_task:item_1 230:task_committed:item_1 289:no_current_task:item_4 314:theta_crossed:item_4 357:task_committed:item_4 426:done:-  
Decision sequence: differs from entry 3 (none (75, 'no_current_task', 'item_6'), b2a (81, 'no_current_task', 'item_6')); task order (consecutive repeats collapsed) identical

Holds:

- `[hold] step=25 robot_0 start planned=6 trigger=theta_crossed pos=(285.19, -412.35)`
- `[hold] step=30 robot_0 end planned=6 executed=6 interrupted=False`

[sep] < 50: none 72–75 (4 t, min 30.87 @73)  
[sep] < 50: b2a 75–78 (4 t, min 30.87 @76)

Counterfactual B3: continues 8, B3 would switch 0, single-task pool 2; cf log equals the run: yes

## s20_off

B2 verdicts:

- 20: trigger=theta_crossed current=item_4 projection=admitted realizable=True reason=realized delta=7 T_r=33.74 remaining=35.24 rho=0.5 bound=17.62 verdict=continue_hold hold=7
- 24: trigger=theta_crossed current=item_4 projection=admitted realizable=True reason=realized delta=3 T_r=33.74 remaining=31.24 rho=0.5 bound=15.62 verdict=continue_hold hold=3
- 30: trigger=theta_crossed current=item_4 projection=admitted realizable=True reason=realized delta=1 T_r=29.95 remaining=25.24 rho=0.5 bound=12.62 verdict=continue_hold hold=1
- 87: trigger=theta_crossed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=57.06 remaining=36.93 rho=0.5 bound=18.47 verdict=continue hold=0
- 91: trigger=theta_crossed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=53.06 remaining=32.93 rho=0.5 bound=16.47 verdict=continue hold=0
- 95: trigger=theta_crossed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=49.06 remaining=28.93 rho=0.5 bound=14.47 verdict=continue hold=0
- 103: trigger=task_committed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=41.94 remaining=20.93 rho=0.5 bound=10.47 verdict=continue hold=0
- 190: trigger=task_committed current=item_7 projection=none verdict=continue hold=0

Decisions none: 0:no_current_task:item_4 20:theta_crossed:item_4 23:task_committed:item_4 24:theta_crossed:item_4 30:theta_crossed:item_4 54:no_current_task:item_6 87:theta_crossed:item_6 91:theta_crossed:item_6 95:theta_crossed:item_6 138:no_current_task:item_7 182:task_committed:item_7  
Decisions b2a: 0:no_current_task:item_4 20:theta_crossed:item_4 24:theta_crossed:item_4 30:theta_crossed:item_4 62:no_current_task:item_6 87:theta_crossed:item_6 91:theta_crossed:item_6 95:theta_crossed:item_6 103:task_committed:item_6 146:no_current_task:item_7 190:task_committed:item_7  
Decision sequence: differs from entry 2 (none (23, 'task_committed', 'item_4'), b2a (24, 'theta_crossed', 'item_4')); task order (consecutive repeats collapsed) identical

Holds:

- `[hold] step=20 robot_0 start planned=7 trigger=theta_crossed pos=(-321.11, -57.77)`
- `[hold] step=24 robot_0 end planned=7 executed=4 interrupted=True by=theta_crossed`
- `[hold] step=24 robot_0 start planned=3 trigger=theta_crossed pos=(-321.11, -57.77)`
- `[hold] step=26 robot_0 end planned=3 executed=3 interrupted=False`
- `[hold] step=30 robot_0 start planned=1 trigger=theta_crossed pos=(-312.17, -75.66)`
- `[hold] step=30 robot_0 end planned=1 executed=1 interrupted=False`

[sep] < 50: none 49–54 (6 t, min 11.64 @51); 133–139 (7 t, min 30.15 @138)  
[sep] < 50: b2a 56–58 (3 t, min 25.40 @57); 141–147 (7 t, min 30.15 @146)

Counterfactual B3: continues 8, B3 would switch 0, single-task pool 1; cf log equals the run: yes

## s20_on

B2 verdicts:

- 6: trigger=theta_crossed current=item_4 projection=admitted realizable=True reason=realized delta=7 T_r=47.74 remaining=49.19 rho=0.5 bound=24.60 verdict=continue_hold hold=7
- 30: trigger=task_committed current=item_4 projection=admitted realizable=True reason=realized delta=1 T_r=29.95 remaining=25.24 rho=0.5 bound=12.62 verdict=continue_hold hold=1
- 57: trigger=theta_crossed current=item_4 projection=admitted realizable=False reason=hold_position_violated delta=None T_r=3.95 remaining=65.10 rho=0.5 bound=32.55 verdict=escalate
- 103: trigger=task_committed current=item_6 projection=admitted realizable=True reason=realized delta=0 T_r=41.94 remaining=20.93 rho=0.5 bound=10.47 verdict=continue hold=0
- 190: trigger=task_committed current=item_7 projection=none verdict=continue hold=0

Decisions none: 0:no_current_task:item_4 6:theta_crossed:item_4 23:task_committed:item_4 54:no_current_task:item_6 57:theta_crossed:item_6 95:task_committed:item_6 138:no_current_task:item_7 182:task_committed:item_7  
Decisions b2a: 0:no_current_task:item_4 6:theta_crossed:item_4 30:task_committed:item_4 57:theta_crossed:item_4 62:no_current_task:item_6 103:task_committed:item_6 146:no_current_task:item_7 190:task_committed:item_7  
Decision sequence: differs from entry 2 (none (23, 'task_committed', 'item_4'), b2a (30, 'task_committed', 'item_4')); task order (consecutive repeats collapsed) identical

Holds:

- `[hold] step=6 robot_0 start planned=7 trigger=theta_crossed pos=(-446.33, 192.67)`
- `[hold] step=12 robot_0 end planned=7 executed=7 interrupted=False`
- `[hold] step=30 robot_0 start planned=1 trigger=task_committed pos=(-312.17, -75.66)`
- `[hold] step=30 robot_0 end planned=1 executed=1 interrupted=False`

[sep] < 50: none 49–54 (6 t, min 11.64 @51); 133–139 (7 t, min 30.15 @138)  
[sep] < 50: b2a 56–58 (3 t, min 25.40 @57); 141–147 (7 t, min 30.15 @146)

Counterfactual B3: continues 4, B3 would switch 0, single-task pool 1; cf log equals the run: yes

## s30_off

B2 verdicts:

- 28: trigger=theta_crossed current=item_4 projection=admitted realizable=True reason=realized delta=6 T_r=46.68 remaining=46.68 rho=0.5 bound=23.34 verdict=continue_hold hold=6
- 46: trigger=task_committed current=item_4 projection=admitted realizable=True reason=realized delta=1 T_r=34.54 remaining=29.54 rho=0.5 bound=14.77 verdict=continue_hold hold=1
- 86: trigger=theta_crossed current=item_2 projection=admitted realizable=True reason=realized delta=0 T_r=73.82 remaining=34.61 rho=0.5 bound=17.31 verdict=continue hold=0
- 121: trigger=task_committed current=item_2 projection=none verdict=continue hold=0

Decisions none: 0:no_current_task:item_4 28:theta_crossed:item_4 40:task_committed:item_4 76:no_current_task:item_2 86:theta_crossed:item_2 114:task_committed:item_2 154:done:-  
Decisions b2a: 0:no_current_task:item_4 28:theta_crossed:item_4 46:task_committed:item_4 83:no_current_task:item_2 86:theta_crossed:item_2 121:task_committed:item_2 161:done:-  
Decision sequence: differs from entry 2 (none (40, 'task_committed', 'item_4'), b2a (46, 'task_committed', 'item_4')); task order (consecutive repeats collapsed) identical

Holds:

- `[hold] step=28 robot_0 start planned=6 trigger=theta_crossed pos=(58.5, -130.2)`
- `[hold] step=33 robot_0 end planned=6 executed=6 interrupted=False`
- `[hold] step=46 robot_0 start planned=1 trigger=task_committed pos=(186.54, -283.85)`
- `[hold] step=46 robot_0 end planned=1 executed=1 interrupted=False`

[sep] < 50: none 21–24 (4 t, min 11.03 @22); 69–76 (8 t, min 11.70 @72); 148–199 (52 t, min 25.28 @149)  
[sep] < 50: b2a 21–24 (4 t, min 11.03 @22); 76–77 (2 t, min 38.57 @77); 155–199 (45 t, min 25.28 @156)

Counterfactual B3: continues 4, B3 would switch 0, single-task pool 2; cf log equals the run: yes

## s30_on

B2 verdicts:

- 21: trigger=theta_crossed current=item_4 projection=admitted realizable=False reason=hold_position_violated delta=None T_r=53.68 remaining=53.68 rho=0.5 bound=26.84 verdict=escalate
- 48: trigger=task_committed current=item_2 projection=admitted realizable=True reason=realized delta=0 T_r=39.09 remaining=27.54 rho=0.5 bound=13.77 verdict=continue hold=0
- 77: trigger=theta_crossed current=item_2 projection=admitted realizable=True reason=realized delta=0 T_r=10.09 remaining=43.61 rho=0.5 bound=21.81 verdict=continue hold=0
- 123: trigger=task_committed current=item_4 projection=none verdict=continue hold=0

Decisions none: 0:no_current_task:item_4 21:theta_crossed:item_2 48:task_committed:item_2 77:theta_crossed:item_2 89:no_current_task:item_4 123:task_committed:item_4 159:done:-  
Decisions b2a: 0:no_current_task:item_4 21:theta_crossed:item_2 48:task_committed:item_2 77:theta_crossed:item_2 89:no_current_task:item_4 123:task_committed:item_4 159:done:-  
Decision sequence: identical

[sep] < 50: none 21–23 (3 t, min 9.57 @22); 153–199 (47 t, min 16.20 @154)  
[sep] < 50: b2a 21–23 (3 t, min 9.57 @22); 153–199 (47 t, min 16.20 @154)

Counterfactual B3: continues 3, B3 would switch 0, single-task pool 1; cf log equals the run: yes

