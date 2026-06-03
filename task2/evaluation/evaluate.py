"""
CRAI-Bench Official Evaluation Script
======================================
Usage:
    python evaluate.py --gold dev/gold_human.tsv --pred predictions.tsv

Output:
    Overall Spearman correlation and MAE against gold human scores,
    plus per-dimension breakdown.
"""

import argparse
import csv
import sys
import warnings
from scipy.stats import spearmanr
from sklearn.metrics import mean_absolute_error

DIMENSIONS = ['CRAI_CEA', 'CRAI_CC', 'CRAI_CS', 'CRAI_CI', 'CRAI_HP', 'CRAI_composite']


def load_tsv(path):
    data = {}
    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        if reader.fieldnames is None or 'id' not in reader.fieldnames:
            print(f"ERROR: '{path}' is missing a header row or 'id' column.")
            print(f"  Found columns: {reader.fieldnames}")
            print(f"  Make sure your predictions file includes the header row.")
            sys.exit(1)
        for row in reader:
            data[row['id']] = {dim: float(row[dim]) for dim in DIMENSIONS if row.get(dim) not in (None, '')}
    return data


def evaluate(gold_path, pred_path):
    gold = load_tsv(gold_path)
    pred = load_tsv(pred_path)

    missing = set(gold.keys()) - set(pred.keys())
    extra   = set(pred.keys()) - set(gold.keys())
    if missing:
        print(f"WARNING: {len(missing)} instances in gold but missing from predictions:")
        for m in sorted(missing):
            print(f"  {m}")
    if extra:
        print(f"WARNING: {len(extra)} predictions not in gold (will be ignored).")

    ids = sorted(set(gold.keys()) & set(pred.keys()))
    if not ids:
        print("ERROR: No overlapping IDs between gold and predictions.")
        sys.exit(1)

    print(f"\nEvaluating on {len(ids)} instances\n")
    print(f"{'Dimension':<20} {'Spearman':>10} {'MAE':>10}")
    print("-" * 42)

    results = {}
    for dim in DIMENSIONS:
        gold_vals = [gold[i][dim] for i in ids if dim in gold[i]]
        pred_vals = [pred[i][dim]  for i in ids if dim in pred[i]]
        if len(gold_vals) < 2:
            continue
        mae = mean_absolute_error(gold_vals, pred_vals)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            rho, _ = spearmanr(gold_vals, pred_vals)

        results[dim] = {'spearman': rho, 'mae': mae}
        marker  = ' <-- PRIMARY' if dim == 'CRAI_composite' else ''
        rho_str = f"{rho:.4f}" if rho == rho else "N/A (constant predictions)"
        print(f"  {dim:<20} {rho_str:>10} {mae:>10.4f}{marker}")

    print("-" * 42)
    composite = results.get('CRAI_composite', {})
    rho_val   = composite.get('spearman')
    mae_val   = composite.get('mae')
    rho_str   = f"{rho_val:.4f}" if rho_val and rho_val == rho_val else "N/A"
    print(f"\nPrimary metric  ->  Spearman: {rho_str}   MAE: {mae_val:.4f}")
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CRAI-Bench evaluation script')
    parser.add_argument('--gold', required=True, help='Path to gold TSV (e.g. dev/gold_human.tsv)')
    parser.add_argument('--pred', required=True, help='Path to your predictions TSV')
    args = parser.parse_args()
    evaluate(args.gold, args.pred)
