/**
 * The scene appearance of one domain (webui/appearance.py): an object type's look, or the default look for a type with
 * no entry; and, since T-viz 1a (iii), its look by state: the first of the type's looks by state whose state holds for
 * the object at the tick replaces the type's look. The page knows forms, never a domain's object types or states:
 * which type takes which form, and which state another form, is data compared by name.
 *
 * A movable object's tint (the scene's cleaning of 9 October 2026): a look by state's own tint, whatever the object's
 * subtype; otherwise its type's tint for its subtype, or its type's tint. Its drawn footprint: its size times its
 * type's `footprint_scale`, a display size only.
 */

import type { Appearance, Extent, FixedLook, MovableLook, ObjectState } from "../gen/messages";

/** The states that hold at a moment, per object. */
export type StatesHeld = ReadonlyMap<string, ReadonlySet<string>>;

const NONE: ReadonlySet<string> = new Set();

export function statesHeld(states: readonly ObjectState[]): StatesHeld {
  const held = new Map<string, Set<string>>();
  for (const s of states) {
    if (s.object === null) continue;
    if (!held.has(s.object)) held.set(s.object, new Set());
    held.get(s.object)!.add(s.state);
  }
  return held;
}

export function fixedLook(appearance: Appearance, type: string, held: ReadonlySet<string> = NONE): FixedLook {
  const entry = appearance.fixed[type];
  if (entry === undefined) return appearance.default_fixed;
  return entry.states.find((s) => held.has(s.state))?.look ?? entry;
}

export function movableLook(appearance: Appearance, type: string, held: ReadonlySet<string> = NONE,
                            subtype: string | null = null): MovableLook {
  const entry = appearance.movable[type];
  if (entry === undefined) return appearance.default_movable;
  const byState = entry.states.find((s) => held.has(s.state))?.look;
  if (byState !== undefined) return byState;
  return { shape: entry.shape, height: entry.height,
           tint: (subtype === null ? undefined : entry.subtype_tints[subtype]) ?? entry.tint };
}

/** A movable object's drawn footprint: its size times its type's share; its size for a type with no entry. */
export function drawnSize(appearance: Appearance, type: string, size: Extent): Extent {
  const scale = appearance.movable[type]?.footprint_scale ?? 1;
  return { x: size.x * scale, y: size.y * scale };
}

/** The states held by one object (none when it holds none). */
export function heldBy(held: StatesHeld, object: string): ReadonlySet<string> {
  return held.get(object) ?? NONE;
}
