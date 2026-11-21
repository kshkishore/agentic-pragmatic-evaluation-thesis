import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os
OUT = os.environ.get("FIG_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures"))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
INK, MUTED, LINE = "#1f1f1f", "#52514e", "#8a8984"
BLUE, BLUE_BG = "#2a78d6", "#e8f1fc"
ORANGE, ORANGE_BG = "#c4501f", "#fdeee6"
GREEN, GREEN_BG = "#11805a", "#e5f5ee"
GREY_BG = "#f3f3f1"

def box(ax, x, y, w, h, title, body=None, fc=GREY_BG, ec=LINE, tc=INK, fs=9.5, bfs=8.2, lw=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.018", fc=fc, ec=ec, lw=lw))
    if body:
        ax.text(x + w / 2, y + h - 0.035, title, ha="center", va="top", fontsize=fs, fontweight="bold", color=tc)
        ax.text(x + w / 2, y + h - 0.085, body, ha="center", va="top", fontsize=bfs, color=MUTED, linespacing=1.45)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=fs, fontweight="bold", color=tc)

def arrow(ax, p, q, color=LINE, style="-|>", lw=1.2, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=11, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", linestyle=ls, shrinkA=2, shrinkB=2))

def canvas(w, h):
    fig = plt.figure(figsize=(w, h), dpi=300); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); return fig, ax

# ---------------------------------------------------------------- Figure 2.1 conceptual framework
fig, ax = canvas(9.2, 5.2)
box(ax, 0.015, 0.04, 0.25, 0.92, "Applied-linguistic theory",
    "Pragmatic competence\n(Canale & Swain; Bachman)\n\nSpeech acts (Austin; Searle)\n\nImplicature (Grice)\n\nPoliteness and face\n(Brown & Levinson)\n\nRegister and audience\n(Halliday; Bell)\n\nDeixis (Levinson)\n\nPragmalinguistic vs.\nsociopragmatic failure\n(Leech; Thomas)\n\nMultimodal meaning\n(Kress & van Leeuwen)", fc=GREY_BG, bfs=7.6)
box(ax, 0.33, 0.66, 0.25, 0.30, "CO-STAR rubric",
    "C Context fit   O Objective\nS Style   T Tone\nA Audience   R Response format\n\nsix anchored 1-5 scales", fc=BLUE_BG, ec=BLUE, tc=BLUE)
box(ax, 0.33, 0.30, 0.25, 0.30, "Golden Dataset",
    "160 items in 10 categories:\nidioms, indirect acts, implicature,\nirony, politeness, deixis, register,\nempathy, intercultural, charts\nspec + reference + variants A, B, C", fc=BLUE_BG, ec=BLUE, tc=BLUE)
box(ax, 0.65, 0.66, 0.33, 0.30, "Agentic pipeline (open-source)",
    "Generator agent: Qwen3-VL-2B, SmolVLM2-2.2B\n\nLinguistic Evaluator: Qwen3-VL-4B\n(independent check: Phi-4-mini)\n\nLangChain + llama.cpp + JSON grammar", fc=ORANGE_BG, ec=ORANGE, tc=ORANGE)
box(ax, 0.65, 0.30, 0.33, 0.30, "Composite metric",
    "$f_{syntax}(x)$: acceptability (CoLA)\n$f_{pragmatics}(x, c)$: CO-STAR scores\n\n$M_{eval} = \\lambda_1 f_{syntax} + \\lambda_2 f_{pragmatics}$", fc=GREEN_BG, ec=GREEN, tc=GREEN)
box(ax, 0.33, 0.04, 0.65, 0.18, "Validation by contrast sets",
    "Known ordering: appropriate A > pragmalinguistic failure B;  A > sociopragmatic failure C   (320 contrasts)\nBaselines: 17 automatic metrics, holistic prompts; checks: second judge, both orders, rewording, sampling, rules", fc="#ffffff", ec=INK, bfs=7.6)
arrow(ax, (0.265, 0.81), (0.33, 0.81)); arrow(ax, (0.265, 0.45), (0.33, 0.45))
ax.text(0.297, 0.835, "translate", ha="center", fontsize=7.5, color=MUTED); ax.text(0.297, 0.475, "design", ha="center", fontsize=7.5, color=MUTED)
arrow(ax, (0.58, 0.81), (0.65, 0.81)); arrow(ax, (0.58, 0.45), (0.65, 0.76), rad=0.0)
arrow(ax, (0.815, 0.66), (0.815, 0.60))
arrow(ax, (0.455, 0.30), (0.455, 0.22)); arrow(ax, (0.815, 0.22), (0.815, 0.30), ls="--", color=GREEN)
ax.text(0.83, 0.255, "tests validity", fontsize=7.5, color=GREEN, va="center")
fig.savefig(os.path.join(OUT, "fig_conceptual.png"), facecolor="white"); plt.close(fig)

# ---------------------------------------------------------------- Figure 3.1 research design
fig, ax = canvas(9.2, 4.8)
box(ax, 0.01, 0.36, 0.17, 0.30, "Golden Dataset", "160 prompts\n(16 with charts)\nCO-STAR specs\nreferences\n480 variants", fc=BLUE_BG, ec=BLUE, tc=BLUE)
ax.text(0.20, 0.93, "Validation path (Experiments 1-4)", fontsize=9.5, fontweight="bold", color=INK)
box(ax, 0.22, 0.62, 0.15, 0.24, "Variants A, B, C", "known ordering\nA > B, A > C", fc=GREY_BG)
box(ax, 0.42, 0.74, 0.22, 0.12, "Reference-based metrics", None, fs=8.5)
box(ax, 0.42, 0.59, 0.22, 0.12, "J1 CO-STAR / holistic / plain", None, fs=8.5, fc=ORANGE_BG, ec=ORANGE, tc=ORANGE)
box(ax, 0.42, 0.44, 0.22, 0.12, "J2 (3 prompts); J1 pairs", None, fs=8.5, fc=ORANGE_BG, ec=ORANGE, tc=ORANGE)
box(ax, 0.70, 0.52, 0.275, 0.34, "Validity and reliability",
    "pairwise accuracy (H1-H3)\nby category and item origin\nanswer-key ablation\nagreement, position, robustness\ndimension independence", fc=GREEN_BG, ec=GREEN, tc=GREEN)
ax.text(0.20, 0.30, "Application path (Experiment 5)", fontsize=9.5, fontweight="bold", color=INK)
box(ax, 0.22, 0.04, 0.15, 0.22, "Generators", "G1 Qwen3-VL-2B\nG2 SmolVLM2-2.2B", fc=GREY_BG)
box(ax, 0.42, 0.04, 0.22, 0.22, "Scoring", "J1 (all), J2 (text)\nf_syntax, 17 metrics, rules", fc=ORANGE_BG, ec=ORANGE, tc=ORANGE)
box(ax, 0.70, 0.04, 0.275, 0.22, "Pragmatic profiles", "M_eval by category and dimension\nλ sensitivity\ncorrelation with BLEU etc.", fc=GREEN_BG, ec=GREEN, tc=GREEN)
arrow(ax, (0.18, 0.60), (0.22, 0.72)); arrow(ax, (0.18, 0.42), (0.22, 0.17))
for y in (0.80, 0.65, 0.50): arrow(ax, (0.37, 0.74), (0.42, y))
for y in (0.80, 0.65, 0.50): arrow(ax, (0.64, y), (0.70, 0.69))
arrow(ax, (0.37, 0.15), (0.42, 0.15)); arrow(ax, (0.64, 0.15), (0.70, 0.15))
fig.savefig(os.path.join(OUT, "fig_design.png"), facecolor="white"); plt.close(fig)

# ---------------------------------------------------------------- Figure 3.3 pipeline architecture
fig, ax = canvas(9.2, 5.6)
box(ax, 0.015, 0.73, 0.175, 0.21, "Data layer", "golden_dataset_v2.json\nimages/*.png\n(rendered from data)", fc=BLUE_BG, ec=BLUE, tc=BLUE)
box(ax, 0.24, 0.73, 0.22, 0.21, "Generator chain", "prompt (+ image) only\nsystem: 'You are a helpful\nassistant.'  greedy, 180 tok", fc=GREY_BG)
box(ax, 0.51, 0.73, 0.22, 0.21, "llama.cpp", "Qwen3-VL-2B  |  SmolVLM2-2.2B\nGGUF Q4_K_M + mmproj", fc=GREY_BG)
box(ax, 0.78, 0.73, 0.195, 0.21, "Generation log", "gen_*.jsonl\noutput, tokens, latency", fc="#ffffff", ec=INK)
box(ax, 0.24, 0.36, 0.22, 0.28, "Evaluator chain (LangChain)", "ChatPromptTemplate:\nrole + 6 rubric dimensions\n+ prompt + CO-STAR spec\n(+ answer key, image)\n+ response", fc=ORANGE_BG, ec=ORANGE, tc=ORANGE)
box(ax, 0.51, 0.36, 0.22, 0.28, "llama.cpp + GBNF grammar", "Qwen3-VL-4B (J1)\nPhi-4-mini (J2, text)\n\ntemperature 0, fixed seed\n{\"diagnosis\":...,\"C\":n,...,\"R\":n}", fc=ORANGE_BG, ec=ORANGE, tc=ORANGE)
box(ax, 0.78, 0.36, 0.195, 0.28, "PydanticOutputParser", "types and ranges\nchecked\n\n-> judge log\n(resumable JSONL)", fc="#ffffff", ec=INK)
box(ax, 0.24, 0.04, 0.735, 0.22, "Scoring module",
    "$f_{pragmatics}$ = mean of $(s_d - 1)/4$ over C, O, S, T, A, R;   $f_{syntax}$ = mean P(acceptable) per sentence (RoBERTa-CoLA)\n$M_{eval} = \\lambda_1 f_{syntax} + \\lambda_2 f_{pragmatics}$;   baselines: 17 automatic metrics (overlap, embedding, generative, NLI, CLIP)", bfs=7.8, fc=GREEN_BG, ec=GREEN, tc=GREEN)
arrow(ax, (0.19, 0.84), (0.24, 0.84)); arrow(ax, (0.46, 0.835), (0.51, 0.835)); arrow(ax, (0.73, 0.835), (0.78, 0.835))
arrow(ax, (0.10, 0.73), (0.24, 0.50), rad=0.15); arrow(ax, (0.8775, 0.73), (0.40, 0.64), rad=0.12)
ax.text(0.63, 0.675, "generated response x", fontsize=7.5, color=MUTED, ha="center")
arrow(ax, (0.46, 0.50), (0.51, 0.50)); arrow(ax, (0.73, 0.50), (0.78, 0.50)); arrow(ax, (0.8775, 0.36), (0.8775, 0.26))
fig.savefig(os.path.join(OUT, "fig_pipeline.png"), facecolor="white"); plt.close(fig)

# ---------------------------------------------------------------- Figure 3.2 chart stimuli grid (16 charts)
from PIL import Image
ims = [Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "study", "images", f"MM-{i:02d}.png")).convert("RGB") for i in range(1, 17)]
w, h = ims[0].size; g = Image.new("RGB", (w * 4, h * 4), "white")
for i, im in enumerate(ims): g.paste(im, ((i % 4) * w, (i // 4) * h))
g.save(os.path.join(OUT, "fig_charts.png"), dpi=(220, 220))
print("done")
