# agent_loop.py
import os
import subprocess
import requests

def run_ollama(prompt):
    res = requests.post("http://localhost:11434/api/generate", 
                        json={"model": "qwen3.5:9b", "prompt": prompt, "stream": False})
    return res.json()['response']

def evaluate():
    # Runs the current model.py and returns the Mean Squared Error (MSE)
    result = subprocess.run(["python3", "model.py"])#, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return float('inf')

best_mse = float('inf')

for i in range(5):  # 5 iterations of the "Ratchet"
    print(f"\n--- Iteration {i+1} ---")
    
    # 1. Ask the agent to improve the code
    instruction = f"Current best MSE is {best_mse}. Edit model.py to try a different function to minimize MSE. Output ONLY the full python code."
    new_code = run_ollama(instruction)
    
    # 2. Apply the change (The "Modify" step)
    with open("model.py", "w") as f:
        f.write(new_code.strip('`python\n'))
    
    # 3. Evaluate
    current_mse = evaluate()
    print(f"Agent proposed change. Resulting MSE: {current_mse}")
    
    # 4. The Ratchet (Keep or Revert)
    if current_mse < best_mse:
        print("✅ Improvement found! Keeping change.")
        best_mse = current_mse
        # Optional: git commit -am "Improvement"
    else:
        print("❌ Regression. Reverting.")
        # In a real setup, you'd use 'git checkout model.py'