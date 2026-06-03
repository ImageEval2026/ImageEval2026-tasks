# Task 2 Scorer

The **primary metric** is **Spearman correlation** between your predicted `CRAI_composite` scores and the human-annotated gold `CRAI_composite` scores. Higher is better.
**Mean Absolute Error (MAE)** on `CRAI_composite` is the secondary metric. Lower is better.

## Run the scorer
```bash
python evaluate.py --gold ../data/dev/gold_human.tsv --pred predictions.tsv
```

## Sample submission
See `sample_submission.tsv` for the required format.

