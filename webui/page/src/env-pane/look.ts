/**
 * The scene appearance of one domain (webui/appearance.py): an object type's look, or the default look for a type with
 * no entry; and, since T-viz 1a (iii), its look by state: the first of the type's looks by state whose state holds for
 * the object at the tick replaces the type's look. The page knows forms, never a domain's object types or states:
 * which type takes which form, and which state another form, is data compared by name.
 */

import type { Appearance, FixedLook, MovableLook, ObjectState } from "../gen/messages";

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

export function movableLook(appearance: Appearance, type: string, held: ReadonlySet<string> = NONE): MovableLook {
  const entry = appearance.movable[type];
  if (entry === undefined) return appearance.default_movable;
  return entry.states.find((s) => held.has(s.state))?.look ?? entry;
}

/** The states held by one object (none when it holds none). */
export function heldBy(held: StatesHeld, object: string): ReadonlySet<string> {
  return held.get(object) ?? NONE;
}
