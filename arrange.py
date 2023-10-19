from corpus import get_grams

layout = ["os/pvzcde.", "anrmkjtlui", "qx,bfgwh;y"]

layout = ["puhgdzv,y.", "nertmcsoia", "b/lkqfwxj;"]

# . y u g d  z v h p ,
# a i e t m  c s r n o
# ; j / k q  f w l b x

# y p h g d  z v u . ,
# i n r t m  c s e a o
# j b l k q  f w / ; x

# . u o f h  b c n l y
# i e a d m  g p r t s
# , / ; k q  w z x j v

chars = get_grams("res/characters.txt", "".join(layout))

cols = [
    sum([chars[layout[y][x]] for y in range(len(layout))])
    for x in range(len(layout[0]))
]

sorted_col = sorted(
    [([layout[y][x] for y in range(len(layout))]) for x in range(len(layout[0]))],
    key=lambda x: sum(chars[c] for c in x),
)

print(sorted_col)

total = sum(cols)


print(total)

import random
import math


def generate_initial_solution():
    # Generate an initial solution within the parameter ranges
    return [...]


def calculate_energy(solution):
    # Calculate the energy (fitness) of a given solution
    return ...


def generate_yi(Ti):
    ui = random.uniform(0, 1)
    sgn = 1 if ui < 0.5 else -1
    return sgn * Ti * ((1 + 1 / Ti) * abs(2 * ui - 1) - 1)


def adaptive_simulated_annealing(max_iterations, T0, D, mi, ni):
    current_solution = generate_initial_solution()
    current_energy = calculate_energy(current_solution)
    best_solution = current_solution
    best_energy = current_energy

    for k in range(max_iterations):
        T = [T0 * math.exp(-mi * (k / max_iterations) ** (1 / D)) for mi in mi]

        # Generate D-dimensional random yi values
        yi = [generate_yi(Ti) for Ti in T]

        # Update the solution parameters based on yi
        new_solution = [current_solution[i] + yi[i] for i in range(D)]

        # Ensure that new_solution is within parameter constraints

        new_energy = calculate_energy(new_solution)

        if new_energy < current_energy:
            current_solution = new_solution
            current_energy = new_energy

        if new_energy < best_energy:
            best_solution = new_solution
            best_energy = new_energy

    return best_solution, best_energy


# Example usage
max_iterations = 1000
T0 = [1.0, 2.0, 3.0]  # Initial temperature for each dimension
D = 3  # Number of dimensions
mi = 0.1  # mi parameter
ni = 1.0  # ni parameter

best_solution, best_energy = adaptive_simulated_annealing(max_iterations, T0, D, mi, ni)
print("Best Solution:", best_solution)
print("Best Energy:", best_energy)
