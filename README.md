# Symbolic Learning with LLMs

A toy autonomous research loop for symbolic regression. The agent utilizes **Qwen 3.5 (9B)** to iteratively refine the model structure using a greedy "ratchet" logic to converge on the lowest Mean Squared Error (MSE).

---

### 🚀 Overview

At each iteration, the agent modifies `train.py`. If the MSE decreases, the change is kept; otherwise, it is reverted. 

Currently, the agent is instructed to only modify the regression function `regression_fn`. The scope of modification may be expanded in future iterations to include optimization hyperparameters or data preprocessing steps.

---

### 📂 Folder Structure

```text
symbolic-learning-agent/
├── agent_loop.py           # The primary orchestration script
├── train_template.py       # The template/seed training script
├── train.py                # The currently best performing training script
└── log/      # Archive of all historical candidates (train_001.py, train_002.py, etc.)
