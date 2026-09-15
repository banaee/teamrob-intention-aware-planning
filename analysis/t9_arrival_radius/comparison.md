# T9 sweep comparison — baseline (aefebc7: walks projected to the target point) vs new (HEAD: walks end at the body's arrival radius)

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
- step=0    deliver_item(?item=item_4) cost=79 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=47 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=31 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=74 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=43 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=27 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_7) cost=24 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_4) cost=80 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_6) cost=44 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_7) cost=23 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_4) cost=75 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_6) cost=40 feasible=True conflicts=0 min_dist=None
- step=33   deliver_item(?item=item_4) cost=73 feasible=True conflicts=0 min_dist=None
- step=33   deliver_item(?item=item_6) cost=61 feasible=True conflicts=0 min_dist=None
+ step=33   deliver_item(?item=item_4) cost=69 feasible=True conflicts=0 min_dist=None
+ step=33   deliver_item(?item=item_6) cost=57 feasible=True conflicts=0 min_dist=None
- step=39   deliver_item(?item=item_6) cost=55 feasible=True conflicts=785 min_dist=133.10103522786702
- step=39   deliver_item(?item=item_4) cost=72 feasible=True conflicts=785 min_dist=275.3005220514368
+ step=39   deliver_item(?item=item_6) cost=51 feasible=True conflicts=715 min_dist=133.431547988033
+ step=39   deliver_item(?item=item_4) cost=67 feasible=True conflicts=717 min_dist=251.4656037581773
- step=63   deliver_item(?item=item_6) cost=30 feasible=True conflicts=301 min_dist=282.4899320941578
- step=63   deliver_item(?item=item_4) cost=76 feasible=True conflicts=303 min_dist=326.65102103903394
+ step=63   deliver_item(?item=item_6) cost=29 feasible=True conflicts=271 min_dist=284.04707534597736
+ step=63   deliver_item(?item=item_4) cost=71 feasible=True conflicts=272 min_dist=326.65102103903394
- step=95   deliver_item(?item=item_4) cost=73 feasible=True conflicts=0 min_dist=None
+ step=95   deliver_item(?item=item_4) cost=69 feasible=True conflicts=0 min_dist=None
- step=109  deliver_item(?item=item_4) cost=59 feasible=True conflicts=666 min_dist=142.2786660376136
+ step=109  deliver_item(?item=item_4) cost=55 feasible=True conflicts=603 min_dist=138.01913335783362
- step=113  deliver_item(?item=item_4) cost=55 feasible=True conflicts=592 min_dist=143.33851563969384
+ step=113  deliver_item(?item=item_4) cost=51 feasible=True conflicts=562 min_dist=143.3385156396938
- step=115  deliver_item(?item=item_4) cost=53 feasible=True conflicts=552 min_dist=143.33851563969387
+ step=115  deliver_item(?item=item_4) cost=49 feasible=True conflicts=522 min_dist=143.33851563969387
- step=131  deliver_item(?item=item_4) cost=35 feasible=True conflicts=230 min_dist=460.74877942168246
+ step=131  deliver_item(?item=item_4) cost=34 feasible=True conflicts=200 min_dist=462.12348726341355
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
- step=0    deliver_item(?item=item_4) cost=79 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=47 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=31 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=74 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=43 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=27 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_7) cost=24 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_4) cost=80 feasible=True conflicts=0 min_dist=None
- step=7    deliver_item(?item=item_6) cost=44 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_7) cost=23 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_4) cost=75 feasible=True conflicts=0 min_dist=None
+ step=7    deliver_item(?item=item_6) cost=40 feasible=True conflicts=0 min_dist=None
- step=11   deliver_item(?item=item_7) cost=20 feasible=True conflicts=404 min_dist=355.8309798073141
- step=11   deliver_item(?item=item_4) cost=84 feasible=True conflicts=1349 min_dist=145.4923009005327
- step=11   deliver_item(?item=item_6) cost=48 feasible=True conflicts=964 min_dist=238.0153833654881
+ step=11   deliver_item(?item=item_7) cost=19 feasible=True conflicts=374 min_dist=355.83097980731407
+ step=11   deliver_item(?item=item_4) cost=77 feasible=True conflicts=1263 min_dist=136.51480541191665
+ step=11   deliver_item(?item=item_6) cost=43 feasible=True conflicts=869 min_dist=258.3440123557938
- step=33   deliver_item(?item=item_4) cost=73 feasible=True conflicts=907 min_dist=360.33618884523327
- step=33   deliver_item(?item=item_6) cost=61 feasible=True conflicts=906 min_dist=133.101035227867
+ step=33   deliver_item(?item=item_4) cost=69 feasible=True conflicts=820 min_dist=328.3287876413511
+ step=33   deliver_item(?item=item_6) cost=57 feasible=True conflicts=820 min_dist=133.51939100504887
- step=63   deliver_item(?item=item_6) cost=30 feasible=True conflicts=301 min_dist=282.4899320941578
- step=63   deliver_item(?item=item_4) cost=76 feasible=True conflicts=303 min_dist=326.65102103903394
+ step=63   deliver_item(?item=item_6) cost=29 feasible=True conflicts=271 min_dist=284.04707534597736
+ step=63   deliver_item(?item=item_4) cost=71 feasible=True conflicts=272 min_dist=326.65102103903394
- step=81   deliver_item(?item=item_6) cost=12 feasible=True conflicts=243 min_dist=154.79429320225282
- step=81   deliver_item(?item=item_4) cost=94 feasible=True conflicts=1229 min_dist=203.16099583581837
+ step=81   deliver_item(?item=item_6) cost=11 feasible=True conflicts=213 min_dist=154.79429320225282
+ step=81   deliver_item(?item=item_4) cost=88 feasible=True conflicts=1139 min_dist=203.16099583581837
- step=95   deliver_item(?item=item_4) cost=73 feasible=True conflicts=947 min_dist=142.2786660376136
+ step=95   deliver_item(?item=item_4) cost=69 feasible=True conflicts=857 min_dist=133.6564062768077
- step=131  deliver_item(?item=item_4) cost=35 feasible=True conflicts=230 min_dist=460.74877942168246
+ step=131  deliver_item(?item=item_4) cost=34 feasible=True conflicts=200 min_dist=462.12348726341355
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
- step=0    deliver_item(?item=item_4) cost=110 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_1) cost=120 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=74 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=89 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=105 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_1) cost=116 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=70 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=85 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_7) cost=49 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_4) cost=105 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_1) cost=123 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_6) cost=89 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_7) cost=48 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_4) cost=100 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_1) cost=118 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_6) cost=84 feasible=True conflicts=0 min_dist=None
- step=29   deliver_item(?item=item_7) cost=44 feasible=True conflicts=893 min_dist=10.280130404034098
- step=29   deliver_item(?item=item_4) cost=110 feasible=True conflicts=931 min_dist=1216.7899111679899
- step=29   deliver_item(?item=item_1) cost=128 feasible=True conflicts=927 min_dist=762.4342605908444
- step=29   deliver_item(?item=item_6) cost=94 feasible=True conflicts=927 min_dist=762.4342605908444
+ step=29   deliver_item(?item=item_7) cost=43 feasible=True conflicts=842 min_dist=42.88956972879639
+ step=29   deliver_item(?item=item_4) cost=104 feasible=True conflicts=858 min_dist=1216.7899111679899
+ step=29   deliver_item(?item=item_1) cost=122 feasible=True conflicts=854 min_dist=740.3381606173278
+ step=29   deliver_item(?item=item_6) cost=88 feasible=True conflicts=854 min_dist=746.3027228081929
- step=33   deliver_item(?item=item_7) cost=40 feasible=True conflicts=810 min_dist=9.520609973538432
- step=33   deliver_item(?item=item_4) cost=114 feasible=True conflicts=842 min_dist=1144.6247463777913
- step=33   deliver_item(?item=item_1) cost=132 feasible=True conflicts=842 min_dist=797.3750676695346
- step=33   deliver_item(?item=item_6) cost=98 feasible=True conflicts=842 min_dist=797.3750676695347
+ step=33   deliver_item(?item=item_7) cost=39 feasible=True conflicts=780 min_dist=50.139147331055526
+ step=33   deliver_item(?item=item_4) cost=109 feasible=True conflicts=812 min_dist=1144.6247463777913
+ step=33   deliver_item(?item=item_1) cost=126 feasible=True conflicts=812 min_dist=769.759777145446
+ step=33   deliver_item(?item=item_6) cost=92 feasible=True conflicts=812 min_dist=774.9501191119177
- step=35   deliver_item(?item=item_7) cost=38 feasible=True conflicts=770 min_dist=9.520609973538207
- step=35   deliver_item(?item=item_4) cost=116 feasible=True conflicts=802 min_dist=1087.5482544080182
- step=35   deliver_item(?item=item_1) cost=134 feasible=True conflicts=802 min_dist=817.7998180280383
- step=35   deliver_item(?item=item_6) cost=100 feasible=True conflicts=802 min_dist=817.7998180280383
+ step=35   deliver_item(?item=item_7) cost=37 feasible=True conflicts=740 min_dist=50.139147331055554
+ step=35   deliver_item(?item=item_4) cost=111 feasible=True conflicts=772 min_dist=1087.5482544080182
+ step=35   deliver_item(?item=item_1) cost=128 feasible=True conflicts=772 min_dist=789.3767414661886
+ step=35   deliver_item(?item=item_6) cost=94 feasible=True conflicts=772 min_dist=794.0814343903278
- step=75   deliver_item(?item=item_4) cost=135 feasible=True conflicts=0 min_dist=None
- step=75   deliver_item(?item=item_1) cost=115 feasible=True conflicts=0 min_dist=None
- step=75   deliver_item(?item=item_6) cost=91 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_4) cost=131 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_1) cost=110 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_6) cost=87 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_6) cost=45 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_4) cost=144 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_1) cost=83 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_6) cost=43 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_4) cost=138 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_1) cost=79 feasible=True conflicts=0 min_dist=None
- step=123  deliver_item(?item=item_6) cost=42 feasible=True conflicts=42 min_dist=404.99382349897513
- step=123  deliver_item(?item=item_4) cost=147 feasible=True conflicts=42 min_dist=404.99382349897513
- step=123  deliver_item(?item=item_1) cost=86 feasible=True conflicts=42 min_dist=404.99382349897513
+ step=123  deliver_item(?item=item_6) cost=40 feasible=True conflicts=21 min_dist=404.99382349897513
+ step=123  deliver_item(?item=item_4) cost=141 feasible=True conflicts=21 min_dist=404.02515836464613
+ step=123  deliver_item(?item=item_1) cost=81 feasible=True conflicts=21 min_dist=404.02515836464613
- step=167  deliver_item(?item=item_4) cost=136 feasible=True conflicts=0 min_dist=None
- step=167  deliver_item(?item=item_1) cost=115 feasible=True conflicts=0 min_dist=None
+ step=167  deliver_item(?item=item_4) cost=132 feasible=True conflicts=0 min_dist=None
+ step=167  deliver_item(?item=item_1) cost=110 feasible=True conflicts=0 min_dist=None
- step=224  deliver_item(?item=item_1) cost=57 feasible=True conflicts=0 min_dist=None
- step=224  deliver_item(?item=item_4) cost=167 feasible=True conflicts=0 min_dist=None
+ step=224  deliver_item(?item=item_1) cost=55 feasible=True conflicts=0 min_dist=None
+ step=224  deliver_item(?item=item_4) cost=161 feasible=True conflicts=0 min_dist=None
- step=247  deliver_item(?item=item_1) cost=34 feasible=True conflicts=682 min_dist=572.3320921594042
- step=247  deliver_item(?item=item_4) cost=190 feasible=True conflicts=1277 min_dist=784.9322914892153
+ step=247  deliver_item(?item=item_1) cost=32 feasible=True conflicts=650 min_dist=595.2502863273698
+ step=247  deliver_item(?item=item_4) cost=183 feasible=True conflicts=1226 min_dist=765.1060449894975
- step=283  deliver_item(?item=item_4) cost=137 feasible=True conflicts=571 min_dist=68.66194452839794
+ step=283  deliver_item(?item=item_4) cost=132 feasible=True conflicts=541 min_dist=68.66194452839795
- step=334  deliver_item(?item=item_4) cost=86 feasible=True conflicts=626 min_dist=1149.7689187139745
+ step=334  deliver_item(?item=item_4) cost=81 feasible=True conflicts=596 min_dist=1149.7689187139745
- step=351  deliver_item(?item=item_4) cost=67 feasible=True conflicts=283 min_dist=1574.7098802731662
+ step=351  deliver_item(?item=item_4) cost=65 feasible=True conflicts=253 min_dist=1575.0979903210684
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
- step=0    deliver_item(?item=item_4) cost=110 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_1) cost=120 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=74 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=89 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=105 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_1) cost=116 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=70 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=85 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_7) cost=49 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_4) cost=105 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_1) cost=123 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_6) cost=89 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_7) cost=48 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_4) cost=100 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_1) cost=118 feasible=True conflicts=0 min_dist=None
+ step=24   deliver_item(?item=item_6) cost=84 feasible=True conflicts=0 min_dist=None
- step=25   deliver_item(?item=item_7) cost=48 feasible=True conflicts=973 min_dist=10.280130404034098
- step=25   deliver_item(?item=item_4) cost=106 feasible=True conflicts=1011 min_dist=1097.3311762141593
- step=25   deliver_item(?item=item_1) cost=124 feasible=True conflicts=1008 min_dist=723.7160124741365
- step=25   deliver_item(?item=item_6) cost=90 feasible=True conflicts=1011 min_dist=723.7160124741365
+ step=25   deliver_item(?item=item_7) cost=47 feasible=True conflicts=924 min_dist=42.81462692997099
+ step=25   deliver_item(?item=item_4) cost=100 feasible=True conflicts=934 min_dist=1110.6976934781198
+ step=25   deliver_item(?item=item_1) cost=118 feasible=True conflicts=930 min_dist=701.4993959549911
+ step=25   deliver_item(?item=item_6) cost=85 feasible=True conflicts=934 min_dist=708.6949320385785
- step=75   deliver_item(?item=item_4) cost=135 feasible=True conflicts=0 min_dist=None
- step=75   deliver_item(?item=item_1) cost=115 feasible=True conflicts=0 min_dist=None
- step=75   deliver_item(?item=item_6) cost=91 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_4) cost=131 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_1) cost=110 feasible=True conflicts=0 min_dist=None
+ step=75   deliver_item(?item=item_6) cost=87 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_6) cost=45 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_4) cost=144 feasible=True conflicts=0 min_dist=None
- step=120  deliver_item(?item=item_1) cost=83 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_6) cost=43 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_4) cost=138 feasible=True conflicts=0 min_dist=None
+ step=120  deliver_item(?item=item_1) cost=79 feasible=True conflicts=0 min_dist=None
- step=123  deliver_item(?item=item_6) cost=42 feasible=True conflicts=42 min_dist=404.99382349897513
- step=123  deliver_item(?item=item_4) cost=147 feasible=True conflicts=42 min_dist=404.99382349897513
- step=123  deliver_item(?item=item_1) cost=86 feasible=True conflicts=42 min_dist=404.99382349897513
+ step=123  deliver_item(?item=item_6) cost=40 feasible=True conflicts=21 min_dist=404.99382349897513
+ step=123  deliver_item(?item=item_4) cost=141 feasible=True conflicts=21 min_dist=404.02515836464613
+ step=123  deliver_item(?item=item_1) cost=81 feasible=True conflicts=21 min_dist=404.02515836464613
- step=163  deliver_item(?item=item_6) cost=2 feasible=True conflicts=39 min_dist=800.8007652026126
- step=163  deliver_item(?item=item_4) cost=187 feasible=True conflicts=2961 min_dist=155.365361377031
- step=163  deliver_item(?item=item_1) cost=126 feasible=True conflicts=2543 min_dist=155.365361377031
+ step=163  deliver_item(?item=item_6) cost=1 feasible=True conflicts=21 min_dist=797.0713551464581
+ step=163  deliver_item(?item=item_4) cost=181 feasible=True conflicts=2874 min_dist=155.36536137703098
+ step=163  deliver_item(?item=item_1) cost=121 feasible=True conflicts=2442 min_dist=155.36536137703098
- step=167  deliver_item(?item=item_4) cost=136 feasible=True conflicts=2739 min_dist=118.37310387534335
- step=167  deliver_item(?item=item_1) cost=115 feasible=True conflicts=2302 min_dist=333.9080014239768
+ step=167  deliver_item(?item=item_4) cost=132 feasible=True conflicts=2649 min_dist=122.56116155584593
+ step=167  deliver_item(?item=item_1) cost=110 feasible=True conflicts=2212 min_dist=333.9080014239768
- step=224  deliver_item(?item=item_1) cost=57 feasible=True conflicts=1142 min_dist=572.3320921594042
- step=224  deliver_item(?item=item_4) cost=167 feasible=True conflicts=1736 min_dist=596.0657898157144
+ step=224  deliver_item(?item=item_1) cost=55 feasible=True conflicts=1112 min_dist=557.5042120983487
+ step=224  deliver_item(?item=item_4) cost=161 feasible=True conflicts=1649 min_dist=590.5992031806635
- step=283  deliver_item(?item=item_4) cost=137 feasible=True conflicts=571 min_dist=68.66194452839794
+ step=283  deliver_item(?item=item_4) cost=132 feasible=True conflicts=541 min_dist=68.66194452839795
- step=314  deliver_item(?item=item_4) cost=106 feasible=True conflicts=1028 min_dist=593.474230144759
+ step=314  deliver_item(?item=item_4) cost=101 feasible=True conflicts=998 min_dist=593.474230144759
- step=351  deliver_item(?item=item_4) cost=67 feasible=True conflicts=283 min_dist=1574.7098802731662
+ step=351  deliver_item(?item=item_4) cost=65 feasible=True conflicts=253 min_dist=1575.0979903210684
```

## s20_off

- first [meta] difference: step 20
- [IR]/[IR-dist] lines: identical up to step 51, first difference at step 52 (line 105 of 400 / 400)
- run end: baseline 190, new 182 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: DIFFERS (1053 / 1050 lines)
- actual robot–human separation, baseline: min 17.7 cm at step 146; ticks below 50 cm: 13 of 200 (runs 55–58, 140–148)
- actual robot–human separation, new:      min 11.6 cm at step 51; ticks below 50 cm: 13 of 200 (runs 49–54, 133–139)

```
- step=20   meta  theta_crossed -> deliver_item(item_6) queue=["deliver_item(item_4)", "deliver_item(item_7)"]
+ step=20   meta  theta_crossed -> deliver_item(item_4) queue=["deliver_item(item_6)", "deliver_item(item_7)"]
+ step=23   proj  none(below_theta)
+ step=23   meta  task_committed -> deliver_item(item_4) queue=["deliver_item(item_6)", "deliver_item(item_7)"]
- step=29   proj  none(below_theta)
- step=29   meta  task_committed -> deliver_item(item_4) queue=["deliver_item(item_6)", "deliver_item(item_7)"]
+ step=54   proj  none(below_theta)
+ step=54   meta  no_current_task -> deliver_item(item_6) queue=["deliver_item(item_7)"]
- step=62   proj  none(below_theta)
- step=62   meta  no_current_task -> deliver_item(item_6) queue=["deliver_item(item_7)"]
- step=103  proj  built
- step=103  meta  task_committed -> deliver_item(item_6) queue=["deliver_item(item_7)"]
+ step=138  proj  none(below_theta)
+ step=138  meta  no_current_task -> deliver_item(item_7) queue=[]
- step=146  proj  none(below_theta)
- step=146  meta  no_current_task -> deliver_item(item_7) queue=[]
+ step=182  proj  none(below_theta)
+ step=182  meta  task_committed -> deliver_item(item_7) queue=[]
- step=190  proj  none(below_theta)
- step=190  meta  task_committed -> deliver_item(item_7) queue=[]
```

[meta-cand] lines that differ (16 of 16 triggers):
```
- step=0    deliver_item(?item=item_4) cost=54 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=71 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=103 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=50 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=66 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=99 feasible=True conflicts=0 min_dist=None
- step=20   deliver_item(?item=item_4) cost=34 feasible=False conflicts=675 min_dist=0.0
- step=20   deliver_item(?item=item_6) cost=56 feasible=True conflicts=696 min_dist=195.51363531406562
- step=20   deliver_item(?item=item_7) cost=87 feasible=True conflicts=693 min_dist=34.64122397505336
+ step=20   deliver_item(?item=item_4) cost=30 feasible=True conflicts=593 min_dist=9.595669774042024
+ step=20   deliver_item(?item=item_6) cost=52 feasible=True conflicts=611 min_dist=202.8121099398404
+ step=20   deliver_item(?item=item_7) cost=83 feasible=True conflicts=608 min_dist=81.38933794707839
+ step=23   deliver_item(?item=item_4) cost=28 feasible=True conflicts=0 min_dist=None
+ step=23   deliver_item(?item=item_6) cost=52 feasible=True conflicts=0 min_dist=None
+ step=23   deliver_item(?item=item_7) cost=83 feasible=True conflicts=0 min_dist=None
- step=24   deliver_item(?item=item_6) cost=52 feasible=True conflicts=600 min_dist=229.00574083100238
- step=24   deliver_item(?item=item_4) cost=35 feasible=True conflicts=601 min_dist=85.5991075288475
- step=24   deliver_item(?item=item_7) cost=89 feasible=True conflicts=597 min_dist=177.33069928828513
+ step=24   deliver_item(?item=item_4) cost=27 feasible=True conflicts=541 min_dist=11.925498219639513
+ step=24   deliver_item(?item=item_6) cost=54 feasible=True conflicts=573 min_dist=168.31072521862558
+ step=24   deliver_item(?item=item_7) cost=83 feasible=True conflicts=570 min_dist=116.33828117428388
- step=29   deliver_item(?item=item_4) cost=31 feasible=True conflicts=0 min_dist=None
- step=29   deliver_item(?item=item_6) cost=57 feasible=True conflicts=0 min_dist=None
- step=29   deliver_item(?item=item_7) cost=87 feasible=True conflicts=0 min_dist=None
- step=30   deliver_item(?item=item_4) cost=30 feasible=True conflicts=477 min_dist=100.2480573237873
- step=30   deliver_item(?item=item_6) cost=57 feasible=True conflicts=482 min_dist=193.6590679876973
- step=30   deliver_item(?item=item_7) cost=87 feasible=True conflicts=480 min_dist=193.6590679876973
+ step=30   deliver_item(?item=item_4) cost=21 feasible=True conflicts=421 min_dist=11.925498219639659
+ step=30   deliver_item(?item=item_6) cost=60 feasible=True conflicts=453 min_dist=137.14894309427726
+ step=30   deliver_item(?item=item_7) cost=88 feasible=True conflicts=451 min_dist=137.14894309427726
+ step=54   deliver_item(?item=item_6) cost=78 feasible=True conflicts=0 min_dist=None
+ step=54   deliver_item(?item=item_7) cost=84 feasible=True conflicts=0 min_dist=None
- step=62   deliver_item(?item=item_6) cost=83 feasible=True conflicts=0 min_dist=None
- step=62   deliver_item(?item=item_7) cost=89 feasible=True conflicts=0 min_dist=None
- step=87   deliver_item(?item=item_6) cost=58 feasible=True conflicts=700 min_dist=453.12738086906757
- step=87   deliver_item(?item=item_7) cost=88 feasible=True conflicts=698 min_dist=356.7512565058609
+ step=87   deliver_item(?item=item_6) cost=45 feasible=True conflicts=646 min_dist=267.0301896492995
+ step=87   deliver_item(?item=item_7) cost=86 feasible=True conflicts=642 min_dist=473.84081669871006
- step=91   deliver_item(?item=item_6) cost=54 feasible=True conflicts=634 min_dist=436.42036798970594
- step=91   deliver_item(?item=item_7) cost=89 feasible=True conflicts=631 min_dist=424.37413482166073
+ step=91   deliver_item(?item=item_6) cost=41 feasible=True conflicts=604 min_dist=227.31087874830015
+ step=91   deliver_item(?item=item_7) cost=88 feasible=True conflicts=601 min_dist=540.8111723256977
- step=95   deliver_item(?item=item_6) cost=50 feasible=True conflicts=554 min_dist=436.42036798970577
- step=95   deliver_item(?item=item_7) cost=90 feasible=True conflicts=551 min_dist=503.2871587194
+ step=95   deliver_item(?item=item_6) cost=40 feasible=True conflicts=521 min_dist=284.5398137322407
+ step=95   deliver_item(?item=item_7) cost=90 feasible=True conflicts=522 min_dist=606.0403032763188
- step=103  deliver_item(?item=item_6) cost=41 feasible=True conflicts=391 min_dist=406.3676233579452
- step=103  deliver_item(?item=item_7) cost=96 feasible=True conflicts=395 min_dist=685.4553639341905
+ step=138  deliver_item(?item=item_7) cost=84 feasible=True conflicts=0 min_dist=None
- step=146  deliver_item(?item=item_7) cost=89 feasible=True conflicts=0 min_dist=None
+ step=182  deliver_item(?item=item_7) cost=42 feasible=True conflicts=0 min_dist=None
- step=190  deliver_item(?item=item_7) cost=43 feasible=True conflicts=0 min_dist=None
```

## s20_on

- first [meta] difference: step 6
- [IR]/[IR-dist] lines: byte-identical (400 lines)
- run end: baseline 176, new 182 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: DIFFERS (1039 / 1039 lines)
- actual robot–human separation, baseline: min 19.1 cm at step 132; ticks below 50 cm: 9 of 200 (runs 126–134)
- actual robot–human separation, new:      min 11.6 cm at step 51; ticks below 50 cm: 13 of 200 (runs 49–54, 133–139)

```
- step=6    meta  theta_crossed -> deliver_item(item_6) queue=["deliver_item(item_4)", "deliver_item(item_7)"]
+ step=6    meta  theta_crossed -> deliver_item(item_4) queue=["deliver_item(item_6)", "deliver_item(item_7)"]
+ step=23   proj  built
+ step=23   meta  task_committed -> deliver_item(item_4) queue=["deliver_item(item_6)", "deliver_item(item_7)"]
- step=29   proj  built
- step=29   meta  task_committed -> deliver_item(item_6) queue=["deliver_item(item_4)", "deliver_item(item_7)"]
+ step=54   proj  none(below_theta)
+ step=54   meta  no_current_task -> deliver_item(item_6) queue=["deliver_item(item_7)"]
- step=57   meta  theta_crossed -> deliver_item(item_6) queue=["deliver_item(item_4)", "deliver_item(item_7)"]
+ step=57   meta  theta_crossed -> deliver_item(item_6) queue=["deliver_item(item_7)"]
- step=72   proj  built
- step=72   meta  no_current_task -> deliver_item(item_4) queue=["deliver_item(item_7)"]
+ step=95   proj  built
+ step=95   meta  task_committed -> deliver_item(item_6) queue=["deliver_item(item_7)"]
- step=101  proj  built
- step=101  meta  task_committed -> deliver_item(item_4) queue=["deliver_item(item_7)"]
- step=132  proj  none(unknown)
- step=132  meta  no_current_task -> deliver_item(item_7) queue=[]
+ step=138  proj  none(unknown)
+ step=138  meta  no_current_task -> deliver_item(item_7) queue=[]
- step=176  proj  none(unknown)
- step=176  meta  task_committed -> deliver_item(item_7) queue=[]
+ step=182  proj  none(unknown)
+ step=182  meta  task_committed -> deliver_item(item_7) queue=[]
```

[meta-cand] lines that differ (13 of 13 triggers):
```
- step=0    deliver_item(?item=item_4) cost=54 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_6) cost=71 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=103 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=50 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_6) cost=66 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=99 feasible=True conflicts=0 min_dist=None
- step=6    deliver_item(?item=item_4) cost=48 feasible=False conflicts=955 min_dist=0.0
- step=6    deliver_item(?item=item_6) cost=65 feasible=True conflicts=975 min_dist=310.99717874052817
- step=6    deliver_item(?item=item_7) cost=98 feasible=True conflicts=972 min_dist=90.18087050430493
+ step=6    deliver_item(?item=item_4) cost=44 feasible=True conflicts=873 min_dist=9.614417989712855
+ step=6    deliver_item(?item=item_6) cost=61 feasible=True conflicts=892 min_dist=319.15514182504495
+ step=6    deliver_item(?item=item_7) cost=94 feasible=True conflicts=890 min_dist=45.80460479486062
+ step=23   deliver_item(?item=item_4) cost=28 feasible=True conflicts=561 min_dist=11.925498219639696
+ step=23   deliver_item(?item=item_6) cost=52 feasible=True conflicts=591 min_dist=180.6232102391427
+ step=23   deliver_item(?item=item_7) cost=83 feasible=True conflicts=588 min_dist=107.20964320898081
- step=29   deliver_item(?item=item_6) cost=41 feasible=True conflicts=497 min_dist=303.0271585556239
- step=29   deliver_item(?item=item_4) cost=46 feasible=True conflicts=502 min_dist=404.1506188070751
- step=29   deliver_item(?item=item_7) cost=96 feasible=True conflicts=500 min_dist=408.27002650314904
+ step=54   deliver_item(?item=item_6) cost=78 feasible=True conflicts=0 min_dist=None
+ step=54   deliver_item(?item=item_7) cost=84 feasible=True conflicts=0 min_dist=None
- step=57   deliver_item(?item=item_6) cost=13 feasible=True conflicts=260 min_dist=158.72541080670683
- step=57   deliver_item(?item=item_4) cost=74 feasible=True conflicts=1304 min_dist=163.3605141634956
- step=57   deliver_item(?item=item_7) cost=124 feasible=True conflicts=1301 min_dist=221.65082468838543
+ step=57   deliver_item(?item=item_6) cost=75 feasible=True conflicts=1211 min_dist=74.44862501832893
+ step=57   deliver_item(?item=item_7) cost=83 feasible=True conflicts=1211 min_dist=74.44862501832893
- step=72   deliver_item(?item=item_4) cost=59 feasible=True conflicts=1000 min_dist=176.5088522228254
- step=72   deliver_item(?item=item_7) cost=89 feasible=True conflicts=1001 min_dist=73.05477339984841
+ step=95   deliver_item(?item=item_6) cost=40 feasible=True conflicts=521 min_dist=284.5398137322407
+ step=95   deliver_item(?item=item_7) cost=90 feasible=True conflicts=522 min_dist=606.0403032763188
- step=101  deliver_item(?item=item_4) cost=29 feasible=True conflicts=431 min_dist=129.0547735472518
- step=101  deliver_item(?item=item_7) cost=88 feasible=True conflicts=435 min_dist=478.76747776465675
- step=132  deliver_item(?item=item_7) cost=89 feasible=True conflicts=0 min_dist=None
+ step=138  deliver_item(?item=item_7) cost=84 feasible=True conflicts=0 min_dist=None
- step=176  deliver_item(?item=item_7) cost=43 feasible=True conflicts=0 min_dist=None
+ step=182  deliver_item(?item=item_7) cost=42 feasible=True conflicts=0 min_dist=None
```

## s30_off

- first [meta] difference: step 28
- [IR]/[IR-dist] lines: identical up to step 73, first difference at step 74 (line 148 of 316 / 310)
- run end: baseline 157, new 154 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: DIFFERS (908 / 902 lines)
- actual robot–human separation, baseline: min 11.0 cm at step 22; ticks below 50 cm: 53 of 200 (runs 21–24, 151–199)
- actual robot–human separation, new:      min 11.0 cm at step 22; ticks below 50 cm: 64 of 200 (runs 21–24, 69–76, 148–199)

```
- step=28   meta  theta_crossed -> deliver_item(item_2) queue=["deliver_item(item_4)"]
+ step=28   meta  theta_crossed -> deliver_item(item_4) queue=["deliver_item(item_2)"]
+ step=40   proj  built
+ step=40   meta  task_committed -> deliver_item(item_4) queue=["deliver_item(item_2)"]
- step=48   proj  built
- step=48   meta  task_committed -> deliver_item(item_2) queue=["deliver_item(item_4)"]
+ step=76   proj  none(below_theta)
+ step=76   meta  no_current_task -> deliver_item(item_2) queue=[]
+ step=86   proj  built
+ step=86   meta  theta_crossed -> deliver_item(item_2) queue=[]
- step=87   proj  built
- step=87   pool  deliver_item(?item=item_2) complete in world: dropped from the pool
- step=87   meta  theta_crossed -> deliver_item(item_4) queue=[]
+ step=114  proj  built
+ step=114  meta  task_committed -> deliver_item(item_2) queue=[]
- step=121  proj  none(below_theta)
- step=121  meta  task_committed -> deliver_item(item_4) queue=[]
+ step=154  proj  none(below_theta)
+ step=154  meta  all tasks complete
- step=157  proj  none(below_theta)
- step=157  meta  all tasks complete
```

[meta-cand] lines that differ (9 of 9 triggers):
```
- step=0    deliver_item(?item=item_2) cost=86 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_4) cost=75 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_2) cost=82 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=71 feasible=True conflicts=0 min_dist=None
- step=28   deliver_item(?item=item_4) cost=47 feasible=False conflicts=929 min_dist=0.0
- step=28   deliver_item(?item=item_2) cost=59 feasible=True conflicts=930 min_dist=130.716325118304
+ step=28   deliver_item(?item=item_4) cost=43 feasible=True conflicts=845 min_dist=16.624760953661962
+ step=28   deliver_item(?item=item_2) cost=55 feasible=True conflicts=843 min_dist=130.716325118304
+ step=40   deliver_item(?item=item_4) cost=33 feasible=True conflicts=634 min_dist=16.93952481802421
+ step=40   deliver_item(?item=item_2) cost=48 feasible=True conflicts=658 min_dist=299.3450736214021
- step=48   deliver_item(?item=item_2) cost=38 feasible=True conflicts=523 min_dist=224.43526119439784
- step=48   deliver_item(?item=item_4) cost=48 feasible=True conflicts=528 min_dist=420.726134366107
+ step=76   deliver_item(?item=item_2) cost=73 feasible=True conflicts=0 min_dist=None
+ step=86   deliver_item(?item=item_2) cost=63 feasible=True conflicts=601 min_dist=325.71522544744374
- step=87   deliver_item(?item=item_4) cost=69 feasible=True conflicts=664 min_dist=237.34206162974257
+ step=114  deliver_item(?item=item_2) cost=36 feasible=True conflicts=106 min_dist=644.2139670613135
- step=121  deliver_item(?item=item_4) cost=34 feasible=True conflicts=0 min_dist=None
```

## s30_on

- first [meta] difference: step 21
- [IR]/[IR-dist] lines: one is a prefix of the other (310 new / 320 baseline lines)
- run end: baseline 159, new 154 (last [meta] step)
- full log minus [meta-cand] and [sep] lines: DIFFERS (915 / 900 lines)
- actual robot–human separation, baseline: min 9.6 cm at step 22; ticks below 50 cm: 50 of 200 (runs 21–23, 153–199)
- actual robot–human separation, new:      min 11.0 cm at step 22; ticks below 50 cm: 64 of 200 (runs 21–24, 69–76, 148–199)

```
- step=21   meta  theta_crossed -> deliver_item(item_2) queue=["deliver_item(item_4)"]
+ step=21   meta  theta_crossed -> deliver_item(item_4) queue=["deliver_item(item_2)"]
+ step=40   proj  built
+ step=40   meta  task_committed -> deliver_item(item_4) queue=["deliver_item(item_2)"]
- step=48   proj  built
- step=48   meta  task_committed -> deliver_item(item_2) queue=["deliver_item(item_4)"]
+ step=76   proj  none(below_theta)
+ step=76   meta  no_current_task -> deliver_item(item_2) queue=[]
- step=77   meta  theta_crossed -> deliver_item(item_2) queue=["deliver_item(item_4)"]
+ step=77   meta  theta_crossed -> deliver_item(item_2) queue=[]
- step=89   proj  built
- step=89   meta  no_current_task -> deliver_item(item_4) queue=[]
+ step=114  proj  built
+ step=114  meta  task_committed -> deliver_item(item_2) queue=[]
- step=123  proj  none(unknown)
- step=123  meta  task_committed -> deliver_item(item_4) queue=[]
+ step=154  proj  none(unknown)
+ step=154  meta  all tasks complete
- step=159  proj  none(unknown)
- step=159  meta  all tasks complete
```

[meta-cand] lines that differ (9 of 9 triggers):
```
- step=0    deliver_item(?item=item_2) cost=86 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_4) cost=75 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_2) cost=82 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=71 feasible=True conflicts=0 min_dist=None
- step=21   deliver_item(?item=item_4) cost=54 feasible=False conflicts=1069 min_dist=0.0
- step=21   deliver_item(?item=item_2) cost=66 feasible=True conflicts=1070 min_dist=22.68288481907288
+ step=21   deliver_item(?item=item_4) cost=50 feasible=True conflicts=981 min_dist=15.37233196754729
+ step=21   deliver_item(?item=item_2) cost=61 feasible=True conflicts=982 min_dist=22.68288481907288
+ step=40   deliver_item(?item=item_4) cost=33 feasible=True conflicts=634 min_dist=16.93952481802421
+ step=40   deliver_item(?item=item_2) cost=48 feasible=True conflicts=658 min_dist=299.3450736214021
- step=48   deliver_item(?item=item_2) cost=39 feasible=True conflicts=523 min_dist=231.1241491722839
- step=48   deliver_item(?item=item_4) cost=48 feasible=True conflicts=528 min_dist=411.9746671560346
+ step=76   deliver_item(?item=item_2) cost=73 feasible=True conflicts=0 min_dist=None
- step=77   deliver_item(?item=item_2) cost=10 feasible=True conflicts=194 min_dist=148.66461418625423
- step=77   deliver_item(?item=item_4) cost=77 feasible=True conflicts=875 min_dist=166.0322841814406
+ step=77   deliver_item(?item=item_2) cost=72 feasible=True conflicts=783 min_dist=42.66204608257219
- step=89   deliver_item(?item=item_4) cost=69 feasible=True conflicts=628 min_dist=274.4955414504407
+ step=114  deliver_item(?item=item_2) cost=36 feasible=True conflicts=106 min_dist=644.2139670613135
- step=123  deliver_item(?item=item_4) cost=34 feasible=True conflicts=0 min_dist=None
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
- step=0    deliver_item(?item=item_4) cost=145 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=157 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_5) cost=163 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=140 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=153 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_5) cost=159 feasible=True conflicts=0 min_dist=None
- step=19   deliver_item(?item=item_4) cost=126 feasible=True conflicts=1957 min_dist=539.3838241912404
- step=19   deliver_item(?item=item_7) cost=138 feasible=True conflicts=1957 min_dist=493.7680674564379
- step=19   deliver_item(?item=item_5) cost=145 feasible=True conflicts=1958 min_dist=646.6475885544559
+ step=19   deliver_item(?item=item_4) cost=121 feasible=True conflicts=1867 min_dist=539.3838241912404
+ step=19   deliver_item(?item=item_7) cost=134 feasible=True conflicts=1868 min_dist=493.76806745643796
+ step=19   deliver_item(?item=item_5) cost=141 feasible=True conflicts=1868 min_dist=646.6475885544559
- step=98   deliver_item(?item=item_4) cost=47 feasible=True conflicts=351 min_dist=562.6915416813515
- step=98   deliver_item(?item=item_7) cost=67 feasible=True conflicts=356 min_dist=946.3994804923683
- step=98   deliver_item(?item=item_5) cost=97 feasible=True conflicts=354 min_dist=1089.2857660215768
+ step=98   deliver_item(?item=item_4) cost=45 feasible=True conflicts=321 min_dist=611.2364898043098
+ step=98   deliver_item(?item=item_7) cost=63 feasible=True conflicts=320 min_dist=963.6380035644273
+ step=98   deliver_item(?item=item_5) cost=92 feasible=True conflicts=322 min_dist=1090.7122970555033
- step=143  deliver_item(?item=item_4) cost=2 feasible=True conflicts=34 min_dist=531.77195230009
- step=143  deliver_item(?item=item_7) cost=112 feasible=True conflicts=238 min_dist=531.77195230009
- step=143  deliver_item(?item=item_5) cost=142 feasible=True conflicts=238 min_dist=531.77195230009
+ step=143  deliver_item(?item=item_4) cost=1 feasible=True conflicts=21 min_dist=531.77195230009
+ step=143  deliver_item(?item=item_7) cost=107 feasible=True conflicts=208 min_dist=531.77195230009
+ step=143  deliver_item(?item=item_5) cost=137 feasible=True conflicts=208 min_dist=531.77195230009
- step=147  deliver_item(?item=item_7) cost=97 feasible=True conflicts=159 min_dist=611.6249570888627
- step=147  deliver_item(?item=item_5) cost=132 feasible=True conflicts=159 min_dist=611.6249570888627
+ step=147  deliver_item(?item=item_7) cost=92 feasible=True conflicts=129 min_dist=611.6249570888627
+ step=147  deliver_item(?item=item_5) cost=128 feasible=True conflicts=129 min_dist=611.6249570888627
- step=195  deliver_item(?item=item_7) cost=48 feasible=True conflicts=0 min_dist=None
- step=195  deliver_item(?item=item_5) cost=112 feasible=True conflicts=0 min_dist=None
+ step=195  deliver_item(?item=item_7) cost=46 feasible=True conflicts=0 min_dist=None
+ step=195  deliver_item(?item=item_5) cost=107 feasible=True conflicts=0 min_dist=None
- step=226  deliver_item(?item=item_7) cost=17 feasible=True conflicts=0 min_dist=None
- step=226  deliver_item(?item=item_5) cost=143 feasible=True conflicts=0 min_dist=None
+ step=226  deliver_item(?item=item_7) cost=15 feasible=True conflicts=0 min_dist=None
+ step=226  deliver_item(?item=item_5) cost=138 feasible=True conflicts=0 min_dist=None
- step=245  deliver_item(?item=item_5) cost=132 feasible=True conflicts=0 min_dist=None
+ step=245  deliver_item(?item=item_5) cost=128 feasible=True conflicts=0 min_dist=None
- step=274  deliver_item(?item=item_5) cost=103 feasible=True conflicts=1152 min_dist=125.35068950315902
+ step=274  deliver_item(?item=item_5) cost=99 feasible=True conflicts=1122 min_dist=125.35068950315895
- step=311  deliver_item(?item=item_5) cost=65 feasible=True conflicts=408 min_dist=882.2022530315627
+ step=311  deliver_item(?item=item_5) cost=64 feasible=True conflicts=378 min_dist=882.5462707157735
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
- step=0    deliver_item(?item=item_4) cost=145 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_7) cost=157 feasible=True conflicts=0 min_dist=None
- step=0    deliver_item(?item=item_5) cost=163 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_4) cost=140 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_7) cost=153 feasible=True conflicts=0 min_dist=None
+ step=0    deliver_item(?item=item_5) cost=159 feasible=True conflicts=0 min_dist=None
- step=19   deliver_item(?item=item_4) cost=126 feasible=True conflicts=1957 min_dist=539.3838241912404
- step=19   deliver_item(?item=item_7) cost=138 feasible=True conflicts=1957 min_dist=493.7680674564379
- step=19   deliver_item(?item=item_5) cost=145 feasible=True conflicts=1958 min_dist=646.6475885544559
+ step=19   deliver_item(?item=item_4) cost=121 feasible=True conflicts=1867 min_dist=539.3838241912404
+ step=19   deliver_item(?item=item_7) cost=134 feasible=True conflicts=1868 min_dist=493.76806745643796
+ step=19   deliver_item(?item=item_5) cost=141 feasible=True conflicts=1868 min_dist=646.6475885544559
- step=98   deliver_item(?item=item_4) cost=47 feasible=True conflicts=351 min_dist=562.6915416813515
- step=98   deliver_item(?item=item_7) cost=67 feasible=True conflicts=356 min_dist=946.3994804923683
- step=98   deliver_item(?item=item_5) cost=97 feasible=True conflicts=354 min_dist=1089.2857660215768
+ step=98   deliver_item(?item=item_4) cost=45 feasible=True conflicts=321 min_dist=611.2364898043098
+ step=98   deliver_item(?item=item_7) cost=63 feasible=True conflicts=320 min_dist=963.6380035644273
+ step=98   deliver_item(?item=item_5) cost=92 feasible=True conflicts=322 min_dist=1090.7122970555033
- step=135  deliver_item(?item=item_4) cost=10 feasible=True conflicts=194 min_dist=361.4613995694038
- step=135  deliver_item(?item=item_7) cost=104 feasible=True conflicts=398 min_dist=361.4613995694038
- step=135  deliver_item(?item=item_5) cost=134 feasible=True conflicts=398 min_dist=361.4613995694038
+ step=135  deliver_item(?item=item_4) cost=8 feasible=True conflicts=165 min_dist=361.4613995694038
+ step=135  deliver_item(?item=item_7) cost=99 feasible=True conflicts=368 min_dist=361.4613995694038
+ step=135  deliver_item(?item=item_5) cost=129 feasible=True conflicts=368 min_dist=361.4613995694038
- step=147  deliver_item(?item=item_7) cost=97 feasible=True conflicts=159 min_dist=611.6249570888627
- step=147  deliver_item(?item=item_5) cost=132 feasible=True conflicts=159 min_dist=611.6249570888627
+ step=147  deliver_item(?item=item_7) cost=92 feasible=True conflicts=129 min_dist=611.6249570888627
+ step=147  deliver_item(?item=item_5) cost=128 feasible=True conflicts=129 min_dist=611.6249570888627
- step=195  deliver_item(?item=item_7) cost=48 feasible=True conflicts=0 min_dist=None
- step=195  deliver_item(?item=item_5) cost=112 feasible=True conflicts=0 min_dist=None
+ step=195  deliver_item(?item=item_7) cost=46 feasible=True conflicts=0 min_dist=None
+ step=195  deliver_item(?item=item_5) cost=107 feasible=True conflicts=0 min_dist=None
- step=203  deliver_item(?item=item_7) cost=40 feasible=True conflicts=798 min_dist=662.2356437586141
- step=203  deliver_item(?item=item_5) cost=120 feasible=True conflicts=1857 min_dist=59.49635359079646
+ step=203  deliver_item(?item=item_7) cost=38 feasible=True conflicts=767 min_dist=662.2356437586141
+ step=203  deliver_item(?item=item_5) cost=115 feasible=True conflicts=1773 min_dist=77.31347513556628
- step=223  deliver_item(?item=item_7) cost=20 feasible=True conflicts=0 min_dist=None
- step=223  deliver_item(?item=item_5) cost=140 feasible=True conflicts=0 min_dist=None
+ step=223  deliver_item(?item=item_7) cost=18 feasible=True conflicts=0 min_dist=None
+ step=223  deliver_item(?item=item_5) cost=135 feasible=True conflicts=0 min_dist=None
- step=245  deliver_item(?item=item_5) cost=132 feasible=True conflicts=0 min_dist=None
+ step=245  deliver_item(?item=item_5) cost=128 feasible=True conflicts=0 min_dist=None
- step=274  deliver_item(?item=item_5) cost=103 feasible=True conflicts=1152 min_dist=125.35068950315902
+ step=274  deliver_item(?item=item_5) cost=99 feasible=True conflicts=1122 min_dist=125.35068950315895
- step=311  deliver_item(?item=item_5) cost=65 feasible=True conflicts=408 min_dist=882.2022530315627
+ step=311  deliver_item(?item=item_5) cost=64 feasible=True conflicts=378 min_dist=882.5462707157735
```

