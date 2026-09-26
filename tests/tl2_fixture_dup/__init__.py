# tests/tl2_fixture_dup/__init__.py
"""
Fixture package for test_tl2_discovery: two modules that each bind a distinct
ScenarioConfig under the same id, so discover_scenarios must refuse it at
import (T-L stage 2, ruling 4). Not a domain; never imported by the run path.
"""
