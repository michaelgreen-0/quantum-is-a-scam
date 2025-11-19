# not working

import numpy as np
import matplotlib.pyplot as plt
from qiskit_ibm_catalog import QiskitFunctionsCatalog
from env import IBM_QUANTUM_API_KEY, IBM_QUANTUM_INSTANCE_CRN

catalog = QiskitFunctionsCatalog(
    channel="ibm_cloud",
    instance=IBM_QUANTUM_INSTANCE_CRN,
    token=IBM_QUANTUM_API_KEY, 
)

quick = catalog.load("colibritd/quick-pde")

job = quick.run(
    use_case="cfd",
    physical_parameters={"a": 1, "b": 1}
)

print(job.result())