import numpy as np

# 1. GET REAL-TIME USER INPUT & DEFINE THE PROBLEM
print("=== EV Fast-Charging Station Scheduler (GWO) ===")
MAX_STATION_POWER = float(input("Enter max station transformer capacity (kW) [e.g., 100]: "))
MAX_CHARGER_POWER = float(input("Enter max power per charger port (kW) [e.g., 40]: "))
NUM_EVS = int(input("Enter number of EVs currently plugged in: "))

ev_energy_needed = np.zeros(NUM_EVS)
ev_urgency = np.zeros(NUM_EVS)

print("\n--- Enter Details for Each EV ---")
for i in range(NUM_EVS):
    ev_energy_needed[i] = float(input(f"EV {i+1} - Energy required (kWh): "))
    ev_urgency[i] = float(input(f"EV {i+1} - Urgency priority (1=Low to 5=High): "))

def objective_function(power_alloc):
    """Minimizes urgency-weighted charging time without overloading the grid."""
    charging_hours = ev_energy_needed / (power_alloc + 0.1)  # +0.1 avoids division by zero
    weighted_delay = np.sum(ev_urgency * charging_hours)
    
    total_power = np.sum(power_alloc)
    overload_penalty = 500.0 * max(0.0, total_power - MAX_STATION_POWER)
    
    return weighted_delay + overload_penalty

# 2. INITIALIZE GWO PARAMETERS
num_wolves = 25
max_iter = 100
lb, ub = 0.0, MAX_CHARGER_POWER

# 3. INITIALIZE POPULATION
positions = np.random.uniform(lb, ub, (num_wolves, NUM_EVS))

alpha_pos, beta_pos, delta_pos = np.zeros(NUM_EVS), np.zeros(NUM_EVS), np.zeros(NUM_EVS)
alpha_score, beta_score, delta_score = float("inf"), float("inf"), float("inf")

# 6. ITERATE
for t in range(max_iter):
    # 4. EVALUATE FITNESS & UPDATE HIERARCHY (Alpha, Beta, Delta)
    for i in range(num_wolves):
        positions[i] = np.clip(positions[i], lb, ub)
        fitness = objective_function(positions[i])

        if fitness < alpha_score:
            delta_score, delta_pos = beta_score, beta_pos.copy()
            beta_score, beta_pos = alpha_score, alpha_pos.copy()
            alpha_score, alpha_pos = fitness, positions[i].copy()
        elif fitness < beta_score:
            delta_score, delta_pos = beta_score, beta_pos.copy()
            beta_score, beta_pos = fitness, positions[i].copy()
        elif fitness < delta_score:
            delta_score, delta_pos = fitness, positions[i].copy()

    # Linearly decrease 'a' from 2 to 0
    a = 2.0 - t * (2.0 / max_iter)

    # 5. UPDATE POSITIONS
    for i in range(num_wolves):
        for d in range(NUM_EVS):
            r1, r2 = np.random.rand(), np.random.rand()
            A1, C1 = 2 * a * r1 - a, 2 * r2
            D_alpha = abs(C1 * alpha_pos[d] - positions[i, d])
            X1 = alpha_pos[d] - A1 * D_alpha

            r1, r2 = np.random.rand(), np.random.rand()
            A2, C2 = 2 * a * r1 - a, 2 * r2
            D_beta = abs(C2 * beta_pos[d] - positions[i, d])
            X2 = beta_pos[d] - A2 * D_beta

            r1, r2 = np.random.rand(), np.random.rand()
            A3, C3 = 2 * a * r1 - a, 2 * r2
            D_delta = abs(C3 * delta_pos[d] - positions[i, d])
            X3 = delta_pos[d] - A3 * D_delta

            positions[i, d] = (X1 + X2 + X3) / 3.0

# 7. OUTPUT THE BEST SOLUTION
print("\n=== Optimal EV Charging Power Allocation (GWO) ===")
for idx in range(NUM_EVS):
    if alpha_pos[idx] > 0.1:
        est_time = f"{ev_energy_needed[idx] / alpha_pos[idx]:.2f} hrs"
    else:
        est_time = "Queued (Waiting)"
    print(f"EV {idx+1} | Need: {ev_energy_needed[idx]:5.1f} kWh | Urgency: {ev_urgency[idx]:.0f} "
          f"-> Power: {alpha_pos[idx]:5.2f} kW | Est. Time: {est_time}")

print(f"\nTotal Station Power Used: {np.sum(alpha_pos):.2f} / {MAX_STATION_POWER} kW")
