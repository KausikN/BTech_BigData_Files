import numpy as np
from scipy import optimize

# Function
def F(x):
    v = ((x**3) -2*(x**2) + x)
    if v == 0:
        return 1
    return (1/((x**3) -2*(x**2) + x))

# Genetic Optimisation
print(optimize.minimize(F, x0=0))
print(optimize.minimize(F, x0=0, method="L-BFGS-B"))
quit()