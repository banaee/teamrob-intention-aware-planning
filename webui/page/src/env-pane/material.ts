/**
 * The scene's one surface material: flat faces without lights, coloured by the way a face is turned (the illustration
 * look of sketch J). Three tones: the face toward the sky, the side toward the light, the side away from it; the side
 * away from the light is hatched with thin diagonal lines in screen space, so the hatching keeps its density at every
 * zoom, as a pen drawing does. The light comes from the north-west: in the tilted view (seen from the south-east) the
 * south faces are light and the east faces shaded; in the view from above only the tops show.
 *
 * Scene axes: x is the layout's x, y is up, z is minus the layout's y (north is -z).
 */

import * as THREE from "three";

export interface Tone {
  top: string;
  light: string;
  shade: string;
  hatch: string | null;    // null: the shaded side is not hatched
}

const shared = {
  uPixelRatio: { value: 1 },
};

/** The device's pixel ratio as a uniform, for another material hatched in screen space (src/env-pane/Paths.tsx). */
export const pixelRatioUniform = shared.uPixelRatio;

/** The hatching's spacing follows the device's pixels; set once per frame size. */
export function setPixelRatio(ratio: number): void {
  shared.uPixelRatio.value = ratio;
}

const vertexShader = /* glsl */ `
  #include <common>
  #include <clipping_planes_pars_vertex>
  varying vec3 vNormalWorld;
  void main() {
    vNormalWorld = normalize(mat3(modelMatrix) * normal);
    #include <begin_vertex>
    #include <project_vertex>
    #include <clipping_planes_vertex>
  }
`;

const fragmentShader = /* glsl */ `
  #include <common>
  #include <clipping_planes_pars_fragment>
  uniform vec3 uTop;
  uniform vec3 uLight;
  uniform vec3 uShade;
  uniform vec3 uHatch;
  uniform float uHatchOn;
  uniform float uSpacing;
  uniform float uWidth;
  uniform float uPixelRatio;
  uniform float uOpacity;
  varying vec3 vNormalWorld;
  void main() {
    #include <clipping_planes_fragment>
    vec3 n = normalize(vNormalWorld);
    vec3 colour;
    if (n.y > 0.6) {
      colour = uTop;
    } else if (n.y < -0.6) {
      colour = uShade;
    } else {
      vec2 h = normalize(n.xz + vec2(1e-5));
      bool shaded = (h.x - h.y) > 0.0;          // more east than south
      colour = shaded ? uShade : uLight;
      if (shaded && uHatchOn > 0.5) {
        float period = uSpacing * uPixelRatio;
        float u = (gl_FragCoord.x - gl_FragCoord.y) * 0.70710678;
        float d = abs(mod(u, period) - 0.5 * period);
        float half_w = 0.5 * uWidth * uPixelRatio;
        float a = 1.0 - smoothstep(half_w - 0.5, half_w + 0.5, d);
        colour = mix(colour, uHatch, a);
      }
    }
    gl_FragColor = vec4(colour, uOpacity);
    #include <colorspace_fragment>
  }
`;

const cache = new Map<string, THREE.ShaderMaterial>();

/** The material of a tone; one instance per tone, spacing and opacity. */
export function illustration(tone: Tone, hatch: { spacing: number; width: number }, opacity = 1): THREE.ShaderMaterial {
  const key = JSON.stringify([tone, hatch, opacity]);
  const found = cache.get(key);
  if (found) return found;
  const material = new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms: {
      uTop: { value: new THREE.Color(tone.top) },
      uLight: { value: new THREE.Color(tone.light) },
      uShade: { value: new THREE.Color(tone.shade) },
      uHatch: { value: new THREE.Color(tone.hatch ?? tone.shade) },
      uHatchOn: { value: tone.hatch === null ? 0 : 1 },
      uSpacing: { value: hatch.spacing },
      uWidth: { value: hatch.width },
      uOpacity: { value: opacity },
      uPixelRatio: shared.uPixelRatio,
    },
    transparent: opacity < 1,
    depthWrite: opacity >= 1,
    // Faces sit a little behind their own outlines, so an edge is never cut by the face it bounds.
    polygonOffset: true,
    polygonOffsetFactor: 1,
    polygonOffsetUnits: 1,
  });
  cache.set(key, material);
  return material;
}
