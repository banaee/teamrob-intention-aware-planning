# Terminology revision: human behaviour, model coverage and the robot's inference

Companion to `docs/glossary.md` §7. It explains, and the glossary decides: where the two differ, the glossary is
right and this file is to be corrected. Ruled by Hadi on 24 September 2026; recorded in `docs/design_decisions.md`,
"Terms for human behaviour, model coverage and the robot's inference".

Why the terms exist. "Unknown" named two things:
- (a) a property of what the human does in the world: the behaviour is outside the robot's models;
- (b) the robot's belief: the mass on the residual hypothesis `unknown`.

The two diverge. A standing human is unmodelled but produces no evidence, so (a) holds and (b) does not move. A
finished work order leaves `unknown` near 0.995 while nothing unmodelled occurs, so (b) is high without (a). The
next design decision, whether `unknown` stays in the Bayesian hypothesis space, has to be stated in terms that
keep them apart. This file fixes those terms. It does not prejudge that decision (section 6).

Numbers below are illustrations from the T-C play (`analysis/tc2c_scripts/`, code at feabe3d, prior on). They
show what the terms separate. They are not a reference for any design argument.

---

## 1. The two groups

Two groups, WORLD and ROBOT. A term from one group is never used for the other.

```
WORLD   ground truth about the observed human's behaviour
        computable from the scenario's script and the robot's hypothesis space
        never received by the robot's mind

ROBOT   what the robot's mind holds and decides
        computed from observations only
```

### 1.1 WORLD: three independent labels

```
WORLD
|
+-- label A: work order          (a behaviour compared with the human's assigned tasks)
|     |
|     +-- assigned task
|     +-- deviation              (any departure from the work order)
|            ^        ^        ^
|            |        |        |
|        produces  produces  produces        the script edits are OPERATIONS,
|            |        |        |             not kinds of deviation
|       interrupt   deviate   abandon        (free Stay / MoveTo(landmark) content
|                                             departs from the work order too)
|
+-- label B: model coverage      (a behaviour compared with the robot's hypothesis space)
|     |
|     +-- modelled behaviour     (a HypothesisKey describes it)
|     +-- unmodelled behaviour   (no HypothesisKey describes it)
|
+-- label C: experimental intent (a property of the SCENARIO, not of one behaviour)
      |
      +-- declared experimental condition   (written in the scenario's description,
                                             e.g. "unmodelled-behaviour condition")
```

Every behaviour has one value on label A and one on label B. The two are independent. The foreseeable task is
where a deviation meets a model: a task in the hypothesis space that is not assigned. It is a combination of the
two labels, not a third value of label A.

```
                        label B: modelled                 label B: unmodelled
                    +---------------------------------+---------------------------------+
 label A: assigned  | an assigned delivery            | (none in kitting: every         |
 task               |                                 |  assigned task has a hypothesis)|
                    +---------------------------------+---------------------------------+
 label A: deviation | FORESEEABLE TASK                | wrong-table delivery            |
                    | (a coffee_break interrupt       | walk to corner_NE               |
                    |  declared foreseeable)          | a stand of 5 minutes            |
                    +---------------------------------+---------------------------------+
```

Coverage is judged at the hypothesis level: not at the schema level, and not by provenance.

```
                          provenance        schema in the domain   a HypothesisKey describes it   label B
coffee_break interrupt    coffee_break      yes                    yes                             modelled
wrong-table delivery      deliver_item      yes                    no (the hypothesis carries      unmodelled
(TODO-87)                                                           the designated table)
```

"Model coverage" is unrelated to the covered fraction f of graded evidence (`covered_fraction`, the share of one
hypothesis's expected path a stretch has closed). f lives inside the robot's evidence; coverage is a world label.

"Scripted" is not a behaviour class: in the simulator every behaviour is scripted. The word only contrasts
simulation with a real deployment.

### 1.2 ROBOT

```
ROBOT
|
+-- recognizer: belief           a distribution; gates nothing
|     |
|     +-- task hypotheses        one per HypothesisKey in the live set
|     +-- `unknown`              the residual hypothesis: the behaviour is none of them
|
+-- recognizer: finding
|     |
|     +-- unexplained            evidence that no live task hypothesis explains the observations
|
+-- meta-planner: gate outcome   theta, asked in _clears_gate() only
      |
      +-- admitted               a task hypothesis cleared theta; its projection is built
                                 (`unknown` above theta is never admitted: none(unknown))
```

The recognizer has no separate output for "unexplained" today. How the finding is represented is part of the
pending decision on `unknown` (section 6). The term fixes what it means, not how it is computed.

### 1.3 The usage rule

```
you are writing about ...            write ...
the implementation                   "the `unknown` hypothesis"
the human's behaviour                "unmodelled behaviour"
the robot's inference result         "unexplained"
```

Not written: "unknown behaviour", "an unknown task", "`unknown` as unmodelled behaviour".

---

## 2. The cases

Label A and label B are the world. The belief column is what the current recognizer does, from the play or the
fixtures named. The finding column applies the definition of "unexplained" to that behaviour of the belief.

| case | label A | label B | belief (current recognizer) | finding |
|---|---|---|---|---|
| an assigned delivery (`deliver(item_3)`) | assigned task | modelled | its hypothesis rises along the walk and clears θ at about half of it; admitted | nothing unexplained |
| a `coffee_break` interrupt declared foreseeable (`interrupt(..., with_=[coffee_break])`) | deviation, produced by `interrupt` | modelled (a foreseeable task) | `coffee_break` rises on the walk to the machine (scenario_11: 0.345), unless an earlier misleading walk refuted it (scenario_41: `coffee_break` ≤ 0.001, `unknown` 0.453; TODO-94) | nothing unexplained in scenario_11; unexplained in scenario_41, although the behaviour is modelled |
| a wrong-table delivery (`deviate(deliver(item_0), destination=kitting_table_1)`, TODO-87) | deviation, produced by `deviate` | unmodelled | the item's delivery leads while the carry still fits it; `unknown` leads once the carry wastes path; no pin, no boundary at the place; after the next boundary the item's delivery leads again (scenario_85, section 3.3) | unexplained only in the middle stretch; not before, not after |
| a walk to corner_NE (`MoveTo("corner_NE")`) | deviation (free primitive) | unmodelled (a landmark: no hypothesis binds one) | `unknown` rises with walked excess path and leads (0.99 in the play's long detours); a walk that stays in line with a live hypothesis does not raise it (scenario_04's walk to the door: the one live hypothesis at 0.58 to 0.61) | unexplained (when the walk wastes path against every live hypothesis) |
| a human standing for 5 minutes (`Stay(n)`) | deviation (a stay the work order does not contain) | unmodelled (no hypothesis describes standing) | frozen where the last walk left it: mid-carry, the carried item's delivery on top (TODO-85); after a boundary, the uniform prior; `unknown` does not rise (I4c) | nothing unexplained: a stand is no evidence |
| a finished work order, idle human | none (the work order is complete; see the note) | no unmodelled behaviour (as ruled; see the note) | `unknown` 0.995 by normalisation: no task hypothesis is left live (scenario_01, prior on); not admitted, `none(unknown)` | nothing unexplained |

NOTE on the last row. It is labelled as ruled: the point of the row is that `unknown` is high with nothing
unmodelled to cause it. Two things are open and are for Hadi: label A has no value for it (nothing is departed
from, and no task is performed), and by the hypothesis-level criterion an idle human who stands has no
`HypothesisKey` describing the stand either, which is the 5-minute row's label B. The row assumes that idleness
after a finished work order is not labelled as behaviour.

The coffee row shows a fourth pattern besides the three of section 3: modelled behaviour that the robot's evidence
does not explain. Unexplained and unmodelled disagree in both directions.

---

## 3. Divergence diagrams

Time runs left to right. "B" is label B (the world), `unknown` is the belief's residual mass, "finding" is the
recognizer's finding.

### 3.1 Standing: unmodelled / nothing unexplained yet

```
the human    walks to shelf, picks up   |  stands still, 5 minutes ....................... |  walks on
B            modelled (the delivery)    |  unmodelled ..................................... |
belief       delivery rising, on top    |  unchanged (no stretch, no observation, I4c)       |
`unknown`    low                        |  low, unchanged                                    |
finding      nothing unexplained        |  nothing unexplained yet (no evidence arrives)     |
```

The world has changed and the robot has received nothing that says so. After an episode boundary the same stand
leaves the belief at the uniform prior (0.498 each over one task and `unknown`), below θ, again with nothing
unexplained.

### 3.2 A walk to corner_NE: unmodelled / high `unknown` / unexplained

```
the human    at the table               |  walks to corner_NE ............................ |  at the corner
B            ...                        |  unmodelled ...................................... |
belief       prior over the live set    |  every live hypothesis's excess path grows         |
`unknown`    1/|Live|                   |  rises, leads (0.99 in the long detours)           |
finding      nothing unexplained        |  unexplained                                       |
```

The case where the two terms agree: unmodelled behaviour, and evidence that no live task hypothesis explains it.

### 3.3 A wrong-table delivery: unmodelled / high belief in a task hypothesis / not unexplained

scenario_85 (`deviate(deliver(item_0), destination=kitting_table_1)`, then `deliver(item_3)`), current recognizer:

```
tick         17 -------- 49 | 50 -------------------- 157 | 158   159 ----------------- 200 ...
the human    carries item_0 toward kitting_table_1        | places item_3, then stands at kitting_table_1
             (placed on the wrong table at 103)           |
B            unmodelled (the wrong-table delivery) .......| the stand: unmodelled
belief       deliver_item(item_0) leads | `unknown` leads | item_3 pinned, boundary; deliver_item(item_0)
             (gate cleared at 8)        |                 | leads again (0.905 at 200): item_0 lies on the
                                        |                 | wrong table, so its delivery is still open
finding      not unexplained            | unexplained     | not unexplained
```

At 17 to 49 and from 159 on the belief is high on a task hypothesis while the behaviour is unmodelled: the robot
is confidently wrong, and "unexplained" does not fire. From 159 the meta-planner admits it and projects a human
carrying item_0 back, while the human stands (TODO-87).

### 3.4 A finished work order: no unmodelled behaviour / `unknown` high by normalisation / nothing unexplained

scenario_01, prior on:

```
the human    last assigned delivery      | release: pinned, episode boundary | idle
B            modelled                    |                                   | (no unmodelled behaviour, as ruled)
live set     {that task, `unknown`}      | {`unknown`} (the rest pinned)     |
`unknown`    0.498 at the prior, falls   | 0.995                             | 0.995
finding      nothing unexplained         | nothing unexplained               | nothing unexplained
```

`unknown` is high because nothing else is live, not because of evidence: the mass follows from normalisation.

---

## 4. The label-C check

```
scenario description  ------------------------------->  declared experimental condition   (label C)
                                                                  |
script + robot's hypothesis space  -->  label B per behaviour ----+
                                                                  |
                                                                  v
                                   an unmodelled behaviour the declared condition does not cover
                                   ==> the run contains UNINTENDED unmodelled behaviour
```

Example: a script that ends with the human standing at a table. The terminal stand is unmodelled. If the scenario
does not declare the blocked case (TODO-80), the stand is unintended, and the run's results carry it. The authoring
convention (glossary §6, **deviation vocabulary**) exists to avoid exactly this.

The check reads the script and the hypothesis space only. Computing the labels is not built; it is recorded under
TODO-92, since the evaluation will need it.

---

## 5. What the terms do not change

- No identifier, constant, log tag or log text: the constant `UNKNOWN`, `UNKNOWN_LIKELIHOOD`,
  `none(unknown)`, `none(unresolved)`, `[IR]` lines and the class `Deviation` keep their names.
- No behaviour: the recognizer, the gate and the planner are unchanged.
- The robot's mind: it receives none of the WORLD labels.

---

## 6. Terms deliberately not introduced

| word | why not now |
|---|---|
| unresolved | a candidate name for a belief that points at no task hypothesis; which states the belief distinguishes is the pending decision on `unknown`. (`none(unresolved)` is existing log text with a different meaning: the projector could not resolve the admitted hypothesis's task.) |
| recognised | would name a recognizer outcome; it would also suggest that the recognizer performs the θ gate, which contradicts the architecture: the gate is the meta-planner's, and its outcome is "admitted" |
| exhausted | a candidate name for a live set with no task hypothesis left (the finished work order); whether that state is represented apart from `unknown` is the pending decision |

All three wait for the architecture decision on whether `unknown` stays in the Bayesian hypothesis space. Where
older records use them as ordinary words, they are not terms.
