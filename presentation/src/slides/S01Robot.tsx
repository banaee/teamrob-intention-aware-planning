/** Slide 1: the robot, introduced by its name in the talk. Its look is kitting's scene appearance, read at build time. */

import kitting from "../../../domains/kitting/appearance.json";
import { paints } from "../../../webui/page/src/env-pane/solids";
import type { FigureLook } from "../../../webui/page/src/gen/messages";
import { FigureAlone } from "../scene/FigureAlone";

// The JSON's figure is read as a string; webui/appearance.py checks it against the figures the page draws.
const robot = kitting.robot as FigureLook;

export function S01Robot() {
  return (
    <section>
      <div className="stage">
        <h1 className="s01-text">This is Anton, a robot.</h1>
        <FigureAlone look={robot} paint={paints.robot} />
      </div>
    </section>
  );
}
