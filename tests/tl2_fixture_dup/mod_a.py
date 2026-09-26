# tests/tl2_fixture_dup/mod_a.py
from shared.types import ScenarioConfig

dup_first = ScenarioConfig(id="scenario_dup", description="first claimant",
                           agents=[], setup="env_setup_01",
                           reference_layouts=["env_layout0"])
