import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set random seed for reproducibility
np.random.seed(0)

# Define parameters
n_months = 60
n_stocks = 50

# Generate date range and stock symbols
dates = pd.date_range('1/1/2020', periods=n_months)
symbols = [f'Stock {i}' for i in range(n_stocks)]

# Generate random returns
returns = pd.DataFrame(np.random.normal(0.001, 0.02, (n_months, n_stocks)), index=dates, columns=symbols)

# Calculate volatility with a rolling window of 20 days
volatility = returns.rolling(window=20).std() * np.sqrt(252) 

# Initialize 3D plot
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Set up meshgrid for 3D plot
x = np.arange(volatility.shape[0])
y = np.arange(volatility.shape[1])
X, Y = np.meshgrid(y, x)
Z = volatility.values

# Plot surface
ax.plot_surface(X, Y, Z)

# Set labels
ax.set_xlabel('Stocks')
ax.set_ylabel('Date')
ax.set_zlabel('Volatility')

# Show plot
plt.show()
