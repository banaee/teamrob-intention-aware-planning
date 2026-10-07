/**
 * Panel 4c, drawn on one canvas by the page (T-viz 1c; Hadi, 7 October 2026, preferred: version A with his changes).
 * Soft boxes in one light-blue tint, each with a header column (title, a small number, a muted line); bands as light
 * tints of the task's colour with the task's text in its deepened tone; lines only for the hypotheses that have led, in
 * their colour, the others thin and grey, with a legend in the belief plot; S with α dashed; the finding as a strip per
 * tick; a hold hatched over the robot's band, a decision a small dot; the distance with a gradient under it and
 * min_separation dotted. No grid lines, no glow and no shadow on a line. Geometry and colours: src/plots/look.ts.
 */

import type { TaskColours } from "../frame/colours";
import { keyText } from "../frame/robot";
import { taskText } from "../frame/activity";
import type { TagValue } from "../gen/messages";
import { theme } from "../theme";
import {
  beliefLines, findingAt, findingBands, heldBands, humanBands, type Lanes, robotBands, type RobotLane, tailLines, trueBands,
} from "./lanes";
import {
  ACCENT, axisStep, BELIEF_TOP, bandFill, bandText, box as boxLook, type Box, FINDING_COLOUR, type Geometry, LABEL, leading,
  mix, PAD, RADIUS, type Row, SCALE, shownTick, softOf, xOf,
} from "./look";

const TAG: Record<TagValue, string> = {
  "in accord": theme.color.tagAccord,
  "not in accord": theme.color.tagNotAccord,
  "no fact": theme.color.lineFaint,
};

export function draw(ctx: CanvasRenderingContext2D, g: Geometry, lanes: Lanes, colours: TaskColours, end: number,
                     viewed: number | null): void {
  const c = theme.color;
  const look = boxLook();
  const n = lanes.length;
  const shown = shownTick(lanes, viewed);
  const px = (t: number) => xOf(g, end, t);
  const mid = (t: number) => px(t + 0.5);
  ctx.clearRect(0, 0, g.width, g.height);
  ctx.textBaseline = "middle";
  const font = (size: number, weight: number = theme.type.weight.regular) => `${weight} ${size}px ${theme.type.family}`;
  const text = (s: string, x: number, y: number, colour: string, opts: { size?: number; weight?: number;
    align?: CanvasTextAlign; spacing?: string; width?: number } = {}) => {
    ctx.font = font(opts.size ?? theme.type.size.xs, opts.weight);
    ctx.fillStyle = colour; ctx.textAlign = opts.align ?? "left";
    ctx.letterSpacing = opts.spacing ?? "0px";
    let shown = s;
    if (opts.width !== undefined) while (shown.length > 1 && ctx.measureText(shown).width > opts.width) shown = shown.slice(0, -2) + "…";
    ctx.fillText(shown, x, y);
    ctx.letterSpacing = "0px";
  };
  const round = (x: number, y: number, w: number, h: number, r: number, fill: string, alpha = 1) => {
    ctx.globalAlpha = alpha; ctx.fillStyle = fill;
    ctx.beginPath(); ctx.roundRect(x, y, Math.max(1, w), h, Math.max(0, Math.min(r, w / 2, h / 2))); ctx.fill();
    ctx.globalAlpha = 1;
  };
  /** A band from tick a to tick b, a light tint of `colour`, its text inside where it fits. */
  const band = (a: number, b: number, y: number, h: number, colour: string, label: string | null) => {
    const x0 = px(a) + 0.5, w = px(b + 1) - px(a) - 1;
    round(x0, y, w, h, 5, bandFill(colour));
    if (label === null) return;
    ctx.font = font(theme.type.size.xs, theme.type.weight.medium);
    if (ctx.measureText(label).width + 14 < w) {
      text(label, x0 + 7, y + h / 2 + 0.5, bandText(colour), { weight: theme.type.weight.medium });
    }
  };
  const polyline = (ys: readonly (number | null)[], y: (v: number) => number, colour: string, weight: number) => {
    ctx.save(); ctx.strokeStyle = colour; ctx.lineWidth = weight; ctx.lineJoin = "round"; ctx.lineCap = "round";
    ctx.beginPath();
    let open = false;
    for (let t = 0; t < n; t++) {
      const v = ys[t];
      if (v === null) { open = false; continue; }
      if (open) ctx.lineTo(mid(t), y(v)); else { ctx.moveTo(mid(t), y(v)); open = true; }
    }
    ctx.stroke(); ctx.restore();
  };
  /** A soft gradient under a line, from `alpha` at the top of the lane to nothing at its foot. */
  const fade = (ys: readonly (number | null)[], y: (v: number) => number, top: number, foot: number, colour: string,
                alpha: number) => {
    const gradient = ctx.createLinearGradient(0, top, 0, foot);
    gradient.addColorStop(0, colour + Math.round(alpha * 255).toString(16).padStart(2, "0"));
    gradient.addColorStop(1, colour + "00");
    ctx.save(); ctx.fillStyle = gradient; ctx.beginPath();
    let open = false, from = 0;
    const close = (t: number) => { ctx.lineTo(mid(t), foot); ctx.lineTo(mid(from), foot); ctx.closePath(); };
    for (let t = 0; t < n; t++) {
      const v = ys[t];
      if (v === null) { if (open) close(t - 1); open = false; continue; }
      if (!open) { ctx.moveTo(mid(t), y(v)); from = t; open = true; } else ctx.lineTo(mid(t), y(v));
    }
    if (open) close(n - 1);
    ctx.fill(); ctx.restore();
  };
  const hline = (y: number, colour: string, dash: number[], weight: number = theme.line.guide) => {
    ctx.save(); ctx.strokeStyle = colour; ctx.lineWidth = weight; ctx.setLineDash(dash); ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(g.x0, y); ctx.lineTo(g.x1, y); ctx.stroke(); ctx.restore();
  };
  /** The dot at the shown tick: the colour inside a white ring. */
  const dot = (x: number, y: number, colour: string) => {
    ctx.fillStyle = "#FFFFFF"; ctx.beginPath(); ctx.arc(x, y, 4.6, 0, 2 * Math.PI); ctx.fill();
    ctx.fillStyle = colour; ctx.beginPath(); ctx.arc(x, y, 3.1, 0, 2 * Math.PI); ctx.fill();
  };

  // =========================================================================
  // The boxes
  // =========================================================================

  for (const b of g.boxes) {
    const x = PAD, w = g.width - 2 * PAD;
    ctx.save();
    ctx.beginPath(); ctx.roundRect(x, b.y, w, b.h, RADIUS); ctx.clip();
    ctx.fillStyle = look.fill; ctx.fillRect(x, b.y, w, b.h);
    ctx.fillStyle = look.header; ctx.fillRect(x, b.y, LABEL - 10, b.h);
    ctx.fillStyle = look.edge; ctx.fillRect(x, b.y, ACCENT, b.h);
    ctx.restore();
    b.rows.forEach((row, i) => { header(b, row, i === 0); plot(row); });
  }

  /** A row's header: the box's title on its first row (with the row's own name where the box holds several), a small
   * number where it helps, a muted line. */
  function header(b: Box, row: Row, first: boolean) {
    const x = PAD + ACCENT + 10, width = LABEL - ACCENT - 26;
    let y = row.y + 6;
    if (first || b.named) {
      const name = b.named ? rowName(row) : "";
      text(`${first ? b.title.toUpperCase() : ""}${first && name ? " · " : ""}${name}`, x, y, look.title,
           { weight: theme.type.weight.medium, spacing: first ? "0.7px" : "0px", width });
      y += 14;
    }
    const value = (s: string, colour: string) => { text(s, x, y + 4, colour, { size: theme.type.size.lg, weight: theme.type.weight.medium }); y += 18; };
    const line = (s: string, colour: string = c.inkSoft) => { if (y < row.y + row.h + 2) text(s, x, y + 2, colour, { width }); y += 13; };
    const t = shown;
    switch (row.kind) {
      case "human": {
        const task = t === null ? null : row.lane.task[t];
        const tag = t === null ? null : row.lane.tag[t];
        if (task !== null) line(`${taskText(task)}${tag !== null && tag.tag !== "no fact" ? ` · ${tag.tag}` : ""}`);
        break;
      }
      case "belief": {
        if (row.off) { line("off", c.inkFaint); break; }
        const lead = t === null ? null : leading(row.lane, t);
        if (lead === null) { value("–", c.lineFaint); break; }
        value(lead.value.toFixed(2), bandText(softOf(colours, lead.key)));
        line(keyText(row.lane.robot, lead.key));
        const held = t === null ? null : row.lane.held[t];
        line(held === null ? "nothing held" : `held · ${keyText(row.lane.robot, held)}`, c.inkFaint);
        break;
      }
      case "tail": {
        if (row.off) { line("off", c.inkFaint); break; }
        const b2 = t === null ? null : row.lane.belief[t];
        const lead = b2 === null || b2.leader === null ? undefined : b2.live.find((h) => h.key === b2.leader);
        value(lead === undefined || lead.tail === null ? "–" : lead.tail.toFixed(2),
              lead === undefined || lead.tail === null ? c.lineFaint : bandText(softOf(colours, lead.key)));
        line(`α ${row.lane.robot.test_level}`, c.inkFaint);
        break;
      }
      case "finding": {
        if (row.off) { line("off", c.inkFaint); break; }
        // the finding's word sits beside the title, on the title's line
        const state = t === null ? null : findingAt(row.lane, t);
        if (state !== null) {
          ctx.font = font(theme.type.size.xs, theme.type.weight.medium); ctx.letterSpacing = "0.7px";
          const tw = ctx.measureText(b.title.toUpperCase()).width; ctx.letterSpacing = "0px";
          round(x + tw + 10, row.y + 1, 8, 8, 2, FINDING_COLOUR[state]);
          ctx.strokeStyle = c.lineFaint; ctx.lineWidth = 0.75;
          ctx.beginPath(); ctx.roundRect(x + tw + 10, row.y + 1, 8, 8, 2); ctx.stroke();
          text(state, x + tw + 22, row.y + 5.5, c.inkSoft);
        }
        break;
      }
      case "fact":
        if (!b.named) line(row.lane.fact);
        break;
      case "robot": {
        const task = t === null ? null : row.lane.task[t];
        line(`${task === null ? "no task" : taskText(task)}${t !== null && row.lane.hold[t] ? " · hold" : ""}`);
        break;
      }
      case "distance": {
        const s = t === null ? null : row.lane.separation[t];
        value(s === null ? "–" : s.minimum.toFixed(0), s === null ? c.lineFaint : s.below ? c.separation : c.ink);
        line(`min ${row.minSep}`, c.inkFaint);
        break;
      }
    }
  }

  function plot(row: Row) {
    switch (row.kind) {
      case "human":
        for (const b of humanBands(row.lane, n)) {
          const colour = softOf(colours, b.value.task.identity);
          band(b.start, b.end, row.y, row.h, colour, taskText(b.value.task));
          if (b.value.tag !== null && b.value.tag.tag !== "no fact") {
            const x0 = px(b.start) + 5, x1 = px(b.end + 1) - 5;
            if (x1 > x0) round(x0, row.y + row.h - 3, x1 - x0, 2, 1, TAG[b.value.tag.tag], 0.85);
          }
        }
        break;
      case "belief": {
        if (row.off) break;
        const robot = row.lane.robot;
        const top = row.y + BELIEF_TOP, h = row.h - BELIEF_TOP - 3;
        const y = (v: number) => top + (1 - v) * h;
        for (const b of heldBands(row.lane, n)) {
          round(px(b.start) + 0.5, row.y + 1, px(b.end + 1) - px(b.start) - 1, 3, 1.5, softOf(colours, b.value), 0.9);
        }
        hline(y(robot.theta), mix(c.robot, "#FFFFFF", 0.35), [3, 4]);
        text("θ", g.x0 - 6, y(robot.theta), c.robotDark, { align: "right" });
        const lines = beliefLines(row.lane, n);
        lead(row.lane, lines, y, top, top + h, true);
        legend(row.lane, row.y + 2);
        break;
      }
      case "tail": {
        if (row.off) break;
        const top = row.y + 3, h = row.h - 5;
        const y = (v: number) => top + (1 - v) * h;
        hline(y(row.lane.robot.test_level), c.separation, [0.1, 3.5], 1.4);
        text("α", g.x0 - 6, y(row.lane.robot.test_level), c.separation, { align: "right" });
        lead(row.lane, tailLines(row.lane, n), y, top, top + h, false);
        break;
      }
      case "finding": {
        if (row.off) break;
        for (const b of findingBands(row.lane, n)) {
          const x0 = px(b.start), w = px(b.end + 1) - px(b.start);
          round(x0, row.y, w, row.h, 3, FINDING_COLOUR[b.value]);
        }
        break;
      }
      case "fact":
        for (const b of trueBands(row.lane.holds, n)) band(b.start, b.end, row.y, row.h, c.inkSoft, row.lane.fact);
        break;
      case "robot": {
        const by = row.y + 3, bh = row.h - 3;
        for (const b of robotBands(row.lane, n)) band(b.start, b.end, by, bh, softOf(colours, b.value.identity), taskText(b.value));
        // a hold: the band hatched over its ticks
        for (const b of trueBands(row.lane.hold, n)) {
          ctx.save();
          ctx.beginPath(); ctx.roundRect(px(b.start) + 0.5, by, px(b.end + 1) - px(b.start) - 1, bh, 5); ctx.clip();
          ctx.strokeStyle = c.robotDark; ctx.globalAlpha = 0.42; ctx.lineWidth = 1;
          ctx.beginPath();
          for (let x = px(b.start) - bh; x < px(b.end + 1); x += 4) { ctx.moveTo(x, by + bh); ctx.lineTo(x + bh, by); }
          ctx.stroke(); ctx.restore();
        }
        // a decision: a small dot on the band's top edge
        for (let t = 0; t < n; t++) {
          if (row.lane.decision[t] === null) continue;
          ctx.fillStyle = "#FFFFFF"; ctx.beginPath(); ctx.arc(mid(t), row.y + 2, 3.2, 0, 2 * Math.PI); ctx.fill();
          ctx.fillStyle = c.robotDark; ctx.beginPath(); ctx.arc(mid(t), row.y + 2, 2, 0, 2 * Math.PI); ctx.fill();
        }
        break;
      }
      case "distance": {
        const top = row.y + 2, h = row.h - 4, span = SCALE * row.minSep;
        const y = (v: number) => top + (1 - Math.min(v, span) / span) * h;
        const rose = mix(c.separation, "#FFFFFF", 0.8);
        for (const b of trueBands(row.lane.separation.slice(0, n).map((s) => s?.below === true), n)) {
          round(px(b.start), row.y, px(b.end + 1) - px(b.start), row.h, 3, rose);
        }
        const ys = row.lane.separation.slice(0, n).map((s) => (s === null ? null : s.minimum));
        fade(ys, y, top, top + h, c.inkSoft, 0.16);
        hline(y(row.minSep), c.separation, [0.1, 3.5], 1.6);
        polyline(ys, y, c.inkSoft, theme.line.plot + 0.25);
        const now = shown === null ? null : row.lane.separation[shown];
        if (now !== null && shown !== null) dot(mid(shown), y(now.minimum), now.below ? c.separation : c.inkSoft);
        break;
      }
    }
  }

  /** A robot's per-hypothesis lines (the belief or S): the others thin and grey, the hypotheses that have led in their
   * colours; under the shown tick's leader a gradient where `area` (the belief), and a dot at the shown tick. */
  function lead(lane: RobotLane, lines: Map<string, (number | null)[]>, y: (v: number) => number, top: number, foot: number,
                area: boolean) {
    const keys = [...lines.keys()];
    for (const k of keys.filter((k) => !lane.leaders.has(k))) polyline(lines.get(k)!, y, c.lineFaint, theme.line.plotFaint);
    const leader = shown === null ? null : lane.belief[shown]?.leader ?? null;
    if (area && leader !== null && lines.has(leader)) fade(lines.get(leader)!, y, top, foot, softOf(colours, leader), 0.22);
    for (const k of keys.filter((k) => lane.leaders.has(k))) polyline(lines.get(k)!, y, softOf(colours, k), theme.line.plotLead);
    const v = leader === null || shown === null ? null : lines.get(leader)?.[shown] ?? null;
    if (leader !== null && shown !== null && v !== null) dot(mid(shown), y(v), softOf(colours, leader));
  }

  /** The belief plot's legend, at its top right: each hypothesis that has led, its colour and its name; "others" in grey. */
  function legend(lane: RobotLane, y: number) {
    const items: [string, string][] = lane.robot.hypotheses.filter((h) => lane.leaders.has(h.key))
      .map((h) => [softOf(colours, h.key), keyText(lane.robot, h.key)]);
    if (lane.robot.hypotheses.length > items.length) items.push([c.lineFaint, "others"]);
    ctx.font = font(theme.type.size.xs);
    const widths = items.map(([, name]) => ctx.measureText(name).width + 22);
    const total = widths.reduce((a, w) => a + w, 0) + 8;
    let x = g.x1 - total;
    round(x - 4, y, total + 4, 16, 8, "#FFFFFF", 0.8);
    items.forEach(([colour, name], i) => {
      round(x + 6, y + 7, 10, 2.5, 1.25, colour);
      text(name, x + 20, y + 8.5, c.inkSoft);
      x += widths[i];
    });
  }

  // =========================================================================
  // The axis, the latest tick, the viewed tick
  // =========================================================================

  const step = axisStep(g, end);
  for (let t = 0; t <= end; t += step) text(`${t}`, px(t), g.axisY + 9, c.inkFaint, { align: "center" });
  const first = g.boxes[0]?.y ?? 0;
  const last = g.boxes.length === 0 ? 0 : g.boxes[g.boxes.length - 1].y + g.boxes[g.boxes.length - 1].h;
  if (n > 0) {
    ctx.strokeStyle = c.ink; ctx.globalAlpha = 0.45; ctx.lineWidth = theme.line.guide;
    ctx.beginPath(); ctx.moveTo(Math.round(mid(n - 1)) + 0.5, first); ctx.lineTo(Math.round(mid(n - 1)) + 0.5, last); ctx.stroke();
    ctx.globalAlpha = 1;
  }
  if (viewed !== null && viewed < n) {
    ctx.strokeStyle = c.past; ctx.lineWidth = theme.line.viewed;
    ctx.beginPath(); ctx.moveTo(mid(viewed), first); ctx.lineTo(mid(viewed), last); ctx.stroke();
    ctx.font = font(theme.type.size.xs, theme.type.weight.medium);
    const label = `${viewed}`;
    const w = ctx.measureText(label).width + 12;
    round(mid(viewed) - w / 2, g.axisY + 1, w, 16, 8, c.past);
    text(label, mid(viewed), g.axisY + 9.5, "#FFFFFF", { align: "center", weight: theme.type.weight.medium });
  }
}

function rowName(r: Row): string {
  return r.kind === "human" ? r.lane.human : r.kind === "fact" ? r.lane.fact
    : r.kind === "distance" ? `${r.lane.robot}–${r.lane.human}` : r.lane.robot.robot;
}
