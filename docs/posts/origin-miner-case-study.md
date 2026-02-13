---
tags:
  - Python
  - Git
  - Forensics
---
# Forensic Git Auditing: Introducing Origin-Miner v1.0.1

*Published: February 12, 2026*

How can you tell the difference between a human writing code and an AI pasting it? That was the question that led me to build **Origin-Miner**.

## The Problem: The "LLM Signature"

Traditional Git statistics focus on lines of code (LOC). However, in the age of AI, volume is cheap. What matters now is **velocity** and **intent**.

### The Forensic Logic

Our engine uses a multi-factor scoring system to determine if a commit is "suspicious." One of the core metrics is **Lines Per Minute (LPM)**.

$$\text{LPM} = \frac{\Delta \text{Lines}}{\Delta \text{Time (Minutes)}}$$

If a developer "writes" 500 lines of complex logic in 2 minutes, the LPM spikes, and the suspicion gate (currently calibrated at **75%**) triggers a flag.

## Key Features

* **SQLite Caching**: High-performance auditing that doesn't re-scan the same history twice.
* **Rich CLI**: Beautiful terminal output for quick team audits.
* **Forensic Normalization**: Our logic accounts for "bursty" coding patterns to avoid false positives on boilerplate.

## Installation

You can install the tool directly from PyPI:

```bash
uv tool install origin-miner
miner --path .
