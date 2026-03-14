import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

# Load data
df = pd.read_csv('data.csv')
x, y = df['x'], df['y']

# --- AGENT MODIFIES ONLY THIS SECTION ---
# Hint: Here we assime a quadratic relationship, but this is just a guess.
# You may try different functions to minimize MSE.
def func(x, a, b, c):
    return a * x**2 + b * x + c

popt, _ = curve_fit(func, x, y)
y_pred = func(x, *popt)
# ---------------------------------------

mse = mean_squared_error(y, y_pred)
print(f"MSE: {mse:.4f}")