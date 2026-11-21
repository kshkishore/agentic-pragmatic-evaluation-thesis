/* Runs the thesis analysis in the browser with Pyodide (Python compiled to WebAssembly).
   It recreates the repository layout in Pyodide's virtual file system, then runs the
   repository's own scripts unchanged: study/analyze_v2.py, tools/tables_ch4.py and the figure scripts. */
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/";
importScripts(PYODIDE + "pyodide.js");

const RESULTS = ["contrast_j1.jsonl", "contrast_j2.jsonl", "pairwise_j1.jsonl", "robust_j1.jsonl",
  "genjudge_j1.jsonl", "genjudge_j2.jsonl", "gen_qwen3vl-2b.jsonl", "gen_smolvlm2-2.2b.jsonl",
  "metrics_contrast.json", "metrics_gen.json", "robust_subset.json"];
const TABLES = ["metrics", "j1conds", "mcnemar2", "devpost", "dims", "charts", "j2", "agree", "throughput", "gens", "pairwise", "robust"];
const FILES = [
  ["study/analyze_v2.py"], ["study/figures_v2.py"], ["study/fig_example.py"], ["study/golden_dataset_v2.json"],
  ["tools/tables_ch4.py"], ["tools/diagrams.py"],
  ...RESULTS.map(f => ["study/results/" + f]),
  ["study/results/summary_v2.json", "/repo/published/summary_v2.json"],
  ...TABLES.map(t => ["tables/" + t + ".md", "/repo/published/tables/" + t + ".md"]),
  ...Array.from({ length: 16 }, (_, i) => ["study/images/MM-" + String(i + 1).padStart(2, "0") + ".png", null, true]),
];
// analyze_v2.py imports one small helper from study/metrics.py; the full module loads torch and
// transformers, which are only needed for computing the metrics, so the helper is provided on its own.
const METRICS_STUB = `import re
def sentences(text):
    parts = re.split(r"(?<=[.!?])\\s+", text.strip())
    return [p for p in parts if p.strip()]
`;

const post = (type, data) => self.postMessage({ type, ...data });
let py = null;

async function step(id, label, fn) {
  post("step", { id, state: "run", label });
  const t0 = performance.now();
  try {
    const detail = await fn();
    post("step", { id, state: "done", label, secs: (performance.now() - t0) / 1000, detail });
  } catch (e) {
    post("step", { id, state: "fail", label, detail: String(e && e.message || e) });
    throw e;
  }
}

async function run(base) {
  await step("python", "Start Python in the browser", async () => {
    py = await loadPyodide({ stdout: s => post("log", { text: s }), stderr: s => post("log", { text: s }) });
    return "Python " + py.runPython("import sys; sys.version.split()[0]");
  });
  await step("packages", "Install numpy, pandas, scipy, scikit-learn, matplotlib, krippendorff", async () => {
    await py.loadPackage(["numpy", "pandas", "scipy", "scikit-learn", "matplotlib", "pillow", "micropip"]);
    const micropip = py.pyimport("micropip");
    await micropip.install("krippendorff");
    return "ready";
  });
  await step("data", "Download the dataset, logs and scripts from the repository", async () => {
    let bytes = 0;
    const mk = p => { const parts = p.split("/").slice(0, -1); let cur = ""; for (const s of parts) { if (!s) continue; cur += "/" + s; try { py.FS.mkdir(cur); } catch (_) {} } };
    await Promise.all(FILES.map(async ([src, dst, binary]) => {
      const r = await fetch(base + src, { cache: "no-store" });
      if (!r.ok) throw new Error("Could not download " + src + " (" + r.status + ")");
      const buf = new Uint8Array(await r.arrayBuffer()); bytes += buf.length;
      const target = dst || "/repo/" + src; mk(target); py.FS.writeFile(target, buf);
    }));
    py.FS.writeFile("/repo/study/metrics.py", METRICS_STUB);
    py.FS.mkdir("/repo/figures");
    return (FILES.length) + " files, " + (bytes / 1e6).toFixed(1) + " MB";
  });
  await step("analyze", "Recompute every statistic (study/analyze_v2.py)", async () => {
    await py.runPythonAsync(`
import os, sys, runpy, warnings
warnings.filterwarnings("ignore")
os.chdir("/repo/study"); sys.path.insert(0, "/repo/study")
runpy.run_path("/repo/study/analyze_v2.py", run_name="__main__")
`);
    return "summary_v2.json written";
  });
  await step("compare", "Compare with the published results", async () => {
    const res = py.runPython(`
import json
def cmp(x, y, p, out):
    if isinstance(x, dict):
        if not isinstance(y, dict): out.append(p); return
        for k in set(x) | set(y):
            if k not in x or k not in y: out.append(p + "/" + str(k))
            else: cmp(x[k], y[k], p + "/" + str(k), out)
    elif isinstance(x, list):
        if not isinstance(y, list) or len(x) != len(y): out.append(p); return
        for i, (u, v) in enumerate(zip(x, y)): cmp(u, v, f"{p}[{i}]", out)
    elif isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool):
        if abs(x - y) > 1e-6 * max(1.0, abs(x)): out.append(p)
    elif x != y: out.append(p)
def count(x):
    if isinstance(x, dict): return sum(count(v) for v in x.values())
    if isinstance(x, list): return sum(count(v) for v in x)
    return 1
a = json.load(open("/repo/published/summary_v2.json")); b = json.load(open("/repo/study/results/summary_v2.json"))
diffs = []; cmp(a, b, "", diffs)
json.dumps({"values": count(a), "diffs": len(diffs), "examples": diffs[:12]})
`);
    const r = JSON.parse(res);
    post("compare", r);
    return r.diffs === 0 ? "All " + r.values.toLocaleString() + " values identical" : r.diffs + " of " + r.values + " values differ";
  });
  await step("tables", "Rebuild the Chapter 4 tables (tools/tables_ch4.py)", async () => {
    py.FS.mkdir("/repo/tables");
    await py.runPythonAsync(`import runpy; runpy.run_path("/repo/tools/tables_ch4.py", run_name="__main__")`);
    const out = {}; let same = 0;
    for (const t of TABLES) {
      const a = py.FS.readFile("/repo/tables/" + t + ".md", { encoding: "utf8" });
      const b = py.FS.readFile("/repo/published/tables/" + t + ".md", { encoding: "utf8" });
      out[t] = { text: a, identical: a === b }; if (a === b) same++;
    }
    post("tables", { tables: out });
    return same + " of " + TABLES.length + " tables identical to the thesis";
  });
  await step("figures", "Redraw the figures (figures_v2.py, fig_example.py, diagrams.py)", async () => {
    await py.runPythonAsync(`
import os, runpy, matplotlib
matplotlib.use("Agg")
os.environ["FIG_DIR"] = "/repo/figures"
for s in ["/repo/study/figures_v2.py", "/repo/study/fig_example.py", "/repo/tools/diagrams.py"]:
    runpy.run_path(s, run_name="__main__")
`);
    const names = py.FS.readdir("/repo/figures").filter(n => n.endsWith(".png")).sort();
    const figs = names.map(n => ({ name: n, data: py.FS.readFile("/repo/figures/" + n) }));
    post("figures", { figs });
    return names.length + " figures";
  });
  const summary = py.FS.readFile("/repo/study/results/summary_v2.json", { encoding: "utf8" });
  const vt = py.FS.readFile("/repo/study/results/variant_table_v2.csv", { encoding: "utf8" });
  const gt = py.FS.readFile("/repo/study/results/gen_table_v2.csv", { encoding: "utf8" });
  post("finished", { files: { "summary_v2.json": summary, "variant_table_v2.csv": vt, "gen_table_v2.csv": gt } });
}

self.onmessage = e => { if (e.data.cmd === "run") run(e.data.base).catch(err => post("error", { text: String(err && err.message || err) })); };
