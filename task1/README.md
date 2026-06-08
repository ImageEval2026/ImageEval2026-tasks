# Task 1: Ayn-VQA — Spoken Visual Question Answering & Hallucination Detection

**Ayn** (عين, "eye") is a culturally grounded Arabic multimodal benchmark. Given a
culturally specific image, a system must (a) answer a **spoken** Arabic question
about it, and (c) tell image-grounded statements apart from plausible but
**hallucinated** ones. Part of the [ImageEval 2026](https://imageeval2026.github.io/)
shared task at ArabicNLP 2026.

Each subtask is offered as two language tracks — **English** and **Modern Standard
Arabic (MSA)** — scored separately, for **four** Codabench competitions in total.

> 📌 Please **[register here](https://docs.google.com/forms/d/e/1FAIpQLSd1QKF4rXD_gbLJlDykLvB0DGMIogwhraeOtWRiQiotucK0zA/viewform)**
> so the organisers can keep you posted on data releases, deadlines, and updates.

__Table of contents:__
- [List of Versions](#list-of-versions)
- [Contents of the Directory](#contents-of-the-directory)
- [Task Description](#task-description)
- [Dataset](#dataset)
- [Scorer and Official Evaluation Metrics](#scorer-and-official-evaluation-metrics)
- [Baselines](#baselines)
- [Format Checker](#format-checker)
- [Submission](#submission)
- [Timeline](#timeline)
- [Licensing](#licensing)
- [Credits](#credits)

---

## List of Versions

* __[v1.0 — May 22, 2026]__ `train`, `dev`, and unlabelled `devtest` released on
  HuggingFace alongside the scorer, format checker, and baselines.
* __[v1.1 — July 20, 2026]__ Blind `test` inputs released; final-evaluation phase opens.

---

## Contents of the Directory

* [data/](./data)<br/>
  The released JSONL files (`train`, `dev`, `devtest` × `en`/`msa`) for both
  subtasks. Images and audio are **not** in this repo — they live on the
  HuggingFace Hub; the JSONL `image`/`audio` fields are relative paths into it.
* [baselines/](./baselines)<br/>
  Ready-to-run Colab notebooks: an open-model baseline (Qwen2.5-Omni / Qwen2.5-VL)
  and a cascaded API baseline (Fanar) for Task 1a.
* [format_checker/](./format_checker)<br/>
  `check_format.py` — validate your prediction CSV before submitting.
* [scorer/](./scorer)<br/>
  `score.py` — the official scorer; computes exactly the Codabench leaderboard
  metrics on a labelled split.
* [README.md](./README.md)<br/>
  This file.

---

## Task Description

### Subtask 1a — Spoken VQA

Given an **image** and a **spoken** question with its options (audio; no text is
provided — the model must listen), choose the correct option.

**Prediction:** the option index `0`, `1` or `2`.

### Subtask 1c — Hallucination Detection

Given an **image** and **three statements**, decide for **each** statement whether
it is **True** (grounded in the image) or **False** (a hallucination). Exactly one
of the three statements is grounded.

**Prediction:** a `true`/`false` label per statement.

The English and MSA tracks of a subtask are parallel: same images, same answers;
the questions/statements are translations of each other. The dataset spans **18
Arab countries**.

---

## Dataset

All splits — including the images and audio — live on the HuggingFace Hub:

> **[QCRI/ImageEval2026-Task1-AynVQA](https://huggingface.co/datasets/QCRI/ImageEval2026-Task1-AynVQA)**

```python
from datasets import load_dataset
ds = load_dataset("QCRI/ImageEval2026-Task1-AynVQA", "task1a_en", split="devtest")
```

The JSONL files under [data/](./data) are the **text** half of the release, kept
here so you can read the format and run the scorer/checker directly. The
`image` and `audio` fields are relative paths (`images/<id>.jpg`,
`audio/<lang>/<id>.wav`) that resolve against the media on the Hub.

| split | labels | items | use |
|---|---|---:|---|
| `train`   | yes | 3000 | training / fine-tuning |
| `dev`     | yes | 500  | local validation (run the scorer here) |
| `devtest` | no  | 500  | development-phase leaderboard target |
| `test`    | no  | 1000 | blind final ranking (human-recorded audio) |

> 🔊 **Task 1a audio:** `train`/`dev`/`devtest` questions are synthetically
> generated (voice cloning); the final `test` audio is **human-recorded** — expect
> a speaker / recording-condition shift.

### Input Data Format

**Task 1a** (`data/task1a/<split>_<lang>.jsonl`):

```json
{"id": "39550e...", "image": "images/39550e....jpg", "audio": "audio/en/39550e....wav", "label": 2}
```

**Task 1c** (`data/task1c/<split>_<lang>.jsonl`):

```json
{"id": "39550e...", "image": "images/39550e....jpg",
 "statements": ["... True or False?", "... True or False?", "... True or False?"],
 "labels": [false, false, true]}
```

`train`/`dev` also carry `country`, `category`, `subcategory`. Gold fields
(`label` / `labels`) are **omitted** from `devtest` and `test`.

### Output Data Format

**Task 1a** — one row per item, columns `id,prediction` (prediction ∈ {0,1,2}):

```
id,prediction
39550e...,2
5f985e...,1
```

**Task 1c** — three rows per item, columns `id,statement_index,prediction`
(`statement_index` ∈ {0,1,2}; `prediction` is `true`/`false`):

```
id,statement_index,prediction
39550e...,0,false
39550e...,1,false
39550e...,2,true
```

---

## Scorer and Official Evaluation Metrics

Each of the four tracks is scored separately; the scorer in [scorer/](./scorer)
reports exactly the Codabench leaderboard columns. A missing or unparseable
prediction always counts as wrong.

**Task 1a — ranking metric: accuracy.** Balanced accuracy (mean per-class recall)
and macro-F1 are also reported.

**Task 1c — ranking metric: combined accuracy** (fraction of items where **all
three** labels are correct). The scorer also reports the hallucination rate,
conditional hallucination rate (CFHR-2/3), and the Q+/Q− accuracies. True/False
is read with the shared-task `evaluate_tf` parser (English and Arabic verdicts,
e.g. `true`/`false`, صح/خطأ).

```bash
# score yourself on a labelled split (dev) before submitting
python scorer/score.py --task 1a --gold data/task1a/dev_en.jsonl --pred prediction.csv
python scorer/score.py --task 1c --gold data/task1c/dev_en.jsonl --pred prediction.csv
```

See [scorer/README.md](./scorer/README.md) for the full metric definitions.

---

## Baselines

Starter **Colab notebooks** (in [baselines/](./baselines)) run end to end —
download the data → run a model → write a Codabench-ready `prediction.zip`:

| baseline | subtask | open in Colab |
|---|---|---|
| Open model — Qwen2.5-Omni (4-bit) | 1a | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ImageEval2026/ImageEval2026-tasks/blob/main/task1/baselines/baseline_task1a_colab.ipynb) |
| Open model — Qwen2.5-VL (4-bit) | 1c | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ImageEval2026/ImageEval2026-tasks/blob/main/task1/baselines/baseline_task1c_colab.ipynb) |
| Cascaded API — Fanar STT → Oryx (no GPU) | 1a | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ImageEval2026/ImageEval2026-tasks/blob/main/task1/baselines/baseline_task1a_fanar_cascade_colab.ipynb) |

(Also mirrored on [Google Drive](https://drive.google.com/drive/folders/1zDO2uXq0fEQhfNj8M2DstkNL1-EEXybT?usp=sharing).)
These are references only — you are free to use your own models, prompts, and
configurations. Reference scores (devtest):

| subtask | track | model | metric | score |
|---|---|---|---|---|
| 1a | English | Qwen2.5-Omni | accuracy | 0.6640 |
| 1a | MSA     | Qwen2.5-Omni | accuracy | 0.3980 |
| 1c | English | Qwen2.5-VL   | combined accuracy | 0.6840 |
| 1c | MSA     | Qwen2.5-VL   | combined accuracy | 0.5080 |

See [baselines/README.md](./baselines/README.md) for details.

---

## Format Checker

Validate your prediction CSV before zipping it as `prediction.zip`:

```bash
python format_checker/check_format.py --task 1a --pred prediction.csv
python format_checker/check_format.py --task 1c --pred prediction.csv --gold data/task1c/devtest_en.jsonl
```

It checks the columns, value ranges, duplicates, and (with `--gold`) that your
ids match the split. See [format_checker/README.md](./format_checker/README.md).

---

## Submission

The competition runs in two phases on Codabench:

1. **Development phase** — submit predictions on `devtest`; the leaderboard is live.
2. **Final-evaluation phase** — submit predictions on the blind `test` set.

Zip your prediction CSV as `prediction.zip` and upload to the matching competition:

| config | subtask | language | Codabench |
|---|---|---|---|
| `task1a_en`  | Spoken VQA | English | [compete](https://www.codabench.org/competitions/17002/) |
| `task1a_msa` | Spoken VQA | MSA     | [compete](https://www.codabench.org/competitions/17001/) |
| `task1c_en`  | Hallucination | English | [compete](https://www.codabench.org/competitions/17000/) |
| `task1c_msa` | Hallucination | MSA     | [compete](https://www.codabench.org/competitions/16999/) |

- Each team should use a single submission account.
- The most recent valid submission before the deadline is final.
- All teams are encouraged to submit a system-description paper.

---

## Timeline

| phase | window | submit on |
|---|---|---|
| **Development** | `2026-05-22 → 2026-07-19` | `devtest` — leaderboard live |
| **Testing** | `2026-07-20 → 2026-07-29` | `test` — blind, final ranking |

Dates may shift — watch the [website](https://imageeval2026.github.io/) and the
[registration form](https://docs.google.com/forms/d/e/1FAIpQLSd1QKF4rXD_gbLJlDykLvB0DGMIogwhraeOtWRiQiotucK0zA/viewform).

---

## Licensing

The dataset is released under **CC BY-NC 4.0** — non-commercial research use only.

---

## Credits

Organizers and acknowledgments are on the task website:
<https://imageeval2026.github.io/>. Contact: <imageeval2026@gmail.com>.
