# Task 2:  Cultural Accuracy Evaluation

The aim of this task is to evaluate whether AI-generated images faithfully represent Qatari and Arab cultural scenes. Given a reference image of an authentic cultural scene, an image caption, and an AI-generated image produced from that caption, participants develop systems that predict cultural accuracy scores using the **Cultural Representation Accuracy Index (CRAI)** — a five-dimensional framework validated against human annotation. The core challenge is that state-of-the-art models such as GPT-4 systematically overestimate cultural accuracy compared to human evaluators, particularly on hallucination detection and cultural integrity. This task directly targets that gap.

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

* __[v1.0 — May 16, 2026]__ Training and development data released alongside evaluation scripts and baselines.
* __[v1.1 — July 20, 2026]__ Test set inputs (captions and images) released. Gold labels remain hidden.

---

## Contents of the Directory

* Main folder: [data](./data)<br/>
  Contains TSV files for train, dev, and test splits. Each split includes `captions.tsv`, `gold_human.tsv`, and `gold_llm.tsv`. Images are distributed separately via the download link below.
* Main folder: [baselines](./baselines)<br/>
  Contains two baseline scripts: a mean baseline and a GPT-4 LLM-as-a-judge baseline. Also contains `requirements.txt`.
* Main folder: [evaluation](./evaluation)<br/>
  Contains the official scorer script `evaluate.py` and a `sample_submission.tsv` showing the required format.
* Main folder: [format_checker](./format_checker)<br/>
  Contains `check_format.py` to validate your submission file before uploading to CodaLab.
* [README.md](./README.md)<br/>
  This file.

---

## Task Description

Text-to-image models are predominantly trained on Western-centric data, leading to systematic misrepresentation of non-Western cultures in AI-generated visual content. Arabic-speaking cultures are particularly affected: distinct national identities are often collapsed into a generic "Arab" visual, erasing culturally specific markers such as Qatari traditional attire (*thobe*, *ghutra*, *agal*), architecture, and practices like sawt music or majlis gatherings.

CRAI-Bench addresses this by providing a benchmark of (reference image, caption, generated image) triples grounded in Qatari culture, annotated by human evaluators using the CRAI framework.

### Input

Each instance consists of three elements:

1. A **reference image** — an authentic photo of a Qatari cultural scene
2. A **caption** — used to prompt a T2I model to generate an image
3. A **generated image** — the AI output produced from that caption

### Output

For each instance, predict CRAI scores across five dimensions:

| Dimension | Code | Weight | Description |
|-----------|------|--------|-------------|
| Cultural Element Accuracy | CEA | 0.30 | Are expected cultural elements present and correctly depicted? |
| Contextual Coherence | CC | 0.20 | Are elements placed in culturally appropriate settings? |
| Cultural Specificity | CS | 0.20 | How specific is the depiction to the target culture? |
| Cultural Integrity | CI | 0.20 | Is the representation truthful and free of distortion? |
| Hallucination Penalty | HP | −0.10 | Are there fabricated cultural elements not in the caption? |

**CRAI Formula:**
```
CRAI_composite = 0.30 × CEA + 0.20 × CC + 0.20 × CS + 0.20 × CI − 0.10 × HP
```

All dimension scores are in [0, 1]. The composite score is also in [0, 1] and can be slightly negative due to the HP penalty.

**Score Interpretation:**

| Range | Interpretation |
|-------|---------------|
| 0.85 – 1.00 | Highly accurate |
| 0.70 – 0.84 | Mostly accurate |
| 0.50 – 0.69 | Moderately accurate |
| 0.30 – 0.49 | Weak |
| Below 0.30 | Poor or misleading |

**Cultural Specificity (CS) Tiers:**

| Score | Meaning |
|-------|---------|
| 1.00 | Uniquely Qatari / target culture |
| 0.75 | Strongly associated with target culture |
| 0.50 | Regionally common across the Arab world |
| 0.25 | Generic Middle Eastern or vague |
| 0.00 | No cultural specificity |

---

## Dataset

### Overview

The dataset consists of (reference image, caption, generated image) triples grounded in Qatari culture. Each of the 40 reference images has five caption versions varying in cultural specificity from fully Qatari-specific (v1) to entirely generic (v5), producing 200 instances in total.

| Split | Images | Instances | Gold Labels |
|-------|--------|-----------|-------------|
| Train | 24 | 120 | Released |
| Dev | 8 | 40 | Released |
| Test | 8 | 40 | Hidden (CodaLab only) |

Cultural categories covered: **people and traditional attire**, **architecture and built environment**, and **objects**.

**Caption Versions:**

| Version | Description |
|---------|-------------|
| v1 | Fully Qatari-specific — uses precise cultural terminology |
| v2 | Culturally grounded but less specific |
| v3 | Regional Arab context, no country-specific markers |
| v4 | Generic Middle Eastern |
| v5 | Entirely generic, no cultural content |

### Download Images

TSV files are in this repository under `data/`. Images must be downloaded separately:

> **[Download images — Google Drive](https://drive.google.com/drive/folders/1aCU3O9TgggLTGwJWtAN5SNIfydL4mKrS?usp=sharing)**

After downloading, unzip and place the `imgs/` folder inside each split directory:

```
data/
├── train/
│   ├── captions.tsv
│   ├── gold_human.tsv
│   ├── gold_llm.tsv
│   └── imgs/
│       ├── ref/           ← reference images  (img_001.jpg ...)
│       └── generated/     ← generated images  (img_001_v1.png ...)
├── dev/
│   ├── captions.tsv
│   ├── gold_human.tsv
│   ├── gold_llm.tsv
│   └── imgs/
│       ├── ref/
│       └── generated/
└── test/                  ← released July 20, 2026
    ├── captions.tsv
    └── imgs/
        ├── ref/
        └── generated/
```

### Input Data Format

**captions.tsv** — one row per instance:
```
id              image_id    version    caption
img_001_v1      img_001     v1         Generate an image of a Qatari man...
img_001_v2      img_001     v2         A man wearing traditional attire...
```

Image naming conventions:
- Reference images: `img_001.jpg`, `img_002.jpg` ... `img_040.jpg`
- Generated images: `img_001_v1.png`, `img_001_v2.png` ... `img_040_v5.png`

### Output Data Format

**gold_human.tsv** and **gold_llm.tsv** — one row per instance:
```
id           image_id  version  CRAI_CEA  CRAI_CC  CRAI_CS  CRAI_CI  CRAI_HP  CRAI_composite  category
img_001_v1   img_001   v1       0.94      0.85     0.50     0.87     0.00     0.72             people
```

`gold_human.tsv` contains scores from human annotators and is the gold standard. `gold_llm.tsv` contains GPT-4 scores provided as a reference point for teams building LLM-based approaches.

---

## Scorer and Official Evaluation Metrics

The **primary metric** is **Spearman correlation** between predicted and human-annotated `CRAI_composite` scores. Higher is better.

**Mean Absolute Error (MAE)** on `CRAI_composite` is the secondary metric. Lower is better.

Both metrics are also reported per dimension (CEA, CC, CS, CI, HP) on the leaderboard.

The official scorer is in [evaluation/evaluate.py](./evaluation/evaluate.py). It also runs format checking before computing metrics.

### Running the Scorer

```bash
python evaluation/evaluate.py --gold data/dev/gold_human.tsv --pred predictions.tsv
```

Expected output format:
```
Evaluating on 40 instances

Dimension              Spearman        MAE
------------------------------------------
  CRAI_CEA               0.5592     0.2945
  CRAI_CC                0.6335     0.2645
  CRAI_CS                0.7481     0.1862
  CRAI_CI                0.4699     0.3167
  CRAI_HP                0.0177     0.3375
  CRAI_composite         0.6455     0.2585 <-- PRIMARY
------------------------------------------
Primary metric  ->  Spearman: 0.6455   MAE: 0.2585
```

---

## Baselines

Baseline scripts are in [baselines/](./baselines).

### Installation

```bash
pip install -r baselines/requirements.txt
```

### Baseline 1 — Mean Baseline

Predicts the training set mean score for every instance regardless of the images. Serves as a floor — any real system should beat this.

```bash
python baselines/baseline_random.py \
    --train data/train/gold_human.tsv \
    --test  data/dev/gold_human.tsv \
    --output predictions.tsv

python evaluation/evaluate.py --gold data/dev/gold_human.tsv --pred predictions.tsv
```

Result: `Spearman: N/A   MAE: 0.3450`

### Baseline 2 — GPT-4 Judge (via OpenRouter)

Uses GPT-4 prompted with the CRAI rubric to score each instance by looking at the reference image, caption, and generated image. This is the organizer baseline from the pilot study.

```bash
python baselines/baseline_gpt4.py \
    --captions data/dev/captions.tsv \
    --ref_dir  data/dev/imgs/ref \
    --gen_dir  data/dev/imgs/generated \
    --output   predictions.tsv \
    --api_key  YOUR_OPENROUTER_KEY

python evaluation/evaluate.py --gold data/dev/gold_human.tsv --pred predictions.tsv
```

Result: `Spearman: 0.6455   MAE: 0.2585`

Get an OpenRouter API key at [https://openrouter.ai/keys](https://openrouter.ai/keys).

### Baseline Summary

| System | Spearman | MAE |
|--------|----------|-----|
| Mean baseline | N/A | 0.3450 |
| GPT-4 via OpenRouter | 0.6250 | 0.2248 |

---

## Format Checker

Before submitting to CodaLab, validate your predictions file:

```bash
python format_checker/check_format.py --pred predictions.tsv --split test
```

The checker verifies that:
- The header row is present with the correct column names
- All required instance IDs are present
- All scores are floats in [0.0, 1.0]
- The composite score matches the weighted formula within a tolerance of 0.01

The scorer also runs format checking automatically, so any issues will be caught before metrics are computed.


## Submission

### Guidelines

The process consists of two phases:

1. **System Development Phase:** Participants build and validate systems using the training and development sets.
2. **Final Evaluation Phase:** Participants submit predictions for the blind test set.

For each phase:

- Each team should maintain a single submission account.
- The most recent valid submission before the deadline will be considered final.
- Output filename conventions will be announced with the starter kit.
- Please include team name and a short method description with each submission.

### Submission Site

The official submission site will be announced on the task website.

## Licensing

Dataset licensing information will be included with the released data files.

## Credits

Please find organizers and acknowledgments on the task website: <https://imageeval2026.github.io/>.
