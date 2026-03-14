import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

# Load data
df = pd.read_csv('data.csv')
x, y = df['x'], df['y']

# --- AGENT MODIFIES THIS SECTION ---
# Current Model: Simple Linear (Bad fit)
y_pred = 0.5 * x
# -----------------------------------

mse = mean_squared_error(y, y_pred)
print(f"MSE: {mse:.4f}")