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
- Slack Channel: <https://join.slack.com/t/mm-eval/shared_invite/zt-44zii4e53-IiZZ3O73Za9XL4umb9mjUQ>
- Email: <imageeval2026@gmail.com>

## Citation

The task overview paper should be cited once available. A provisional BibTeX entry is provided in [bibtex/bibliography.bib](bibtex/bibliography.bib).

### Mandatory citations.



```bibtex
@inproceedings{imageeval-2026,
    title = {{ImageEval 2026}: Culturally Grounded {A}rabic Multimodal Evaluation},
    author = {Abdaljalil, Samir and
              Bhatti, Hunzalah Hassan and
              Bashiti, Ahlam and
              Amir, Farina and
              Hasan, Md Arid and
              Mousi, Basel and
              Durrani, Nadir and
              Dalvi, Fahim and
              Sheikh Ali, Zien and
              Serpedin, Erchin and
              Kurban, Hasan and
              Jarrar, Mustafa and
              Chowdhury, Shammur Absar and
              Alam, Firoj},
    booktitle = {Proceedings of the Fourth Arabic Natural Language Processing Conference: Shared Tasks},
    month = oct,
    year = {2026},
    address = {Budapest, Hungary},
    publisher = {Association for Computational Linguistics}
}

@article{alam2025everydaymmqa,
  title = {{OASIS}: A Multilingual and Multimodal Dataset for Culturally Grounded Spoken Visual QA},
  author = {Alam, Firoj and Shahroor, Ali Ezzat and Hasan, Md. Arid and Ali, Zien Sheikh and Bhatti, Hunzalah Hassan and Kmainasi, Mohamed Bayan and Chowdhury, Shammur Absar and Mousi, Basel and Dalvi, Fahim and Durrani, Nadir and Milic-Frayling, Natasa},
  journal = {arXiv preprint arXiv:2510.06371},
  year = {2025},
}

@inproceedings{mousi-etal-2026-correct,
    title = "Once Correct, Still Wrong: Counterfactual Hallucination in Multilingual Vision-Language Models",
    author = "Mousi, Basel  and
      Dalvi, Fahim  and
      Chowdhury, Shammur Absar  and
      Alam, Firoj  and
      Durrani, Nadir",
    editor = "Liakata, Maria  and
      Moreira, Viviane P.  and
      Zhang, Jiajun  and
      Jurgens, David",
    booktitle = "Findings of the {A}ssociation for {C}omputational {L}inguistics: {ACL} 2026",
    month = jul,
    year = "2026",
    address = "San Diego, California, United States",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.findings-acl.234/",
    doi = "10.18653/v1/2026.findings-acl.234",
    pages = "4763--4788",
    ISBN = "979-8-89176-395-1",
}

@inproceedings{mousi2026said,
  title     = {Said Aloud, Read Different: Cross-Modal Instability in Multimodal Models},
  author    = {Mousi, Basel and Dalvi, Fahim and Chowdhury, Shammur and Alam, Firoj and Durrani, Nadir},
  booktitle = {Proceedings of Interspeech 2026},
  year      = {2026},
  address   = {Sydney, Australia},
  note = {accepted}
}
```



## Related Resources

<!-- - Task website: <https://imageeval2026.github.io/> -->
<!-- - Task 1 dataset (HuggingFace): <https://huggingface.co/datasets/QCRI/AynVQA-ArabicNLP26> -->
