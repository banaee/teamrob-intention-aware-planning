# tests/tl2_fixture_dup/mod_b.py
from shared.types import ScenarioConfig

dup_second = ScenarioConfig(id="scenario_dup", description="second claimant",
                            agents=[], setup="env_setup_01",
                            reference_layouts=["env_layout_01"])
