import numpy as np
import matplotlib.pyplot as plt

#create a non-normally distributed population data
population = no.random.exponential(scale=2, size=1000000)

#sample means
sample.means =[]

#take 1000 samples of size 50 and compute their means
for i in range(1000):
    sample = np.random.choice(population, 50)
    sample_means.append(sample.mean())

#plotting the sameple means (should approximate a normal distribution)
plt.hist(sample_means, bins=50, density=True)
plt.title('Sample Means of Exponential Distribution')
plt.xlabel('Sample Mean')
plt.ylabel('Frequency')

# add a linear line to the histogram
plt.axvline(x=np.mean(sample_means), color='r', linestyle='--', linewidth=2)
plt.show()

#poisson distribution based on population size above
population = np.random.poisson(lam=2, size=1000000)
sample_means =[]
for i in range(1000):
    sample = np.random.choice(population, 50)
    sample_means.append(sample.mean())
plt.hist(population, bins=50, density=True)
plt.title('Poisson Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

