#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import numpy as np
import json

from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker, MarkerArray

# ============================================================
# COMMENTED OUT — planner and task planner not yet connected
# Will be replaced by colleague's framework modules
# ------------------------------------------------------------
# from local_planner_priest_interrupt import PRIESTLocalPlanner
# from task_planner_interrupt import TaskPlanner
# ============================================================

LAYOUT_PATH = "/home/fatemeh/Github_human_robot_codes/Github/teamrob-intention-aware-planning/domains/dock_loading/env_layout1.json"
CM      = 0.01    # centimetres → metres
MESH_PKG = "planner"

# Zone colors (r, g, b, alpha)
ZONE_COLORS = {
    "zone_hall_dry":    (0.2, 0.6, 1.0, 0.15),   # blue
    "zone_hall_frozen": (0.4, 0.9, 1.0, 0.15),   # cyan
    "zone_hall_center": (0.6, 0.9, 0.3, 0.15),   # light green
    "zone_dock":        (0.9, 0.7, 0.1, 0.15),   # amber
    "zone_truck":       (0.7, 0.4, 0.1, 0.15),   # brown
    "zone_office":      (0.8, 0.5, 0.9, 0.15),   # purple
}

# Pallet color by good_type
PALLET_COLORS = {
    "dry":    (0.9, 0.7, 0.2, 0.9),   # yellow — dry goods
    "frozen": (0.2, 0.7, 1.0, 0.9),   # blue   — frozen goods
    None:     (0.6, 0.6, 0.6, 0.6),   # grey   — empty pallet
}


# =============================================================================
# Layout loader
# =============================================================================

def load_layout(path: str) -> dict:
    with open(path, "r") as f:
        raw = json.load(f)

    layout = {}

    # ------------------------------------------------------------------
    # Robot
    # ------------------------------------------------------------------
    r = raw["robots"][0]
    layout["robot"] = {
        "id": r["id"],
        "x":  r["initial_x"] * CM,
        "y":  r["initial_y"] * CM,
        "orientation_deg": r.get("orientation_deg", 0),
    }

    # ------------------------------------------------------------------
    # Human
    # ------------------------------------------------------------------
    h = raw["humans"][0]
    layout["human"] = {
        "id": h["id"],
        "x":  h["initial_x"] * CM,
        "y":  h["initial_y"] * CM,
        "orientation_deg": h.get("orientation_deg", 0),
    }

    # ------------------------------------------------------------------
    # Zones
    # ------------------------------------------------------------------
    layout["zones"] = [
        {
            "id":    z["id"],
            "label": z["label"],
            "x_min": z["bounds"]["x_min"] * CM,
            "x_max": z["bounds"]["x_max"] * CM,
            "y_min": z["bounds"]["y_min"] * CM,
            "y_max": z["bounds"]["y_max"] * CM,
        }
        for z in raw.get("zones", [])
    ]

    # ------------------------------------------------------------------
    # env_objects — split by type
    # ------------------------------------------------------------------
    env_objects = raw.get("env_objects", [])
    obj_by_id   = {o["id"]: o for o in env_objects}

    # Truck
    truck_list = [o for o in env_objects if o["type"] == "truck"]
    layout["trucks"] = [
        {
            "id": o["id"],
            "x":  o["position"][0] * CM,
            "y":  o["position"][1] * CM,
            "sx": o["size"][0] * CM,
            "sy": o["size"][1] * CM,
        }
        for o in truck_list
    ]

    # Delivery areas
    layout["delivery_areas"] = [
        {
            "id": o["id"],
            "x":  o["position"][0] * CM,
            "y":  o["position"][1] * CM,
            "sx": o["size"][0] * CM,
            "sy": o["size"][1] * CM,
            "zone": o.get("zone", ""),
        }
        for o in env_objects if o["type"] == "delivery_area"
    ]

    # Empty bays
    layout["empty_bays"] = [
        {
            "id": o["id"],
            "x":  o["position"][0] * CM,
            "y":  o["position"][1] * CM,
            "sx": o["size"][0] * CM,
            "sy": o["size"][1] * CM,
            "zone": o.get("zone", ""),
        }
        for o in env_objects if o["type"] == "empty_bay"
    ]

    # Gate
    layout["gates"] = [
        {
            "id": o["id"],
            "x":  o["position"][0] * CM,
            "y":  o["position"][1] * CM,
            "sx": o["size"][0] * CM,
            "sy": o["size"][1] * CM,
        }
        for o in env_objects if o["type"] == "gate"
    ]

    # Coffee machine
    cm_list = [o for o in env_objects if o["type"] == "coffee_machine"]
    layout["coffee_machine"] = {
        "x": cm_list[0]["position"][0] * CM,
        "y": cm_list[0]["position"][1] * CM,
    } if cm_list else None

    # ------------------------------------------------------------------
    # Items (pallets) — spread out within their container
    # Multiple pallets in same container get offset so they don't overlap
    # ------------------------------------------------------------------
    container_map = {}   # container_id → list of items
    for item in raw.get("items", []):
        cid = item["initial_container"]
        container_map.setdefault(cid, []).append(item)

    layout["items"] = []
    for cid, items in container_map.items():
        # Find container position from env_objects
        container = obj_by_id.get(cid)
        if container is None:
            # Container might be a zone — use zone centre
            zone = next((z for z in layout["zones"] if z["id"] == cid), None)
            if zone:
                cx = (zone["x_min"] + zone["x_max"]) / 2.0
                cy = (zone["y_min"] + zone["y_max"]) / 2.0
            else:
                cx, cy = 0.0, 0.0
            container_sx = 1.0
            container_sy = 1.0
        else:
            cx = container["position"][0] * CM
            cy = container["position"][1] * CM
            container_sx = container["size"][0] * CM
            container_sy = container["size"][1] * CM

        # Spread items in a grid within the container
        n      = len(items)
        cols   = max(1, int(np.ceil(np.sqrt(n))))
        rows   = max(1, int(np.ceil(n / cols)))
        item_w = (container["size"][0] * CM) / cols if container else 0.5
        item_h = (container["size"][1] * CM) / rows if container else 0.5

        for idx, item in enumerate(items):
            col = idx % cols
            row = idx // cols
            # offset from container centre
            ox = (col - (cols - 1) / 2.0) * item_w
            oy = (row - (rows - 1) / 2.0) * item_h

            layout["items"].append({
                "id":         item["id"],
                "type":       item["type"],
                "good_type":  item.get("good_type"),
                "is_empty":   item.get("is_empty", False),
                "is_scanned": item.get("is_scanned", False),
                "container":  cid,
                "x":          cx + ox,
                "y":          cy + oy,
                "sx":         item["size"][0] * CM,
                "sy":         item["size"][1] * CM,
            })

    return layout


# =============================================================================
# ROS2 Node
# =============================================================================

class DockVisualizer(Node):

    def __init__(self):
        super().__init__("dock_visualizer")

        self.layout = load_layout(LAYOUT_PATH)
        self.get_logger().info(
            f"Loaded dock layout: "
            f"{len(self.layout['zones'])} zones, "
            f"{len(self.layout['items'])} pallets"
        )

        # Publishers
        self.zone_pub         = self.create_publisher(MarkerArray, "/zones",            100)
        self.pose_pub         = self.create_publisher(PoseStamped, "/robot_pose",       100)
        self.robot_marker_pub = self.create_publisher(Marker,      "/robot_marker",     100)
        self.hum_pub          = self.create_publisher(MarkerArray, "/humans",           100)
        self.env_pub          = self.create_publisher(MarkerArray, "/env_objects",      100)
        self.pallet_pub       = self.create_publisher(MarkerArray, "/pallets",          100)
        self.coffee_pub       = self.create_publisher(Marker,      "/coffee_marker",      1)
        self.task_label_pub   = self.create_publisher(Marker,      "/task_label",       100)

        # --------------------------------------------------------
        # COMMENTED OUT — planner setup
        # --------------------------------------------------------
        # self.local_planner = PRIESTLocalPlanner(config)
        # self.task_planner  = TaskPlanner(tasks=[...])
        # --------------------------------------------------------

        self.create_timer(1.0, self._publish_environment)
        self.get_logger().info("DockVisualizer ready — publishing to RViz")

    # =========================================================================
    # Timer callback
    # =========================================================================

    def _publish_environment(self):
        self.publish_zones()
        self.publish_robot()
        self.publish_human()
        self.publish_env_objects()
        self.publish_pallets()
        if self.layout["coffee_machine"]:
            self.publish_coffee_machine()
        self.publish_task_label("Dock unloading domain — planner not yet connected")

    # =========================================================================
    # Zones — transparent colored floor panels
    # =========================================================================

    def publish_zones(self):
        arr = MarkerArray()
        for i, zone in enumerate(self.layout["zones"]):
            cx = (zone["x_min"] + zone["x_max"]) / 2.0
            cy = (zone["y_min"] + zone["y_max"]) / 2.0
            sx = abs(zone["x_max"] - zone["x_min"])
            sy = abs(zone["y_max"] - zone["y_min"])
            r, g, b, a = ZONE_COLORS.get(zone["id"], (0.5, 0.5, 0.5, 0.15))

            # Floor panel
            m = Marker()
            m.header.frame_id = "map"
            m.header.stamp = self.get_clock().now().to_msg()
            m.ns = "zones"
            m.id = i
            m.type = Marker.CUBE
            m.action = Marker.ADD
            m.pose.position.x = float(cx)
            m.pose.position.y = float(cy)
            m.pose.position.z = -0.05
            m.pose.orientation.w = 1.0
            m.scale.x = float(sx)
            m.scale.y = float(sy)
            m.scale.z = 0.01
            m.color.r = r
            m.color.g = g
            m.color.b = b
            m.color.a = a
            arr.markers.append(m)

            # Zone label
            t = Marker()
            t.header.frame_id = "map"
            t.header.stamp = m.header.stamp
            t.ns = "zone_labels"
            t.id = 100 + i
            t.type = Marker.TEXT_VIEW_FACING
            t.action = Marker.ADD
            t.pose.position.x = float(zone["x_min"] + 0.2)
            t.pose.position.y = float(zone["y_max"] - 0.2)
            t.pose.position.z = 0.3
            t.scale.z = 0.3
            t.color.r = r
            t.color.g = g
            t.color.b = b
            t.color.a = 1.0
            t.text = zone["label"]
            arr.markers.append(t)

        self.zone_pub.publish(arr)

    # =========================================================================
    # Robot
    # =========================================================================

    def publish_robot(self):
        x   = self.layout["robot"]["x"]
        y   = self.layout["robot"]["y"]
        deg = self.layout["robot"]["orientation_deg"]
        half_rad = np.radians(deg) / 2

        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.type = Marker.MESH_RESOURCE
        m.mesh_resource = f"package://{MESH_PKG}/meshes/hokuyo.dae"
        m.mesh_use_embedded_materials = True
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.position.z = 0.0
        m.pose.orientation.z = float(np.sin(half_rad))
        m.pose.orientation.w = float(np.cos(half_rad))
        m.scale.x = 7.0
        m.scale.y = 7.0
        m.scale.z = 3.0
        m.color.a = 1.0
        m.id = 0
        m.ns = "robot"
        self.robot_marker_pub.publish(m)

        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = m.header.stamp
        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.orientation.w = 1.0
        self.pose_pub.publish(pose)

    # =========================================================================
    # Human
    # =========================================================================

    def publish_human(self):
        x   = self.layout["human"]["x"]
        y   = self.layout["human"]["y"]
        deg = self.layout["human"]["orientation_deg"]
        half_rad = np.radians(deg) / 2

        arr = MarkerArray()
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.type = Marker.MESH_RESOURCE
        m.mesh_resource = f"package://{MESH_PKG}/meshes/walk.dae"
        m.mesh_use_embedded_materials = True
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.orientation.z = float(np.sin(half_rad))
        m.pose.orientation.w = float(np.cos(half_rad))
        m.scale.x = 0.8
        m.scale.y = 0.8
        m.scale.z = 1.2
        m.color.r = 0.0
        m.color.g = 0.2
        m.color.b = 1.0
        m.color.a = 1.0
        m.ns = "humans"
        m.id = 0
        arr.markers.append(m)
        self.hum_pub.publish(arr)

    # =========================================================================
    # Environment objects — truck, gate, delivery areas, empty bays
    # All rendered as cubes for now
    # =========================================================================

    def publish_env_objects(self):
        arr = MarkerArray()
        marker_id = 0

        # Truck — dark grey box
        for truck in self.layout["trucks"]:
            m = self._cube_marker(
                ns="truck", mid=marker_id,
                x=truck["x"], y=truck["y"], z=0.5,
                sx=truck["sx"], sy=truck["sy"], sz=1.0,
                r=0.3, g=0.3, b=0.3, a=0.3,
            )
            arr.markers.append(m)
            arr.markers.append(self._text_marker(
                ns="truck_label", mid=1000 + marker_id,
                x=truck["x"], y=truck["y"], z=1.5,
                text="Truck", scale=0.6,
                r=1.0, g=1.0, b=1.0,
            ))
            marker_id += 1

        # Gate — thin red bar
        for gate in self.layout["gates"]:
            m = self._cube_marker(
                ns="gate", mid=marker_id,
                x=gate["x"], y=gate["y"], z=0.3,
                sx=gate["sx"], sy=max(gate["sy"], 0.1), sz=1.6,
                r=0.9, g=0.1, b=0.1, a=0.9,
            )
            arr.markers.append(m)
            arr.markers.append(self._text_marker(
                ns="gate_label", mid=1000 + marker_id,
                x=gate["x"], y=gate["y"], z=0.9,
                text="Dock Gate", scale=0.4,
                r=1.0, g=0.3, b=0.3,
            ))
            marker_id += 1

        # Delivery areas — green outlined boxes
        for da in self.layout["delivery_areas"]:
            m = self._cube_marker(
                ns="delivery_area", mid=marker_id,
                x=da["x"], y=da["y"], z=0.02,
                sx=da["sx"], sy=da["sy"], sz=0.04,
                r=0.1, g=0.8, b=0.2, a=0.5,
            )
            arr.markers.append(m)
            arr.markers.append(self._text_marker(
                ns="delivery_area_label", mid=1000 + marker_id,
                x=da["x"], y=da["y"], z=0.4,
                text=da["id"].replace("_", " "),
                scale=0.35,
                r=0.1, g=0.8, b=0.2,
            ))
            marker_id += 1

        # Empty bays — grey outlined boxes
        for eb in self.layout["empty_bays"]:
            m = self._cube_marker(
                ns="empty_bay", mid=marker_id,
                x=eb["x"], y=eb["y"], z=0.02,
                sx=eb["sx"], sy=eb["sy"], sz=0.04,
                r=0.6, g=0.6, b=0.6, a=0.4,
            )
            arr.markers.append(m)
            arr.markers.append(self._text_marker(
                ns="empty_bay_label", mid=1000 + marker_id,
                x=eb["x"], y=eb["y"], z=0.4,
                text=eb["id"].replace("_", " "),
                scale=0.35,
                r=0.6, g=0.6, b=0.6,
            ))
            marker_id += 1

        self.env_pub.publish(arr)

    # =========================================================================
    # Pallets — cubes colored by good_type
    # TODO: replace with mesh when available
    # =========================================================================

    def publish_pallets(self):
        arr = MarkerArray()
        for i, item in enumerate(self.layout["items"]):

            if item["is_empty"]:
                # Empty pallet — just the pallet mesh
                m = Marker()
                m.header.frame_id = "map"
                m.header.stamp = self.get_clock().now().to_msg()
                m.ns = "pallets"
                m.id = i
                m.type = Marker.MESH_RESOURCE
                m.mesh_resource = f"package://{MESH_PKG}/meshes/Pallet.dae"  # ← exact filename
                m.mesh_use_embedded_materials = False   # ← disable embedded, use our color instead
                m.color.r = 0.76
                m.color.g = 0.60
                m.color.b = 0.42
                m.color.a = 1.0
                m.action = Marker.ADD
                m.pose.position.x = float(item["x"])
                m.pose.position.y = float(item["y"])
                m.pose.position.z = 0.0
                m.pose.orientation.x = float(np.sin(np.radians(90) / 2))
                m.pose.orientation.y = 0.0
                m.pose.orientation.z = 0.0
                m.pose.orientation.w = float(np.cos(np.radians(90) / 2))
                m.scale.x = 0.09
                m.scale.y = 0.18
                m.scale.z = 0.17
                m.color.a = 1.0
                arr.markers.append(m)

            else:
                # Non-empty pallet — pallet base mesh
                m = Marker()
                m.header.frame_id = "map"
                m.header.stamp = self.get_clock().now().to_msg()
                m.ns = "pallets"
                m.id = i
                m.type = Marker.MESH_RESOURCE
                m.mesh_resource = f"package://{MESH_PKG}/meshes/Pallet.dae"  # ← exact filename
                # m.mesh_use_embedded_materials = True
                m.mesh_use_embedded_materials = False   # ← disable embedded, use our color instead
                m.color.r = 0.76
                m.color.g = 0.60
                m.color.b = 0.42
                m.color.a = 1.0
                m.action = Marker.ADD
                m.pose.position.x = float(item["x"])
                m.pose.position.y = float(item["y"])
                m.pose.position.z = 0.0
                m.pose.orientation.x = float(np.sin(np.radians(90) / 2))
                m.pose.orientation.y = 0.0
                m.pose.orientation.z = 0.0
                m.pose.orientation.w = float(np.cos(np.radians(90) / 2))
                m.scale.x = 0.09
                m.scale.y = 0.18
                m.scale.z = 0.17
                m.color.a = 1.0
                arr.markers.append(m)

                # Boxes on top — ClutteringA mesh
                boxes = Marker()
                boxes.header.frame_id = "map"
                boxes.header.stamp = m.header.stamp
                boxes.ns = "pallet_boxes"
                boxes.id = i
                boxes.type = Marker.MESH_RESOURCE
                boxes.mesh_resource = f"package://{MESH_PKG}/meshes/aws_robomaker_warehouse_ClutteringC_01_visual.DAE"  # ← exact filename
                boxes.mesh_use_embedded_materials = True
                boxes.action = Marker.ADD
                boxes.pose.position.x = float(item["x"])
                boxes.pose.position.y = float(item["y"])
                boxes.pose.position.z = 0.15   # ← height of pallet, adjust after seeing in RViz
                boxes.pose.orientation.w = 1.0
                boxes.scale.x = 0.4
                boxes.scale.y = 0.4
                boxes.scale.z = 0.4
                boxes.color.a = 1.0
                arr.markers.append(boxes)

            # Label — black text
            good = item["good_type"] or "empty"
            scanned = "✓" if item["is_scanned"] else "?"
            arr.markers.append(self._text_marker(
                ns="pallet_labels", mid=1000 + i,
                x=item["x"], y=item["y"], z=0.8,
                text=f"{item['id']}\n{good} {scanned}",
                scale=0.25,
                r=0.0, g=0.0, b=0.0,
            ))

        self.pallet_pub.publish(arr)

    # =========================================================================
    # Coffee machine
    # =========================================================================

    def publish_coffee_machine(self):
        x = self.layout["coffee_machine"]["x"]
        y = self.layout["coffee_machine"]["y"]

        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "coffee_machine"
        m.id = 0
        m.type = Marker.CUBE
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.position.z = 0.5
        m.pose.orientation.w = 1.0
        m.scale.x = 0.4
        m.scale.y = 0.4
        m.scale.z = 0.8
        m.color.r = 0.4
        m.color.g = 0.25
        m.color.b = 0.1
        m.color.a = 1.0
        self.coffee_pub.publish(m)

        t = Marker()
        t.header.frame_id = "map"
        t.header.stamp = m.header.stamp
        t.ns = "coffee_machine_label"
        t.id = 1
        t.type = Marker.TEXT_VIEW_FACING
        t.action = Marker.ADD
        t.pose.position.x = float(x)
        t.pose.position.y = float(y - 0.5)
        t.pose.position.z = 1.2
        t.scale.z = 0.3
        t.color.r = 0.7
        t.color.g = 0.7
        t.color.b = 0.0
        t.color.a = 1.0
        t.text = "Coffee Machine"
        self.coffee_pub.publish(t)

    # =========================================================================
    # Status label
    # =========================================================================

    def publish_task_label(self, text: str):
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "task_label"
        m.id = 0
        m.type = Marker.TEXT_VIEW_FACING
        m.action = Marker.ADD
        m.pose.position.x = 0.0
        m.pose.position.y = 6.0
        m.pose.position.z = 2.0
        m.scale.z = 0.5
        m.color.r = 1.0
        m.color.g = 0.0
        m.color.b = 0.0
        m.color.a = 1.0
        m.text = text
        self.task_label_pub.publish(m)

    # =========================================================================
    # Marker helpers
    # =========================================================================

    def _cube_marker(self, ns, mid, x, y, z, sx, sy, sz,
                     r, g, b, a) -> Marker:
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = ns
        m.id = mid
        m.type = Marker.CUBE
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.position.z = float(z)
        m.pose.orientation.w = 1.0
        m.scale.x = float(sx)
        m.scale.y = float(sy)
        m.scale.z = float(sz)
        m.color.r = float(r)
        m.color.g = float(g)
        m.color.b = float(b)
        m.color.a = float(a)
        return m

    def _text_marker(self, ns, mid, x, y, z, text,
                     scale, r, g, b) -> Marker:
        t = Marker()
        t.header.frame_id = "map"
        t.header.stamp = self.get_clock().now().to_msg()
        t.ns = ns
        t.id = mid
        t.type = Marker.TEXT_VIEW_FACING
        t.action = Marker.ADD
        t.pose.position.x = float(x)
        t.pose.position.y = float(y)
        t.pose.position.z = float(z)
        t.pose.orientation.w = 1.0
        t.scale.z = float(scale)
        t.color.r = float(r)
        t.color.g = float(g)
        t.color.b = float(b)
        t.color.a = 1.0
        t.text = text
        return t


# =============================================================================
# Entry point
# =============================================================================

def main(args=None):
    rclpy.init(args=args)
    node = DockVisualizer()
    rclpy.spin(node)


if __name__ == "__main__":
    main()
