/**
 * Panel 4c, version A: the page's own drawing on one canvas (T-viz 1c, the two versions). Flat and crisp, in the manner
 * of the scene's line drawing: soft tinted boxes, a faint dashed grid, bands as light tints of the task's colour with
 * the task's text in its deepened tone, lines only for the hypotheses that have led with a gradient fading under them, a
 * hold hatched over the robot's band, a decision a small dot; a dot at the shown tick and a large number beside the
 * belief and the distance. Geometry and colours: src/plots/look.ts.
 */

import type { TaskColours } from "../frame/colours";
import { keyText } from "../frame/robot";
import { taskText } from "../frame/activity";
import type { TagValue } from "../gen/messages";
import { theme } from "../theme";
import { beliefLines, heldBands, humanBands, type Lanes, robotBands, trueBands } from "./lanes";
import {
  ACCENT, axisStep, bandFill, bandText, BELIEF_TOP, type Box, type Geometry, LABEL, leading, mix, PAD, RADIUS, SCALE, shownTick,
  softOf, toneOf, xOf,
} from "./look";

const TAG: Record<TagValue, string> = {
  "in accord": theme.color.tagAccord,
  "not in accord": theme.color.tagNotAccord,
  "no fact": theme.color.lineFaint,
};

export function drawA(ctx: CanvasRenderingContext2D, g: Geometry, lanes: Lanes, colours: TaskColours, end: number,
                      viewed: number | null): void {
  const c = theme.color;
  const n = lanes.length;
  const px = (t: number) => xOf(g, end, t);
  const mid = (t: number) => px(t + 0.5);
  const step = axisStep(g, end);
  ctx.clearRect(0, 0, g.width, g.height);
  ctx.textBaseline = "middle";
  const font = (size: number, weight: number = theme.type.weight.regular) => `${weight} ${size}px ${theme.type.family}`;
  const text = (s: string, x: number, y: number, colour: string, opts: { size?: number; weight?: number;
    align?: CanvasTextAlign; spacing?: string } = {}) => {
    ctx.font = font(opts.size ?? theme.type.size.xs, opts.weight);
    ctx.fillStyle = colour; ctx.textAlign = opts.align ?? "left";
    ctx.letterSpacing = opts.spacing ?? "0px";
    ctx.fillText(s, x, y);
    ctx.letterSpacing = "0px";
  };
  const round = (x: number, y: number, w: number, h: number, r: number, fill: string, alpha = 1) => {
    ctx.globalAlpha = alpha; ctx.fillStyle = fill;
    ctx.beginPath(); ctx.roundRect(x, y, Math.max(1, w), h, Math.min(r, w / 2, h / 2)); ctx.fill();
    ctx.globalAlpha = 1;
  };
  /** A band from tick a to tick b, a light tint of `colour`, its text inside where it fits. */
  const band = (a: number, b: number, y: number, h: number, colour: string, label: string | null) => {
    const x0 = px(a) + 0.5, w = px(b + 1) - px(a) - 1;
    round(x0, y, w, h, 4, bandFill(colour));
    if (label === null) return;
    ctx.font = font(theme.type.size.xs, theme.type.weight.medium);
    if (ctx.measureText(label).width + 12 < w) {
      text(label, x0 + 6, y + h / 2 + 0.5, bandText(colour), { weight: theme.type.weight.medium });
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
  const hline = (y: number, colour: string, dash: number[], weight: number = theme.line.guide) => {
    ctx.save(); ctx.strokeStyle = colour; ctx.lineWidth = weight; ctx.setLineDash(dash); ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(g.x0, y); ctx.lineTo(g.x1, y); ctx.stroke(); ctx.restore();
  };

  /** A soft gradient under a line, from `alpha` at the top of the lane to nothing at its foot. */
  const fade = (ys: readonly (number | null)[], y: (v: number) => number, foot: number, colour: string, alpha: number) => {
    const gradient = ctx.createLinearGradient(0, foot - 90, 0, foot);
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
  /** The dot at the shown tick: the colour inside a white ring, a soft halo around it. */
  const dot = (x: number, y: number, colour: string) => {
    ctx.fillStyle = colour + "1F"; ctx.beginPath(); ctx.arc(x, y, 7, 0, 2 * Math.PI); ctx.fill();
    ctx.fillStyle = "#FFFFFF"; ctx.beginPath(); ctx.arc(x, y, 5, 0, 2 * Math.PI); ctx.fill();
    ctx.fillStyle = colour; ctx.beginPath(); ctx.arc(x, y, 3.4, 0, 2 * Math.PI); ctx.fill();
  };
  /** A large number in the box's right column, a short caption under it. */
  const big = (value: string, caption: string | null, y: number, colour: string) => {
    const x = g.x1 + 18, w = g.width - PAD - x - 10;
    text(value, x, y, colour, { size: theme.type.size.xxl, weight: theme.type.weight.medium });
    if (caption === null) return;
    ctx.font = font(theme.type.size.xs);
    let shown = caption;
    while (shown.length > 1 && ctx.measureText(shown).width > w) shown = shown.slice(0, -2) + "…";
    text(shown, x, y + 22, c.inkSoft);
  };
  const shown = shownTick(lanes, viewed);

  for (const box of g.boxes) drawBox(box);

  function drawBox(box: Box) {
    const tone = toneOf(box.tone);
    const x = PAD, w = g.width - 2 * PAD;
    // the box: its tint, its left edge, its title
    ctx.save();
    ctx.beginPath(); ctx.roundRect(x, box.y, w, box.h, RADIUS); ctx.clip();
    ctx.fillStyle = tone.fill; ctx.fillRect(x, box.y, w, box.h);
    ctx.fillStyle = tone.edge; ctx.fillRect(x, box.y, ACCENT, box.h);
    // a faint dashed grid at the axis' numbers
    ctx.strokeStyle = c.lineFaint; ctx.lineWidth = 1; ctx.setLineDash([2, 5]);
    for (let t = step; t < end; t += step) {
      ctx.beginPath(); ctx.moveTo(Math.round(px(t)) + 0.5, box.y + 6); ctx.lineTo(Math.round(px(t)) + 0.5, box.y + box.h - 6); ctx.stroke();
    }
    ctx.restore();
    text(box.title.toUpperCase(), x + ACCENT + 9, box.y + 13, tone.title,
         { size: theme.type.size.xs, weight: theme.type.weight.medium, spacing: "0.7px" });

    for (const row of box.rows) {
      const name = (s: string) => { if (box.named) text(s, PAD + LABEL - 8, row.y + Math.min(row.h, 18) / 2, c.inkFaint, { align: "right" }); };
      switch (row.kind) {
        case "human": {
          name(row.lane.human);
          for (const b of humanBands(row.lane, n)) {
            const colour = softOf(colours, b.value.task.identity);
            band(b.start, b.end, row.y, row.h, colour, taskText(b.value.task));
            if (b.value.tag !== null && b.value.tag.tag !== "no fact") {
              const x0 = px(b.start) + 4, x1 = px(b.end + 1) - 4;
              if (x1 > x0) round(x0, row.y + row.h - 3, x1 - x0, 2, 1, TAG[b.value.tag.tag], 0.8);
            }
          }
          break;
        }
        case "belief": {
          const robot = row.lane.robot;
          name(robot.robot);
          if (row.off) { text("off", g.x0 + 4, row.y + row.h / 2, c.inkFaint); break; }
          const top = row.y + BELIEF_TOP, h = row.h - BELIEF_TOP - 3;
          const y = (v: number) => top + (1 - v) * h;
          for (const b of heldBands(row.lane, n)) {
            round(px(b.start) + 0.5, row.y + 2, px(b.end + 1) - px(b.start) - 1, 3, 1.5, softOf(colours, b.value), 0.9);
          }
          hline(y(robot.theta), mix(c.robot, "#FFFFFF", 0.35), [3, 4]);
          text("θ", g.x0 - 8, y(robot.theta), c.robotDark, { align: "right" });
          const lines = beliefLines(row.lane, n);
          const keys = [...lines.keys()];
          for (const k of keys.filter((k) => !row.lane.leaders.has(k))) polyline(lines.get(k)!, y, c.lineFaint, theme.line.plotFaint);
          // the gradient under the leader at the shown tick only, so that two fills never mix
          const leader = shown === null ? null : row.lane.belief[shown]?.leader ?? null;
          if (leader !== null && lines.has(leader)) fade(lines.get(leader)!, y, top + h, softOf(colours, leader), 0.24);
          for (const k of keys.filter((k) => row.lane.leaders.has(k))) polyline(lines.get(k)!, y, softOf(colours, k), theme.line.plotLead);
          // the leader at the shown tick: a dot on its line, a large number beside the box, its name under it
          const lead = shown === null ? null : leading(row.lane, shown);
          if (lead !== null && shown !== null) {
            const colour = softOf(colours, lead.key);
            dot(mid(shown), y(lead.value), colour);
            big(lead.value.toFixed(2), keyText(robot, lead.key), row.y + 16, bandText(colour));
          } else big("–", null, row.y + 16, c.lineFaint);
          break;
        }
        case "fact": {
          name(row.lane.fact);
          for (const b of trueBands(row.lane.holds, n)) band(b.start, b.end, row.y, row.h, c.inkSoft, row.lane.fact);
          break;
        }
        case "robot": {
          name(row.lane.robot.robot);
          const by = row.y + 3, bh = row.h - 3;
          for (const b of robotBands(row.lane, n)) band(b.start, b.end, by, bh, softOf(colours, b.value.identity), taskText(b.value));
          // a hold: the band hatched over its ticks
          for (const b of trueBands(row.lane.hold, n)) {
            ctx.save();
            ctx.beginPath(); ctx.roundRect(px(b.start) + 0.5, by, px(b.end + 1) - px(b.start) - 1, bh, 4); ctx.clip();
            ctx.strokeStyle = c.robotDark; ctx.globalAlpha = 0.45; ctx.lineWidth = 1;
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
          name(`${row.lane.robot}–${row.lane.human}`);
          const top = row.y + 2, h = row.h - 4, span = SCALE * row.minSep;
          const y = (v: number) => top + (1 - Math.min(v, span) / span) * h;
          const rose = mix(c.separation, "#FFFFFF", 0.8);
          for (const b of trueBands(row.lane.separation.slice(0, n).map((s) => s?.below === true), n)) {
            round(px(b.start), row.y, px(b.end + 1) - px(b.start), row.h, 2, rose);
          }
          // a soft area under the distance, then its line
          const ys = row.lane.separation.slice(0, n).map((s) => (s === null ? null : s.minimum));
          fade(ys, y, top + h, c.inkSoft, 0.16);
          hline(y(row.minSep), c.separation, [0.1, 3.5], 1.6);
          polyline(ys, y, c.inkSoft, theme.line.plot + 0.25);
          const now = shown === null ? null : row.lane.separation[shown];
          if (now !== null && shown !== null) {
            dot(mid(shown), y(now.minimum), now.below ? c.separation : c.inkSoft);
            big(now.minimum.toFixed(0), `min ${row.minSep}`, row.y + 16, now.below ? c.separation : c.ink);
          } else big("–", null, row.y + 16, c.lineFaint);
          break;
        }
      }
    }
  }

  // the axis' numbers
  for (let t = 0; t <= end; t += step) text(`${t}`, px(t), g.axisY + 9, c.inkFaint, { align: "center" });

  // the latest tick through all boxes, a dot at its head; the viewed earlier tick in the past colour
  const first = g.boxes[0]?.y ?? 0;
  const last = g.boxes.length === 0 ? 0 : g.boxes[g.boxes.length - 1].y + g.boxes[g.boxes.length - 1].h;
  if (n > 0) {
    ctx.strokeStyle = c.ink; ctx.globalAlpha = 0.5; ctx.lineWidth = theme.line.guide;
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
