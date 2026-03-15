import os
import shutil
import subprocess
import requests
import re

def run_ollama_chat(messages):
    """
    Uses the Chat API to maintain conversation state.
    """
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "qwen3.5:9b",
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.6  # Reduced for more consistent structural reasoning
        }
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return res.json()['message']['content']
    except Exception as e:
        print(f"Ollama API Error: {e}")
        return None


def evaluate(filename="train.py"):
    """
    Executes the script and captures the MSE via regex parsing.
    """
    if not os.path.exists(filename):
        return float('inf')
    try:
        # Increased timeout slightly for complex curve_fit operations
        result = subprocess.run(["python3", filename], capture_output=True, text=True, timeout=15)
        
        if result.returncode != 0:
            # It's helpful to print the error so you can see why the agent failed
            print(f"Runtime Error: {result.stderr.splitlines()[-1]}")
            return float('inf')

        # Use regex to find the float value after 'MSE:'
        match = re.search(r"MSE:\s*([\d\.e\+\-]+)", result.stdout)
        if match:
            return float(match.group(1))
        
        print(f"Parsing Error: Could not find MSE in output: {result.stdout}")
        return float('inf')
        
    except subprocess.TimeoutExpired:
        print(f"Timeout: {filename} exceeded time limit.")
        return float('inf')
    except Exception as e:
        print(f"Unexpected Evaluation Error: {e}")
        return float('inf')



# --- CONFIGURATION ---
TEMPLATE_FILE = "train_template.py"
TARGET_FILE = "train.py"
ITERATIONS = 5

# 0. Initialize Workspace
if not os.path.exists(TEMPLATE_FILE):
    raise FileNotFoundError(f"Critical: {TEMPLATE_FILE} not found. Cannot initialize loop.")

# Copy template to target to start the session
shutil.copyfile(TEMPLATE_FILE, TARGET_FILE)
print(f"Initialized {TARGET_FILE} from {TEMPLATE_FILE}")

# Initialize System Persona
messages = [
    {
        "role": "system", 
        "content": "You are a System Identification agent. You iterate on Python code to fit a dataset. "
                   "Always output the FULL code for train.py inside a ```python code block."
    }
]

# --- BASELINE EVALUATION ---
# Before starting, check if a baseline exists and score it
best_mse = evaluate(TARGET_FILE)
if best_mse == float('inf'):
    print("No valid baseline found in train.py. Starting from scratch.")
else:
    print(f"Initial Baseline MSE: {best_mse:.4f}")

best_code = ""

# Start the Loop
for i in range(ITERATIONS):
    print(f"\n--- Iteration {i+1} ---")
    
    # Read current state of the code to show the agent its 'Old Code'
    current_code = ""
    if os.path.exists(TARGET_FILE):
        with open(TARGET_FILE, "r") as f:
            current_code = f.read()

    # Construct the User Message with History/State
    prompt = f"Current Best MSE: {best_mse}\n"
    if current_code:
        prompt += f"Current Code in {TARGET_FILE}:\n```python\n{current_code}\n```\n"
    
    prompt += ("You can ONLY modify function regression_fn (e.g., try other polynomials, exponentials, logarithmic, trigonometric, ....) "
               "Do NOT change the structure of the code outside of that function."
               "Do NOT try different functions in the same iteration."
               "The objective is to minimize MSE"
        )
    
    messages.append({"role": "user", "content": prompt})
    
    # 1. Generate new hypothesis
    response = run_ollama_chat(messages)
    if not response: break
    
    # 2. Extract code from Markdown
    code_match = re.search(r'```python\n(.*?)\n```', response, re.DOTALL)
    new_hypothetical_code = code_match.group(1) if code_match else response
    
    # 3. Apply change and Evaluate
    # We use a temporary file to evaluate before committing to the 'best' state
    with open("temp_candidate.py", "w") as f:
        f.write(new_hypothetical_code)
    
    current_mse = evaluate("temp_candidate.py")
    print(f"Candidate MSE: {current_mse}")

    # 4. The Ratchet (Logic for keeping/reverting)
    if current_mse < best_mse:
        print(f"✅ IMPROVEMENT: {best_mse:.4f} -> {current_mse:.4f}")
        best_mse = current_mse
        best_code = new_hypothetical_code
        with open(TARGET_FILE, "w") as f:
            f.write(best_code)
        
        # Add success to context
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": f"Success. MSE improved to {current_mse}."})
    else:
        print(f"❌ REGRESSION: MSE was {current_mse:.4f}. Reverting to best known code.")
        # We don't overwrite TARGET_FILE, keeping the best version intact.
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": f"Failure. That change resulted in MSE {current_mse}. Try a different approach than the one above."})

print(f"\nOptimization Finished. Best MSE: {best_mse}")