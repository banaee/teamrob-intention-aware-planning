/**
 * Panel 4c, version B (T-viz 1c, the two versions; Hadi, 7 October 2026): the look of the ReUI chart components
 * (reui.io, MIT), in a light scheme, on ReUI's chart base, Recharts, with ReUI's styling written in the page's CSS (ReUI's
 * code needs Tailwind and shadcn, which the page does not use; Motion, ReUI's animation library, was tried and left out:
 * the shapes' growth is a CSS transition, cheaper in a long sim-run). Each lane is a card as a shadcn card: white,
 * rounded, a fine ring and a faint shadow; its header column, in the tint of the right panel's block that matches it,
 * holds the title, a large number where it helps (the leading belief, the present distance) and a muted line. The belief
 * and the distance are Recharts areas: a smooth line with a gradient fading under it, a faint dashed horizontal grid, no
 * axes, a dot at the shown tick; the charts' right edge moves on by a short transition as ticks arrive. The task lanes
 * and context are not charts: rounded shapes in soft tints on the same tick axis; a hold is the stripe texture ReUI uses.
 * Geometry and colours are shared with version A (src/plots/look.ts); the values are the lanes'.
 */

import { memo, useMemo } from "react";
import { Area, ComposedChart, Line, ReferenceArea, ReferenceDot, XAxis, YAxis } from "recharts";

import type { TaskColours } from "../frame/colours";
import { keyText } from "../frame/robot";
import { taskText } from "../frame/activity";
import type { TagValue } from "../gen/messages";
import { theme } from "../theme";
import {
  beliefLines, heldBands, humanBands, type Lanes, type PairLane, robotBands, type RobotLane, trueBands,
} from "./lanes";
import {
  axisStep, bandText, type Box, type Geometry, leading, mix, PAD, type Row, SCALE, shownTick, softOf, toneOf, xOf,
} from "./look";

const TAG: Record<TagValue, string | null> = {
  "in accord": theme.color.tagAccord,
  "not in accord": theme.color.tagNotAccord,
  "no fact": null,
};

/** A shape grows, and the charts' edge moves on, in a time shorter than a tick at the default speed. */
const TOP = 6;      // px: the belief's 1 below the row's top, the held admission above it

interface Props { g: Geometry; lanes: Lanes; length: number; colours: TaskColours; end: number; viewed: number | null }

export const PlotsB = memo(function PlotsB({ g, lanes, length, colours, end, viewed }: Props) {
  const c = theme.color;
  const n = length;
  const shown = shownTick(lanes, viewed);
  const step = axisStep(g, end);
  const ticks: number[] = [];
  for (let t = 0; t <= end; t += step) ticks.push(t);
  const plotW = g.x1 - g.x0;
  const pct = (t: number) => `${(100 * t) / end}%`;
  const px = (t: number) => (t / end) * plotW;

  /** A rounded shape from tick a to tick b in a soft tint of `colour`, its text where it fits; it grows with Motion. */
  const shape = (key: string, a: number, b: number, colour: string, label: string | null, strip: string | null = null) => {
    const w = px(b + 1 - a);
    return (
      <div key={key} className="pb-band" style={{ left: px(a), width: w, background: mix(colour, "#FFFFFF", 0.8), color: bandText(colour) }}>
        {label !== null && w > 96 && <span>{label}</span>}
        {strip !== null && w > 14 && <i className="pb-strip" style={{ background: strip }} />}
      </div>
    );
  };

  const first = g.boxes[0]?.y ?? 0;
  const lastBox = g.boxes[g.boxes.length - 1];
  const last = lastBox === undefined ? 0 : lastBox.y + lastBox.h;

  return (
    <div className="pb" style={{ width: g.width, height: g.height }}>
      {g.boxes.map((box, bi) => <Card key={bi} box={box} g={g} lanes={lanes} shown={shown} colours={colours} />)}
      {g.boxes.flatMap((box) => box.rows).map((r, ri) => {
        const at = { left: g.x0, width: plotW, top: r.y, height: r.h };
        switch (r.kind) {
          case "human":
            return (
              <div key={ri} className="pb-lane" style={at}>
                {humanBands(r.lane, n).map((b, i) => shape(`${i}`, b.start, b.end, softOf(colours, b.value.task.identity),
                  taskText(b.value.task), b.value.tag === null ? null : TAG[b.value.tag.tag]))}
              </div>
            );
          case "fact":
            return (
              <div key={ri} className="pb-lane" style={at}>
                {trueBands(r.lane.holds, n).map((b, i) => shape(`${i}`, b.start, b.end, c.inkSoft, r.lane.fact))}
              </div>
            );
          case "robot":
            return (
              <div key={ri} className="pb-lane pb-robot" style={at}>
                {robotBands(r.lane, n).map((b, i) => shape(`${i}`, b.start, b.end, softOf(colours, b.value.identity), taskText(b.value)))}
                {trueBands(r.lane.hold, n).map((b, i) => (
                  <div key={`h${i}`} className="pb-hold" style={{ left: px(b.start), width: px(b.end + 1 - b.start) }} />
                ))}
                {r.lane.decision.slice(0, n).map((d, t) => (d === null ? null
                  : <i key={`d${t}`} className="pb-decision" style={{ left: pct(t + 0.5) }} />))}
              </div>
            );
          case "belief":
            return r.off
              ? <div key={ri} className="pb-lane pb-off" style={at}>off</div>
              : <Belief key={ri} lane={r.lane} at={at} n={n} end={end} colours={colours} shown={shown} />;
          case "distance":
            return <Distance key={ri} lane={r.lane} minSep={r.minSep} at={at} n={n} end={end} shown={shown} />;
        }
      })}
      {ticks.map((t) => (
        <span key={t} className="pb-axis" style={{ left: xOf(g, end, t), top: g.axisY + 1 }}>{t}</span>
      ))}
      {n > 0 && <i className="pb-now" style={{ left: xOf(g, end, n - 0.5), top: first + 6, height: last - first - 12 }} />}
      {viewed !== null && viewed < n && (
        <>
          <i className="pb-viewed" style={{ left: xOf(g, end, viewed + 0.5), top: first, height: last - first }} />
          <span className="pb-viewed-tick" style={{ left: xOf(g, end, viewed + 0.5), top: g.axisY }}>{viewed}</span>
        </>
      )}
    </div>
  );
});

// =============================================================================
// The cards and their header columns
// =============================================================================

function Card({ box, g, lanes, shown, colours }: {
  box: Box; g: Geometry; lanes: Lanes; shown: number | null; colours: TaskColours;
}) {
  const tone = toneOf(box.tone);
  const header = g.x0 - PAD - 16;
  return (
    <div className="pb-card" style={{ left: PAD, width: g.width - 2 * PAD, top: box.y, height: box.h }}>
      <div className="pb-head" style={{ width: header, background: tone.fill }}>
        {box.rows.map((r, i) => <Head key={i} row={r} first={i === 0} title={box.title} box={box} lanes={lanes} shown={shown}
                                      colours={colours} />)}
      </div>
    </div>
  );
}

/** A row's header: the card's title on its first row, a large number where it helps, a muted line. */
function Head({ row, first, title, box, shown, colours }: {
  row: Row; first: boolean; title: string; box: Box; lanes: Lanes; shown: number | null; colours: TaskColours;
}) {
  const c = theme.color;
  const top = row.y - box.y;
  const t = shown;
  let number: { text: string; colour: string } | null = null;
  let line: string | null = null;
  let badge: { text: string; colour: string } | null = null;
  switch (row.kind) {
    case "human": {
      const task = t === null ? null : row.lane.task[t];
      const tag = t === null ? null : row.lane.tag[t];
      line = task === null ? "no task" : taskText(task);
      if (tag !== null && tag.tag !== "no fact") badge = { text: tag.tag, colour: TAG[tag.tag]! };
      break;
    }
    case "belief": {
      if (row.off) { line = "off"; break; }
      const lead = t === null ? null : leading(row.lane, t);
      number = lead === null ? { text: "–", colour: c.lineFaint } : { text: lead.value.toFixed(2), colour: bandText(softOf(colours, lead.key)) };
      line = lead === null ? null : keyText(row.lane.robot, lead.key);
      const held = t === null ? null : row.lane.held[t];
      if (held !== null) badge = { text: "held", colour: softOf(colours, held) };
      break;
    }
    case "fact":
      line = row.lane.fact;
      if (t !== null && row.lane.holds[t]) badge = { text: "now", colour: c.inkSoft };
      break;
    case "robot": {
      const task = t === null ? null : row.lane.task[t];
      line = task === null ? "no task" : taskText(task);
      if (t !== null && row.lane.hold[t]) badge = { text: "hold", colour: c.robotDark };
      break;
    }
    case "distance": {
      const s = t === null ? null : row.lane.separation[t];
      number = s === null ? { text: "–", colour: c.lineFaint } : { text: s.minimum.toFixed(0), colour: s.below ? c.separation : c.ink };
      line = `min ${row.minSep}`;
      if (s?.below) badge = { text: "below", colour: c.separation };
      break;
    }
  }
  return (
    <div className="pb-head-row" style={{ top: Math.max(0, top - 2) }}>
      {(first || box.named) && (
        <div className="pb-head-title">
          <span>{first ? title : ""}{box.named ? `${first ? " · " : ""}${rowName(row)}` : ""}</span>
          {badge !== null && (
            <em style={{ color: mix(badge.colour, c.ink, 0.25), background: mix(badge.colour, "#FFFFFF", 0.86) }}>{badge.text}</em>
          )}
        </div>
      )}
      {number !== null && <strong style={{ color: number.colour }}>{number.text}</strong>}
      {line !== null && <small>{line}</small>}
    </div>
  );
}

function rowName(r: Row): string {
  return r.kind === "human" ? r.lane.human : r.kind === "fact" ? r.lane.fact
    : r.kind === "distance" ? `${r.lane.robot}–${r.lane.human}` : r.lane.robot.robot;
}

// =============================================================================
// The two charts
// =============================================================================

interface At { left: number; width: number; top: number; height: number }

/** The guides under a chart, across the whole card: a faint dashed grid at `lines` (as ReUI's horizontal grid) and one
 * dashed line of meaning (θ, min_separation), not clipped by the chart's reveal. */
function Guides({ at, margin, lines, max, dashed }: {
  at: At; margin: number; lines: number[]; max: number;
  dashed: { value: number; colour: string; dash: string; width: number; label: string | null };
}) {
  const c = theme.color;
  const y = (v: number) => margin + (1 - v / max) * (at.height - 2 * margin);
  return (
    <svg className="pb-guides" style={{ left: at.left, top: at.top }} width={at.width} height={at.height}>
      {lines.map((v) => <line key={v} x1={0} x2={at.width} y1={y(v)} y2={y(v)} stroke={c.lineFaint} strokeOpacity={0.8}
                              strokeDasharray="3 3" />)}
      <line x1={0} x2={at.width} y1={y(dashed.value)} y2={y(dashed.value)} stroke={dashed.colour} strokeWidth={dashed.width}
            strokeDasharray={dashed.dash} strokeLinecap="round" />
      {dashed.label !== null && (
        <text x={-6} y={y(dashed.value)} textAnchor="end" dominantBaseline="central" fill={c.robotDark}
              fontSize={theme.type.size.xs}>{dashed.label}</text>
      )}
    </svg>
  );
}

/** The ticks a chart draws: every tick while there are fewer than one per 6 px, else every k-th tick and the latest (a
 * long sim-run's line has more ticks than pixels; drawing all of them makes every step slow). The values are the lanes'. */
function drawn(n: number, width: number): number[] {
  const k = Math.max(1, Math.ceil(n / Math.max(100, Math.floor(width / 6))));
  const out: number[] = [];
  for (let t = 0; t < n; t += k) out.push(t);
  if (n > 0 && out[out.length - 1] !== n - 1) out.push(n - 1);
  return out;
}

/** The chart shown up to just past the latest tick: its right edge moves on by a short transition as ticks arrive, so
 * that the line grows (Recharts' own animation stays off: it animates by index and leaves a stale curve across a gap). */
function reveal(at: At, n: number, end: number): string {
  const right = Math.max(0, at.width - ((n + 0.5) / end) * at.width - 10);
  return `inset(-12px ${right}px -12px -40px)`;
}

/** A very light glow around the dot at the shown tick (a blur of the dot under it). Lines have none (Hadi, 7 October
 * 2026); the gradients under the leading belief and the distance stay, as the area under them has a meaning (how sure
 * the robot is; the room between robot and human). */
function Glow({ id, blur }: { id: string; blur: number }) {
  return (
    <filter id={id} x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation={blur} result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  );
}

function Belief({ lane, at, n, end, colours, shown }: {
  lane: RobotLane; at: At; n: number; end: number; colours: TaskColours; shown: number | null;
}) {
  const c = theme.color;
  const robot = lane.robot;
  // one object per tick: its x, and per hypothesis of the space its belief, or null where it is not live
  const { data, keys } = useMemo(() => {
    const lines = beliefLines(lane, n);
    const keys = [...lines.keys()];
    const cols = keys.map((k) => lines.get(k)!);
    return { keys, data: drawn(n, at.width).map((t) => ({ x: t + 0.5, v: cols.map((col) => col[t]) })) };
  }, [lane, n, at.width]);
  const lead = shown === null ? null : leading(lane, shown);
  const height = at.height - TOP;
  // the gradient under the leader at the shown tick only, so that two fills never mix
  const id = robot.robot;
  return (
    <>
      <div className="pb-lane" style={{ ...at, height: 3 }}>
        {heldBands(lane, n).map((b, i) => (
          <i key={i} className="pb-held" style={{ left: `${(100 * b.start) / end}%`, width: `${(100 * (b.end + 1 - b.start)) / end}%`,
                                                 background: softOf(colours, b.value) }} />
        ))}
      </div>
      <Guides at={{ ...at, top: at.top + TOP, height }} margin={2} lines={[0, 0.5, 1]} max={1}
              dashed={{ value: robot.theta, colour: mix(c.robot, "#FFFFFF", 0.3), dash: "4 4", width: 1, label: "θ" }} />
      <div className="pb-chart" style={{ ...at, top: at.top + TOP, height, clipPath: reveal(at, n, end) }}>
        <ComposedChart width={at.width} height={height} data={data} margin={{ top: 2, right: 0, bottom: 2, left: 0 }}>
          <defs>
            {keys.map((k, i) => (lane.leaders.has(k) ? (
              <linearGradient key={k} id={`pb-${id}-fade-${i}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={softOf(colours, k)} stopOpacity={0.35} />
                <stop offset="95%" stopColor={softOf(colours, k)} stopOpacity={0} />
              </linearGradient>
            ) : null))}
            <Glow id={`pb-${id}-dot-glow`} blur={1.5} />
          </defs>
          <XAxis type="number" dataKey="x" domain={[0, end]} hide />
          <YAxis type="number" domain={[0, 1]} hide />
          {keys.map((k, i) => (lane.leaders.has(k) ? null : (
            <Line key={k} dataKey={(d: { v: (number | null)[] }) => d.v[i]} type="monotone" stroke={c.lineFaint}
                  strokeWidth={1} dot={false} activeDot={false} isAnimationActive={false} connectNulls={false} />
          )))}
          {keys.map((k, i) => (!lane.leaders.has(k) ? null : (
            <Area key={k} dataKey={(d: { v: (number | null)[] }) => d.v[i]} type="monotone" stroke={softOf(colours, k)}
                  strokeWidth={2} fill={k === lead?.key ? `url(#pb-${id}-fade-${i})` : "none"} dot={false}
                  activeDot={false} connectNulls={false} baseValue={0} isAnimationActive={false} />
          )))}
          {lead !== null && shown !== null && (
            <ReferenceDot x={shown + 0.5} y={lead.value} r={4.5} fill={softOf(colours, lead.key)} stroke="#FFFFFF"
                          strokeWidth={2} filter={`url(#pb-${id}-dot-glow)`} />
          )}
        </ComposedChart>
      </div>
    </>
  );
}

function Distance({ lane, minSep, at, n, end, shown }: {
  lane: PairLane; minSep: number; at: At; n: number; end: number; shown: number | null;
}) {
  const c = theme.color;
  const span = SCALE * minSep;
  const accent = c.robot;
  const data = useMemo(() => drawn(n, at.width).map((t) => {
    const s = lane.separation[t];
    return { x: t + 0.5, d: s === null ? null : Math.min(s.minimum, span) };
  }), [lane, n, span, at.width]);
  const below = trueBands(lane.separation.slice(0, n).map((s) => s?.below === true), n);
  const now = shown === null ? null : lane.separation[shown];
  const id = `${lane.robot}-${lane.human}`;
  return (
    <>
    <Guides at={at} margin={3} lines={[0, span / 2, span]} max={span}
            dashed={{ value: minSep, colour: c.separation, dash: "0.1 3.5", width: 1.6, label: null }} />
    <div className="pb-chart" style={{ ...at, clipPath: reveal(at, n, end) }}>
      <ComposedChart width={at.width} height={at.height} data={data} margin={{ top: 3, right: 0, bottom: 3, left: 0 }}>
        <defs>
          <linearGradient id={`pb-${id}-distance`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={accent} stopOpacity={0.28} />
            <stop offset="95%" stopColor={accent} stopOpacity={0} />
          </linearGradient>
          <pattern id={`pb-${id}-stripe`} patternUnits="userSpaceOnUse" width="6" height="6">
            <path d="M0,6 L6,0" stroke={c.separation} strokeWidth="1" opacity="0.35" />
          </pattern>
          <Glow id={`pb-${id}-dot-glow`} blur={1.5} />
        </defs>
        <XAxis type="number" dataKey="x" domain={[0, end]} hide />
        <YAxis type="number" domain={[0, span]} hide />
        {below.map((b, i) => (
          <ReferenceArea key={`b${i}`} x1={b.start} x2={b.end + 1} fill={`url(#pb-${id}-stripe)`} stroke="none" radius={4} />
        ))}
        {below.map((b, i) => (
          <ReferenceArea key={`bb${i}`} x1={b.start} x2={b.end + 1} fill={mix(c.separation, "#FFFFFF", 0.82)} fillOpacity={0.7}
                         stroke="none" radius={4} />
        ))}
        <Area dataKey="d" type="monotone" stroke={accent} strokeWidth={2} fill={`url(#pb-${id}-distance)`} dot={false} activeDot={false} connectNulls={false} baseValue={0}
              isAnimationActive={false} />
        {now !== null && shown !== null && (
          <ReferenceDot x={shown + 0.5} y={Math.min(now.minimum, span)} r={4.5} fill={now.below ? c.separation : accent}
                        stroke="#FFFFFF" strokeWidth={2} filter={`url(#pb-${id}-dot-glow)`} />
        )}
      </ComposedChart>
    </div>
    </>
  );
}
