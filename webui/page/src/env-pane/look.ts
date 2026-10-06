/**
 * The scene appearance of one domain (webui/appearance.py): an object type's look, or the default look for a type with
 * no entry. The page knows forms, never a domain's object types; which type takes which form is data.
 */

import type { Appearance, FixedLook, MovableLook } from "../gen/messages";

export function fixedLook(appearance: Appearance, type: string): FixedLook {
  return appearance.fixed[type] ?? appearance.default_fixed;
}

export function movableLook(appearance: Appearance, type: string): MovableLook {
  return appearance.movable[type] ?? appearance.default_movable;
}
