/**
 * The web-ui's theme (T-viz 0.3): the one file that holds the page's colours, line weights, spacing and type sizes.
 * The page's CSS reads them as variables (applyTheme); the scene reads them from here and takes its colours from
 * nowhere else.
 *
 * Semantic colours: a colour is kept for one meaning everywhere on the page. `robot` marks the robot and what
 * concerns it, `human` the human. The rest of the scene is nearly monochrome, so that these two stay readable.
 */

export const theme = {
  color: {
    page: "#F3F4F7",          // the page's ground
    surface: "#FFFFFF",       // panels, the env-pane's frame, label pills
    floor: "#FCFCFD",         // the space's floor
    floorEdge: "#E6E8EF",     // the floor plate's thickness
    ink: "#1E2230",           // text; movable objects
    inkSoft: "#5A6074",       // secondary text
    inkFaint: "#9097AB",      // tertiary text, labels on the floor
    line: "#717892",          // outlines of the scene
    lineFaint: "#C3C7D4",     // areas, the floor grid, frames
    labelFaint: "#B3B8C8",    // labels on the floor of passive things: small and light, they inform little
    faceTop: "#FFFFFF",       // background objects: the face toward the sky
    faceLight: "#F2F3F8",     // the side toward the light
    faceShade: "#E3E6EF",     // the side away from the light, hatched
    hatch: "#9EA4BB",
    shadow: "#1E2230",        // drawn at `opacity.shadow`
    activeTop: "#F4F0E8",     // active objects: a warm neutral tone
    activeLight: "#E9E2D4",
    activeShade: "#D9CFBC",
    activeLine: "#8A7E68",
    movableTop: "#4B5166",    // movable objects: solid ink
    movableLight: "#383D4F",
    movableShade: "#2A2E3C",
    movableLine: "#E9EBF2",   // their edges, light on dark
    robot: "#3B5BDB",
    robotLight: "#A7B8F5",
    robotDark: "#2A44B0",
    human: "#D9653B",
    humanLight: "#F4C2A9",
    humanDark: "#A9482A",
    vest: "#F2D024",          // the person's work safety vest: safety yellow (a trial, T-viz 1a)
    vestLight: "#F8E57A",
    vestDark: "#C9A90F",
    // Panel 4a (T-viz 1a (iv)): a script line's state, and the tag per task. One colour per value.
    stateOpen: "#9097AB",
    stateProgress: "#D9653B",   // the human's colour: what the human is doing
    stateSuspended: "#B7862A",
    stateCompleted: "#3E8C63",
    stateAbandoned: "#9A4A6E",
    stateInfeasible: "#7A8094",
    tagAccord: "#2F7F86",
    tagNotAccord: "#B5652A",
    tagNoFact: "#9097AB",
    // Panel 4c (T-viz 1c): the viewed earlier tick, the distance below min_separation and its line.
    past: "#C27C0E",
    pastLight: "#FBF1DF",
    below: "#F6C9C4",
    separation: "#C2413B",
  },
  /** One colour per task (T-viz 1c): the first ten tasks of a sim-run, in a fixed order (src/frame/colours.ts), get
   * these hues; every further task the neutral `taskOther`. Validated as a categorical palette on the light surface
   * (the dataviz validator: lightness, chroma, adjacent CVD ΔE 6.4, legal with the labels and tooltips the page has). */
  task: ["#7d8a00", "#0e8fb3", "#4a3aa7", "#b5591e", "#e87ba4", "#008300", "#c2185b", "#1baf7a", "#eda100", "#e34948"],
  taskOther: "#B9BDCB",
  /** Panel 4c's task colours (T-viz 1c, the two versions; the bottom panel only until Hadi chooses): dusty tones of
   * middle lightness, drawn mostly as light tints (bands) and as lines only for a hypothesis that has led, so that few
   * colours show at once and the panel sits with the right panel's tinted blocks. Every further task `taskSoftOther`. */
  taskSoft: ["#4E8F8B", "#8A6FB0", "#C08A3E", "#6E8F4E", "#B0607A", "#5A7FB0", "#9A7B5F", "#4F6D8A"],
  taskSoftOther: "#A3A8B8",
  opacity: {
    shadow: 0.10,
    agentRing: 0.12,
    barrierFace: 0.35,
    counterTop: 0.4,          // a counter's top, see-through so that an agent at it is not hidden (T-viz 1a (iii))
    plotFaint: 0.45,          // panel 4c (T-viz 1c): a belief line of a hypothesis that has never led
    plotFact: 0.75,           // panel 4c: a timeline fact's band
    plotHold: 0.85,           // panel 4c: a hold's strip
  },
  line: {                     // px
    object: 1.3,
    agent: 1.3,
    floor: 1.1,
    area: 1.0,
    movable: 1.0,
    plot: 1.25,               // panel 4c (T-viz 1c): the distance
    plotLead: 2,              // a belief line of a hypothesis that has led
    plotFaint: 1,             // the other belief lines
    guide: 1,                 // θ, min_separation, the axis, the latest tick
    viewed: 2,                // the viewed earlier tick
  },
  hatch: {                    // px, in screen space
    spacing: 4,
    width: 0.9,
  },
  space: { xs: 4, sm: 8, md: 12, lg: 16, xl: 24, xxl: 32 },   // px
  radius: { frame: 10, pill: 999 },                        // px
  type: {
    family: "'IBM Plex Sans', system-ui, sans-serif",
    mono: "'IBM Plex Mono', ui-monospace, monospace",
    size: { xs: 10, sm: 11, md: 13, lg: 15, xl: 18, xxl: 24 },   // px; xxl: panel 4c's large numbers (T-viz 1c)
    weight: { regular: 400, medium: 500 },
  },
  scene: {                    // in the layout's unit, on the floor
    areaLabel: 26,            // an area's id, at most
    passiveLabel: 13,         // a background object's id
    activeLabel: 18,          // an active object's id
    gridStep: 100,
  },
} as const;

export type Theme = typeof theme;

/** The theme's values as CSS variables on the document, for the page's stylesheet. */
export function applyTheme(): void {
  const root = document.documentElement.style;
  for (const [name, value] of Object.entries(theme.color)) root.setProperty(`--color-${name}`, value);
  for (const [name, value] of Object.entries(theme.space)) root.setProperty(`--space-${name}`, `${value}px`);
  for (const [name, value] of Object.entries(theme.radius)) root.setProperty(`--radius-${name}`, `${value}px`);
  for (const [name, value] of Object.entries(theme.type.size)) root.setProperty(`--type-${name}`, `${value}px`);
  for (const [name, value] of Object.entries(theme.type.weight)) root.setProperty(`--weight-${name}`, `${value}`);
  root.setProperty("--font", theme.type.family);
  root.setProperty("--font-mono", theme.type.mono);
  root.setProperty("--line-frame", "1px");
}
