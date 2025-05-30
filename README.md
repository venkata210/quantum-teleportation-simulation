# Quantum Teleportation Simulation

A comprehensive quantum teleportation simulation using Qiskit that demonstrates how quantum information can be transferred from Alice to Bob through quantum entanglement and classical communication.

## 🔬 What is Quantum Teleportation?

Quantum teleportation is a quantum communication protocol that allows the transfer of quantum information from one location to another, without physically moving the quantum system itself. It relies on:

1. **Quantum Entanglement**: A shared entangled state between sender and receiver
2. **Bell Measurement**: A joint measurement that extracts classical information
3. **Classical Communication**: Sending measurement results to complete the protocol
4. **Conditional Operations**: Applying corrections based on classical information

## 🎯 Features

This simulation implements:

- ✅ 3-qubit quantum circuit initialization
- ✅ Arbitrary state preparation using Ry rotation gate
- ✅ Bell pair creation (quantum entanglement)
- ✅ Bell measurement on Alice's qubits
- ✅ Conditional corrections based on classical measurement results
- ✅ Circuit visualization with matplotlib
- ✅ Measurement results histogram
- ✅ Aer simulator integration
- ✅ **Bonus**: Bloch sphere visualization of states before and after teleportation
- ✅ Fidelity analysis to verify successful teleportation

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or navigate to this repository:
```bash
cd /workspaces/quantum-teleportation-simulation
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Simulation

Execute the main simulation:
```bash
python quantum_teleportation.py
```

## 📊 What You'll See

The simulation will display:

1. **Step-by-step protocol execution** with detailed explanations
2. **Circuit diagram** showing all quantum gates and measurements
3. **Measurement results histogram** displaying all possible outcomes
4. **Teleportation analysis** including fidelity calculations
5. **Bloch sphere visualizations** comparing initial and final states

## 🔧 Customization

You can modify the simulation by changing the `theta` parameter in the `main()` function:

```python
theta = np.pi/4  # 45 degrees
theta = np.pi/2  # 90 degrees  
theta = np.pi/6  # 30 degrees
```

This changes the initial quantum state that Alice prepares: `|ψ⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩`

## 📈 Understanding the Results

### Circuit Layout
- **Qubit 0**: Alice's qubit (to be teleported)
- **Qubit 1**: Alice's half of the Bell pair
- **Qubit 2**: Bob's half of the Bell pair (receives teleported state)

### Measurement Outcomes
The 3-bit measurement results represent:
- **Bit 0**: Alice's first measurement
- **Bit 1**: Alice's second measurement  
- **Bit 2**: Bob's final measurement (the teleported state)

### Success Criteria
- **Fidelity > 0.95**: Indicates successful teleportation
- **Bob's results match expected probabilities** for the original state

## 🧮 The Mathematics

The quantum teleportation protocol transfers the state:
```
|ψ⟩ = α|0⟩ + β|1⟩
```

Through the following steps:
1. **Initial state**: |ψ⟩₀ ⊗ |Φ⁺⟩₁₂ 
2. **Bell measurement**: Projects onto Bell basis
3. **Classical communication**: 2 classical bits
4. **Correction operations**: X^b Z^a |ψ⟩ where a,b are measurement results

## 🎓 Educational Value

This simulation helps understand:
- Quantum entanglement and its role in quantum communication
- The no-cloning theorem (information is transferred, not copied)
- The relationship between quantum and classical information
- Quantum circuit design and measurement strategies

## 🔍 Technical Details

- **Simulator**: Qiskit Aer (quantum circuit simulator)
- **Gates Used**: Ry, H (Hadamard), CNOT, CZ (Controlled-Z)
- **Measurements**: Computational basis measurements
- **Visualizations**: matplotlib with Qiskit plotting functions

## 📚 Further Reading

- [Quantum Teleportation Paper (Bennett et al., 1993)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.70.1895)
- [Qiskit Textbook on Quantum Teleportation](https://qiskit.org/textbook/ch-algorithms/teleportation.html)
- [IBM Quantum Experience](https://quantum-computing.ibm.com/)

## 🤝 Contributing

Feel free to improve this simulation by:
- Adding more visualization options
- Implementing different initial states
- Adding noise models for realistic simulation
- Creating interactive parameter controls

---

*Built with ❤️ using Qiskit and Python*