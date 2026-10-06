import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The page is static: it reads the exported samples from public/samples/ (T-viz 0.3). Stage 1a adds the server.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, strictPort: true },
});
