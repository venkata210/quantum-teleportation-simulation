from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

print("🔬 Quantum Teleportation Simulation")
print("=" * 50)

# Create 3-qubit circuit
qc = QuantumCircuit(3, 3)

# Step 1: Alice's arbitrary state
theta = np.pi/3
print(f"Step 1: Preparing Alice's state (θ = {theta:.3f})")
qc.ry(theta, 0)

# Step 2: Bell pair
print("Step 2: Creating Bell pair")
qc.h(1)
qc.cx(1, 2)

# Step 3: Bell measurement
print("Step 3: Bell measurement")
qc.cx(0, 1)
qc.h(0)
qc.measure([0, 1], [0, 1])

# Step 4: Corrections
qc.cx(1, 2)
qc.cz(0, 2)
qc.measure(2, 2)

print("\nCircuit:")
print(qc.draw(output='text'))

# Simulate
simulator = AerSimulator()
job = simulator.run(qc, shots=1000)
result = job.result()
counts = result.get_counts()

print("\nResults:")
for outcome, count in sorted(counts.items()):
    prob = count/1000
    print(f"{outcome}: {count:3d} ({prob:.3f})")

# Expected vs actual
expected_0 = np.cos(theta/2)**2
expected_1 = np.sin(theta/2)**2

bob_0 = sum(count for outcome, count in counts.items() if outcome[-1] == '0')
bob_1 = sum(count for outcome, count in counts.items() if outcome[-1] == '1')

print(f"\nBob's teleported state:")
print(f"P(|0⟩) = {bob_0/1000:.3f} (expected: {expected_0:.3f})")
print(f"P(|1⟩) = {bob_1/1000:.3f} (expected: {expected_1:.3f})")

print("\n✅ Teleportation complete!")
