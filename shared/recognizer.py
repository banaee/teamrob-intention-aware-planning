"""
shared/recognizer.py

PURPOSE:
    The robot's "Human intention inference" module (see robot agent architecture, HCM paper).
    Maintains and updates a belief distribution over human task intentions.
    Answers: "Given what I have observed, what is the human most likely trying to do?"

WHAT THIS MODULE DOES:
    - Receives one Observation at a time from the simulator
    - Updates a probability distribution P(τ | observations) over all known intentions T
    - Returns a BeliefState after each update

WHAT THIS MODULE DOES NOT DO:
    - Does NOT decide what the robot should do (that is planner.py)
    - Does NOT build Observations (that is mesa_sim/obs_builder.py or ROS equivalent)
    - Does NOT know about Mesa, ROS, or any simulator internals
    - Does NOT resolve task parameters or placeholders

INPUTS:
    - Observation         from mesa_sim/obs_builder.py (or ROS equivalent)
    - KnowledgeBase       injected once at construction (shared/domain_knowledge.py)
    - prev_belief         its own previous output, passed back by the robot agent

OUTPUTS:
    - BeliefState         consumed by shared/replanning.py and shared/planner.py

ALGORITHM (skeleton):
    Currently returns a uniform distribution over all known intentions.
    TODO: Replace with Bayesian update: P(τ|μ_t) ∝ P(μ_t|τ) · P(τ) · ω_context(τ)
"""

from shared.types import Observation, BeliefState
from shared.domain_knowledge import DomainKnowledgeBase 


class IntentionRecognizer:

    def __init__(self, knowledge: DomainKnowledgeBase):
        """
        knowledge: provides the intention set T used to initialize distributions.
        """
        self.knowledge = knowledge
        self._intentions = knowledge.get_all_intentions()
        self._history = []  # store past observations if needed for future updates
        

    def update(self, obs: Observation, prev_belief: BeliefState | None = None) -> BeliefState:
        """
        Update belief over human intentions given a new observation.

        INPUT:
            obs         - latest Observation from the simulator
            prev_belief - previous BeliefState (None = start from uniform prior)

        OUTPUT:
            new BeliefState at obs.timestamp

        SKELETON BEHAVIOUR:
            Returns uniform distribution over all intentions.
            TODO: Real Bayesian update in Phase 4.
        """
        n = len(self._intentions)
        uniform_prob = 1.0 / n if n > 0 else 0.0

        distribution = {intention: uniform_prob for intention in self._intentions}
        most_likely = self._intentions[0] if self._intentions else "unknown"

        # dummy predicted next action — replaced by real prediction in Phase 4
        # predicted = self.knowledge.get_task_actions(most_likely)
        # predicted_next = {most_likely: predicted} if predicted else {}

        # TODO Phase 4: predict next actions from TaskSchema decomposition
        predicted_next = {}

        self._history.append(obs)  

        return BeliefState(
            timestamp=obs.timestamp,
            agent_id=obs.agent_id,
            distribution=distribution,
            most_likely=most_likely,
            confidence=uniform_prob,
            predicted_next_actions=predicted_next,
        )