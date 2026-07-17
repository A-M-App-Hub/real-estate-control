import { API_BASE } from "./lib/api";

export default function App() {
  return (
    <main style={{ fontFamily: "system-ui", padding: "2rem" }}>
      <h1><PROJECT_DISPLAY_NAME></h1>
      <p>Frontend React — API hub: <code>{API_BASE}</code></p>
    </main>
  );
}
