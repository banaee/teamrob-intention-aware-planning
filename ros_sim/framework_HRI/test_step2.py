# test_step2.py
from layout_adapter import ContinuousLayoutAdapter

adapter = ContinuousLayoutAdapter("/home/fatemeh/Github_human_robot_codes/Github/teamrob-intention-aware-planning/domains/kitting/env_layout1.json")  # adjust filename if different

print("shelf_0 position:", adapter.position_of("shelf_0"))
print("shelf_0 zone:    ", adapter.zone_of("shelf_0"))
print("kitting_table pos:", adapter.position_of("kitting_table"))

pos = adapter.position_of("shelf_0")
print("zone_of_pos check:", adapter.zone_of_pos(pos))
