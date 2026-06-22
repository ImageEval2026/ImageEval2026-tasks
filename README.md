# [ImageEval](https://imageeval2026.github.io/) at ArabicNLP 2026

ImageEval is a shared task on Arabic multimodal generation and understanding, with a special emphasis on Arabic cultural grounding.
This repository will contain the datasets, format checkers, scorers, baselines, and starter-kit material for each task.

- [Task 1: Cultural Grounding in Arabic Multimodal Generation and Understanding](task1)

A culturally grounded Arabic multimodal benchmark. **Subtask 1a (Spoken VQA):** given an image and a *spoken* Arabic question with its options (audio), predict the correct option. **Subtask 1b (Hallucination Detection):** given an image and three statements, judge each as image-grounded (True) or hallucinated (False); exactly one is grounded. Each subtask runs in two language tracks, **English** and **Modern Standard Arabic (MSA)**, scored separately. Data on [HuggingFace](https://huggingface.co/datasets/QCRI/AynVQA-ArabicNLP26).

- [Task 2: Cultural Accuracy Evaluation for Text-to-Image Generation](task2)

Given a reference image of a Qatari cultural scene, a culturally grounded English image caption, and an AI-generated image produced from that caption, participants must produce a CRAI score in [0,1] across five dimensions. Systems are evaluated against human-annotated gold CRAI scores. This subtask benchmarks LLM-as-a-judge approaches against human cultural annotation in Qatari contexts.

## Repository Structure

```text
.
├── bibtex/
│   └── bibliography.bib
├── task1/
│   ├── baselines/
│   ├── data/
│   ├── format_checker/
│   ├── scorer/
│   └── README.md
├── task2/
│   ├── baselines/
│   ├── data/
│   ├── format_checker/
│   ├── scorer/
│   └── README.md
├── README.md
└── requirements.txt
```

## Timeline

The official schedule is maintained on the [task website](https://imageeval2026.github.io/):

- **May 22, 2026:** Task website, training/development data, and evaluation scripts released
- **July 20, 2026:** Registration deadline and blind test set release
- **July 30, 2026:** Final results announced
- **August 15, 2026:** System description papers due
- **August 25, 2026:** Notification of acceptance
- **September 5, 2026:** Camera-ready papers due
- **October 24-29, 2026:** ArabicNLP main conference

## Licensing

Please check the task-specific directory for licensing information for the respective dataset. Unless otherwise stated in the released files, dataset material is intended for research use under the task terms.

## Contact

- Website: <https://imageeval2026.github.io/>
- Slack Channel: <https://join.slack.com/t/mm-eval/shared_invite/zt-41j09ml4j-WMn0NzhqAgT9ZK6e1L8eBA>
- Email: <imageeval2026@gmail.com>

## Citation

The task overview paper should be cited once available. A provisional BibTeX entry is provided in [bibtex/bibliography.bib](bibtex/bibliography.bib).

<!-- ```bibtex
TBA
``` -->

## Related Resources

<!-- - Task website: <https://imageeval2026.github.io/> -->
<!-- - Task 1 dataset (HuggingFace): <https://huggingface.co/datasets/QCRI/AynVQA-ArabicNLP26> -->
