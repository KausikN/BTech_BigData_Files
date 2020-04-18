import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return (1/(x*x*x+2*x*x+x))


x = np.arange(-10, 10, 0.1)
plt.plot(x, f(x))
plt.show()

from scipy import optimize

# The default (Nelder Mead)
print(optimize.minimize(f, x0=0))
print(optimize.minimize(f, x0=0, method="L-BFGS-B"))