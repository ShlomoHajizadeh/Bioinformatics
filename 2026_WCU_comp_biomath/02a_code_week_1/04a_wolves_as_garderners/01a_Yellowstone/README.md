\# Yellowstone Wolf-Bison Ecosystem Model



\## Overview

This project simulates the interaction between wolves, bison, and the environment in Yellowstone National Park. The model demonstrates how wolves act as ecosystem engineers by influencing bison movement patterns, which in turn affects vegetation and forest regrowth.



\## Background

After wolves were reintroduced to Yellowstone in 1995, biologists observed unexpected changes: forests expanded and grasslands recovered. Wolves kept large herbivores like bison moving, preventing overgrazing and allowing trees to regrow.



\## Model Description



\### Agents

\- \*\*Wolves (W)\*\*: Move randomly every k time steps, can occupy both grassland and forest cells

\- \*\*Bison (B)\*\*: Move socially toward cells with more bison, restricted to grassland cells



\### Environment

\- \*\*Toroidal lattice\*\*: Wrap-around boundaries (nx × ny grid)

\- \*\*Grassland cells\*\*: 6 stages (0-5), affected by bison grazing pressure

\- \*\*Forest cells\*\*: Converted from stage-5 grassland after ecological memory delay



\### Rules

1\. Bison are attracted to cells with more bison (social behavior)

2\. Bison flee from cells occupied by wolves

3\. Grassland stage changes based on bison density:

&#x20;  - Stage -1 if >20 bison (overgrazing)

&#x20;  - Stage 0 if 1-20 bison

&#x20;  - Stage +1 if 0 bison (recovery)

4\. Stage-5 grassland converts to forest after m=3 consecutive time steps



\## Installation



```bash

pip install -r requirements.txt

