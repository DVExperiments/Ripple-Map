# Ripple Map v1.0

**Everything is connected.** An interactive, visual systems-thinking learning lab by DV Experiments.

Ripple Map helps learners discover the people, infrastructure, materials, rules, ecosystems and information that support a familiar technology or public service. Unlike a static concept map, it invites them to investigate actual relationships in a curated starter model, test hypothetical disruptions and make their own systems-thinking hypotheses.

## Quick start / local preview

1. Download and unzip the project.
2. **Windows:** double-click `Preview_on_Windows.bat` (uses Python's built-in `http.server`; Python 3.10+ required). Alternatively, **double-click `index.html` directly** in any modern browser; the essential app works without a local server.
3. **macOS/Linux:** double-click `index.html`, or open a terminal in the folder and run `python3 preview.py`.
4. Pick a topic, reveal layers, examine nodes, try a failure, reflect, and export your work.

**No API keys, subscriptions, external APIs, libraries, signups or internet connectivity required for the local app.** The web edition uses HTML, CSS and plain JavaScript to run on GitHub Pages. Python is used for the optional preview launcher and maintainers' content generator/testing, not on the hosted website.

## Activity flow

### 1. Explore
- Start with the visible service, core technology and physical infrastructure.
- Switch on **Data & information**, **People & organisations**, **Rules & economics**, and **Ecology & materials** to reveal overlooked systems.
- Click nodes or use the accessible **Inspect** dropdown to explore *what supports what* and *why*.
- Follow arrows conceptually: **A → B (requires)** means this teaching model considers B dependent on A. Dotted lines indicate potential influences or effects rather than hard dependencies.
- Identify a critical supporting part and explain your reasoning.
- **Feedback loop:** an optional example illustrates possible reinforcing dynamics rather than a single straight-line chain.
- **Add your own element** or **Link two elements** to propose missing connections. These are labelled as **your hypotheses** and can be rearranged by dragging their nodes.

### 2. Stress test
- Choose one of three curated disruption scenarios per map.
- A deterministic graph trace identifies **downstream elements at risk along declared required-support links**, and highlights them in the graph.
- This is not a physical simulation, an engineering assessment, or a prediction of real-world failures. Actual systems may have redundancy, alternative supply, delays and compensating behaviour not included in these simplified maps.
- Suggest a resilience/adaptation response and identify a trade-off or new dependency.

### 3. Reflect
- Define your system boundary, consider stakeholders and power, look for second-order effects, and write a research question about an uncertain connection.
- Select **Complete investigation** to save a snapshot in **My maps**.

### 4. Review
- A 100-point **activity-completion indicator** shows which steps were attempted. This is *not a grade of the factual correctness, ethics or quality of a map*.
- Export **Markdown portfolio notes**, an editable **SVG map**, or a **PNG image**.
- Reopen completed maps in the history area; export / import your data as JSON.

## Seven system maps (v1.0)

| Map | What learners examine |
|---|---|
| Everyday AI Assistant | Electricity, compute, data, operators, policy and environmental resource needs |
| Public EV Charging Network | Grid capacity, sites, interoperability, payments and driver confidence |
| Safe Urban Water Supply | Catchment ecology, treatment, pipes, workers, rules and community trust |
| Contactless Card Payment | Hardware, authorisation networks, banks, fraud controls and inclusion |
| Video Healthcare Consultation | Connectivity, care work, privacy, access and clinical responsibilities |
| Community Solar Microgrid | Solar generation, storage, power controls, governance and reliability |
| Satellite Navigation | Satellites, clocks, maps, ground systems, rules and user's decisions |

**Content:** 137 curated system elements, 155 relationships, 21 hypothetical disruptions, and seven illustrative feedback loops. These maps are starter teaching models, not comprehensive or live engineering diagrams. Different technologies may have different architectures and requirements in real contexts.

## Publish to GitHub Pages

1. Create a **public** GitHub repository named `Ripple-Map` (or choose your own name).
2. Extract this ZIP and upload **the files inside the extracted directory**, not the outer directory itself, to the **repository root**. `index.html` must appear in the root alongside `dv-project.json`, `assets/` and `README.md`.
3. GitHub repository → **Settings → Pages → Build and deployment → Deploy from a branch**. Select `main` and `/(root)`, then Save.
4. If using `dvexperiments` as your GitHub username and `Ripple-Map` as the repository name, the expected URL is **https://dvexperiments.github.io/Ripple-Map/**. The site will become live only after GitHub has deployed it.
5. `dv-project.json` is included with title, summary, cover, highlight features and `embed: true` for your existing DV Experiments auto-sync dashboard. Your dashboard must have access to this public repository to discover it.

You can also embed the published URL in a Wix site or other page using an iframe if that website supports embeds. Each user's saved content stays in **their own browser** (not shared among users).

## How the system model works

- Every node is assigned one of six category lenses, or is the central service.
- Every link has a source, target, type (`requires`, `influences`, `affects`) and authored explanation.
- Cascading-impact highlights follow **only** directed `requires` links, using breadth-first graph traversal. Highlighting communicates **potential exposure through the model**, not assured failure, severity, probabilities or time dynamics.
- Dotted `influences` and `affects` links invite analysis of people, ecology, governance and indirect consequences but are **not** automatically treated as deterministic failure chains.
- Feedback loops are curated illustrative stories; do not infer an independently validated causal loop from their presence.
- A user-created node and relationship expresses a hypothesis. They are saved with the student's draft in the browser and included in exports.

### Transparent 100-point rubric

| Activity | Maximum points |
|---|---:|
| Investigate up to 10 elements | 20 |
| Reveal the six system lenses | 15 |
| Mark a critical element | 10 |
| Explain that selection | 15 |
| Test a disruption | 10 |
| Suggest an adaptation and trade-off | 10 |
| Answer four reflection questions | 20 |
| **Total** | **100** |

Answers are not automatically fact-checked or judged by an AI. The feedback encourages reflection and enquiry rather than giving false certainty.

## Contents

```
index.html               Application entry point (upload to root)
assets/app.js            Interface and interactions
assets/engine.js         Dependency tracing, layout and activity-completion rubric
assets/content.js        Browser-ready content (generated)
assets/content.json      Curated scenario and relationship data
assets/styles.css        Responsive interface
assets/cover.svg         Dashboard cover art
assets/icon.svg          App icon
sw.js                    Offline cache after first hosted visit
manifest.webmanifest     Browser install metadata
dv-project.json          DV Experiments dashboard metadata
preview.py               Optional Python HTTP preview
Preview_on_Windows.bat    Windows double-click preview
DEPLOY_QUICK_START.txt   Plain-language deployment instructions
tools/generate_content.py  Edit and regenerate case studies (Python standard library)
tests/test_engine.cjs    JavaScript unit tests (developer only)
tests/test_browser.py    Browser integration tests (Playwright needed only for development)
```

## Privacy, accessibility and limitations

- No telemetry, login, API calls, third-party libraries or advertisements. Work is stored locally via `localStorage`. Export backups before clearing your browser data or switching devices. Private browsing or storage restrictions may prevent persistence.
- Map nodes can be inspected through a normal HTML dropdown or via keyboard (Tab / Enter) as an alternative to direct mouse/touch interactions. Actions are also available through buttons, and text alternatives describe relationship reasons.
- The interface adapts to phone screens. The visual map pans and zooms; mobile readers can use the list-based inspector below it.
- Local opening via `file://` works for core features; an optional localhost or hosted preview is more reliable for persistent storage and PNG exports. Service-worker offline caching runs only in supported secure contexts after the first hosted visit; it does not apply to `file://`.
- No live technical documentation is fetched. Content is an educational simplification that should be challenged and extended with recent, local or discipline-specific evidence before using it for real decisions.
- When teaching in Aotearoa New Zealand, consider Te Tiriti, Indigenous authority, local governance, environmental responsibilities and whose knowledge is absent. The maps intentionally do not claim to represent specific iwi/hapū positions.

## Suggested 15–25 minute classroom use

1. **3 min:** Ask what a technology requires beyond the obvious device or interface.
2. **5 min:** Reveal two extra lenses and trace the support behind the service.
3. **5 min:** Compare critical dependencies in pairs; ask why opinions differ.
4. **5 min:** Stress-test a failure and discuss possible alternate paths and trade-offs.
5. **5 min:** Add one missing system element and export a map / reflection to the MTF Digital Portfolio.

## License

MIT (see `LICENSE`). Scenario content and explanations are provided for general educational purposes. Author: DV Experiments, 2026.
