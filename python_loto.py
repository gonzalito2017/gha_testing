import random
import numpy as np
import pandas as pd
from collections import Counter
from math import log2

#entropía está cerca de su valor máximo:
#Hmax=log2(41)≈5.3576 bits.

# | Cantidad de sorteos | ¿Sirve para encontrar patrones?     | Entropía esperada |
# | ------------------- | ----------------------------------- | ----------------- |
# | 100                 | Puede haber sesgos espurios (ruido) | \~4.5 – 5.2 bits  |
# | 1.000               | Más estable, pero aún algo variable | \~5.3 bits        |
# | 10.000              | Prácticamente uniforme              | \~5.3576 bits     |



# 1. Simulación de datos históricos (100 sorteos con 6 números entre 1 y 41)
np.random.seed(42)
historical_draws = [sorted(random.sample(range(1, 42), 6)) for _ in range(10000)]

# 2. Contar frecuencia de aparición de cada número
all_numbers = [num for draw in historical_draws for num in draw]
frequency = Counter(all_numbers)

# 3. Calcular distribución de probabilidad (normalizada)
total_counts = sum(frequency.values())
prob_dist = {num: freq / total_counts for num, freq in frequency.items()}

# Asegurar que todos los números estén representados
for i in range(1, 42):
    if i not in prob_dist:
        prob_dist[i] = 0.00001  # Evita log2(0) y permite algo de aleatoriedad

# 4. Calcular entropía del sistema
entropy = -sum(p * log2(p) for p in prob_dist.values())
print(f"Entropía del sistema: {entropy:.4f} bits")

# 5. Generar una jugada ponderada: más probabilidad a los números más frecuentes
numbers = list(prob_dist.keys())
probabilities = list(prob_dist.values())

# Normalizar por si suman más de 1 (por el ajuste)
probabilities = np.array(probabilities)
probabilities = probabilities / probabilities.sum()

# Elegir 6 números distintos con probabilidad ponderada
predicted_draw = np.random.choice(numbers, size=6, replace=False, p=probabilities)
predicted_draw.sort()
print("Jugada sugerida:", predicted_draw)
