import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
import warnings
warnings.filterwarnings('ignore')

class QuantumTeleportationSimulator:
    """
    A class to simulate quantum teleportation protocol
    """
    
    def __init__(self):
        self.simulator = AerSimulator()
        self.qreg = QuantumRegister(3, 'q')  # 3 qubits: Alice's qubit, Bell pair
        self.creg = ClassicalRegister(3, 'c')  # 3 classical bits for measurements
        self.circuit = QuantumCircuit(self.qreg, self.creg)
        
    def prepare_arbitrary_state(self, theta=np.pi/3):
        """
        Prepare Alice's qubit (q0) in an arbitrary state using Ry rotation
        
        Args:
            theta (float): Rotation angle for the Ry gate
        """
        print(f"Step 1: Preparing Alice's qubit in arbitrary state with θ = {theta:.3f}")
        self.circuit.ry(theta, self.qreg[0])  # Rotate Alice's qubit
        self.circuit.barrier()
        
    def create_bell_pair(self):
        """
        Create a Bell pair (entangled state) between qubits 1 and 2
        This creates the entanglement resource needed for teleportation
        """
        print("Step 2: Creating Bell pair between qubits 1 and 2")
        # Create Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
        self.circuit.h(self.qreg[1])  # Put qubit 1 in superposition
        self.circuit.cx(self.qreg[1], self.qreg[2])  # Entangle qubits 1 and 2
        self.circuit.barrier()
        
    def bell_measurement(self):
        """
        Perform Bell measurement on Alice's qubit and her half of the Bell pair
        This is the key step that "teleports" the quantum information
        """
        print("Step 3: Performing Bell measurement on qubits 0 and 1")
        # Bell measurement: CNOT followed by Hadamard, then measurement
        self.circuit.cx(self.qreg[0], self.qreg[1])
        self.circuit.h(self.qreg[0])
        self.circuit.barrier()
        
        # Measure Alice's qubits
        self.circuit.measure(self.qreg[0], self.creg[0])
        self.circuit.measure(self.qreg[1], self.creg[1])
        self.circuit.barrier()
        
    def conditional_corrections(self):
        """
        Apply conditional corrections to Bob's qubit based on Alice's measurement results
        This completes the teleportation protocol
        """
        print("Step 4: Applying conditional corrections to Bob's qubit")
        # If Alice measured 1 in the second qubit, apply X gate to Bob's qubit
        self.circuit.cx(self.creg[1], self.qreg[2])
        
        # If Alice measured 1 in the first qubit, apply Z gate to Bob's qubit
        self.circuit.cz(self.creg[0], self.qreg[2])
        
        self.circuit.barrier()
        
    def final_measurement(self):
        """
        Measure Bob's qubit to verify the teleportation
        """
        print("Step 5: Measuring Bob's qubit")
        self.circuit.measure(self.qreg[2], self.creg[2])
        
    def build_complete_circuit(self, theta=np.pi/3):
        """
        Build the complete quantum teleportation circuit
        
        Args:
            theta (float): Rotation angle for Alice's initial state
        """
        print("Building Quantum Teleportation Circuit")
        print("=" * 50)
        
        self.prepare_arbitrary_state(theta)
        self.create_bell_pair()
        self.bell_measurement()
        self.conditional_corrections()
        self.final_measurement()
        
        print("Circuit construction complete!")
        return self.circuit
        
    def simulate_circuit(self, shots=1024):
        """
        Simulate the quantum teleportation circuit
        
        Args:
            shots (int): Number of simulation runs
            
        Returns:
            dict: Measurement results
        """
        print(f"\nSimulating circuit with {shots} shots...")
        
        # Transpile circuit for the simulator
        transpiled_circuit = transpile(self.circuit, self.simulator)
        
        # Run the simulation
        job = self.simulator.run(transpiled_circuit, shots=shots)
        result = job.result()
        counts = result.get_counts()
        
        print("Simulation complete!")
        return counts
        
    def analyze_results(self, counts, theta=np.pi/3):
        """
        Analyze the teleportation results
        
        Args:
            counts (dict): Measurement results from simulation
            theta (float): The original rotation angle
        """
        print("\nTeleportation Analysis")
        print("=" * 30)
        
        # Calculate expected probabilities for the teleported state
        # |ψ⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩
        prob_0 = np.cos(theta/2)**2
        prob_1 = np.sin(theta/2)**2
        
        print(f"Original state: cos({theta/2:.3f})|0⟩ + sin({theta/2:.3f})|1⟩")
        print(f"Expected P(|0⟩) = {prob_0:.3f}")
        print(f"Expected P(|1⟩) = {prob_1:.3f}")
        
        # Analyze Bob's measurement results (last bit)
        bob_0_count = 0
        bob_1_count = 0
        total_shots = sum(counts.values())
        
        for outcome, count in counts.items():
            bob_bit = outcome[-1]  # Last bit is Bob's measurement
            if bob_bit == '0':
                bob_0_count += count
            else:
                bob_1_count += count
                
        measured_prob_0 = bob_0_count / total_shots
        measured_prob_1 = bob_1_count / total_shots
        
        print(f"\nMeasured results for Bob's qubit:")
        print(f"P(|0⟩) = {measured_prob_0:.3f} (expected: {prob_0:.3f})")
        print(f"P(|1⟩) = {measured_prob_1:.3f} (expected: {prob_1:.3f})")
        
        # Calculate fidelity (how close the results are to expected)
        fidelity = np.sqrt(prob_0 * measured_prob_0) + np.sqrt(prob_1 * measured_prob_1)
        print(f"Teleportation fidelity: {fidelity:.3f}")
        
        if fidelity > 0.95:
            print("✅ Teleportation successful!")
        else:
            print("⚠️  Teleportation may have some errors")


def print_circuit(circuit):
    """
    Print the quantum circuit in text format
    """
    print("\nQuantum Teleportation Circuit:")
    print("=" * 60)
    print(circuit.draw(output='text'))


def print_measurement_results(counts):
    """
    Print the measurement results in a formatted way
    """
    print("\nMeasurement Results:")
    print("=" * 40)
    print("Outcome (q0 q1 q2) | Count | Probability")
    print("-" * 40)
    
    total_shots = sum(counts.values())
    
    # Sort outcomes for better readability
    sorted_outcomes = sorted(counts.items())
    
    for outcome, count in sorted_outcomes:
        probability = count / total_shots
        print(f"{outcome:^15} | {count:^5} | {probability:.3f}")
    
    print("-" * 40)
    print(f"Total shots: {total_shots}")
    
    # Analyze Alice's and Bob's results separately
    print("\nDetailed Analysis:")
    print("Alice's measurements (q0, q1):")
    alice_counts = {}
    bob_0_count = 0
    bob_1_count = 0
    
    for outcome, count in counts.items():
        alice_result = outcome[:2]  # First two bits
        bob_result = outcome[2]     # Last bit
        
        if alice_result in alice_counts:
            alice_counts[alice_result] += count
        else:
            alice_counts[alice_result] = count
            
        if bob_result == '0':
            bob_0_count += count
        else:
            bob_1_count += count
    
    for alice_outcome, count in sorted(alice_counts.items()):
        prob = count / total_shots
        print(f"  {alice_outcome}: {count} ({prob:.3f})")
    
    print(f"\nBob's final measurements (q2):")
    print(f"  |0⟩: {bob_0_count} ({bob_0_count/total_shots:.3f})")
    print(f"  |1⟩: {bob_1_count} ({bob_1_count/total_shots:.3f})")


def main():
    """
    Main function to run the quantum teleportation simulation
    """
    print("🔬 Quantum Teleportation Simulation")
    print("=" * 50)
    print("This simulation demonstrates quantum teleportation using Qiskit")
    print("We will teleport an arbitrary quantum state from Alice to Bob\n")
    
    # Initialize the simulator
    teleportation = QuantumTeleportationSimulator()
    
    # Choose an arbitrary state (you can modify this angle)
    theta = np.pi/3  # 60 degrees
    print(f"Alice's initial state parameter: θ = {theta:.3f} radians ({np.degrees(theta):.1f}°)")
    
    # Build the complete teleportation circuit
    circuit = teleportation.build_complete_circuit(theta)
    
    # Print the circuit
    print_circuit(circuit)
    
    # Simulate the circuit
    counts = teleportation.simulate_circuit(shots=1024)
    
    # Print measurement results
    print_measurement_results(counts)
    
    # Analyze the results
    teleportation.analyze_results(counts, theta)
    
    print("\n" + "=" * 50)
    print("🎉 Quantum Teleportation Simulation Complete!")
    print("Alice has successfully teleported her quantum state to Bob!")
    
    print("\n📚 Understanding the Protocol:")
    print("1. Alice prepares her qubit in state cos(π/6)|0⟩ + sin(π/6)|1⟩")
    print("2. A Bell pair is shared between Alice (q1) and Bob (q2)")
    print("3. Alice performs Bell measurement on her qubits (q0, q1)")
    print("4. Based on Alice's results, corrections are applied to Bob's qubit")
    print("5. Bob's final measurement should match Alice's original state!")


if __name__ == "__main__":
    main()
