# Symbolic Regression with LLMs

A toy autonomous research loop for symbolic regression. The agent utilizes a local **Qwen 3.5 (9B)** LM (installed through ollama) to iteratively refine `train.py` using a greedy "ratchet" logic to lower the Mean Squared Error (MSE).

---

### 🚀 Overview

At each iteration, the agent modifies `train.py`. If the MSE decreases, the change is kept; otherwise, it is reverted. 

Currently, the agent is instructed to only modify the regression function `regression_fn`. The scope of the modification may be modified.

---

### 📂 Folder Structure

```text
symbolic-learning-agent/
├── agent_loop.py           # The primary orchestration script
├── train_template.py       # The template/seed training script
├── train.py                # The currently best performing training script
├── train.py                # Support material (including ollama commands to spawn qwen)
└── log/                    # Generated candidates (train_001.py, train_002.py, etc.)
```
