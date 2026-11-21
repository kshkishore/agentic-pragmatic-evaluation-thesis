/* Page logic: tabs, the in-browser run (via site/worker.js), published results and the dataset explorer. */
const BASE = new URL(".", location.href).href;
const $ = s => document.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

const TABLES = ["throughput", "metrics", "j1conds", "mcnemar2", "devpost", "dims", "charts", "j2", "agree", "pairwise", "robust", "gens"];
const FIGS = [
  ["fig_example.png", "Figure 1.1 · Example item IRO-02"], ["fig_conceptual.png", "Figure 2.1 · Conceptual framework"],
  ["fig_design.png", "Figure 3.1 · Research design"], ["fig_charts.png", "Figure 3.2 · The sixteen chart stimuli"],
  ["fig_pipeline.png", "Figure 3.3 · Pipeline architecture"], ["fig_metrics.png", "Figure 4.1 · Metrics and J1 on A–B and A–C"],
  ["fig_variants.png", "Figure 4.2 · Scores of the A, B and C variants"], ["fig_cat_heat_AB.png", "Figure 4.3 · A–B accuracy by category"],
  ["fig_lambda.png", "Figure 4.4 · M_eval by weight λ"], ["fig_cat_heat_all.png", "Figure 4.5 · Accuracy by category, all contrasts"],
  ["fig_profiles.png", "Figure 4.6 · CO-STAR dimension profiles"], ["fig_robust.png", "Figure 4.7 · Rewording and sampling"],
  ["fig_generators.png", "Figure 4.8 · The two generators"], ["fig_criterion.png", "Figure 4.9 · Judge scores and rule-based checks"],
];
const FIGCAP = Object.fromEntries(FIGS);
const CATS = { IDI: "Idioms", ISA: "Indirect speech acts", IMP: "Implicature and presupposition", IRO: "Irony", REF: "Reference and deixis",
  REG: "Register and audience", FTA: "Politeness and face-threatening acts", EMP: "Empathy", CUL: "Intercultural pragmatics", MM: "Charts (multimodal)" };

/* ---------- tabs ---------- */
function show(tab) {
  document.querySelectorAll(".tabs button").forEach(b => b.setAttribute("aria-selected", b.dataset.tab === tab));
  document.querySelectorAll(".panel").forEach(p => p.hidden = p.id !== tab);
  if (tab === "results") loadPublished();
  if (tab === "explore") loadExplorer();
  history.replaceState(null, "", "#" + tab);
}
document.querySelectorAll(".tabs button").forEach(b => b.onclick = () => show(b.dataset.tab));
document.querySelectorAll("[data-goto]").forEach(b => b.onclick = e => { e.preventDefault(); show(b.dataset.goto); window.scrollTo(0, 0); });
const initial = location.hash.slice(1); if (["overview", "reproduce", "results", "explore"].includes(initial)) show(initial);

/* ---------- markdown tables ---------- */
function mdTable(md, extra = "") {
  const lines = md.trim().split("\n");
  const cap = lines[0].startsWith("|") ? "" : lines.shift();
  const rows = lines.filter(l => l.startsWith("|") && !/^\|\s*-{3}/.test(l)).map(l => l.slice(1, -1).split("|").map(c => c.trim()));
  const [head, ...body] = rows;
  return `<div class="tbl"><p class="cap">${esc(cap)}${extra}</p><div class="scroll"><table><thead><tr>${head.map(h => `<th>${esc(h)}</th>`).join("")}</tr></thead>
  <tbody>${body.map(r => `<tr>${r.map(c => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div></div>`;
}

/* ---------- published results ---------- */
let pubLoaded = false;
async function loadPublished() {
  if (pubLoaded) return; pubLoaded = true;
  const texts = await Promise.all(TABLES.map(t => fetch(BASE + "tables/" + t + ".md").then(r => r.text())));
  $("#pub-tables").innerHTML = texts.map(t => mdTable(t)).join("");
  $("#pub-figs").innerHTML = FIGS.map(([f, c]) => `<figure><a href="figures/${f}" target="_blank"><img loading="lazy" src="figures/${f}" alt="${esc(c)}"></a><figcaption>${esc(c)}</figcaption></figure>`).join("");
}

/* ---------- run in the browser ---------- */
const STEPS = [["python", "Start Python in the browser"], ["packages", "Install the scientific packages"], ["data", "Download the dataset, logs and scripts"],
  ["analyze", "Recompute every statistic (study/analyze_v2.py)"], ["compare", "Compare with the published results"],
  ["tables", "Rebuild the Chapter 4 tables (tools/tables_ch4.py)"], ["figures", "Redraw the figures"]];
function renderSteps() {
  $("#steps").innerHTML = STEPS.map(([id, l]) => `<li id="st-${id}"><span class="ico"></span><div><div class="lab">${esc(l)}</div><div class="detail"></div></div><span class="secs"></span></li>`).join("");
}
renderSteps();
let timer = null;
$("#run").onclick = () => {
  const btn = $("#run"); btn.disabled = true; btn.textContent = "Running…";
  renderSteps(); $("#log").textContent = ""; $("#verdict").hidden = true; $("#downloads").hidden = true; $("#run-tables").innerHTML = ""; $("#run-figs").innerHTML = "";
  const t0 = Date.now(); timer = setInterval(() => { $("#elapsed").textContent = Math.round((Date.now() - t0) / 1000) + " s elapsed"; }, 1000);
  const w = new Worker("site/worker.js");
  w.onmessage = e => {
    const m = e.data;
    if (m.type === "log") { const p = $("#log"); p.textContent += m.text + "\n"; p.scrollTop = p.scrollHeight; }
    if (m.type === "step") {
      const li = $("#st-" + m.id); li.className = m.state;
      if (m.label) li.querySelector(".lab").textContent = m.label;
      if (m.detail) li.querySelector(".detail").textContent = m.detail;
      if (m.secs != null) li.querySelector(".secs").textContent = m.secs.toFixed(1) + " s";
    }
    if (m.type === "compare") {
      const v = $("#verdict"); v.hidden = false;
      if (m.diffs === 0) { v.className = "verdict ok"; v.innerHTML = `<b>Reproduced.</b> All ${m.values.toLocaleString()} values in <code>summary_v2.json</code> recomputed in your browser are identical to the published results.`; }
      else { v.className = "verdict bad"; v.innerHTML = `<b>${m.diffs} of ${m.values.toLocaleString()} values differ</b> from the published results. First differences:<ul>${m.examples.map(x => `<li>${esc(x)}</li>`).join("")}</ul>`; }
    }
    if (m.type === "tables") {
      $("#run-tables").innerHTML = "<h2>Tables rebuilt in your browser</h2>" + TABLES.map(t => {
        const x = m.tables[t]; return mdTable(x.text, x.identical ? ' <span class="badge ok">identical to thesis</span>' : ' <span class="badge bad">differs</span>');
      }).join("");
    }
    if (m.type === "figures") {
      $("#run-figs").innerHTML = m.figs.map(f => {
        const url = URL.createObjectURL(new Blob([f.data], { type: "image/png" }));
        return `<figure><a href="${url}" download="${f.name}"><img src="${url}" alt="${esc(FIGCAP[f.name] || f.name)}"></a><figcaption>${esc(FIGCAP[f.name] || f.name)} · redrawn</figcaption></figure>`;
      }).join("");
      $("#run-figs").insertAdjacentHTML("beforebegin", "");
    }
    if (m.type === "finished" || m.type === "error") {
      clearInterval(timer); btn.disabled = false; btn.textContent = "Run again"; w.terminate();
      if (m.type === "error") { const v = $("#verdict"); v.hidden = false; v.className = "verdict bad"; v.innerHTML = "<b>The run stopped:</b> " + esc(m.text) + "<br>Check your internet connection and try again; the Python output below may show more."; }
      if (m.files) {
        const d = $("#downloads"); d.hidden = false;
        d.innerHTML = "<span class='muted'>Download what you computed:</span>" + Object.entries(m.files).map(([n, t]) =>
          `<a href="${URL.createObjectURL(new Blob([t], { type: n.endsWith(".json") ? "application/json" : "text/csv" }))}" download="${n}">${n}</a>`).join("");
      }
    }
  };
  w.postMessage({ cmd: "run", base: BASE });
};

/* ---------- explorer ---------- */
let DS = null, VT = {}, GT = {}, GOUT = {}, DIAG = {}, GDIAG = {}, current = null;
function csv(text) {
  const rows = []; let row = [], f = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
    else if (c === '"') q = true; else if (c === ",") { row.push(f); f = ""; } else if (c === "\n") { row.push(f); rows.push(row); row = []; f = ""; } else if (c !== "\r") f += c;
  }
  if (f || row.length) { row.push(f); rows.push(row); }
  const [h, ...b] = rows; return b.filter(r => r.length === h.length).map(r => Object.fromEntries(h.map((k, i) => [k, r[i]])));
}
const jsonl = t => t.trim().split("\n").map(l => JSON.parse(l));
async function loadExplorer() {
  if (DS) return;
  $("#item-view").innerHTML = '<p class="muted">Loading the dataset…</p>';
  const get = p => fetch(BASE + p).then(r => { if (!r.ok) throw new Error(p); return r.text(); });
  const [ds, vt, gt, g1, g2, c1, c2, j1, j2] = await Promise.all(["study/golden_dataset_v2.json", "study/results/variant_table_v2.csv", "study/results/gen_table_v2.csv",
    "study/results/gen_qwen3vl-2b.jsonl", "study/results/gen_smolvlm2-2.2b.jsonl", "study/results/contrast_j1.jsonl", "study/results/contrast_j2.jsonl",
    "study/results/genjudge_j1.jsonl", "study/results/genjudge_j2.jsonl"].map(get));
  DS = JSON.parse(ds);
  csv(vt).forEach(r => VT[r.item + "|" + r.cand] = r);
  csv(gt).forEach(r => GT[r.generator + "|" + r.item] = r);
  [...jsonl(g1), ...jsonl(g2)].forEach(r => GOUT[r.generator + "|" + r.item] = r.output);
  [...jsonl(c1), ...jsonl(c2)].filter(r => r.condition === "costar").forEach(r => DIAG[r.judge + "|" + r.item + "|" + r.cand] = r.scores.diagnosis);
  [...jsonl(j1), ...jsonl(j2)].forEach(r => GDIAG[r.judge + "|" + r.generator + "|" + r.item] = r.scores.diagnosis);
  const sel = $("#f-cat"); Object.entries(CATS).forEach(([k, v]) => sel.insertAdjacentHTML("beforeend", `<option value="${k}">${k} · ${esc(v)}</option>`));
  sel.onchange = renderList; $("#f-q").oninput = renderList;
  renderList(); select(DS[0].id);
}
function renderList() {
  const cat = $("#f-cat").value, q = $("#f-q").value.trim().toLowerCase();
  const items = DS.filter(it => (!cat || it.category === cat) && (!q || JSON.stringify([it.prompt, it.reference, it.candidates]).toLowerCase().includes(q)));
  $("#f-count").textContent = items.length + " of " + DS.length + " items";
  $("#item-list").innerHTML = items.map(it => `<li data-id="${it.id}" ${it.id === current ? 'aria-current="true"' : ""}><span class="id">${it.id}</span>${esc(it.prompt.length > 90 ? it.prompt.slice(0, 88) + "…" : it.prompt)}</li>`).join("");
  document.querySelectorAll("#item-list li").forEach(li => li.onclick = () => select(li.dataset.id));
}
const n = (x, d = 2) => (x === "" || x == null || isNaN(+x)) ? "–" : (+x).toFixed(d);
const dims = (r, p) => ["C", "O", "S", "T", "A", "R"].map(k => `<span><b>${k}</b>${r[p + "_" + k] ? (+r[p + "_" + k]).toFixed(0) : "–"}</span>`).join("");
function select(id) {
  current = id; const it = DS.find(x => x.id === id);
  document.querySelectorAll("#item-list li").forEach(li => li.toggleAttribute("aria-current", li.dataset.id === id));
  const cs = it.costar, lab = { A: "A · appropriate", B: "B · pragmalinguistic / grounding failure", C: "C · sociopragmatic failure" };
  const resp = ["A", "B", "C"].map(c => {
    const r = VT[id + "|" + c] || {}; const d1 = DIAG["qwen3vl-4b|" + id + "|" + c], d2 = DIAG["phi4-mini|" + id + "|" + c];
    return `<div class="resp ${c}"><div class="lab">${lab[c]}</div><div class="txt">${esc(it.candidates[c])}</div>
      <div class="scores"><span><b>J1 rubric</b>${n(r.J1_costar)}</span>${dims(r, "J1_costar")}<span><b>J1 holistic+spec</b>${n(r.J1_spec_holistic)}</span><span><b>J1 plain</b>${n(r.J1_plain)}</span></div>
      ${r.J2_costar ? `<div class="scores" style="margin-top:4px"><span><b>J2 rubric</b>${n(r.J2_costar)}</span>${dims(r, "J2_costar")}<span><b>J2 holistic+spec</b>${n(r.J2_spec_holistic)}</span><span><b>J2 plain</b>${n(r.J2_plain)}</span></div>` : ""}
      <div class="scores" style="margin-top:4px"><span><b>BLEU</b>${n(r.bleu, 1)}</span><span><b>chrF</b>${n(r.chrf, 1)}</span><span><b>BERTScore</b>${n(r.bertscore, 1)}</span><span><b>NLI-bi</b>${n(r.nli_bi, 1)}</span><span><b>words</b>${n(r.n_words, 0)}</span></div>
      ${d1 ? `<div class="diag">J1: “${esc(d1.replace(/^[:\s]+/, ""))}”</div>` : ""}${d2 ? `<div class="diag">J2: “${esc(d2.replace(/^[:\s]+/, ""))}”</div>` : ""}</div>`;
  }).join("");
  const gens = [["qwen3vl-2b", "G1 · Qwen3-VL-2B-Instruct"], ["smolvlm2-2.2b", "G2 · SmolVLM2-2.2B-Instruct"]].map(([g, l]) => {
    const r = GT[g + "|" + id] || {}; const d1 = GDIAG["qwen3vl-4b|" + g + "|" + id], d2 = GDIAG["phi4-mini|" + g + "|" + id];
    return `<div class="resp G"><div class="lab">${l}</div><div class="txt">${esc(GOUT[g + "|" + id])}</div>
      <div class="scores"><span><b>J1</b>${n(r.J1)}</span>${dims(r, "J1")}${r.J2 ? `<span><b>J2</b>${n(r.J2)}</span>${dims(r, "J2")}` : ""}<span><b>format rule</b>${r.fmt_ok === "True" ? "met" : "not met"}</span><span><b>words</b>${n(r.n_words, 0)}</span></div>
      ${d1 ? `<div class="diag">J1: “${esc(d1.replace(/^[:\s]+/, ""))}”</div>` : ""}${d2 ? `<div class="diag">J2: “${esc(d2.replace(/^[:\s]+/, ""))}”</div>` : ""}</div>`;
  }).join("");
  $("#item-view").innerHTML = `<h3>${it.id} <span class="muted" style="font-family:system-ui,sans-serif;font-weight:400;font-size:.9rem">· ${esc(CATS[it.category])} · ${esc(it.phenomenon)} · origin: ${esc(it.origin)}</span></h3>
    <p class="prompt">${esc(it.prompt)}</p>${it.image ? `<img class="chart-img" src="study/images/${it.image}" alt="Chart for ${it.id}">` : ""}
    <dl class="spec">${["context", "objective", "style", "tone", "audience", "response_format"].map(k => `<dt>${k.replace("_", " ")}</dt><dd>${esc(cs[k])}</dd>`).join("")}
    ${it.answer_key ? `<dt>answer key</dt><dd>${esc(it.answer_key)}</dd>` : ""}</dl>
    <div class="ref"><b>Reference.</b> ${esc(it.reference)}</div>${resp}
    <h4>Replies of the two generators</h4>${gens}
    <p class="muted" style="font-size:.8rem">Scores: judge totals are normalised to 0–1; C O S T A R are the six rubric dimensions (1–5): Context, Objective, Style, Tone, Audience, Response format.</p>`;
}
