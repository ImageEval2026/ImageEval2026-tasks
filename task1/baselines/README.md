# Task 1 Baselines

Starter **Colab notebooks** that run end to end — install deps → download the
data from HuggingFace → run a model → write a Codabench-ready `prediction.zip`.
They default to the **English** track and the **devtest** split; both are flags
you can flip in the config cell (`LANG = "en" | "msa"`). These are **references
only** — you are free to use your own models, prompts, and configurations.

| notebook | subtask | what it does | open in Colab |
|---|---|---|---|
| [`baseline_task1a_colab.ipynb`](./baseline_task1a_colab.ipynb) | 1a | open omni model **Qwen2.5-Omni-3B** (4-bit), listens to the audio + sees the image | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ImageEval2026/ImageEval2026-tasks/blob/main/task1/baselines/baseline_task1a_colab.ipynb) |
| [`baseline_task1c_colab.ipynb`](./baseline_task1c_colab.ipynb) | 1c | open VLM **Qwen2.5-VL-3B** (4-bit), True/False per statement | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ImageEval2026/ImageEval2026-tasks/blob/main/task1/baselines/baseline_task1c_colab.ipynb) |
| [`baseline_task1a_fanar_cascade_colab.ipynb`](./baseline_task1a_fanar_cascade_colab.ipynb) | 1a | **cascaded API** baseline: Fanar `Aura-STT` (speech→text) → `Oryx` (image understanding); **no GPU** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ImageEval2026/ImageEval2026-tasks/blob/main/task1/baselines/baseline_task1a_fanar_cascade_colab.ipynb) |

The notebooks are also mirrored on
[Google Drive](https://drive.google.com/drive/folders/1zDO2uXq0fEQhfNj8M2DstkNL1-EEXybT?usp=sharing).

## Running

- **Open-model notebooks** need a GPU runtime — in Colab, *Runtime → Change
  runtime type → T4 GPU*. They load the model in **4-bit** so it fits a free T4.
- **Fanar cascade** needs no GPU, just a Fanar API key (set it in the config cell).
  Get one at [api.fanar.qa](https://api.fanar.qa/).
- Each notebook ends by writing `prediction.zip` in the submission format, ready
  to upload to the matching Codabench competition.

## Reference scores (devtest)

| subtask | track | model | metric | score |
|---|---|---|---|---|
| 1a | English | Qwen2.5-Omni | accuracy | 0.6640 |
| 1a | MSA     | Qwen2.5-Omni | accuracy | 0.3980 |
| 1c | English | Qwen2.5-VL   | combined accuracy | 0.6840 |
| 1c | MSA     | Qwen2.5-VL   | combined accuracy | 0.5080 |

## Local install (if running outside Colab)

```bash
pip install -r requirements.txt
```
