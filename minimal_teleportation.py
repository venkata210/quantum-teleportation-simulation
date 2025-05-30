#!/usr/bin/env python3

print("Starting Quantum Teleportation Demo...")

try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    import numpy as np
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)

# Create quantum circuit
print("Creating 3-qubit circuit...")
qc = QuantumCircuit(3, 3)

# Step 1: Prepare Alice's arbitrary state
theta = np.pi/3
print(f"Step 1: Preparing Alice's state (θ = {theta:.3f})")
qc.ry(theta, 0)
qc.barrier()

# Step 2: Create Bell pair
print("Step 2: Creating Bell pair")
qc.h(1)
qc.cx(1, 2)
qc.barrier()

# Step 3: Bell measurement
print("Step 3: Bell measurement")
qc.cx(0, 1)
qc.h(0)
qc.measure(0, 0)
qc.measure(1, 1)
qc.barrier()

# Step 4: Corrections
print("Step 4: Conditional corrections")
qc.cx(1, 2)
qc.cz(0, 2)
qc.measure(2, 2)

print("Circuit construction complete!")
print("\nCircuit diagram:")
print(qc.draw(output='text', fold=-1))

# Simulate
print("\nRunning simulation...")
simulator = AerSimulator()
job = simulator.run(qc, shots=1000)
result = job.result()
counts = result.get_counts()

print("\nResults:")
for outcome, count in sorted(counts.items()):
    print(f"{outcome}: {count}")

# Analyze Bob's qubit (last bit)
bob_0 = sum(count for outcome, count in counts.items() if outcome[-1] == '0')
bob_1 = sum(count for outcome, count in counts.items() if outcome[-1] == '1')
total = bob_0 + bob_1

print(f"\nBob's final state:")
print(f"|0⟩: {bob_0} ({bob_0/total:.3f})")
print(f"|1⟩: {bob_1} ({bob_1/total:.3f})")

# Expected probabilities
expected_0 = np.cos(theta/2)**2
expected_1 = np.sin(theta/2)**2
print(f"\nExpected probabilities:")
print(f"|0⟩: {expected_0:.3f}")
print(f"|1⟩: {expected_1:.3f}")

print("\n🎉 Quantum teleportation simulation complete!")
