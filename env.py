import os
from dotenv import load_dotenv

load_dotenv()

IBM_QUANTUM_API_KEY=os.getenv("IBM_QUANTUM_API_KEY")
IBM_QUANTUM_INSTANCE_CRN=os.getenv("IBM_QUANTUM_INSTANCE_CRN")