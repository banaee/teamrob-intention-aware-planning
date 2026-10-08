/**
 * The architecture diagram, drawn by React Flow from the model (model.ts): one diagram whose state is a talk stage.
 * The page lays out every arrow (a smooth step between two element sides) and draws it; nothing is an image.
 *
 * What a talk stage adds is drawn at full strength and the rest recedes; on a click (`revealed`) the additions appear
 * smoothly (a fade, an arrow drawn along its length) and an arrow that gives way fades out. That is the only motion.
 * `colouring: "questions"` colours the elements by the question each answers (know, believe, decide), for the recap.
 * `questionTags` lays the three questions over the empty frames (talk stage 0).
 *
 * The diagram takes no pointer: a click goes to the deck. Its canvas keeps the model's proportions and is scaled to
 * the space it is given, so every talk stage shows the elements at the same places.
 */

import {
  type Edge, EdgeLabelRenderer, type EdgeProps, getSmoothStepPath, Handle, type Node, type NodeProps, Position,
  ReactFlow, ReactFlowProvider,
} from "@xyflow/react";
import { useLayoutEffect, useMemo, useRef, useState } from "react";

import { QUESTION_HEADER, type Question, type TalkStage } from "../talk";
import { ARROWS, type Arrow, DESIGN, ELEMENTS, type Element, type Part, presence, type Presence,
  type Side } from "./model";

export type Colouring = "new" | "questions";

interface Props {
  stage: TalkStage;
  revealed: boolean;
  colouring?: Colouring;
  questionTags?: boolean;
  tagsShown?: boolean;
  /** The block opened (unboxing.tsx): it stays, the rest recedes. */
  focus?: string | null;
}

export function Architecture(props: Props) {
  return (
    <ReactFlowProvider>
      <Diagram {...props} />
    </ReactFlowProvider>
  );
}

const PAD = 8;    // the canvas's margin around the model, in the model's unit

function Diagram({ stage, revealed, colouring = "new", questionTags = false, tagsShown = true, focus = null }: Props) {
  const box = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState<{ w: number; h: number } | null>(null);
  useLayoutEffect(() => {
    const div = box.current!;
    const observer = new ResizeObserver(() => setSize({ w: div.clientWidth, h: div.clientHeight }));
    observer.observe(div);
    return () => observer.disconnect();
  }, []);
  const zoom = size === null ? 1 : Math.min(size.w / (DESIGN.w + 2 * PAD), size.h / (DESIGN.h + 2 * PAD));
  const viewport = size === null ? { x: 0, y: 0, zoom: 1 } : {
    x: (size.w - DESIGN.w * zoom) / 2, y: (size.h - DESIGN.h * zoom) / 2, zoom,
  };

  const nodes = useMemo(() => buildNodes(stage, revealed, colouring, questionTags, tagsShown, focus),
    [stage, revealed, colouring, questionTags, tagsShown, focus]);
  const edges = useMemo(() => buildEdges(stage, revealed, colouring), [stage, revealed, colouring]);
  // Something is new only once the talk stage's additions are shown, and only if the talk stage adds or removes
  // anything (the recap, talk stage 7, adds nothing); then the rest recedes.
  const changes = ELEMENTS.some((e) => e.stage === stage) || ARROWS.some((a) => a.stage === stage || a.leaves === stage)
    || ELEMENTS.some((e) => e.sub.some((s) => s.stage === stage));
  const hasNew = revealed && stage > 0 && changes && colouring === "new";

  return (
    <div className={`architecture colouring-${colouring}${hasNew ? " has-new" : ""}${focus !== null ? " focusing" : ""}`}
         ref={box}>
      {size !== null && (
        <ReactFlow nodes={nodes} edges={edges} nodeTypes={NODE_TYPES} edgeTypes={EDGE_TYPES} viewport={viewport}
                   onViewportChange={() => {}} nodesDraggable={false} nodesConnectable={false}
                   elementsSelectable={false} panOnDrag={false} zoomOnScroll={false} zoomOnPinch={false}
                   zoomOnDoubleClick={false} preventScrolling={false} minZoom={0.05} maxZoom={4}
                   proOptions={{ hideAttribution: true }} />
      )}
    </div>
  );
}

// ------------------------------------------------------------------------------------------------------------------
// Nodes

interface HandleSpec { id: string; side: Side; at: number; type: "source" | "target" }

interface ElementData extends Record<string, unknown> {
  element: Element;
  presence: Presence;
  stage: TalkStage;
  revealed: boolean;
  handles: HandleSpec[];
}

interface TagData extends Record<string, unknown> { question: Question; shown: boolean }

type ElementNode = Node<ElementData, "element">;
type TagNode = Node<TagData, "tag">;

const POSITION: Record<Side, Position> = {
  top: Position.Top, bottom: Position.Bottom, left: Position.Left, right: Position.Right,
};

function handlesOf(element: Element): HandleSpec[] {
  const specs: HandleSpec[] = [];
  for (const a of ARROWS) {
    if (a.from.el === element.id) specs.push({ id: `${a.id}:s`, side: a.from.side, at: a.from.at, type: "source" });
    if (a.to.el === element.id) specs.push({ id: `${a.id}:t`, side: a.to.side, at: a.to.at, type: "target" });
  }
  return specs;
}

function buildNodes(stage: TalkStage, revealed: boolean, colouring: Colouring, tags: boolean,
                    tagsShown: boolean, focus: string | null): (ElementNode | TagNode)[] {
  const byId = new Map(ELEMENTS.map((e) => [e.id, e]));
  const nodes: (ElementNode | TagNode)[] = ELEMENTS.map((element) => {
    const parent = element.parent === null ? null : byId.get(element.parent)!;
    return {
      id: element.id,
      type: "element",
      position: parent === null ? { x: element.box.x, y: element.box.y }
        : { x: element.box.x - parent.box.x, y: element.box.y - parent.box.y },
      parentId: element.parent ?? undefined,
      width: element.box.w,
      height: element.box.h,
      draggable: false,
      selectable: false,
      data: { element, presence: grown(presence(element.stage, null, stage, revealed), element.sub, stage, revealed),
              stage, revealed, handles: handlesOf(element) },
      className: [colouring === "questions" && element.question !== null ? `q-${element.question}` : "",
        element.id === focus ? "focused" : ""].join(" "),
    };
  });
  if (tags) {
    const places: [Question, number, number][] = [["know", 145, 320], ["believe", 675, 320], ["decide", 1420, 320]];
    for (const [question, x, y] of places) {
      nodes.push({ id: `tag-${question}`, type: "tag", position: { x: x - 160, y: y - 40 }, width: 320, height: 80,
                   draggable: false, selectable: false, data: { question, shown: tagsShown } });
    }
  }
  return nodes;
}

/** An element or an arrow present since an earlier talk stage whose text grows at this one counts as new. */
function grown(p: Presence, parts: Part[], stage: TalkStage, revealed: boolean): Presence {
  return p === "old" && revealed && parts.some((part) => part.stage === stage) ? "new" : p;
}

/** The text of a list of parts at a talk stage: the parts shown, the ones new at this stage marked. */
function PartsText({ parts, stage, revealed }: { parts: Part[]; stage: TalkStage; revealed: boolean }) {
  const shown = revealed ? stage : stage - 1;
  const visible = parts.filter((p) => p.stage <= shown);
  return (
    <>
      {visible.map((p, i) => (
        <span key={p.text} className={[p.stage === stage && revealed && stage > 0 ? "part-new" : "",
          p.who === "human" ? "part-human" : ""].join(" ")}>
          {i > 0 && ", "}{p.text}
        </span>
      ))}
    </>
  );
}

function ElementNodeView({ data }: NodeProps<ElementNode>) {
  const { element, presence: p, stage, revealed, handles } = data;
  const sub = element.sub.length > 0 && <div className="el-sub"><PartsText parts={element.sub} stage={stage}
                                                                             revealed={revealed} /></div>;
  const code = element.code !== null && <span className="el-code">{element.code}</span>;
  return (
    <div className={`el el-${element.kind} presence-${p}`}>
      <Shape kind={element.kind} w={element.box.w} h={element.box.h} />
      {(element.kind === "layer" || element.kind === "column" || element.kind === "component") ? (
        <div className="el-head">
          {element.kind === "layer" && <span className="robot-dot" />}
          <span className="el-label">{element.label}</span>
          {code}
          {element.kind === "column" && sub}
        </div>
      ) : element.kind === "world" ? (
        <div className="el-world">
          <span className="el-label">{element.label}</span>
          <span className="el-sub"><PartsText parts={element.sub} stage={stage} revealed={revealed} /></span>
        </div>
      ) : (
        <div className="el-body">
          {code}
          <span className="el-label">{element.label}</span>
          {sub}
        </div>
      )}
      {handles.map((h) => (
        <Handle key={h.id} id={h.id} type={h.type} position={POSITION[h.side]} isConnectable={false}
                className="el-handle"
                style={h.side === "top" || h.side === "bottom" ? { left: `${h.at * 100}%` } : { top: `${h.at * 100}%` }} />
      ))}
    </div>
  );
}

/** One shape per kind (6.1), drawn behind the text: a sheet with a folded corner for given information, a cylinder
 * for sensed information, a framed box with a head for a function, a solid rounded block for a mechanism. */
function Shape({ kind, w, h }: { kind: Element["kind"]; w: number; h: number }) {
  const s = 1.5;   // half the outline, so that it is not cut at the edge
  let path: string;
  switch (kind) {
    case "knowledge": {
      const f = 26;
      path = `M${s},${s} H${w - f} L${w - s},${f} V${h - s} H${s} Z M${w - f},${s} V${f} H${w - s}`;
      break;
    }
    case "sensed": {
      const e = 14;
      path = `M${s},${e} A${w / 2 - s},${e - s} 0 0 1 ${w - s},${e} V${h - e} A${w / 2 - s},${e - s} 0 0 1 ${s},${h - e} Z`
        + ` M${s},${e} A${w / 2 - s},${e - s} 0 0 0 ${w - s},${e}`;
      break;
    }
    default:
      return null;
  }
  return (
    <svg className="el-shape" width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
      <path d={path} />
    </svg>
  );
}

function TagNodeView({ data }: NodeProps<TagNode>) {
  return <div className={`q-tag q-tag-${data.question} presence-${data.shown ? "new" : "absent"}`}>{QUESTION_HEADER[data.question]}</div>;
}

const NODE_TYPES = { element: ElementNodeView, tag: TagNodeView };

// ------------------------------------------------------------------------------------------------------------------
// Arrows

interface ArrowData extends Record<string, unknown> {
  arrow: Arrow;
  presence: Presence;
  stage: TalkStage;
  revealed: boolean;
  colouring: Colouring;
}

type ArrowEdge = Edge<ArrowData, "arrow">;

function buildEdges(stage: TalkStage, revealed: boolean, colouring: Colouring): ArrowEdge[] {
  return ARROWS.map((arrow) => ({
    id: arrow.id,
    type: "arrow",
    source: arrow.from.el,
    sourceHandle: `${arrow.id}:s`,
    target: arrow.to.el,
    targetHandle: `${arrow.id}:t`,
    zIndex: 10,
    selectable: false,
    focusable: false,
    data: { arrow, presence: grown(presence(arrow.stage, arrow.leaves, stage, revealed), arrow.label, stage, revealed),
            stage, revealed, colouring },
  }));
}

function ArrowView({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, data }: EdgeProps<ArrowEdge>) {
  const { arrow, presence: p, stage, revealed } = data!;
  const [path, labelX, labelY] = getSmoothStepPath({ sourceX, sourceY, targetX, targetY, sourcePosition,
                                                     targetPosition, borderRadius: 14, offset: 18 });
  const marker = `arrowhead-${id}`;
  return (
    <>
      <g className={`arrow presence-${p}${arrow.centre ? " arrow-centre" : ""}`}>
        <defs>
          <marker id={marker} viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5"
                  orient="auto-start-reverse" markerUnits="strokeWidth">
            <path d="M0,0 L10,5 L0,10 z" className="arrowhead" />
          </marker>
        </defs>
        <path d={path} className="arrow-line" pathLength={1} markerEnd={`url(#${marker})`} />
      </g>
      {arrow.label.length > 0 && (
        <EdgeLabelRenderer>
          <div className={`arrow-label presence-${p}${arrow.centre ? " arrow-centre" : ""}`}
               style={{ transform: `translate(-50%, -50%) translate(${labelX + arrow.labelOffset.dx}px, ${labelY + arrow.labelOffset.dy}px)`,
                        ...(arrow.labelWidth === null ? {} : { width: arrow.labelWidth, whiteSpace: "normal", textAlign: "center" }) }}>
            <PartsText parts={arrow.label} stage={stage} revealed={revealed} />
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
}

const EDGE_TYPES = { arrow: ArrowView };
