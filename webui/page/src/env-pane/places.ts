/**
 * Display places (glossary §11; handoff section 9; docs/handoffs/plan_T-viz_1a.md, section 4, "Freed display places"): where the page
 * draws each movable object inside the footprint of the fixed object that holds it. A display convention, not a world
 * fact: in the world every movable object in a container has exactly the container's position. Never written anywhere.
 *
 * The rule (T-viz 1a (iii)):
 * - Each fixed object has one grid of places over its footprint, fixed for the sim-run: the most places that hold the
 *   run's largest movable object at its own size, with the gap of the 0.3 trial between two.
 * - The places are numbered from the footprint's centre outward, nearest first; equal distances row by row from the
 *   north-west. A container with one object shows it in its middle, and no place moves.
 * - An arriving object takes the lowest-numbered free place and keeps it while it stays; a freed place is taken by the
 *   next arrival. At the start the setup's order fills the places from the first.
 * - More objects than places: the next ones go on a second layer, on the places in the same order, then a third.
 * - Determined by the sequence of tick updates (each fixed object's objects in their order of arrival), so the same
 *   sim-run always gives the same picture, a reload included.
 */

import type { FixedObjectContents } from "../gen/messages";

export interface Footprint {
  x: number;       // centre, the layout's x
  y: number;       // centre, the layout's y
  sx: number;      // extent along x
  sy: number;      // extent along y
}

export interface Extent {
  x: number;
  y: number;
}

export interface Place {
  x: number;
  y: number;
}

/** A place of a fixed object's grid, and the layer it is on (0 the lowest). */
export interface Slot extends Place {
  layer: number;
}

const GAP_SHARE = 0.12;   // the gap between two objects, as a share of the larger extent of the largest object
const EPSILON = 1e-6;

/** A fixed object's places, numbered from the centre outward; `largest` the run's largest movable extents. */
export function placeGrid(footprint: Footprint, largest: Extent): Place[] {
  const gap = GAP_SHARE * Math.max(largest.x, largest.y);
  const stepX = largest.x + gap;
  const stepY = largest.y + gap;
  const columns = Math.max(1, Math.floor((footprint.sx + gap + EPSILON) / stepX));
  const rows = Math.max(1, Math.floor((footprint.sy + gap + EPSILON) / stepY));
  const cells: { place: Place; row: number; column: number; distance: number }[] = [];
  for (let row = 0; row < rows; row++) {
    for (let column = 0; column < columns; column++) {
      const dx = (column - (columns - 1) / 2) * stepX;
      const dy = ((rows - 1) / 2 - row) * stepY;            // row 0 to the north
      cells.push({ place: { x: footprint.x + dx, y: footprint.y + dy }, row, column, distance: Math.hypot(dx, dy) });
    }
  }
  cells.sort((a, b) => (Math.abs(a.distance - b.distance) > EPSILON ? a.distance - b.distance
    : a.row !== b.row ? a.row - b.row : a.column - b.column));
  return cells.map((c) => c.place);
}

/** Per fixed object, the place number of each movable object in it (layer k holds numbers k·n to k·n + n − 1 of a
 * grid of n places). */
export type PlaceBook = ReadonlyMap<string, ReadonlyMap<string, number>>;

export const EMPTY_BOOK: PlaceBook = new Map();

/** The book brought to a tick: an object that left frees its number; an object that stays keeps it; an arriving one
 * (in the order of arrival) takes the lowest free number. */
export function nextBook(book: PlaceBook, contents: readonly FixedObjectContents[]): PlaceBook {
  const next = new Map<string, ReadonlyMap<string, number>>();
  for (const c of contents) {
    const before = book.get(c.fixed_object);
    const numbers = new Map<string, number>();
    const taken = new Set<number>();
    for (const id of c.movable_objects) {
      const n = before?.get(id);
      if (n !== undefined) { numbers.set(id, n); taken.add(n); }
    }
    let free = 0;
    for (const id of c.movable_objects) {
      if (numbers.has(id)) continue;
      while (taken.has(free)) free++;
      numbers.set(id, free);
      taken.add(free);
    }
    next.set(c.fixed_object, numbers);
  }
  return next;
}

/** Where a place number is drawn on a grid. */
export function slotOf(grid: readonly Place[], number: number): Slot {
  const place = grid[number % grid.length];
  return { ...place, layer: Math.floor(number / grid.length) };
}
