from config import api_key
from qiskit_ibm_runtime import QiskitRuntimeService


QiskitRuntimeService.save_account(api_key)
