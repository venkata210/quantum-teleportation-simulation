"""
Simple Quantum Teleportation Demonstration
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

def main():
    print("🔬 Quantum Teleportation Simulation")
    print("=" * 50)
    
    # Create a 3-qubit circuit with 3 classical bits
    qc = QuantumCircuit(3, 3)
    
    # Step 1: Prepare Alice's arbitrary state (qubit 0)
    theta = np.pi/3  # 60 degrees
    print(f"Step 1: Preparing Alice's qubit with θ = {theta:.3f} radians")
    qc.ry(theta, 0)
    qc.barrier()
    
    # Step 2: Create Bell pair between qubits 1 and 2
    print("Step 2: Creating Bell pair (entanglement)")
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()
    
    # Step 3: Bell measurement on qubits 0 and 1
    print("Step 3: Performing Bell measurement")
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()
    
    # Measure Alice's qubits
    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.barrier()
    
    # Step 4: Conditional corrections based on Alice's measurements
    print("Step 4: Applying conditional corrections")
    qc.cx(1, 2)  # Apply X if second measurement is 1
    qc.cz(0, 2)  # Apply Z if first measurement is 1
    qc.barrier()
    
    # Step 5: Measure Bob's qubit
    print("Step 5: Measuring Bob's final state")
    qc.measure(2, 2)
    
    # Display the circuit
    print("\nQuantum Circuit:")
    print("=" * 40)
    print(qc.draw(output='text'))
    
    # Simulate the circuit
    print("\nRunning simulation...")
    simulator = AerSimulator()
    transpiled_qc = transpile(qc, simulator)
    job = simulator.run(transpiled_qc, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Analyze results
    print("\nMeasurement Results:")
    print("=" * 40)
    total_shots = sum(counts.values())
    
    # Calculate expected probabilities for original state
    prob_0_expected = np.cos(theta/2)**2
    prob_1_expected = np.sin(theta/2)**2
    
    print(f"Original state: cos({theta/2:.3f})|0⟩ + sin({theta/2:.3f})|1⟩")
    print(f"Expected P(|0⟩) = {prob_0_expected:.3f}")
    print(f"Expected P(|1⟩) = {prob_1_expected:.3f}")
    print()
    
    # Analyze Bob's results (last bit)
    bob_0_count = 0
    bob_1_count = 0
    
    print("All measurement outcomes:")
    for outcome, count in sorted(counts.items()):
        probability = count / total_shots
        bob_bit = outcome[-1]
        print(f"{outcome} | Count: {count:4d} | Prob: {probability:.3f}")
        
        if bob_bit == '0':
            bob_0_count += count
        else:
            bob_1_count += count
    
    # Bob's final state analysis
    bob_prob_0 = bob_0_count / total_shots
    bob_prob_1 = bob_1_count / total_shots
    
    print(f"\nBob's final state (teleported):")
    print(f"P(|0⟩) = {bob_prob_0:.3f} (expected: {prob_0_expected:.3f})")
    print(f"P(|1⟩) = {bob_prob_1:.3f} (expected: {prob_1_expected:.3f})")
    
    # Calculate fidelity
    fidelity = np.sqrt(prob_0_expected * bob_prob_0) + np.sqrt(prob_1_expected * bob_prob_1)
    print(f"\nTeleportation fidelity: {fidelity:.3f}")
    
    if fidelity > 0.95:
        print("✅ Teleportation successful!")
    else:
        print("⚠️  Teleportation may have some errors")
    
    print("\n" + "=" * 50)
    print("🎉 Quantum Teleportation Complete!")
    print("Alice's quantum state has been successfully transferred to Bob!")

if __name__ == "__main__":
    main()
