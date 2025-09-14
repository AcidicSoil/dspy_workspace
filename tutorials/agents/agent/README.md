# agent – Purpose

## About
Defines the ReAct-style agent used in the tutorial. The agent combines reasoning steps with tool usage to answer multi-hop questions.

## Contents
- `react_agent.py` – constructs and returns a configured DSPy agent.

## How to Use
Call `create_react_agent()` from this module to obtain an agent instance for training or evaluation.

## Development Notes
The agent depends on tool functions (e.g., Wikipedia search) residing in `../tools`.

## Related Links
- [ReAct paper](https://arxiv.org/abs/2210.03629)

## Status/TODO
Future versions may expose additional configuration options and support more tools.
