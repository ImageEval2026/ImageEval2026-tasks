"""
CRAI-Bench Random Baseline
===========================
Predicts the mean score from the training set for every instance.
Serves as a sanity-check floor — any real system should beat this.

Usage:
    python baseline_random.py --train train/gold_human.tsv --test dev/gold_human.tsv --output predictions.tsv
"""

import argparse
import csv
import statistics

DIMENSIONS = ['CRAI_CEA', 'CRAI_CC', 'CRAI_CS', 'CRAI_CI', 'CRAI_HP', 'CRAI_composite']


def load_tsv(path):
    rows = []
    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            rows.append(row)
    return rows


def main(train_path, test_path, output_path):
    train_rows = load_tsv(train_path)
    test_rows  = load_tsv(test_path)

    # Compute mean per dimension from training set
    train_means = {}
    for dim in DIMENSIONS:
        vals = [float(r[dim]) for r in train_rows if r.get(dim) not in (None, '')]
        train_means[dim] = statistics.mean(vals) if vals else 0.5

    print("Training set means (used as predictions):")
    for dim, mean in train_means.items():
        print(f"  {dim:<20}: {mean:.4f}")

    # Write predictions
    out_cols = ['id'] + DIMENSIONS
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=out_cols, delimiter='\t')
        writer.writeheader()
        for row in test_rows:
            out = {'id': row['id']}
            for dim in DIMENSIONS:
                out[dim] = round(train_means[dim], 4)
            writer.writerow(out)

    print(f"\nPredictions written to {output_path} ({len(test_rows)} instances)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CRAI-Bench mean baseline')
    parser.add_argument('--train',  required=True, help='Path to training gold TSV')
    parser.add_argument('--test',   required=True, help='Path to test/dev input TSV')
    parser.add_argument('--output', default='predictions.tsv', help='Output predictions file')
    args = parser.parse_args()
    main(args.train, args.test, args.output)
