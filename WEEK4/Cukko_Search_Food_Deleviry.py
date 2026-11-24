
import random
import math

locations = {}

n = int(input("Enter number of customers: "))

locations["Restaurant"] = (
    float(input("Enter restaurant X coordinate: ")),
    float(input("Enter restaurant Y coordinate: "))
)

customers = []

for i in range(n):
    name = "Customer" + str(i + 1)
    print("\nEnter location of", name)
    x = float(input("X coordinate: "))
    y = float(input("Y coordinate: "))
    locations[name] = (x, y)
    customers.append(name)

N = int(input("\nEnter number of nests: "))
Pa = float(input("Enter discovery probability (0 to 1): "))
iterations = int(input("Enter maximum iterations: "))

def distance(a, b):
    x1, y1 = locations[a]
    x2, y2 = locations[b]
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def fitness(route):
    total = 0
    current = "Restaurant"

    for customer in route:
        total += distance(current, customer)
        current = customer

    total += distance(current, "Restaurant")
    return total

def levy_flight(route):
    new_route = route.copy()

    if len(route) >= 2:
        step = abs(random.gauss(0, 1) /
                   random.gauss(0, 1))

        swaps = max(1, min(len(route), int(step * 3)))

        for _ in range(swaps):
            i, j = random.sample(range(len(route)), 2)
            new_route[i], new_route[j] = new_route[j], new_route[i]

    return new_route

nests = [
    random.sample(customers, len(customers))
    for _ in range(N)
]

best_route = min(nests, key=fitness)
best_distance = fitness(best_route)

for iteration in range(iterations):

    for i in range(N):
        new_route = levy_flight(nests[i])
        j = random.randrange(N)

        if fitness(new_route) < fitness(nests[j]):
            nests[j] = new_route

    nests.sort(key=fitness)

    abandon_count = int(Pa * N)

    for i in range(N - abandon_count, N):
        nests[i] = random.sample(customers, len(customers))

    current_best = min(nests, key=fitness)

    if fitness(current_best) < best_distance:
        best_route = current_best.copy()
        best_distance = fitness(best_route)

print("\n========== FOOD DELIVERY RESULT ==========")

print("\nOptimized Delivery Route:")

print("Restaurant", end="")

for customer in best_route:
    print(" ->", customer, end="")

print(" -> Restaurant")

print("\nMinimum Delivery Distance:",
      round(best_distance, 2), "units")

print("\nTotal Customers:", n)
print("Total Nests:", N)
print("Discovery Probability:", Pa)
print("Iterations:", iterations)

print("\n==========================================")
