# config – Purpose

## About
Holds configuration utilities for the tutorial's agent, primarily model selection and initialization.

## Contents
- `models.py` – defines `setup_models()` which configures the language models used during training and evaluation.

## How to Use
Import `setup_models` to obtain model instances tailored for your hardware or API endpoints.

## Development Notes
The default configuration targets local models via LiteLLM; adjust to suit your environment.

## Related Links
- [LiteLLM](https://github.com/BerriAI/litellm)

## Status/TODO
Consider adding YAML-based configuration for easier customization.
