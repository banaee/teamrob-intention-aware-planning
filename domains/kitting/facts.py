# domains/kitting/facts.py
"""
The facts kitting declares that are not physical (T-G A5; T-K part 1): its timeline facts, which hold only on the ticks
of a window of the timeline in force (the registry's "timeline_facts"; AM34, AM40), and its object states (the
registry's "states"). The objects here are the declarations themselves: a scenario's timeline names them by identity
(script.window), a setup's JSON by name, resolved at load against these objects.
"""

from shared.types import StateDeclaration

# Timeline facts (T-K part 1, AM13, AM37; facts about no object)
BREAK_TIME = StateDeclaration("break_time", None)   # the site's break time
ROOM_WARM = StateDeclaration("room_warm", None)     # the room is warm

# Object states (T-G A5)
AC_ON = StateDeclaration("ac_on", "ac_switch")      # the A/C switch is on; set by switch_on (T-K part 1, AM18, AM43)
