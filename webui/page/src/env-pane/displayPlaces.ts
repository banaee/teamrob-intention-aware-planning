/**
 * Display places (glossary §11; handoff section 9): where the page draws each movable object inside the footprint of
 * the fixed object that holds it. A display convention, not a world fact: in the world every movable object in a
 * container has exactly the container's position. Never written anywhere.
 *
 * The rule: the objects fill a grid over the footprint in their order of arrival (the tick update's
 * `fixed_object_contents`; at the start the setup's order), row by row from the north-west corner. Of the grids that
 * hold the objects at their own size inside the footprint, the one whose shape is nearest the footprint's; the gap
 * between two objects shrinks to what the footprint leaves. When no grid fits, the nearest shape, and the objects
 * overlap. An object keeps its own size.
 *
 * Stage 1a keeps an object's place while it stays (requirement 2): this function gives the places of one list; the
 * page's state keeps them from tick to tick.
 */

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

const GAP_SHARE = 0.12;   // the gap between two objects, as a share of the larger object's extent

export function displayPlaces(footprint: Footprint, sizes: readonly Extent[]): Place[] {
  const n = sizes.length;
  if (n === 0) return [];
  const mx = Math.max(...sizes.map((s) => s.x));
  const my = Math.max(...sizes.map((s) => s.y));
  const gap = GAP_SHARE * Math.max(mx, my);
  const cellX = mx + gap;
  const cellY = my + gap;

  const fits = (c: number) => c * mx <= footprint.sx && Math.ceil(n / c) * my <= footprint.sy;
  const misfit = (c: number) =>      // how far the grid's shape is from the footprint's
    Math.abs(Math.log((c * cellX) / (Math.ceil(n / c) * cellY) / (footprint.sx / footprint.sy)));
  const counts = Array.from({ length: n }, (_, i) => i + 1);
  const fitting = counts.filter(fits);
  const columns = (fitting.length > 0 ? fitting : counts).reduce((a, b) => (misfit(b) < misfit(a) ? b : a));
  const rows = Math.ceil(n / columns);
  const stepX = Math.min(cellX, columns > 1 ? (footprint.sx - mx) / (columns - 1) : cellX);
  const stepY = Math.min(cellY, rows > 1 ? (footprint.sy - my) / (rows - 1) : cellY);

  return sizes.map((_, i) => {
    const column = i % columns;
    const row = Math.floor(i / columns);
    return {
      x: footprint.x + (column - (columns - 1) / 2) * stepX,
      y: footprint.y - (row - (rows - 1) / 2) * stepY,     // row 0 to the north
    };
  });
}
