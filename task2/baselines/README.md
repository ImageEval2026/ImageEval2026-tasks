# Task 2 Baselines

## Installation
```bash
pip install -r requirements.txt
```

## Baseline 1 — Mean Baseline
```bash
python baseline_random.py \
    --train ../data/train/gold_human.tsv \
    --test  ../data/dev/gold_human.tsv \
    --output predictions.tsv
```

## Baseline 2 — GPT-4 Judge via OpenRouter
```bash
python baseline_gpt4.py \
    --captions ../data/dev/captions.tsv \
    --ref_dir  ../data/dev/imgs/ref \
    --gen_dir  ../data/dev/imgs/generated \
    --output   predictions.tsv \
    --api_key  YOUR_OPENROUTER_KEY
```

