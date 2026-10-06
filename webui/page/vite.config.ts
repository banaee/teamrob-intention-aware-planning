import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The page is served built by the web-ui's server (mesa_sim/run_webui.py, T-viz 1a). During the page's development,
// Vite's dev server passes /api/ to a server running on port 8000.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, strictPort: true, proxy: { "/api": "http://127.0.0.1:8000" } },
});
