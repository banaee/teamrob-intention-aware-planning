import "@fontsource/ibm-plex-sans/400.css";
import "@fontsource/ibm-plex-sans/500.css";
import "@fontsource/ibm-plex-mono/400.css";
import "reveal.js/reveal.css";
import "./deck.css";

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { applyTheme } from "../../webui/page/src/theme";
import { Deck } from "./Deck";

applyTheme();
createRoot(document.getElementById("root")!).render(<StrictMode><Deck /></StrictMode>);
