import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  // Hub App Space: path_prefix /{slug}/ — obrigatório para assets e API relativas.
  base: "/<REPO_NAME>/",
  build: {
    outDir: "../dist",
    emptyOutDir: true,
  },
});
