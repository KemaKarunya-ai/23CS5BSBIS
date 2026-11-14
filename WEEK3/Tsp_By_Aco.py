
import numpy as np
import random

# ---------------------------------------
# 1. Define the cities and coordinates
# ---------------------------------------

cities = {
    0: (0, 0),
    1: (2, 3),
    2: (5, 2),
    3: (6, 6),
    4: (8, 3)
}

n = len(cities)

# Calculate distance between every pair of cities
distance = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if i != j:
            x1, y1 = cities[i]
            x2, y2 = cities[j]

            distance[i][j] = np.sqrt(
                (x2 - x1)**2 + (y2 - y1)**2
            )

# ---------------------------------------
# 2. Initialize ACO parameters
# ---------------------------------------

num_ants = 5
alpha = 1
beta = 2
rho = 0.5
Q = 100
iterations = 50


# Initial pheromone values
pheromone = np.ones((n, n))

# Heuristic information (1 / distance)
heuristic = 1 / (distance + 1e-10)

best_path = None
best_distance = float('inf')

# ---------------------------------------
# 3. Construct solutions
# ---------------------------------------

for iteration in range(iterations):

    all_paths = []
    all_distances = []

    for ant in range(num_ants):

        start = random.randint(0, n - 1)
        path = [start]

        unvisited = list(range(n))
        unvisited.remove(start)

        while unvisited:

            current = path[-1]

            probabilities = []

            for city in unvisited:

                value = (
                    pheromone[current][city] ** alpha
                ) * (
                    heuristic[current][city] ** beta
                )

                probabilities.append(value)

            total = sum(probabilities)

            probabilities = [
                p / total for p in probabilities
            ]

            next_city = random.choices(
                unvisited,
                weights=probabilities
            )[0]

            path.append(next_city)
            unvisited.remove(next_city)

        # Return to starting city
        path.append(start)

        # Calculate total route distance
        total_distance = 0

        for i in range(len(path) - 1):
            total_distance += distance[path[i]][path[i + 1]]

        all_paths.append(path)
        all_distances.append(total_distance)

        # Update best solution
        if total_distance < best_distance:
            best_distance = total_distance
            best_path = path.copy()

    # ---------------------------------------
    # 4. Update pheromones
    # ---------------------------------------

    pheromone *= (1 - rho)

    for path, route_distance in zip(
        all_paths, all_distances
    ):

        deposit = Q / route_distance

        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]

            pheromone[a][b] += deposit
            pheromone[b][a] += deposit

# ---------------------------------------
# 5 & 6. Output the best solution
# ---------------------------------------

print("Best Route:", best_path)
print("Shortest Distance:", round(best_distance, 2))
