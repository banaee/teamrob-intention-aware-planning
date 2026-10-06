/**
 * Display places (src/env-pane/places.ts; plan_T-viz_1a.md, section 4, "Freed display places"): the grid numbered from the centre
 * outward; a place kept while its object stays; a freed place taken by the next arrival; layers beyond the grid.
 */

import { describe, expect, it } from "vitest";

import { EMPTY_BOOK, foldBook, nextBook, placeGrid, slotOf } from "../src/env-pane/places";

const box = (fixed_object: string, ...movable_objects: string[]) => ({ fixed_object, movable_objects });

describe("the grid", () => {
  it("holds the most places of the largest object, the nearest the centre first", () => {
    // 3 x 3 places of 20 x 20 with a gap of 2.4 on a 70 x 70 footprint at (100, 0)
    const grid = placeGrid({ x: 100, y: 0, sx: 70, sy: 70 }, { x: 20, y: 20 });
    expect(grid).toHaveLength(9);
    expect(grid[0]).toEqual({ x: 100, y: 0 });
    // then the four at one step, row by row from the north-west: north, west, east, south
    expect(grid.slice(1, 5).map((p) => [Math.round((p.x - 100) * 10) / 10, Math.round(p.y * 10) / 10])).toEqual([[0, 22.4], [-22.4, 0], [22.4, 0], [0, -22.4]]);
    // then the corners from the north-west
    expect(grid.slice(5).map((p) => [Math.sign(p.x - 100), Math.sign(p.y)])).toEqual([[-1, 1], [1, 1], [-1, -1], [1, -1]]);
  });

  it("has one place when the largest object does not fit, and puts a lone object half a place off an even middle", () => {
    expect(placeGrid({ x: 0, y: 0, sx: 10, sy: 10 }, { x: 20, y: 20 })).toEqual([{ x: 0, y: 0 }]);
    const two = placeGrid({ x: 0, y: 0, sx: 45, sy: 20 }, { x: 20, y: 20 });
    expect(two).toHaveLength(2);
    expect(two[0].x).toBeCloseTo(-11.2);       // equal distances: the western first
  });
});

describe("the book", () => {
  it("fills the places from the first in the order of arrival, and keeps them while the objects stay", () => {
    let book = nextBook(EMPTY_BOOK, [box("rack_a", "a", "b", "c")]);
    expect([...book.get("rack_a")!]).toEqual([["a", 0], ["b", 1], ["c", 2]]);
    book = nextBook(book, [box("rack_a", "a", "c")]);            // b left
    expect([...book.get("rack_a")!]).toEqual([["a", 0], ["c", 2]]);
    book = nextBook(book, [box("rack_a", "a", "c", "d", "e")]);  // d takes b's freed place, e the next free one
    expect([...book.get("rack_a")!]).toEqual([["a", 0], ["c", 2], ["d", 1], ["e", 3]]);
    book = nextBook(book, [box("rack_b", "b")]);                 // rack_a empty, absent from the tick update
    expect(book.has("rack_a")).toBe(false);
    expect([...book.get("rack_b")!]).toEqual([["b", 0]]);
  });

  it("puts the objects beyond the grid on the next layer, on the places in the same order", () => {
    const grid = [{ x: 0, y: 0 }, { x: 1, y: 0 }];
    expect([0, 1, 2, 3, 4].map((n) => slotOf(grid, n))).toEqual([
      { x: 0, y: 0, layer: 0 }, { x: 1, y: 0, layer: 0 }, { x: 0, y: 0, layer: 1 }, { x: 1, y: 0, layer: 1 },
      { x: 0, y: 0, layer: 2 }]);
  });

  it("gives the same book from the same sequence", () => {
    const sequence = [[box("s", "a", "b")], [box("s", "b")], [box("s", "b", "c")], [box("s", "b", "c", "a")]];
    const fold = () => sequence.reduce(nextBook, EMPTY_BOOK);
    expect([...fold().get("s")!]).toEqual([...fold().get("s")!]);
    expect([...fold().get("s")!]).toEqual([["b", 1], ["c", 0], ["a", 2]]);
  });
});

describe("the fold over a sim-run's tick updates", () => {
  const sequence = [[box("s", "a", "b", "c")], [box("s", "a", "c")], [box("s", "a", "c", "d")], [box("s", "c", "d", "a")]];
  const whole = sequence.reduce(nextBook, EMPTY_BOOK);

  it("gives, one tick at a time, the book of the whole sequence at once (a reload keeps the picture)", () => {
    let fold = null;
    for (let n = 1; n <= sequence.length; n++) fold = foldBook(fold, "run_1", sequence.slice(0, n));
    expect([...fold!.book.get("s")!]).toEqual([...whole.get("s")!]);
    expect([...foldBook(null, "run_1", sequence).book.get("s")!]).toEqual([...whole.get("s")!]);
  });

  it("starts anew for another sim-run, or a shorter sequence", () => {
    const fold = foldBook(null, "run_1", sequence);
    const other = foldBook(fold, "run_2", [[box("s", "c", "d")]]);
    expect([...other.book.get("s")!]).toEqual([["c", 0], ["d", 1]]);
    const shorter = foldBook(fold, "run_1", sequence.slice(0, 1));
    expect([...shorter.book.get("s")!]).toEqual([["a", 0], ["b", 1], ["c", 2]]);
  });
});
