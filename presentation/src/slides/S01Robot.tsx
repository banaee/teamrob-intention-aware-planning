/**
 * Slide 1, two steps: the robot alone; then the same robot in a room, the view moving back until the whole room shows.
 * The room and the robot's look are kitting's, recorded from the web-ui's own piece (scripts/record_view.py).
 */

import { useRef } from "react";

import recorded from "../../data/kitting_env_layout_01.json";
import { useShown } from "../Deck";
import { type Recorded, RobotInRoom } from "../scene/RobotInRoom";

// The JSON's enumerations are read as strings; the recording wrote the web-ui's messages (LayoutView, Appearance).
const room = recorded as unknown as Recorded;
// A free place on the floor, in zone_NE, with nothing between it and the tilted view's camera.
const PLACE = { x: 150, y: 100 };

export function S01Robot() {
  const second = useRef<HTMLHeadingElement>(null);
  const inRoom = useShown(second);
  return (
    <section>
      <div className="stage">
        <h1 className="s01-text">This is Anton, a robot.</h1>
        <h1 className="s01-text fragment" ref={second}>Anton is in a factory setup.</h1>
        <RobotInRoom recorded={room} place={PLACE} inRoom={inRoom} />
      </div>
    </section>
  );
}
