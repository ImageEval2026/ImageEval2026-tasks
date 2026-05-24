# Task 2:  Cultural Accuracy Evaluation

The aim of this task is ....

__Table of contents:__
- [List of Versions](#list-of-versions)
- [Contents of the Directory](#contents-of-the-directory)
- [Task Description](#task-description)
- [Dataset](#dataset)
- [Scorer and Official Evaluation Metrics](#scorer-and-official-evaluation-metrics)
- [Baselines](#baselines)
- [Format Checker](#format-checker)
- [Submission](#submission)
- [Licensing](#licensing)
- [Credits](#credits)

## List of Versions

* __[TBD]__ Training and development data will be released after task acceptance and data packaging.

## Contents of the Directory

* Main folder: [data](./data)<br/>
  Contains files for Task 2 subtasks once released.
* Main folder: [baselines](./baselines)<br/>
  Contains baseline scripts for the task once released.
* Main folder: [format_checker](./format_checker)<br/>
  Contains scripts to check submission file format once released.
* Main folder: [scorer](./scorer)<br/>
  Contains official scorer scripts once released.
* [README.md](./README.md)<br/>
  This file.

## Task Description


## Dataset

### Input Data Format


### Output Data Format


## Scorer and Official Evaluation Metrics

The official metric for all subtasks is **macro-F1**. Accuracy, macro-precision, macro-recall, and weighted F1 may also be reported.

The scorer will be released in [scorer](./scorer). It will invoke the format checker before computing metrics.

## Baselines

Baseline scripts will be released in [baselines](./baselines). Planned starter baselines include majority, random, and transformer-based text baselines.

## Format Checker

The format checker will be released in [format_checker](./format_checker). It will verify that submission files follow the expected structure before scoring.

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
