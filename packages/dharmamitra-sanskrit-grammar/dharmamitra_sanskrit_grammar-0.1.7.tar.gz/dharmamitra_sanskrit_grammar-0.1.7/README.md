# Sanskrit Processor

A Python package for processing Sanskrit text using the Dharmamitra API.

## Installation

```bash
pip install dharmamitra-sanskrit-grammar
```

## Usage

```python
from dharmamitra_sanskrit_grammar import DharmamitraSanskritProcessor

# Initialize the processor
processor = DharmamitraSanskritProcessor()

# Process a batch of sentences
sentences = [
    "tapaḥsvādhyāyanirataṃ tapasvī vāgvidāṃ varam",
    "nāradaṃ paripapraccha vālmīkirmunipuṃgavam"
]

# Using different modes
results = processor.process_batch(
    sentences,
    mode="lemma",  # or 'unsandhied' or 'unsandhied-lemma-morphosyntax'
    human_readable_tags=True
)
```

## Available Modes

- `lemma`: Basic lemmatization
- `unsandhied`: Word segmentation only
- `unsandhied-lemma-morphosyntax`: Full analysis with word segmentation, lemmatization, and morphosyntax

## Output format

Default is 'dict', but if you set it to 'string' you will get a simple string version of just the lemmas in 'lemma' mode or the unsandhied surface forms in 'unsandhied' mode. This should be handy for information-retrieval setups. 

## Project 
You can visit an interactive version of this at [dharmamitra.org]. 
A github repository for the underlying model is [here](https://github.com/sebastian-nehrdich/byt5-sanskrit-analyzers/). 

## Citation 
The preprint is available on [arxiv](https://arxiv.org/abs/2409.13920). 
If you like our work and use it in your research, feel free to cite the paper:
```
@inproceedings{
nehrdichetal2024,
title={One Model is All You Need: ByT5-Sanskrit, a Unified Model for Sanskrit {NLP} Tasks},
author={Nehrdich, Sebastian and Hellwig, Oliver and Keutzer, Kurt},
booktitle={Findings of the 2024 Conference on Empirical Methods in Natural Language Processing},
year={2024},
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.