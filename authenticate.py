from qiskit_ibm_runtime import QiskitRuntimeService
from env import IBM_QUANTUM_API_KEY

# Save the account. This stores the key securely on your machine.
QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform", 
    token=IBM_QUANTUM_API_KEY,
    overwrite=True
    )

print("Account saved successfully!")