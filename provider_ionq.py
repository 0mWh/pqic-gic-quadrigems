import requests
from qbraid.runtime import IonQProvider

from qiskit import (
	QuantumCircuit as QC,
	QuantumRegister as QR,
	ClassicalRegister as CR
)


class IONQ:
    def __init__(self, ionq_api_key:str):
        # authentication
        self.provider = IonQProvider(ionq_api_key)
        self.headers = {
            'Authorization': f'apiKey {ionq_api_key}'
        }
        self.qcbuilders = {
            'h': lambda qc,g: qc.h(g['targets']),
            'x': lambda qc,g: qc.cx(g['controls'], g['targets']) if g['controls'] else qc.x(g['targets']),
            'zz': lambda qc,g: qc.rzz(g['rotation'], *g['targets']),
            'rx': lambda qc,g: qc.rx(g['rotation'], g['targets']),
        }

    # job object to job_id
    def jobid(self, job_obj) -> str:
        print('todo j2str', job_obj)
    
    # job_id to job object
    def job(self, job_id:str):
        return requests.get(f'https://api.ionq.co/v0.3/jobs/{job_id}', headers=self.headers).json()

    # print a list of all QPUs
    def printqpus(self):
        for dev in self.provider.get_devices():
            meta = dev.metadata()
            s = meta['average_queue_time']
            print(
                'ionq',
                dev,
                f"{dev.num_qubits}qb",
                dev.status(),
                f"queue {s//86400}d{s%86400//3600}h{s%3600//60}m{s%60}s" if s > 0 else 'now!',
            )

    # get the result of a job id as bitstring-probs
    def jobresult(self, job_id:str, raw:bool=False):
        probs = requests.get(f'https://api.ionq.co/v0.3/jobs/{job_id}/results', headers=self.headers).json()
        qubits = max(map(int,probs.keys())).bit_length()
        try: probs = {'{:0{}b}'.format(int(k), qubits): v for k, v in probs.items()}
        except: return probs
        return probs

    # get the circuit as it was executed on the machine
    def jobcircuit(self, job_id:str):
        j = requests.get(f'https://api.ionq.co/v0.3/jobs/{job_id}/program', headers=self.headers).json()
        bits = j['body']['qubits']
        qc = QC(qr:=QR(bits), cr:=CR(bits))
        for gate in j['body']['circuit']:
            self.qcbuilders[gate['gate']](qc,gate)
        qc.barrier()
        qc.measure(qr, cr)
        return qc
