# Dataset card: Golden Dataset of pragmatic contrasts

## Summary

The Golden Dataset is a contrast set for testing whether evaluation measures detect pragmatic failure in the responses of AI assistants.

- **Size:** 160 items, in ten categories of 16.
- **Item content:** each item has a user prompt, a six-field CO-STAR specification of what an appropriate response must achieve, a reference response, and three response variants written to a fixed design.
- **Contrasts:** each item yields an A–B and an A–C contrast, 320 in total, whose correct ordering (A first) is known by construction.

| Variant | Design |
|---|---|
| A | Appropriate: satisfies every field of the specification; worded independently of the reference |
| B | Pragmalinguistic or grounding failure: one failure of interpretation (literal reading, reversed implicature, accepted false presupposition, wrongly anchored deixis) or a wrong chart value; reuses as much of the reference's wording as the failure allows |
| C | Sociopragmatic failure: broadly the intended content in an inappropriate register, tone or level of complexity (slang, condescension, jargon, curtness, a stereotype) |

## Categories

| Code | Category | Items |
|---|---|---|
| IDI | Idioms and proverbs | 16 |
| ISA | Indirect speech acts | 16 |
| IMP | Implicature and presupposition | 16 |
| IRO | Irony and non-literal stance | 16 |
| REF | Reference, deixis and ellipsis | 16 |
| REG | Register and audience design | 16 |
| FTA | Politeness and face-threatening acts | 16 |
| EMP | Empathy and affective stance | 16 |
| CUL | Intercultural pragmatics (several items on Indian English and Indian social conventions) | 16 |
| MM | Chart-grounded multimodal prompts (bar, line, pie, grouped bar, scatter) | 16 |

## Files

- `study/golden_dataset_v2.json` is the canonical file, with 160 items. Fields are described in [`docs/CODEBOOK.md`](docs/CODEBOOK.md).
- `study/images/MM-01.png` … `MM-16.png` are the chart stimuli. Each is rendered from the `chart` data stored in its item, and `answer_key` is derived from the same data.
- `data_exports/items.csv` has one row per item. `data_exports/responses_long.csv` has one row per response (the reference and A, B, C).
- The source files are `study/items_*.py` (the 112 items written for the main study) and `study/golden_dataset.json` and `study/golden_dataset_ext.json` (the 48 pilot items). `study/build_v2.py` assembles them.

## Construction

- **Authorship:** all items were written new, by one researcher trained in applied linguistics. No item is taken from an existing benchmark, which reduces the risk of training-data contamination.
- **Development and freeze:**
  - 32 items (the first eight of IDI, ISA, REG and MM, `origin = "pilot"`) were used to develop the rubric and prompts, which were then frozen.
  - 16 held-out items (`origin = "pilot-heldout"`) were written next.
  - 112 items (`origin = "new"`) were written after that.
  - Every IRO, IMP, REF, FTA, EMP and CUL item was written after the freeze.
- **Automatic design checks** were run by `build_v2.py` before any model saw the items:
  - B's chrF to the reference had to exceed A's by more than ten points;
  - A's chrF had to stay below 60;
  - large length differences between A and B were flagged and corrected.
- **Resulting means over the 480 variants:**

  | Measure | A | B | C |
  |---|---|---|---|
  | BLEU against the reference | 6.2 | 54.9 | — |
  | BERTScore | 90.6 | 95.7 | — |
  | Length (words) | 24.2 | 26.1 | 14.9 |

## Intended uses

The dataset is meant for:
- meta-evaluation of automatic metrics and LLM judges on pragmatic appropriateness;
- diagnosing which kind of failure (pragmalinguistic or sociopragmatic) a measure can detect;
- use as prompts for testing generators, with the specification as the marking scheme.

## Limitations

- **Single author:** the items reflect one person's judgments of appropriateness. Culturally situated items encode typical rather than universal norms.
- **Clear failures:** the designed failures are clearer than many natural ones, so accuracy on the contrasts is an upper bound for natural outputs.
- **Built-in surface features:**
  - B's overlap with the reference is built in, so the A–B contrasts measure how strongly a measure follows that cue, rather than discovering it.
  - C variants are the shortest, so length is a confound on A–C.
- **Small categories:** with 16 items per category, only large differences between categories are detectable.
- **Language:** the dataset covers English only (standard written English, with a few Indian English items).
- **Charts:** the charts are simple, and 14 of 16 print their values on the marks.
- **No human ratings:** the items carry no human ratings. Their validity rests on the design and the automatic checks.

## Content warning

C variants deliberately include inappropriate language, such as condescension, curt replies to bereavement and a cultural stereotype, so that evaluation measures can be tested on them. Do not use them as generation or training targets.

## Licence

CC BY 4.0. See `LICENSE-DATA`.
