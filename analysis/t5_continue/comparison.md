# T5 sweep comparison — baseline (T7/T8 baselines, 4c5684e) vs new (HEAD, continue costs nothing)

PYTHONHASHSEED=0, the eight sweep conditions. `-` = baseline only, `+` = new only; unchanged decisions are not listed.

## s00_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (334 lines)
- run end: baseline 166, new 166 (last [meta] step)
- full log minus [executor] lines: DIFFERS (1153 / 1153 lines)
- [executor] lines: 16 baseline / 16 new; continue_plan in new: 4
```
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=24
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=22
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=18
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=16
```

decision sequence unchanged.

## s00_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (338 lines)
- run end: baseline 168, new 168 (last [meta] step)
- full log minus [executor] lines: DIFFERS (1151 / 1151 lines)
- [executor] lines: 15 baseline / 15 new; continue_plan in new: 2
```
- [executor] _load_plan: robot_0 goal=deliver_item actions=2
+ [executor] continue_plan: robot_0 goal=deliver_item actions=2 action_index 0->0 queue_len=20
- [executor] _load_plan: robot_0 goal=deliver_item actions=2
+ [executor] continue_plan: robot_0 goal=deliver_item actions=2 action_index 0->0 queue_len=12
```

decision sequence unchanged.

## s20_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (400 lines)
- run end: baseline 190, new 190 (last [meta] step)
- full log minus [executor] lines: DIFFERS (1062 / 1062 lines)
- [executor] lines: 18 baseline / 18 new; continue_plan in new: 4
```
- [executor] _load_plan: robot_0 goal=deliver_item actions=2
+ [executor] continue_plan: robot_0 goal=deliver_item actions=2 action_index 0->0 queue_len=29
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=16
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=12
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=8
```

decision sequence unchanged.

## s20_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (400 lines)
- run end: baseline 176, new 176 (last [meta] step)
- full log minus [executor] lines: DIFFERS (1043 / 1043 lines)
- [executor] lines: 14 baseline / 14 new; continue_plan in new: 1
```
- [executor] _load_plan: robot_0 goal=deliver_item actions=2
+ [executor] continue_plan: robot_0 goal=deliver_item actions=2 action_index 0->0 queue_len=12
```

decision sequence unchanged.

## s30_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (316 lines)
- run end: baseline 157, new 157 (last [meta] step)
- full log minus [executor] lines: byte-identical (906 / 906 lines)
- [executor] lines: 10 baseline / 10 new; continue_plan in new: 0

decision sequence unchanged.

## s30_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (320 lines)
- run end: baseline 159, new 159 (last [meta] step)
- full log minus [executor] lines: byte-identical (913 / 913 lines)
- [executor] lines: 12 baseline / 12 new; continue_plan in new: 1
```
- [executor] _load_plan: robot_0 goal=deliver_item actions=2
+ [executor] continue_plan: robot_0 goal=deliver_item actions=2 action_index 0->0 queue_len=9
```

decision sequence unchanged.

## s40_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (758 lines)
- run end: baseline 378, new 378 (last [meta] step)
- full log minus [executor] lines: DIFFERS (1997 / 1997 lines)
- [executor] lines: 23 baseline / 23 new; continue_plan in new: 4
```
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=78
- [executor] _load_plan: robot_0 goal=deliver_item actions=2
+ [executor] continue_plan: robot_0 goal=deliver_item actions=2 action_index 0->0 queue_len=1
- [executor] _load_plan: robot_0 goal=deliver_item actions=2
+ [executor] continue_plan: robot_0 goal=deliver_item actions=2 action_index 0->0 queue_len=16
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=37
```

decision sequence unchanged.

## s40_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (758 lines)
- run end: baseline 378, new 378 (last [meta] step)
- full log minus [executor] lines: DIFFERS (1998 / 1998 lines)
- [executor] lines: 24 baseline / 24 new; continue_plan in new: 5
```
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=78
- [executor] _load_plan: robot_0 goal=deliver_item actions=2
+ [executor] continue_plan: robot_0 goal=deliver_item actions=2 action_index 0->0 queue_len=9
- [executor] _load_plan: robot_0 goal=deliver_item actions=2
+ [executor] continue_plan: robot_0 goal=deliver_item actions=2 action_index 0->0 queue_len=39
- [executor] _load_plan: robot_0 goal=deliver_item actions=2
+ [executor] continue_plan: robot_0 goal=deliver_item actions=2 action_index 0->0 queue_len=19
- [executor] _load_plan: robot_0 goal=deliver_item actions=4
+ [executor] continue_plan: robot_0 goal=deliver_item actions=4 action_index 0->0 queue_len=37
```

decision sequence unchanged.

