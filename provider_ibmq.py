import requests
from qbraid.runtime import QiskitRuntimeProvider

import zlib, base64
import qiskit.qpy
import qbraid


class IBMQ:
    def __init__(self, ibm_api_key:str, ibm_crn:str):
        # authentication
        self.provider = QiskitRuntimeProvider(channel="ibm_cloud", token=ibm_api_key)
        self.headers = {
            'Accept': 'application/json',
            'IBM-API-Version': '2025-05-01',
            'Authorization': 'Bearer ' + \
                requests.post('https://iam.cloud.ibm.com/identity/token', headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                }, data = f'grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={ibm_api_key}'
            ).json()['access_token'],
            'Service-CRN': ibm_crn
        }
        self.job2id = {
            qbraid.runtime.ibm.job.QiskitJob: lambda v: v.id,
            qbraid.runtime.ibm.job.RuntimeJobV2: lambda v: v.job_id(),
            str: lambda x: x,
        }

    # job object to job_id
    def jobid(self, job_obj) -> str:
        return self.job2id[type(job_obj)](job_obj)
    
    # job_id to job object
    def job(self, job_id:str):
        return self.provider.runtime_service.job(job_id)

    # print a list of all QPUs
    def printqpus(self):
        for dev in self.provider.get_devices():
            meta = dev.metadata()
            print(
                'ibmq',
                dev,
                f"{dev.num_qubits}qb",
                dev.status(),
            )

    # get the result of a job id as bitstring-counts or ints
    def jobresult(self, job_id:str, raw:bool=False):
        job = self.provider.runtime_service.job(job_id)
        if raw:
            return {
                k: v.array.squeeze()
                for k, v in self.provider.runtime_service.job(job_id).result()[0].data.items()
            }
        else:
            return job.result()[0].join_data().get_counts()

    # get the circuit as it was executed on the machine
    def jobcircuit(self, job_id:str):
        j = requests.get(f'https://quantum.cloud.ibm.com/api/v1/jobs/{job_id}', headers=self.headers).json()
        qvs, qcs = [], []
        try:
            for thing in j['params']['pubs'][0]:
                if isinstance(thing, dict):
                    if thing['__type__'] == 'QuantumCircuit':
                        qvs.append(thing['__value__'])
        except: print(j)
        for i, qv in enumerate(qvs):
            with open(f'/tmp/{job_id}_{i}.qpy','wb') as f:
                f.write(zlib.decompress(base64.b64decode(j['params']['pubs'][0][0]['__value__']), wbits = zlib.MAX_WBITS))
            with open(f'/tmp/{job_id}_{i}.qpy','rb') as f:
                qc, = qiskit.qpy.load(f)
                qcs.append(qc)
        if len(qcs) == 1:
            return qcs[0]
        else:
            return qcs