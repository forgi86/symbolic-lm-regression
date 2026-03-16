# Symbolic Regression with LLMs

A toy autonomous research loop for symbolic regression. The agent utilizes a local **Qwen 3.5 (9B)** language model to iteratively refine `train.py` using a greedy "ratchet" logic. Just one goal - lower the Mean Squared Error!

This is my first experiment with agents and it is heavily vibe-coded. Forgive me if it's too naive or redundant!

---

### 🚀 Overview

At each iteration, the agent edits `train.py`. Currently, it is instructed to only change the regressor function `regression_fn`. In the template it is:

```python
def regression_fn(x, a, b, c):
    return a * x**2 + b * x + c
```
However, the data is better described by a sinusoid.

**The Ratchet Logic:**
- If the MSE decreases, the change is promoted to the new "best" state.
- If the MSE increases or the script fails, the change is discarded, but the failure is logged to inform the next iteration.

---

### 🧪 Usage

1. Start the Ollama server (in a separate terminal):

```bash
ollama serve
```

2. Pull / run the local model (in another terminal):

```bash
ollama run qwen2.5:9b
```

3. Run the agent loop:

```bash
python agent_loop.py
```
---

#### Outcome
At the third iteration, the agent proposes:
```python
def regression_fn(x, a, b, c):
    return a * np.sin(b * x) + c
```
This solves the benchmark!

---

### Requirements
The code happily runs on my MacBook Pro M2, 16GB.

---

### 📂 Folder Structure

```text
symbolic-learning-agent/
├── agent_loop.py           # The primary orchestration script
├── train_template.py       # The template/seed training script
├── train.py                # The currently best performing training script
├── README.md               # Project documentation and setup instructions
└── log/                    # Generated candidates (train_001.py, train_002.py, etc.)
```
