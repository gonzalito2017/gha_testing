import random
import numpy as np
from collections import Counter
from math import log2

#entropía está cerca de su valor máximo:
#Hmax=log2(25)≈4.64 bits

# 1. Simular sorteos históricos
random.seed(26)
historical_draws = [sorted(random.sample(range(1, 26), 14)) for _ in range(1000000)]

# 2. Contar frecuencia de cada número
all_numbers = [num for draw in historical_draws for num in draw]
frequency = Counter(all_numbers)

# 3. Distribución de probabilidad normalizada
total_counts = sum(frequency.values())
prob_dist = {num: freq / total_counts for num, freq in frequency.items()}

# Asegurar que todos los números existan con mínima probabilidad
for i in range(1, 26):
    if i not in prob_dist:
        prob_dist[i] = 0.00001

# 4. Calcular entropía
entropy = -sum(p * log2(p) for p in prob_dist.values())
print(f"Entropía del sistema: {entropy:.4f} bits")

# 5. Generar jugada ponderada
numbers = list(prob_dist.keys())
probabilities = np.array([prob_dist[n] for n in numbers])
probabilities /= probabilities.sum()  # normalizar

predicted_draw = np.random.choice(numbers, size=14, replace=False, p=probabilities)
predicted_draw.sort()
print("Jugada sugerida:", predicted_draw)
