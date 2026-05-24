# [ImageEval](https://imageeval2026.github.io/) at ArabicNLP 2026

ImageEval is an shared task focusing on Arabic Multimodal Generation and Understanding with an special emphasis of Arabic Cultural Grounding.
This repository will contain the datasets, format checkers, scorers, baselines, and starter-kit material for each task.

- [Task 1: Visual Question Answering and Hallucination Detection](task1)

The shared task on *culturally grounded Arabic visual question answering and hallucination detection*. Participants are given an *image* together with an *Arabic question* in MCQ format and must predict the correct answer. The task is offered in *MSA*, *Egyptian*, and *Levantine* Arabic. In addition, the hallucination track evaluates whether systems can distinguish image-grounded interpretations from plausible but unsupported alternatives. Culturally grounded Arabic visual question answering and hallucination detection

- [Task 2: Cultural Accuracy Evaluation in Image Generation](task2)

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

The official schedule is maintained on the task website:

- Task website, training and development data, and evaluation scripts: May 25, 2026
- Registration deadline and blind test set release: July 25, 2026
- Final submission deadline and release of final results: July 30, 2026
- Camera-ready system description papers: August 22, 2026

## Licensing

Please check the task-specific directory for licensing information for the respective dataset. Unless otherwise stated in the released files, dataset material is intended for research use under the task terms.

## Contact

- Website: <https://imageeval2026.github.io/>
- Slack Channel:
- Email: <imageeval2026@gmail.com>

## Citation

The task overview paper should be cited once available. A provisional BibTeX entry is provided in [bibtex/bibliography.bib](bibtex/bibliography.bib).

```bibtex
TBA
```

## Related Resources
https://github.com/ImageEval2026/ImageEval2026-tasks
