# Task 1 Data

The **canonical dataset, including images and audio, lives on the HuggingFace Hub**:

> **[QCRI/ImageEval2026-Task1-AynVQA](https://huggingface.co/datasets/QCRI/ImageEval2026-Task1-AynVQA)**

```python
from datasets import load_dataset
ds = load_dataset("QCRI/AynVQA", "task1a_en", split="devtest")
```

This folder holds only the **JSONL text files** (no images, no audio) so you can
read the format and run the [scorer](../scorer) and [format checker](../format_checker)
without downloading the full media. The `image` and `audio` fields are relative
paths (`images/<id>.jpg`, `audio/<lang>/<id>.wav`) that **point into the media on
the Hub**.

```
data/
├── task1a/
│   ├── train_en.jsonl    train_msa.jsonl     (3000 items, labelled)
│   ├── dev_en.jsonl      dev_msa.jsonl       (500 items, labelled)
│   └── devtest_en.jsonl  devtest_msa.jsonl   (500 items, no labels)
└── task1b/
    ├── train_en.jsonl    train_msa.jsonl
    ├── dev_en.jsonl      dev_msa.jsonl
    └── devtest_en.jsonl  devtest_msa.jsonl
```

The blind **`test`** split (human-recorded audio for Task 1a) is released on the
Hub for the final-evaluation phase.

## Fields

**Task 1a**, `id`, `image`, `audio`, and (labelled splits only) `label` ∈ {0,1,2}.
**Task 1b**, `id`, `image`, `statements` (3), and (labelled splits only) `labels`
(three booleans, exactly one `true`).

`train`/`dev` additionally include `country`, `category`, `subcategory`. These and
the gold labels are omitted from `devtest` and `test`.

## Licensing

CC BY-NC 4.0, non-commercial research use only.
