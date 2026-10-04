# Context knowledge in the robot's belief: the method

Status: the design records hold the rulings and their reasons and are authoritative (`docs/design_decisions.md`, "T-K: context knowledge in the recognizer's belief"; `docs/design_records.md`, "T-K"). This document states the result of the rulings. If the two disagree, the records win and this document is corrected. A ruling that changes the method of context knowledge updates this document in the same records step.

It states the method as ruled by Hadi on 3 October 2026 (AM35 to AM39). Section 13 is a derivation from the method, not a ruling. It describes the concept, the formulas and worked examples. It does not describe the implementation. The values are modelling assumptions. Terms: `docs/glossary.md` §5.

## 1. The idea

Without context knowledge, the robot judges what the human is doing from movement alone. Before any movement, every live hypothesis is equally probable. A coffee break then starts with the same probability as a delivery.

Context knowledge is what the robot knows about the situation before the human moves. It changes only the robot's starting expectation, the prior. It never drives the human, and it removes no hypothesis.

The robot's belief at each tick is the prior multiplied by the evidence from movement.

## 2. The hypotheses

The belief ranges over modelled behaviour only:

- the assigned tasks (in kitting: the deliveries; in dock_loading: the scans);
- the foreseeable tasks (coffee break, A/C activation, office break).

Unmodelled behaviour, for example the exit walk, has no hypothesis and no share of the belief.

Notation at tick $t$:

- $H_t$: the set of live hypotheses.
- $A_t$: the live hypotheses of the assigned tasks. Together they are "the assigned tasks as a whole".
- $H_t^f$: the live hypotheses of foreseeable task $f$, one per object the task can use (one per coffee machine, for example).

Exception: with assignment knowledge off (an ablation), every work task of the task model takes the place of the assigned tasks.

## 3. The facts

$C_t$ is the set of crisp facts that hold at tick $t$. A fact holds or does not hold. There are three sources.

1. A timeline fact: a context fact on the setup's timeline of context facts, with an authored window, for example "break time" or "room warm".
   $c \in C_t \iff a_c \le t < b_c$
2. An object state, read from the world state, for example "the A/C is on".
3. A recency fact of task $f$: the robot's memory of observed completions holds an observed completion of $f$ within the recency duration.
   $\mathit{recent}_f \in C_t \iff 0 \le t - t_f^{\mathrm{obs}} < d_f$
   Here $t_f^{\mathrm{obs}}$ is the tick of the last observed completion of $f$, and $d_f$ is the declared recency duration.

The half-open window edges are a reading that the build's plan must confirm.

## 4. The strength of a foreseeable task: three levels

Each foreseeable task has a strength $s_f(t) > 0$. Two conditions select it. Each condition is one fact or a conjunction of facts. Each is optional.

- The suppressing condition $\sigma_f$: the task was just done, or is pointless now.
- The raising condition $\rho_f$: the situation calls for the task.

$$
s_f(t) = \begin{cases}
s^{\mathrm{sup}} & \text{if } C_t \models \sigma_f \\
s_f^{\mathrm{raised}} & \text{else if } C_t \models \rho_f \\
s^{\mathrm{ord}} & \text{otherwise}
\end{cases}
$$

The suppressing condition is tested first. The suppressed strength and the ordinary strength are declared once per domain and hold for every foreseeable task of the domain. The raised strength is declared per task, with the raising condition.

| task | suppressing condition | raising condition | raised strength | recency duration |
|---|---|---|---|---|
| coffee break | recent coffee break | break time | 2 | 90 ticks |
| A/C activation | the A/C is on | room warm | 0.5 | none |
| office break | recent office break | none | none | 135 ticks |

Suppressed strength: $s^{\mathrm{sup}} = 0.005$. Ordinary strength: $s^{\mathrm{ord}} = 0.02$.

## 5. Weights and probabilities

A weight is a number before normalisation. A probability is a weight divided by the sum of all weights.

- The assigned tasks as a whole have the weight 1 while at least one of them is live. The value 1 is a fixed reference, not a probability.
- Each foreseeable task $f$ with a live hypothesis has the weight $s_f(t)$.

So a strength is a ratio:

$$
s_f = \frac{\pi(\text{foreseeable task } f)}{\pi(\text{the assigned tasks as a whole})}
$$

Its proposed reading, not validated: at a moment when the human starts a new task, the odds that the task is $f$ and not an assigned task. With only $f$ and the assigned tasks live, the probability that the next task start is $f$ is

$$
p = \frac{s}{1 + s}
$$

| strength | $p$ | in words |
|---|---|---|
| 0.005 | 0.005 | 1 of 201 task starts |
| 0.02 | 0.02 | 1 of 51 |
| 0.5 | 0.33 | 1 of 3 |
| 1 | 0.5 | 1 of 2 |
| 2 | 0.67 | 2 of 3 |
| 3 | 0.75 | 3 of 4 |

Why a ratio and not a declared probability: the set of live hypotheses changes during a run. A declared probability would have to be declared again for every possible set. A ratio against a fixed reference stays valid for every set, and the normalisation gives the probabilities each time.

## 6. The prior

$$
Z_t = \mathbb{1}[A_t \neq \emptyset] + \sum_{f:\, H_t^f \neq \emptyset} s_f(t)
$$

$$
\pi_t(h) = \begin{cases}
\dfrac{1}{Z_t\,|A_t|} & h \in A_t \\[2ex]
\dfrac{s_f(t)}{Z_t\,|H_t^f|} & h \in H_t^f
\end{cases}
$$

The prior is a two-level distribution. First the weights divide the probability between the assigned tasks as a whole and each foreseeable task. Then each group's share is divided equally among its live hypotheses.

The prior sums to 1 over all live hypotheses:

$$
\sum_{h \in A_t} \frac{1}{Z_t\,|A_t|} + \sum_{f} \sum_{h \in H_t^f} \frac{s_f(t)}{Z_t\,|H_t^f|} = \frac{1 + \sum_f s_f(t)}{Z_t} = 1
$$

With context knowledge off, the prior is equal: $\pi_t(h) = 1 / |H_t|$.

## 7. The belief

$E_t(h)$ is the evidence: the movement likelihood accumulated in the present episode. It restarts equal over $H_t$ at an episode boundary. It contains no context.

$$
P_t(h) = \frac{\pi_t(h)\,E_t(h)}{\sum_{h' \in H_t} \pi_t(h')\,E_t(h')}
$$

Two properties:

- The prior is recomputed at every tick from $C_t$. It multiplies the evidence once. It is never folded into $E_t$, so a fact is not counted again at each tick.
- The factorisation rests on one assumption: given the task, the movement does not depend on the context, $p(o_{1:t} \mid h, C) = p(o_{1:t} \mid h)$.

The belief sums to 1 over the live hypotheses. There is no share for "none of the modelled tasks".

## 8. The gate (unchanged by context knowledge)

The meta-planner admits the leading hypothesis $h^*$ when three conditions hold:

1. $P_t(h^*) \ge \theta$, with $\theta = 0.75$.
2. It is adequate: the observed movement does not contradict it. A hypothesis turns inadequate after about 334 cm of excess path, or after 17 ticks of standing.
3. It is warranted.
   - An assigned task has commitment warrant, from the assignment. It can be admitted before any distinguishing movement.
   - A foreseeable task needs observation warrant. It has two sources. The first is the path-cost gain toward the target: the human's path cost to the task's target has decreased since the start of the present phase. One step that brings the human closer satisfies it. The second is the observed completion of the hypothesis's previous step, which entered the present phase. In a phase without a movement target (a wait), the second is the only source.

## 9. The procedure in four steps

1. For each foreseeable task, test the suppressing condition and then the raising condition on the facts that hold now. Select the strength.
2. Write the weights: 1 for the assigned tasks as a whole, the selected strength for each foreseeable task.
3. Add the weights. The sum is $Z$.
4. Divide each weight by $Z$. Divide each group's probability equally among its live hypotheses.

## 10. Worked examples of the prior

The room: one coffee machine, one A/C switch. The human is assigned three deliveries.

| state | live deliveries | coffee weight | A/C weight | $Z$ | each delivery | coffee | A/C |
|---|---|---|---|---|---|---|---|
| 1. Start, no fact holds | 3 | 0.02 | 0.02 | 1.04 | 0.321 | 0.019 | 0.019 |
| 2. Break time begins | 3 | 2 | 0.02 | 3.02 | 0.110 | 0.662 | 0.007 |
| 3. Coffee break observed complete, break time still holds | 3 | 0.005 | 0.02 | 1.025 | 0.325 | 0.005 | 0.020 |
| 4. Break time over, recency passed, one delivery done, room warm | 2 | 0.02 | 0.5 | 1.52 | 0.329 | 0.013 | 0.329 |
| 5. Human switched the A/C on, room still warm | 2 | 0.02 | 0.005 | 1.025 | 0.488 | 0.020 | 0.005 |
| 6. One delivery left | 1 | 0.02 | 0.005 | 1.025 | 0.976 | 0.020 | 0.005 |
| 7. No delivery left, A/C on | 0 | 0.02 | 0.005 | 0.025 | none | 0.8 | 0.2 |
| 8. Break time and room warm, A/C off | 3 | 2 | 0.5 | 3.5 | 0.095 | 0.571 | 0.143 |

How to read the rows:

- State 1: no condition is satisfied. Both foreseeable tasks are ordinary. $Z = 1 + 0.02 + 0.02$.
- State 2: "break time" holds and "recent" does not. The coffee break is raised to 2. Coffee: $2 / 3.02 = 0.662$. Each delivery: $1 / (3 \times 3.02) = 0.110$.
- State 3: "recent" holds for 90 ticks after the observed completion. The suppressing condition is tested first, so the coffee break is suppressed even though break time holds. If break time still holds after the 90 ticks, state 2 returns.
- State 4: "room warm" holds and the A/C is off. The A/C activation is raised to 0.5. It is then as probable as one of the two deliveries.
- State 5: the A/C is on. The suppressing condition is satisfied, so the room being warm no longer raises the task.
- State 6: the group's weight is still 1, with one member. That delivery takes the whole share, $1 / 1.025$.
- State 7: no assigned task is live, so the group contributes 0. The two foreseeable tasks share the whole prior in the ratio of their weights, 4 to 1.
- State 8: both raising conditions are satisfied. The weights are 1, 2 and 0.5.

In every row the probabilities sum to 1.

## 11. From the prior to the belief

Take state 2. The human walks toward the shelf of delivery 1. The evidence values are invented for the illustration.

| hypothesis | prior | evidence | prior × evidence | belief |
|---|---|---|---|---|
| delivery 1 | 0.110 | 0.90 | 0.0993 | 0.825 |
| delivery 2 | 0.110 | 0.04 | 0.0044 | 0.037 |
| delivery 3 | 0.110 | 0.03 | 0.0033 | 0.028 |
| coffee break | 0.662 | 0.02 | 0.0132 | 0.110 |
| A/C activation | 0.007 | 0.01 | 0.0001 | 0.001 |
| sum | 1 | 1 | 0.1204 | 1 |

The belief is each product divided by the sum of the products. The prior favoured the coffee break at 0.662. The movement gives delivery 1 a belief of 0.825, which is above the threshold.

In state 1 the same evidence gives delivery 1 a belief of 0.926. The difference between 0.926 and 0.825 is the cost of break time on a human who keeps working.

How much evidence a lone delivery needs in break time, against the coffee break alone, to reach the threshold:

| raised strength of the coffee break | delivery's prior | evidence odds needed for the delivery |
|---|---|---|
| 1 | 0.50 | 3 to 1 |
| 2 | 0.33 | 6 to 1 |
| 3 | 0.25 | 9 to 1 |

## 12. The state with no assigned task live

In state 7 the two foreseeable tasks take the whole prior, because the prior must sum to 1 and no hypothesis exists for unmodelled behaviour. In reality the most probable behaviour then is unmodelled: the human leaves or stands.

What the gate does in that state, in three cases:

1. The human stands. The path cost to the coffee machine does not decrease, so there is no warrant. The gate refuses.
2. The human walks away from the coffee machine. No decrease, no warrant. The gate refuses.
3. The human walks somewhere unmodelled, and the walk happens to bring the human closer to the coffee machine. Warrant holds after one step. Adequacy holds until the excess path reaches about 334 cm. The gate admits the coffee break. A retraction follows later.

Case 3 exists without context knowledge too. Its cause is that an unmodelled walk has no hypothesis. The strengths are not its cause.

What the prior adds: when the two foreseeable tasks are at different levels, the threshold no longer separates them by movement alone.

- Equal prior: the coffee break needs an evidence share of 0.75 against the A/C activation.
- Prior 0.8 against 0.2 (state 7): it needs an evidence share of 0.43.
- Example: the evidence is 0.55 for the A/C activation and 0.45 for the coffee break. The belief in the coffee break is $0.36 / 0.47 = 0.77$.

In state 7 the difference between the two tasks rests on knowledge: the A/C is already on, so its activation is suppressed. When both foreseeable tasks are ordinary, the prior is 0.5 and 0.5, the same as without context knowledge.

This state is no argument for or against any strength value. It stays a recorded consequence.

## 13. Context knowledge off: the equivalent strength

With context knowledge off, every live hypothesis has the prior $1 / |H_t|$. Let $n$ be the number of live assigned tasks and $m_f$ the number of live hypotheses of foreseeable task $f$.

$$
s_f^{\text{equiv}} = \frac{m_f / |H_t|}{n / |H_t|} = \frac{m_f}{n}
$$

With one coffee machine and no other foreseeable task:

| live assigned tasks | equivalent strength | coffee break's prior, off | on, ordinary | on, break time |
|---|---|---|---|---|
| 4 | 0.25 | 0.20 | 0.02 | 0.67 |
| 3 | 0.33 | 0.25 | 0.02 | 0.67 |
| 2 | 0.5 | 0.33 | 0.02 | 0.67 |
| 1 | 1 | 0.50 | 0.02 | 0.67 |

- The equal prior treats the foreseeable task as one more task of the same kind as each assigned task. Its equivalent strength rises as the human completes the assignment, with no knowledge behind the rise.
- It also rises with the number of objects: two coffee machines give twice the equivalent strength.
- Context knowledge replaces this by a strength that depends only on the situation.

## 14. The revision of the strengths and its reasons

The design before the revision: each foreseeable task had one condition, one low strength and one high strength.

| task | condition | low | high |
|---|---|---|---|
| coffee break | break time and not recent | 0.02 | 3 |
| A/C activation | room warm and A/C not on | 0.005 | 0.2 |
| office break | not recent | 0.005 | 0.02 |

The principle behind the revision: a number must not decide between two hypotheses that the robot has no knowledge to tell apart. A value changes because of an argument about what it states about the human. No run of a scenario and no comparison with the threshold changes a value.

What was found:

1. One low and one high value cannot state three situations. A coffee break just completed, outside break time, kept 0.02. The office break in the same situation fell to 0.005.
2. The knowledge that exists is a classification of the situation: suppressed, ordinary, raised. Differences between tasks at the same level rested on no stated knowledge.
3. The value 3 for the coffee break in break time asserts that 3 of 4 task starts are the coffee break. Held over a whole period, it asserts that the human almost never starts an assigned task in break time. It also puts much weight on the coffee break before the human takes a single step toward the machine.
4. The value 0.2 for the A/C activation in a warm room asserts that the human lets 6 task starts pass on average before the activation.

What was ruled:

- Three levels per foreseeable task, with a suppressing condition and a raising condition (section 4). The conditions need no "not".
- The coffee break's raised strength is 2. Source: break time favours the coffee break. It is more probable than an assigned task, and not as strongly as 3 stated. The value 1 was not taken, because it asserts no direction.
- The A/C activation's raised strength is 0.5. Source: a warm room is a matter of comfort with no stated time, so the human more often starts an assigned task first, and the activation follows within about 3 task starts.
- The two raised strengths lie on opposite sides of 1. Break time is a scheduled norm of the site. A warm room is a weaker call.
- A room that is not warm, with the A/C off, gives the A/C activation the ordinary strength 0.02. Nothing states that the task is pointless there.
- A coffee break just completed is suppressed in every situation, inside break time too.
- The group's name is "the assigned tasks as a whole".

Alternatives not taken: keeping the six values and only fixing their meaning; a coarse declared scale (0.01, 0.1, 1, 10); one raised strength shared by all tasks.

## 15. Known consequences and open questions

Consequences to measure, not reasons to adjust the design:

- A human who works through break time: the robot expects a break and recognises the assigned task later (section 11).
- One assigned task left, no raising fact: its prior is about 0.98. The gate can admit it early on its assignment. If the human then takes a foreseeable task, a retraction follows.
- A crisp fact that changes in the middle of an episode changes the prior at once, with no new movement.

Open questions:

- Which value the gate compares with the threshold: the belief over the live hypotheses, or the output after its scaling by the pinned hypotheses. It is to be argued from what each value means.
- Unmodelled behaviour has no hypothesis and no share of the belief (section 12).
- The later extension from crisp facts to degrees was stated for the pair of low and high strength. It must be restated for two conditions.
- The reading of a strength as a ratio of task starts is proposed and not validated. No strength is measured at a real site.
