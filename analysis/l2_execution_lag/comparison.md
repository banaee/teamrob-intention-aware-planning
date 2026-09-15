# L2 sweep comparison — baseline (T9 baselines: no completion latency, human projection at step 0) vs new (HEAD: per-action completion latency, human projection at the observation offset)

PYTHONHASHSEED=0, ten conditions. `-` = baseline only, `+` = new only; unchanged decisions are not listed.

## s00_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (334 lines)
- run end: baseline 166, new 166 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: byte-identical (1152 / 1152 lines)
- actual robot–human separation, baseline: min 8.2 cm at step 163; ticks below 50 cm: 139 of 300 (runs 161–299)
- actual robot–human separation, new:      min 8.2 cm at step 163; ticks below 50 cm: 139 of 300 (runs 161–299)

decision sequence unchanged.

[meta-cand] lines that differ (10 of 10 triggers):
```
- step=0    deliver_item(?item=item_4) cost=74 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=43 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=27 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=78 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=47 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=31 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_7) cost=23 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_4) cost=75 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_6) cost=40 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_7) cost=25 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_4) cost=81 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_6) cost=46 feasible=True conflicts=0 min_dist=None
- step=33   deliver_item(?item=item_4) cost=69 feasible=True conflicts=0 min_dist=None
- step=33   deliver_item(?item=item_6) cost=57 feasible=True conflicts=0 min_dist=None
+ step=33   deliver_item(?item=item_4) cost=73 feasible=True conflicts=0 min_dist=None
+ step=33   deliver_item(?item=item_6) cost=61 feasible=True conflicts=0 min_dist=None
- step=39   deliver_item(?item=item_6) cost=51 feasible=True conflicts=715 min_dist=133.431547988033
- step=39   deliver_item(?item=item_4) cost=67 feasible=True conflicts=717 min_dist=251.4656037581773
+ step=39   deliver_item(?item=item_6) cost=55 feasible=True conflicts=805 min_dist=142.29683038142613
+ step=39   deliver_item(?item=item_4) cost=71 feasible=True conflicts=809 min_dist=281.4383856481172
- step=63   deliver_item(?item=item_6) cost=29 feasible=True conflicts=271 min_dist=284.04707534597736
- step=63   deliver_item(?item=item_4) cost=71 feasible=True conflicts=272 min_dist=326.65102103903394
+ step=63   deliver_item(?item=item_6) cost=31 feasible=True conflicts=313 min_dist=224.0860666860602
+ step=63   deliver_item(?item=item_4) cost=77 feasible=True conflicts=316 min_dist=326.65102103903394
- step=95   deliver_item(?item=item_4) cost=69 feasible=True conflicts=0 min_dist=None
+ step=95   deliver_item(?item=item_4) cost=73 feasible=True conflicts=0 min_dist=None
- step=109  deliver_item(?item=item_4) cost=55 feasible=True conflicts=603 min_dist=138.01913335783362
+ step=109  deliver_item(?item=item_4) cost=59 feasible=True conflicts=694 min_dist=145.99820680955318
- step=113  deliver_item(?item=item_4) cost=51 feasible=True conflicts=562 min_dist=143.3385156396938
+ step=113  deliver_item(?item=item_4) cost=55 feasible=True conflicts=606 min_dist=145.9982068095532
- step=115  deliver_item(?item=item_4) cost=49 feasible=True conflicts=522 min_dist=143.33851563969387
+ step=115  deliver_item(?item=item_4) cost=53 feasible=True conflicts=566 min_dist=145.9982068095532
- step=131  deliver_item(?item=item_4) cost=34 feasible=True conflicts=200 min_dist=462.12348726341355
+ step=131  deliver_item(?item=item_4) cost=36 feasible=True conflicts=242 min_dist=402.13573882367996
```

## s00_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (338 lines)
- run end: baseline 168, new 168 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: byte-identical (1149 / 1149 lines)
- actual robot–human separation, baseline: min 8.2 cm at step 163; ticks below 50 cm: 139 of 300 (runs 161–299)
- actual robot–human separation, new:      min 8.2 cm at step 163; ticks below 50 cm: 139 of 300 (runs 161–299)

decision sequence unchanged.

[meta-cand] lines that differ (8 of 8 triggers):
```
- step=0    deliver_item(?item=item_4) cost=74 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=43 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=27 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=78 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=47 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=31 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_7) cost=23 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_4) cost=75 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_6) cost=40 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_7) cost=25 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_4) cost=81 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_6) cost=46 feasible=True conflicts=0 min_dist=None
- step=11   deliver_item(?item=item_7) cost=19 feasible=True conflicts=374 min_dist=355.83097980731407
- step=11   deliver_item(?item=item_4) cost=77 feasible=True conflicts=1263 min_dist=136.51480541191665
- step=11   deliver_item(?item=item_6) cost=43 feasible=True conflicts=869 min_dist=258.3440123557938
+ step=11   deliver_item(?item=item_7) cost=21 feasible=True conflicts=396 min_dist=354.72725551788614
+ step=11   deliver_item(?item=item_4) cost=83 feasible=True conflicts=1357 min_dist=147.88250011902596
+ step=11   deliver_item(?item=item_6) cost=49 feasible=True conflicts=981 min_dist=253.5932228195933
- step=33   deliver_item(?item=item_4) cost=69 feasible=True conflicts=820 min_dist=328.3287876413511
- step=33   deliver_item(?item=item_6) cost=57 feasible=True conflicts=820 min_dist=133.51939100504887
+ step=33   deliver_item(?item=item_4) cost=73 feasible=True conflicts=910 min_dist=353.74353121315943
+ step=33   deliver_item(?item=item_6) cost=61 feasible=True conflicts=908 min_dist=142.58824557930367
- step=63   deliver_item(?item=item_6) cost=29 feasible=True conflicts=271 min_dist=284.04707534597736
- step=63   deliver_item(?item=item_4) cost=71 feasible=True conflicts=272 min_dist=326.65102103903394
+ step=63   deliver_item(?item=item_6) cost=31 feasible=True conflicts=313 min_dist=224.0860666860602
+ step=63   deliver_item(?item=item_4) cost=77 feasible=True conflicts=316 min_dist=326.65102103903394
- step=81   deliver_item(?item=item_6) cost=11 feasible=True conflicts=213 min_dist=154.79429320225282
- step=81   deliver_item(?item=item_4) cost=88 feasible=True conflicts=1139 min_dist=203.16099583581837
+ step=81   deliver_item(?item=item_6) cost=13 feasible=True conflicts=235 min_dist=141.29715651982056
+ step=81   deliver_item(?item=item_4) cost=94 feasible=True conflicts=1231 min_dist=223.01625963590845
- step=95   deliver_item(?item=item_4) cost=69 feasible=True conflicts=857 min_dist=133.6564062768077
+ step=95   deliver_item(?item=item_4) cost=73 feasible=True conflicts=947 min_dist=141.61293942184412
- step=131  deliver_item(?item=item_4) cost=34 feasible=True conflicts=200 min_dist=462.12348726341355
+ step=131  deliver_item(?item=item_4) cost=36 feasible=True conflicts=242 min_dist=402.13573882367996
```

## s10_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (842 lines)
- run end: baseline 420, new 420 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: byte-identical (2238 / 2238 lines)
- actual robot–human separation, baseline: min 30.9 cm at step 73; ticks below 50 cm: 4 of 450 (runs 72–75)
- actual robot–human separation, new:      min 30.9 cm at step 73; ticks below 50 cm: 4 of 450 (runs 72–75)

decision sequence unchanged.

[meta-cand] lines that differ (14 of 14 triggers):
```
- step=0    deliver_item(?item=item_4) cost=105 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_1) cost=116 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=70 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=85 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=109 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_1) cost=120 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=74 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=89 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_7) cost=48 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_4) cost=100 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_1) cost=118 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_6) cost=84 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_7) cost=50 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_4) cost=106 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_1) cost=124 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_6) cost=90 feasible=True conflicts=0 min_dist=None
- step=29   deliver_item(?item=item_7) cost=43 feasible=True conflicts=842 min_dist=42.88956972879639
- step=29   deliver_item(?item=item_4) cost=104 feasible=True conflicts=858 min_dist=1216.7899111679899
- step=29   deliver_item(?item=item_1) cost=122 feasible=True conflicts=854 min_dist=740.3381606173278
- step=29   deliver_item(?item=item_6) cost=88 feasible=True conflicts=854 min_dist=746.3027228081929
+ step=29   deliver_item(?item=item_7) cost=45 feasible=True conflicts=880 min_dist=42.88956972879639
+ step=29   deliver_item(?item=item_4) cost=110 feasible=True conflicts=954 min_dist=1230.6388498870238
+ step=29   deliver_item(?item=item_1) cost=128 feasible=True conflicts=946 min_dist=735.4388356748575
+ step=29   deliver_item(?item=item_6) cost=94 feasible=True conflicts=910 min_dist=741.5226702730195
- step=33   deliver_item(?item=item_7) cost=39 feasible=True conflicts=780 min_dist=50.139147331055526
- step=33   deliver_item(?item=item_4) cost=109 feasible=True conflicts=812 min_dist=1144.6247463777913
- step=33   deliver_item(?item=item_1) cost=126 feasible=True conflicts=812 min_dist=769.759777145446
- step=33   deliver_item(?item=item_6) cost=92 feasible=True conflicts=812 min_dist=774.9501191119177
+ step=33   deliver_item(?item=item_7) cost=41 feasible=True conflicts=795 min_dist=42.889569728796374
+ step=33   deliver_item(?item=item_4) cost=115 feasible=True conflicts=858 min_dist=1140.0803444797236
+ step=33   deliver_item(?item=item_1) cost=132 feasible=True conflicts=858 min_dist=774.6614565969417
+ step=33   deliver_item(?item=item_6) cost=98 feasible=True conflicts=858 min_dist=779.7337927522581
- step=35   deliver_item(?item=item_7) cost=37 feasible=True conflicts=740 min_dist=50.139147331055554
- step=35   deliver_item(?item=item_4) cost=111 feasible=True conflicts=772 min_dist=1087.5482544080182
- step=35   deliver_item(?item=item_1) cost=128 feasible=True conflicts=772 min_dist=789.3767414661886
- step=35   deliver_item(?item=item_6) cost=94 feasible=True conflicts=772 min_dist=794.0814343903278
+ step=35   deliver_item(?item=item_7) cost=39 feasible=True conflicts=755 min_dist=42.889569728796495
+ step=35   deliver_item(?item=item_4) cost=117 feasible=True conflicts=818 min_dist=1098.4741212216559
+ step=35   deliver_item(?item=item_1) cost=134 feasible=True conflicts=818 min_dist=794.2790267816601
+ step=35   deliver_item(?item=item_6) cost=100 feasible=True conflicts=818 min_dist=798.8660395317173
- step=75   deliver_item(?item=item_4) cost=131 feasible=True conflicts=0 min_dist=None
- step=75   deliver_item(?item=item_1) cost=110 feasible=True conflicts=0 min_dist=None
- step=75   deliver_item(?item=item_6) cost=87 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_4) cost=135 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_1) cost=114 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_6) cost=91 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_6) cost=43 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_4) cost=138 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_1) cost=79 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_6) cost=45 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_4) cost=144 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_1) cost=85 feasible=True conflicts=0 min_dist=None
- step=123  deliver_item(?item=item_6) cost=40 feasible=True conflicts=21 min_dist=404.99382349897513
- step=123  deliver_item(?item=item_4) cost=141 feasible=True conflicts=21 min_dist=404.02515836464613
- step=123  deliver_item(?item=item_1) cost=81 feasible=True conflicts=21 min_dist=404.02515836464613
+ step=123  deliver_item(?item=item_6) cost=42 feasible=True conflicts=65 min_dist=406.80790252162524
+ step=123  deliver_item(?item=item_4) cost=147 feasible=True conflicts=43 min_dist=403.91149321504406
+ step=123  deliver_item(?item=item_1) cost=87 feasible=True conflicts=43 min_dist=403.91149321504406
- step=167  deliver_item(?item=item_4) cost=132 feasible=True conflicts=0 min_dist=None
- step=167  deliver_item(?item=item_1) cost=110 feasible=True conflicts=0 min_dist=None
+ step=167  deliver_item(?item=item_4) cost=136 feasible=True conflicts=0 min_dist=None
+ step=167  deliver_item(?item=item_1) cost=114 feasible=True conflicts=0 min_dist=None
- step=224  deliver_item(?item=item_1) cost=55 feasible=True conflicts=0 min_dist=None
- step=224  deliver_item(?item=item_4) cost=161 feasible=True conflicts=0 min_dist=None
+ step=224  deliver_item(?item=item_1) cost=57 feasible=True conflicts=0 min_dist=None
+ step=224  deliver_item(?item=item_4) cost=167 feasible=True conflicts=0 min_dist=None
- step=247  deliver_item(?item=item_1) cost=32 feasible=True conflicts=650 min_dist=595.2502863273698
- step=247  deliver_item(?item=item_4) cost=183 feasible=True conflicts=1226 min_dist=765.1060449894975
+ step=247  deliver_item(?item=item_1) cost=34 feasible=True conflicts=678 min_dist=615.2291541627636
+ step=247  deliver_item(?item=item_4) cost=189 feasible=True conflicts=1316 min_dist=761.0711480901864
- step=283  deliver_item(?item=item_4) cost=132 feasible=True conflicts=541 min_dist=68.66194452839795
+ step=283  deliver_item(?item=item_4) cost=136 feasible=True conflicts=583 min_dist=70.62910326213753
- step=334  deliver_item(?item=item_4) cost=81 feasible=True conflicts=596 min_dist=1149.7689187139745
+ step=334  deliver_item(?item=item_4) cost=85 feasible=True conflicts=641 min_dist=1168.6094394385839
- step=351  deliver_item(?item=item_4) cost=65 feasible=True conflicts=253 min_dist=1575.0979903210684
+ step=351  deliver_item(?item=item_4) cost=67 feasible=True conflicts=295 min_dist=1528.0382859055628
```

## s10_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (842 lines)
- run end: baseline 420, new 420 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: byte-identical (2228 / 2228 lines)
- actual robot–human separation, baseline: min 30.9 cm at step 73; ticks below 50 cm: 4 of 450 (runs 72–75)
- actual robot–human separation, new:      min 30.9 cm at step 73; ticks below 50 cm: 4 of 450 (runs 72–75)

decision sequence unchanged.

[meta-cand] lines that differ (12 of 12 triggers):
```
- step=0    deliver_item(?item=item_4) cost=105 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_1) cost=116 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=70 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=85 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=109 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_1) cost=120 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=74 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=89 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_7) cost=48 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_4) cost=100 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_1) cost=118 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_6) cost=84 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_7) cost=50 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_4) cost=106 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_1) cost=124 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_6) cost=90 feasible=True conflicts=0 min_dist=None
- step=25   deliver_item(?item=item_7) cost=47 feasible=True conflicts=924 min_dist=42.81462692997099
- step=25   deliver_item(?item=item_4) cost=100 feasible=True conflicts=934 min_dist=1110.6976934781198
- step=25   deliver_item(?item=item_1) cost=118 feasible=True conflicts=930 min_dist=701.4993959549911
- step=25   deliver_item(?item=item_6) cost=85 feasible=True conflicts=934 min_dist=708.6949320385785
+ step=25   deliver_item(?item=item_7) cost=49 feasible=True conflicts=957 min_dist=42.81462692997099
+ step=25   deliver_item(?item=item_4) cost=106 feasible=True conflicts=1029 min_dist=1090.7034848947405
+ step=25   deliver_item(?item=item_1) cost=124 feasible=True conflicts=1021 min_dist=696.5755876384421
+ step=25   deliver_item(?item=item_6) cost=91 feasible=True conflicts=1029 min_dist=703.8956715623859
- step=75   deliver_item(?item=item_4) cost=131 feasible=True conflicts=0 min_dist=None
- step=75   deliver_item(?item=item_1) cost=110 feasible=True conflicts=0 min_dist=None
- step=75   deliver_item(?item=item_6) cost=87 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_4) cost=135 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_1) cost=114 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_6) cost=91 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_6) cost=43 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_4) cost=138 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_1) cost=79 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_6) cost=45 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_4) cost=144 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_1) cost=85 feasible=True conflicts=0 min_dist=None
- step=123  deliver_item(?item=item_6) cost=40 feasible=True conflicts=21 min_dist=404.99382349897513
- step=123  deliver_item(?item=item_4) cost=141 feasible=True conflicts=21 min_dist=404.02515836464613
- step=123  deliver_item(?item=item_1) cost=81 feasible=True conflicts=21 min_dist=404.02515836464613
+ step=123  deliver_item(?item=item_6) cost=42 feasible=True conflicts=65 min_dist=406.80790252162524
+ step=123  deliver_item(?item=item_4) cost=147 feasible=True conflicts=43 min_dist=403.91149321504406
+ step=123  deliver_item(?item=item_1) cost=87 feasible=True conflicts=43 min_dist=403.91149321504406
- step=163  deliver_item(?item=item_6) cost=1 feasible=True conflicts=21 min_dist=797.0713551464581
- step=163  deliver_item(?item=item_4) cost=181 feasible=True conflicts=2874 min_dist=155.36536137703098
- step=163  deliver_item(?item=item_1) cost=121 feasible=True conflicts=2442 min_dist=155.36536137703098
+ step=163  deliver_item(?item=item_6) cost=3 feasible=True conflicts=43 min_dist=782.6060479588194
+ step=163  deliver_item(?item=item_4) cost=187 feasible=True conflicts=2968 min_dist=145.0118445884532
+ step=163  deliver_item(?item=item_1) cost=127 feasible=True conflicts=2558 min_dist=145.0118445884532
- step=167  deliver_item(?item=item_4) cost=132 feasible=True conflicts=2649 min_dist=122.56116155584593
- step=167  deliver_item(?item=item_1) cost=110 feasible=True conflicts=2212 min_dist=333.9080014239768
+ step=167  deliver_item(?item=item_4) cost=136 feasible=True conflicts=2719 min_dist=102.58964113434584
+ step=167  deliver_item(?item=item_1) cost=114 feasible=True conflicts=2284 min_dist=327.0588874778821
- step=224  deliver_item(?item=item_1) cost=55 feasible=True conflicts=1112 min_dist=557.5042120983487
- step=224  deliver_item(?item=item_4) cost=161 feasible=True conflicts=1649 min_dist=590.5992031806635
+ step=224  deliver_item(?item=item_1) cost=57 feasible=True conflicts=1138 min_dist=577.4800227730337
+ step=224  deliver_item(?item=item_4) cost=167 feasible=True conflicts=1737 min_dist=586.4453517707393
- step=283  deliver_item(?item=item_4) cost=132 feasible=True conflicts=541 min_dist=68.66194452839795
+ step=283  deliver_item(?item=item_4) cost=136 feasible=True conflicts=583 min_dist=70.62910326213753
- step=314  deliver_item(?item=item_4) cost=101 feasible=True conflicts=998 min_dist=593.474230144759
+ step=314  deliver_item(?item=item_4) cost=105 feasible=True conflicts=1046 min_dist=613.4741941842202
- step=351  deliver_item(?item=item_4) cost=65 feasible=True conflicts=253 min_dist=1575.0979903210684
+ step=351  deliver_item(?item=item_4) cost=67 feasible=True conflicts=295 min_dist=1528.0382859055628
```

## s20_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (400 lines)
- run end: baseline 182, new 182 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: byte-identical (1050 / 1050 lines)
- actual robot–human separation, baseline: min 11.6 cm at step 51; ticks below 50 cm: 13 of 200 (runs 49–54, 133–139)
- actual robot–human separation, new:      min 11.6 cm at step 51; ticks below 50 cm: 13 of 200 (runs 49–54, 133–139)

decision sequence unchanged.

[meta-cand] lines that differ (11 of 11 triggers):
```
- step=0    deliver_item(?item=item_4) cost=50 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=66 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=99 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=54 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=70 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=103 feasible=True conflicts=0 min_dist=None
- step=20   deliver_item(?item=item_4) cost=30 feasible=True conflicts=593 min_dist=9.595669774042024
- step=20   deliver_item(?item=item_6) cost=52 feasible=True conflicts=611 min_dist=202.8121099398404
- step=20   deliver_item(?item=item_7) cost=83 feasible=True conflicts=608 min_dist=81.38933794707839
+ step=20   deliver_item(?item=item_4) cost=34 feasible=True conflicts=589 min_dist=9.595669774042024
+ step=20   deliver_item(?item=item_6) cost=56 feasible=True conflicts=702 min_dist=206.50636310430062
+ step=20   deliver_item(?item=item_7) cost=87 feasible=True conflicts=697 min_dist=41.10199275332592
- step=23   deliver_item(?item=item_4) cost=28 feasible=True conflicts=0 min_dist=None
- step=23   deliver_item(?item=item_6) cost=52 feasible=True conflicts=0 min_dist=None
- step=23   deliver_item(?item=item_7) cost=83 feasible=True conflicts=0 min_dist=None
+ step=23   deliver_item(?item=item_4) cost=30 feasible=True conflicts=0 min_dist=None
+ step=23   deliver_item(?item=item_6) cost=58 feasible=True conflicts=0 min_dist=None
+ step=23   deliver_item(?item=item_7) cost=89 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_4) cost=27 feasible=True conflicts=541 min_dist=11.925498219639513
- step=24   deliver_item(?item=item_6) cost=54 feasible=True conflicts=573 min_dist=168.31072521862558
- step=24   deliver_item(?item=item_7) cost=83 feasible=True conflicts=570 min_dist=116.33828117428388
+ step=24   deliver_item(?item=item_4) cost=29 feasible=True conflicts=551 min_dist=9.469938627647608
+ step=24   deliver_item(?item=item_6) cost=60 feasible=True conflicts=620 min_dist=167.91309947860464
+ step=24   deliver_item(?item=item_7) cost=89 feasible=True conflicts=615 min_dist=129.80681256286056
- step=30   deliver_item(?item=item_4) cost=21 feasible=True conflicts=421 min_dist=11.925498219639659
- step=30   deliver_item(?item=item_6) cost=60 feasible=True conflicts=453 min_dist=137.14894309427726
- step=30   deliver_item(?item=item_7) cost=88 feasible=True conflicts=451 min_dist=137.14894309427726
+ step=30   deliver_item(?item=item_4) cost=23 feasible=True conflicts=431 min_dist=9.469938627647624
+ step=30   deliver_item(?item=item_6) cost=66 feasible=True conflicts=457 min_dist=138.79759010645
+ step=30   deliver_item(?item=item_7) cost=94 feasible=True conflicts=495 min_dist=138.79759010645
- step=54   deliver_item(?item=item_6) cost=78 feasible=True conflicts=0 min_dist=None
- step=54   deliver_item(?item=item_7) cost=84 feasible=True conflicts=0 min_dist=None
+ step=54   deliver_item(?item=item_6) cost=82 feasible=True conflicts=0 min_dist=None
+ step=54   deliver_item(?item=item_7) cost=88 feasible=True conflicts=0 min_dist=None
- step=87   deliver_item(?item=item_6) cost=45 feasible=True conflicts=646 min_dist=267.0301896492995
- step=87   deliver_item(?item=item_7) cost=86 feasible=True conflicts=642 min_dist=473.84081669871006
+ step=87   deliver_item(?item=item_6) cost=49 feasible=True conflicts=739 min_dist=207.49166803492636
+ step=87   deliver_item(?item=item_7) cost=90 feasible=True conflicts=731 min_dist=454.22053580122247
- step=91   deliver_item(?item=item_6) cost=41 feasible=True conflicts=604 min_dist=227.31087874830015
- step=91   deliver_item(?item=item_7) cost=88 feasible=True conflicts=601 min_dist=540.8111723256977
+ step=91   deliver_item(?item=item_6) cost=45 feasible=True conflicts=651 min_dist=207.49166803492656
+ step=91   deliver_item(?item=item_7) cost=92 feasible=True conflicts=644 min_dist=533.5355273827737
- step=95   deliver_item(?item=item_6) cost=40 feasible=True conflicts=521 min_dist=284.5398137322407
- step=95   deliver_item(?item=item_7) cost=90 feasible=True conflicts=522 min_dist=606.0403032763188
+ step=95   deliver_item(?item=item_6) cost=42 feasible=True conflicts=563 min_dist=224.9390826171469
+ step=95   deliver_item(?item=item_7) cost=96 feasible=True conflicts=566 min_dist=613.6579171635376
- step=138  deliver_item(?item=item_7) cost=84 feasible=True conflicts=0 min_dist=None
+ step=138  deliver_item(?item=item_7) cost=88 feasible=True conflicts=0 min_dist=None
- step=182  deliver_item(?item=item_7) cost=42 feasible=True conflicts=0 min_dist=None
+ step=182  deliver_item(?item=item_7) cost=44 feasible=True conflicts=0 min_dist=None
```

## s20_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (400 lines)
- run end: baseline 182, new 182 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: byte-identical (1039 / 1039 lines)
- actual robot–human separation, baseline: min 11.6 cm at step 51; ticks below 50 cm: 13 of 200 (runs 49–54, 133–139)
- actual robot–human separation, new:      min 11.6 cm at step 51; ticks below 50 cm: 13 of 200 (runs 49–54, 133–139)

decision sequence unchanged.

[meta-cand] lines that differ (8 of 8 triggers):
```
- step=0    deliver_item(?item=item_4) cost=50 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=66 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=99 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=54 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=70 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=103 feasible=True conflicts=0 min_dist=None
- step=6    deliver_item(?item=item_4) cost=44 feasible=True conflicts=873 min_dist=9.614417989712855
- step=6    deliver_item(?item=item_6) cost=61 feasible=True conflicts=892 min_dist=319.15514182504495
- step=6    deliver_item(?item=item_7) cost=94 feasible=True conflicts=890 min_dist=45.80460479486062
+ step=6    deliver_item(?item=item_4) cost=48 feasible=True conflicts=873 min_dist=9.614417989712855
+ step=6    deliver_item(?item=item_6) cost=65 feasible=True conflicts=980 min_dist=259.2074510811941
+ step=6    deliver_item(?item=item_7) cost=98 feasible=True conflicts=976 min_dist=81.86564839364374
- step=23   deliver_item(?item=item_4) cost=28 feasible=True conflicts=561 min_dist=11.925498219639696
- step=23   deliver_item(?item=item_6) cost=52 feasible=True conflicts=591 min_dist=180.6232102391427
- step=23   deliver_item(?item=item_7) cost=83 feasible=True conflicts=588 min_dist=107.20964320898081
+ step=23   deliver_item(?item=item_4) cost=30 feasible=True conflicts=571 min_dist=9.469938627647613
+ step=23   deliver_item(?item=item_6) cost=58 feasible=True conflicts=637 min_dist=177.9175406740098
+ step=23   deliver_item(?item=item_7) cost=89 feasible=True conflicts=632 min_dist=120.76229789705182
- step=54   deliver_item(?item=item_6) cost=78 feasible=True conflicts=0 min_dist=None
- step=54   deliver_item(?item=item_7) cost=84 feasible=True conflicts=0 min_dist=None
+ step=54   deliver_item(?item=item_6) cost=82 feasible=True conflicts=0 min_dist=None
+ step=54   deliver_item(?item=item_7) cost=88 feasible=True conflicts=0 min_dist=None
- step=57   deliver_item(?item=item_6) cost=75 feasible=True conflicts=1211 min_dist=74.44862501832893
- step=57   deliver_item(?item=item_7) cost=83 feasible=True conflicts=1211 min_dist=74.44862501832893
+ step=57   deliver_item(?item=item_6) cost=79 feasible=True conflicts=1302 min_dist=93.67500031118935
+ step=57   deliver_item(?item=item_7) cost=87 feasible=True conflicts=1302 min_dist=76.32697855712962
- step=95   deliver_item(?item=item_6) cost=40 feasible=True conflicts=521 min_dist=284.5398137322407
- step=95   deliver_item(?item=item_7) cost=90 feasible=True conflicts=522 min_dist=606.0403032763188
+ step=95   deliver_item(?item=item_6) cost=42 feasible=True conflicts=563 min_dist=224.9390826171469
+ step=95   deliver_item(?item=item_7) cost=96 feasible=True conflicts=566 min_dist=613.6579171635376
- step=138  deliver_item(?item=item_7) cost=84 feasible=True conflicts=0 min_dist=None
+ step=138  deliver_item(?item=item_7) cost=88 feasible=True conflicts=0 min_dist=None
- step=182  deliver_item(?item=item_7) cost=42 feasible=True conflicts=0 min_dist=None
+ step=182  deliver_item(?item=item_7) cost=44 feasible=True conflicts=0 min_dist=None
```

## s30_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (310 lines)
- run end: baseline 154, new 154 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: byte-identical (902 / 902 lines)
- actual robot–human separation, baseline: min 11.0 cm at step 22; ticks below 50 cm: 64 of 200 (runs 21–24, 69–76, 148–199)
- actual robot–human separation, new:      min 11.0 cm at step 22; ticks below 50 cm: 64 of 200 (runs 21–24, 69–76, 148–199)

decision sequence unchanged.

[meta-cand] lines that differ (6 of 6 triggers):
```
- step=0    deliver_item(?item=item_2) cost=82 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_4) cost=71 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_2) cost=86 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=75 feasible=True conflicts=0 min_dist=None
- step=28   deliver_item(?item=item_4) cost=43 feasible=True conflicts=845 min_dist=16.624760953661962
- step=28   deliver_item(?item=item_2) cost=55 feasible=True conflicts=843 min_dist=130.716325118304
+ step=28   deliver_item(?item=item_4) cost=47 feasible=True conflicts=823 min_dist=16.624760953661962
+ step=28   deliver_item(?item=item_2) cost=59 feasible=True conflicts=931 min_dist=147.8598820822604
- step=40   deliver_item(?item=item_4) cost=33 feasible=True conflicts=634 min_dist=16.93952481802421
- step=40   deliver_item(?item=item_2) cost=48 feasible=True conflicts=658 min_dist=299.3450736214021
+ step=40   deliver_item(?item=item_4) cost=35 feasible=True conflicts=638 min_dist=16.93952481802421
+ step=40   deliver_item(?item=item_2) cost=54 feasible=True conflicts=706 min_dist=319.29605814304034
- step=76   deliver_item(?item=item_2) cost=73 feasible=True conflicts=0 min_dist=None
+ step=76   deliver_item(?item=item_2) cost=77 feasible=True conflicts=0 min_dist=None
- step=86   deliver_item(?item=item_2) cost=63 feasible=True conflicts=601 min_dist=325.71522544744374
+ step=86   deliver_item(?item=item_2) cost=67 feasible=True conflicts=690 min_dist=341.5277410304672
- step=114  deliver_item(?item=item_2) cost=36 feasible=True conflicts=106 min_dist=644.2139670613135
+ step=114  deliver_item(?item=item_2) cost=38 feasible=True conflicts=150 min_dist=584.2831484831181
```

## s30_on

- first [meta] difference: step 21
- [IR]/[IR-dist] lines: one is a prefix of the other (320 new / 310 baseline lines)
- run end: baseline 154, new 159 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: DIFFERS (900 / 915 lines)
- actual robot–human separation, baseline: min 11.0 cm at step 22; ticks below 50 cm: 64 of 200 (runs 21–24, 69–76, 148–199)
- actual robot–human separation, new:      min 9.6 cm at step 22; ticks below 50 cm: 50 of 200 (runs 21–23, 153–199)

```
- step=21   meta  theta_crossed -> deliver_item(item_4) queue=["deliver_item(item_2)"]
+ step=21   meta  theta_crossed -> deliver_item(item_2) queue=["deliver_item(item_4)"]
- step=40   proj  built
- step=40   meta  task_committed -> deliver_item(item_4) queue=["deliver_item(item_2)"]
+ step=48   proj  built
+ step=48   meta  task_committed -> deliver_item(item_2) queue=["deliver_item(item_4)"]
- step=76   proj  none(below_theta)
- step=76   meta  no_current_task -> deliver_item(item_2) queue=[]
- step=77   meta  theta_crossed -> deliver_item(item_2) queue=[]
+ step=77   meta  theta_crossed -> deliver_item(item_2) queue=["deliver_item(item_4)"]
+ step=89   proj  built
+ step=89   meta  no_current_task -> deliver_item(item_4) queue=[]
- step=114  proj  built
- step=114  meta  task_committed -> deliver_item(item_2) queue=[]
+ step=123  proj  none(unknown)
+ step=123  meta  task_committed -> deliver_item(item_4) queue=[]
- step=154  proj  none(unknown)
- step=154  meta  all tasks complete
+ step=159  proj  none(unknown)
+ step=159  meta  all tasks complete
```

[meta-cand] lines that differ (9 of 9 triggers):
```
- step=0    deliver_item(?item=item_2) cost=82 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_4) cost=71 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_2) cost=86 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=75 feasible=True conflicts=0 min_dist=None
- step=21   deliver_item(?item=item_4) cost=50 feasible=True conflicts=981 min_dist=15.37233196754729
- step=21   deliver_item(?item=item_2) cost=61 feasible=True conflicts=982 min_dist=22.68288481907288
+ step=21   deliver_item(?item=item_4) cost=54 feasible=False conflicts=949 min_dist=0.49296688528208676
+ step=21   deliver_item(?item=item_2) cost=65 feasible=True conflicts=1070 min_dist=9.43749337532574
- step=40   deliver_item(?item=item_4) cost=33 feasible=True conflicts=634 min_dist=16.93952481802421
- step=40   deliver_item(?item=item_2) cost=48 feasible=True conflicts=658 min_dist=299.3450736214021
+ step=48   deliver_item(?item=item_2) cost=39 feasible=True conflicts=535 min_dist=182.2423603808806
+ step=48   deliver_item(?item=item_4) cost=50 feasible=True conflicts=543 min_dist=393.33834237118464
- step=76   deliver_item(?item=item_2) cost=73 feasible=True conflicts=0 min_dist=None
- step=77   deliver_item(?item=item_2) cost=72 feasible=True conflicts=783 min_dist=42.66204608257219
+ step=77   deliver_item(?item=item_2) cost=10 feasible=True conflicts=187 min_dist=133.02099143783684
+ step=77   deliver_item(?item=item_4) cost=78 feasible=True conflicts=850 min_dist=185.66982750451044
+ step=89   deliver_item(?item=item_4) cost=69 feasible=True conflicts=622 min_dist=274.33050587894166
- step=114  deliver_item(?item=item_2) cost=36 feasible=True conflicts=106 min_dist=644.2139670613135
+ step=123  deliver_item(?item=item_4) cost=34 feasible=True conflicts=0 min_dist=None
```

## s40_off

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (758 lines)
- run end: baseline 378, new 378 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: byte-identical (1999 / 1999 lines)
- actual robot–human separation, baseline: min 4.6 cm at step 373; ticks below 50 cm: 29 of 400 (runs 371–399)
- actual robot–human separation, new:      min 4.6 cm at step 373; ticks below 50 cm: 29 of 400 (runs 371–399)

decision sequence unchanged.

[meta-cand] lines that differ (10 of 10 triggers):
```
- step=0    deliver_item(?item=item_4) cost=140 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=153 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_5) cost=159 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=144 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=157 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_5) cost=163 feasible=True conflicts=0 min_dist=None
- step=19   deliver_item(?item=item_4) cost=121 feasible=True conflicts=1867 min_dist=539.3838241912404
- step=19   deliver_item(?item=item_7) cost=134 feasible=True conflicts=1868 min_dist=493.76806745643796
- step=19   deliver_item(?item=item_5) cost=141 feasible=True conflicts=1868 min_dist=646.6475885544559
+ step=19   deliver_item(?item=item_4) cost=125 feasible=True conflicts=1959 min_dist=540.2894977532013
+ step=19   deliver_item(?item=item_7) cost=138 feasible=True conflicts=1960 min_dist=493.8713991293892
+ step=19   deliver_item(?item=item_5) cost=145 feasible=True conflicts=1960 min_dist=651.7041890552717
- step=98   deliver_item(?item=item_4) cost=45 feasible=True conflicts=321 min_dist=611.2364898043098
- step=98   deliver_item(?item=item_7) cost=63 feasible=True conflicts=320 min_dist=963.6380035644273
- step=98   deliver_item(?item=item_5) cost=92 feasible=True conflicts=322 min_dist=1090.7122970555033
+ step=98   deliver_item(?item=item_4) cost=47 feasible=True conflicts=363 min_dist=551.2875491864474
+ step=98   deliver_item(?item=item_7) cost=69 feasible=True conflicts=347 min_dist=958.5313929714155
+ step=98   deliver_item(?item=item_5) cost=98 feasible=True conflicts=366 min_dist=1079.0456112062775
- step=143  deliver_item(?item=item_4) cost=1 feasible=True conflicts=21 min_dist=531.77195230009
- step=143  deliver_item(?item=item_7) cost=107 feasible=True conflicts=208 min_dist=531.77195230009
- step=143  deliver_item(?item=item_5) cost=137 feasible=True conflicts=208 min_dist=531.77195230009
+ step=143  deliver_item(?item=item_4) cost=3 feasible=True conflicts=43 min_dist=531.77195230009
+ step=143  deliver_item(?item=item_7) cost=113 feasible=True conflicts=250 min_dist=526.1217447189691
+ step=143  deliver_item(?item=item_5) cost=143 feasible=True conflicts=250 min_dist=526.1217447189691
- step=147  deliver_item(?item=item_7) cost=92 feasible=True conflicts=129 min_dist=611.6249570888627
- step=147  deliver_item(?item=item_5) cost=128 feasible=True conflicts=129 min_dist=611.6249570888627
+ step=147  deliver_item(?item=item_7) cost=96 feasible=True conflicts=171 min_dist=612.5296253928537
+ step=147  deliver_item(?item=item_5) cost=132 feasible=True conflicts=171 min_dist=599.1895423564388
- step=195  deliver_item(?item=item_7) cost=46 feasible=True conflicts=0 min_dist=None
- step=195  deliver_item(?item=item_5) cost=107 feasible=True conflicts=0 min_dist=None
+ step=195  deliver_item(?item=item_7) cost=48 feasible=True conflicts=0 min_dist=None
+ step=195  deliver_item(?item=item_5) cost=113 feasible=True conflicts=0 min_dist=None
- step=226  deliver_item(?item=item_7) cost=15 feasible=True conflicts=0 min_dist=None
- step=226  deliver_item(?item=item_5) cost=138 feasible=True conflicts=0 min_dist=None
+ step=226  deliver_item(?item=item_7) cost=17 feasible=True conflicts=0 min_dist=None
+ step=226  deliver_item(?item=item_5) cost=144 feasible=True conflicts=0 min_dist=None
- step=245  deliver_item(?item=item_5) cost=128 feasible=True conflicts=0 min_dist=None
+ step=245  deliver_item(?item=item_5) cost=132 feasible=True conflicts=0 min_dist=None
- step=274  deliver_item(?item=item_5) cost=99 feasible=True conflicts=1122 min_dist=125.35068950315895
+ step=274  deliver_item(?item=item_5) cost=103 feasible=True conflicts=1170 min_dist=126.8927153191629
- step=311  deliver_item(?item=item_5) cost=64 feasible=True conflicts=378 min_dist=882.5462707157735
+ step=311  deliver_item(?item=item_5) cost=66 feasible=True conflicts=420 min_dist=822.547091264412
```

## s40_on

- first [meta] difference: none
- [IR]/[IR-dist] lines: byte-identical (758 lines)
- run end: baseline 378, new 378 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: byte-identical (1999 / 1999 lines)
- actual robot–human separation, baseline: min 4.6 cm at step 373; ticks below 50 cm: 29 of 400 (runs 371–399)
- actual robot–human separation, new:      min 4.6 cm at step 373; ticks below 50 cm: 29 of 400 (runs 371–399)

decision sequence unchanged.

[meta-cand] lines that differ (11 of 11 triggers):
```
- step=0    deliver_item(?item=item_4) cost=140 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=153 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_5) cost=159 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=144 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=157 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_5) cost=163 feasible=True conflicts=0 min_dist=None
- step=19   deliver_item(?item=item_4) cost=121 feasible=True conflicts=1867 min_dist=539.3838241912404
- step=19   deliver_item(?item=item_7) cost=134 feasible=True conflicts=1868 min_dist=493.76806745643796
- step=19   deliver_item(?item=item_5) cost=141 feasible=True conflicts=1868 min_dist=646.6475885544559
+ step=19   deliver_item(?item=item_4) cost=125 feasible=True conflicts=1959 min_dist=540.2894977532013
+ step=19   deliver_item(?item=item_7) cost=138 feasible=True conflicts=1960 min_dist=493.8713991293892
+ step=19   deliver_item(?item=item_5) cost=145 feasible=True conflicts=1960 min_dist=651.7041890552717
- step=98   deliver_item(?item=item_4) cost=45 feasible=True conflicts=321 min_dist=611.2364898043098
- step=98   deliver_item(?item=item_7) cost=63 feasible=True conflicts=320 min_dist=963.6380035644273
- step=98   deliver_item(?item=item_5) cost=92 feasible=True conflicts=322 min_dist=1090.7122970555033
+ step=98   deliver_item(?item=item_4) cost=47 feasible=True conflicts=363 min_dist=551.2875491864474
+ step=98   deliver_item(?item=item_7) cost=69 feasible=True conflicts=347 min_dist=958.5313929714155
+ step=98   deliver_item(?item=item_5) cost=98 feasible=True conflicts=366 min_dist=1079.0456112062775
- step=135  deliver_item(?item=item_4) cost=8 feasible=True conflicts=165 min_dist=361.4613995694038
- step=135  deliver_item(?item=item_7) cost=99 feasible=True conflicts=368 min_dist=361.4613995694038
- step=135  deliver_item(?item=item_5) cost=129 feasible=True conflicts=368 min_dist=361.4613995694038
+ step=135  deliver_item(?item=item_4) cost=10 feasible=True conflicts=187 min_dist=358.94889175583666
+ step=135  deliver_item(?item=item_7) cost=105 feasible=True conflicts=410 min_dist=365.2598751036304
+ step=135  deliver_item(?item=item_5) cost=135 feasible=True conflicts=410 min_dist=365.2598751036304
- step=147  deliver_item(?item=item_7) cost=92 feasible=True conflicts=129 min_dist=611.6249570888627
- step=147  deliver_item(?item=item_5) cost=128 feasible=True conflicts=129 min_dist=611.6249570888627
+ step=147  deliver_item(?item=item_7) cost=96 feasible=True conflicts=171 min_dist=612.5296253928537
+ step=147  deliver_item(?item=item_5) cost=132 feasible=True conflicts=171 min_dist=599.1895423564388
- step=195  deliver_item(?item=item_7) cost=46 feasible=True conflicts=0 min_dist=None
- step=195  deliver_item(?item=item_5) cost=107 feasible=True conflicts=0 min_dist=None
+ step=195  deliver_item(?item=item_7) cost=48 feasible=True conflicts=0 min_dist=None
+ step=195  deliver_item(?item=item_5) cost=113 feasible=True conflicts=0 min_dist=None
- step=203  deliver_item(?item=item_7) cost=38 feasible=True conflicts=767 min_dist=662.2356437586141
- step=203  deliver_item(?item=item_5) cost=115 feasible=True conflicts=1773 min_dist=77.31347513556628
+ step=203  deliver_item(?item=item_7) cost=40 feasible=True conflicts=796 min_dist=663.73321344863
+ step=203  deliver_item(?item=item_5) cost=121 feasible=True conflicts=1868 min_dist=68.44837916158727
- step=223  deliver_item(?item=item_7) cost=18 feasible=True conflicts=0 min_dist=None
- step=223  deliver_item(?item=item_5) cost=135 feasible=True conflicts=0 min_dist=None
+ step=223  deliver_item(?item=item_7) cost=20 feasible=True conflicts=0 min_dist=None
+ step=223  deliver_item(?item=item_5) cost=141 feasible=True conflicts=0 min_dist=None
- step=245  deliver_item(?item=item_5) cost=128 feasible=True conflicts=0 min_dist=None
+ step=245  deliver_item(?item=item_5) cost=132 feasible=True conflicts=0 min_dist=None
- step=274  deliver_item(?item=item_5) cost=99 feasible=True conflicts=1122 min_dist=125.35068950315895
+ step=274  deliver_item(?item=item_5) cost=103 feasible=True conflicts=1170 min_dist=126.8927153191629
- step=311  deliver_item(?item=item_5) cost=64 feasible=True conflicts=378 min_dist=882.5462707157735
+ step=311  deliver_item(?item=item_5) cost=66 feasible=True conflicts=420 min_dist=822.547091264412
```

