"""
CRAI-Bench Format Checker
==========================
Validates a submission file before uploading to CodaLab.
Catches common errors early so you don't waste a submission attempt.

Usage:
    python format_checker/check_format.py --pred predictions.tsv --split dev
    python format_checker/check_format.py --pred predictions.tsv --split test

The --split argument tells the checker how many instances to expect:
    dev  = 40 instances
    test = 40 instances
"""

import argparse
import csv
import math
import sys

DIMENSIONS     = ['CRAI_CEA', 'CRAI_CC', 'CRAI_CS', 'CRAI_CI', 'CRAI_HP', 'CRAI_composite']
REQUIRED_COLS  = ['id'] + DIMENSIONS
WEIGHTS        = {'CRAI_CEA': 0.30, 'CRAI_CC': 0.20, 'CRAI_CS': 0.20, 'CRAI_CI': 0.20, 'CRAI_HP': -0.10}
CS_VALID       = {0.0, 0.25, 0.50, 0.75, 1.0}
COMPOSITE_TOL  = 0.01   # allowable rounding error in composite score
SPLIT_SIZES    = {'dev': 40, 'test': 40, 'train': 120}


def check_format(pred_path, split):
    errors   = []
    warnings = []
    passed   = True

    # ── 1. File opens and is readable ────────────────────────────────────────
    try:
        with open(pred_path, encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            errors.append("File is empty.")
            return False, errors, warnings
    except FileNotFoundError:
        errors.append(f"File not found: {pred_path}")
        return False, errors, warnings
    except Exception as e:
        errors.append(f"Could not read file: {e}")
        return False, errors, warnings

    # ── 2. Parse TSV ─────────────────────────────────────────────────────────
    with open(pred_path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')

        # 2a. Header row present
        if reader.fieldnames is None:
            errors.append("File has no header row. First row must be the column names.")
            return False, errors, warnings

        # 2b. Required columns present
        missing_cols = [c for c in REQUIRED_COLS if c not in reader.fieldnames]
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")
            errors.append(f"  Found columns: {list(reader.fieldnames)}")
            errors.append(f"  Expected:      {REQUIRED_COLS}")
            return False, errors, warnings

        extra_cols = [c for c in reader.fieldnames if c not in REQUIRED_COLS]
        if extra_cols:
            warnings.append(f"Extra columns will be ignored: {extra_cols}")

        rows = list(reader)

    # ── 3. Row count ─────────────────────────────────────────────────────────
    expected_count = SPLIT_SIZES.get(split)
    if expected_count and len(rows) != expected_count:
        errors.append(
            f"Wrong number of instances: found {len(rows)}, expected {expected_count} for '{split}' split."
        )
        passed = False

    # ── 4. Per-row validation ─────────────────────────────────────────────────
    seen_ids        = {}
    id_format_bad   = []
    score_bad       = []
    cs_bad          = []
    composite_bad   = []

    for i, row in enumerate(rows, start=2):  # start=2 because row 1 is header
        row_id = row.get('id', '').strip()

        # 4a. ID format: must be img_NNN_vN
        if not row_id:
            errors.append(f"Row {i}: missing id.")
            passed = False
            continue

        parts = row_id.rsplit('_', 1)
        if len(parts) != 2 or not parts[0].startswith('img_') or parts[1] not in ['v1','v2','v3','v4','v5']:
            id_format_bad.append(f"Row {i}: '{row_id}' — expected format img_NNN_vN (e.g. img_011_v3)")

        # 4b. Duplicate IDs
        if row_id in seen_ids:
            errors.append(f"Duplicate id '{row_id}' at rows {seen_ids[row_id]} and {i}.")
            passed = False
        seen_ids[row_id] = i

        # 4c. All scores are valid floats in [0, 1]
        scores = {}
        for dim in DIMENSIONS:
            val = row.get(dim, '').strip()
            if val == '':
                score_bad.append(f"Row {i} ({row_id}): '{dim}' is empty.")
                passed = False
                continue
            try:
                f_val = float(val)
            except ValueError:
                score_bad.append(f"Row {i} ({row_id}): '{dim}' = '{val}' is not a number.")
                passed = False
                continue
            if not (-0.15 <= f_val <= 1.0):
                score_bad.append(
                    f"Row {i} ({row_id}): '{dim}' = {f_val:.4f} is out of range. "
                    f"Expected [0.0, 1.0] (composite may be slightly negative due to HP)."
                )
                passed = False
            scores[dim] = f_val

        # 4d. CS must be one of the five valid tiers
        if 'CRAI_CS' in scores:
            if round(scores['CRAI_CS'], 2) not in CS_VALID:
                cs_bad.append(
                    f"Row {i} ({row_id}): CRAI_CS = {scores['CRAI_CS']} is not a valid tier. "
                    f"Must be one of {sorted(CS_VALID)}."
                )

        # 4e. Composite score matches formula within tolerance
        if all(d in scores for d in DIMENSIONS):
            expected_composite = sum(WEIGHTS[d] * scores[d] for d in WEIGHTS)
            actual_composite   = scores['CRAI_composite']
            if abs(expected_composite - actual_composite) > COMPOSITE_TOL:
                composite_bad.append(
                    f"Row {i} ({row_id}): CRAI_composite = {actual_composite:.4f} "
                    f"but formula gives {expected_composite:.4f} "
                    f"(diff = {abs(expected_composite - actual_composite):.4f}, tolerance = {COMPOSITE_TOL})."
                )

    # Consolidate per-row errors
    if id_format_bad:
        errors.extend(id_format_bad)
        passed = False
    if score_bad:
        errors.extend(score_bad)
    if cs_bad:
        warnings.extend(cs_bad)   # warning not error — some systems may predict continuous CS
    if composite_bad:
        errors.extend(composite_bad)
        passed = False

    return passed, errors, warnings


def main():
    parser = argparse.ArgumentParser(description='CRAI-Bench submission format checker')
    parser.add_argument('--pred',  required=True, help='Path to your predictions TSV')
    parser.add_argument('--split', required=True, choices=['train', 'dev', 'test'],
                        help='Which split you are predicting (dev or test)')
    args = parser.parse_args()

    print(f"Checking: {args.pred}  (split: {args.split})\n")
    passed, errors, warnings = check_format(args.pred, args.split)

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  [!] {w}")
        print()

    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  [x] {e}")
        print()

    if passed and not errors:
        print("FORMAT CHECK PASSED — your file is ready to submit.")
        sys.exit(0)
    else:
        print("FORMAT CHECK FAILED — fix the errors above before submitting.")
        sys.exit(1)


if __name__ == '__main__':
    main()
