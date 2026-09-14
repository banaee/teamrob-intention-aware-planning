# T7/T8 sweep comparison — baseline (adf9aea) vs new (HEAD)

PYTHONHASHSEED=0, the eight sweep conditions. `-` = baseline only, `+` = new only; unchanged decisions are not listed.

## s00_off

- first [meta] difference: step 166
- [IR]/[IR-dist] lines: new is a prefix of baseline (334 of 346 lines; the robot finishes earlier and stops observing)
- run end: baseline 172, new 166 (last [meta] step)

```
- step=166  proj  none(unresolved)
- step=166  meta  theta_crossed -> deliver_item(item_4) queue=[]
+ step=166  proj  none(unknown)
+ step=166  pool  deliver_item(?item=item_4) complete in world: dropped from the pool
+ step=166  meta  all tasks complete
- step=168  proj  none(unresolved)
- step=168  meta  task_committed -> deliver_item(item_4) queue=[]
- step=172  proj  none(unresolved)
- step=172  meta  all tasks complete
```

## s00_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (338 lines)
- run end: baseline 168, new 168 (last [meta] step)

```
- step=168  proj  none(unresolved)
+ step=168  proj  none(unknown)
```

## s20_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (400 lines)
- run end: baseline 190, new 190 (last [meta] step)

decision sequence unchanged.

## s20_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (400 lines)
- run end: baseline 176, new 176 (last [meta] step)

```
- step=132  proj  none(unresolved)
+ step=132  proj  none(unknown)
- step=176  proj  none(unresolved)
+ step=176  proj  none(unknown)
```

## s30_off

- first [meta] difference: step 87
- [IR]/[IR-dist] lines: identical up to step 154, first difference at step 155 (line 310 of 328 / 316)
- run end: baseline 163, new 157 (last [meta] step)

```
- step=87   meta  theta_crossed -> deliver_item(item_2) queue=["deliver_item(item_4)"]
+ step=87   pool  deliver_item(?item=item_2) complete in world: dropped from the pool
+ step=87   meta  theta_crossed -> deliver_item(item_4) queue=[]
- step=89   proj  built
- step=89   meta  task_committed -> deliver_item(item_2) queue=["deliver_item(item_4)"]
- step=93   proj  built
- step=93   meta  no_current_task -> deliver_item(item_4) queue=[]
+ step=121  proj  none(below_theta)
+ step=121  meta  task_committed -> deliver_item(item_4) queue=[]
- step=127  proj  none(below_theta)
- step=127  meta  task_committed -> deliver_item(item_4) queue=[]
+ step=157  proj  none(below_theta)
+ step=157  meta  all tasks complete
- step=163  proj  none(below_theta)
- step=163  meta  all tasks complete
```

## s30_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (320 lines)
- run end: baseline 159, new 159 (last [meta] step)

```
- step=123  proj  none(unresolved)
+ step=123  proj  none(unknown)
- step=159  proj  none(unresolved)
+ step=159  proj  none(unknown)
```

## s40_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (758 lines)
- run end: baseline 378, new 378 (last [meta] step)

```
- step=226  proj  none(unresolved)
+ step=226  proj  none(unknown)
- step=245  proj  none(unresolved)
+ step=245  proj  none(unknown)
```

## s40_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (758 lines)
- run end: baseline 378, new 378 (last [meta] step)

```
- step=223  proj  none(unresolved)
+ step=223  proj  none(unknown)
- step=245  proj  none(unresolved)
+ step=245  proj  none(unknown)
```

