import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The deck imports the web-ui page's own source modules (../webui/page/src). Those import react, three and
// @react-three/*, which would resolve from webui/page/node_modules: two copies of React and of R3F, and the hooks
// break. `dedupe` resolves them from the deck's own node_modules, at the same pinned versions (scripts/pins.mjs).
// fs.allow: the repository's root (relative to the deck's root), whose webui/page/src and domains/ the deck reads.

export default defineConfig({
  base: "./",
  plugins: [react()],
  resolve: { dedupe: ["react", "react-dom", "three", "@react-three/fiber", "@react-three/drei"] },
  server: { port: 5174, strictPort: true, host: "127.0.0.1", fs: { allow: [".."] } },
  preview: { port: 4173, strictPort: true, host: "127.0.0.1" },
});
