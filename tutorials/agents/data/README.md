# data – Purpose

## About
Contains dataset utilities for the DSPy ReAct agent tutorial. Currently includes a loader for the HoVer question-answering dataset.

## Contents
- `hover_loader.py` – fetches and formats HoVer examples using `dspy.datasets`.

## How to Use
Import `load_hover_data` from this module within training or evaluation scripts to obtain prepared datasets.

## Development Notes
Requires the `datasets` package (<4.0.0) and network access to download data.

## Related Links
- [HoVer dataset](https://hover-nlp.github.io/)

## Status/TODO
Extend with additional dataset loaders as tutorials expand.
