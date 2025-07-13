import requests
from qbraid.runtime import QiskitRuntimeProvider

import zlib, base64
import qiskit.qpy
import numpy as np
import qbraid
from collections import Counter


class IBMQ:
    def _build_headers(self):
        self.headers = {
            'Accept': 'application/json',
            'IBM-API-Version': '2025-05-01',
            'Authorization': 'Bearer ' + \
                requests.post('https://iam.cloud.ibm.com/identity/token', headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                }, data = f'grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={self._ibm_api_key}'
            ).json()['access_token'],
            'Service-CRN': self._ibm_crn
        }
    
    def __init__(self, ibm_api_key:str, ibm_crn:str):
        # authentication
        self.provider = QiskitRuntimeProvider(channel="ibm_cloud", token=ibm_api_key)
        self._ibm_api_key = ibm_api_key
        self._ibm_crn = ibm_crn
        self.job2id = {
            qbraid.runtime.ibm.job.QiskitJob: lambda v: v.id,
            qbraid.runtime.ibm.job.RuntimeJobV2: lambda v: v.job_id(),
            str: lambda x: x,
        }
        self._build_headers()

    # recover if possible. True=signal OK, redo
    def _recover_error(self, response:dict) -> bool:
        if response.get('error', None) is None:
            return False
        try:
            if response['error'][0]['code'] == 1200:
                self._build_headers()
                return True
        except: pass
        return False

    # job object to job_id
    def jobid(self, job_obj) -> str:
        return self.job2id[type(job_obj)](job_obj)
    
    # job_id to job object
    def job(self, job_id:str):
        return self.provider.runtime_service.job(job_id)

    # print a list of all QPUs
    def printqpus(self) -> None:
        for dev in self.provider.get_devices():
            meta = dev.metadata()
            print(
                'ibmq',
                dev,
                f"{dev.num_qubits}qb",
                dev.status(),
            )

    # get the result of a job_id as bitstring-count(s)
    def jobresult(self, job_id:str):
        """Get the results from a job_id.
        return:
            answer[circuit_index][register_name][bitstring] = count
            the columns `register_name` and `circuit_index` are squeezed.
        """
        j=requests.get(f'https://quantum.cloud.ibm.com/api/v1/jobs/{job_id}/results', headers=self.headers).json()
        # extract data from api endpoint 
        datas = [
            {
                c: [
                    r['__value__']['data']['__value__']['fields'][c]['__value__']['num_bits'],
                    self._decode(np.load, r['__value__']['data']['__value__']['fields'][c]['__value__']['array']['__value__']),
                ]
                for c in r['__value__']['data']['__value__']['field_names']
            }
            for r in j['__value__']['pub_results']
        ]
        # convert to arr[circuit_index][register_name][bitstring] = count
        results = {
            index: {
                c: {
                    '{:0{}b}'.format(i, bits): count
                    for i, count in Counter(np.sum(raw << (8 * np.array(range(raw.shape[1])[::-1])), axis=1)).items()
                }
                for c, (bits, raw) in data.items()
            }
            for index, data in enumerate(datas)
        }
        # squeeze register_name column
        results = {
            index: result[list(result.keys())[0]] if len(result.keys()) == 1 else result
            for index, result in results.items()
        }
        # squeeze circuit_index column
        if len(results.keys()) == 1: return results[list(results.keys())[0]]
        return results
    
    # get the result of a job_id as bitstring-count(s)
    def jobresult_qbraid(self, job_id:str) -> dict[str,int]|list[dict[str,int]]:
        job = self.provider.runtime_service.job(job_id)
        result = job.result()
        # arr[circuit_index][bitstring] = count
        out = {
            i: inside_job.join_data().get_counts()
            for i, inside_job in enumerate(result)
        }
        return out[0] if len(out) == 1 else out

    # decode the api encoding format
    def _decode(self, load_func, data:bytes, tempname:str='decodingfile') -> any:
        with open(f'/tmp/{tempname}', 'wb') as f:
            f.write(zlib.decompress(base64.b64decode(data), wbits=zlib.MAX_WBITS))
        with open(f'/tmp/{tempname}', 'rb') as f:
            return load_func(f)

    # get the circuit as it was executed on the machine
    def jobcircuit(self, job_id:str):
        j = requests.get(f'https://quantum.cloud.ibm.com/api/v1/jobs/{job_id}', headers=self.headers).json()
        if self._recover_error(j): return self.jobcircuit(job_id)
        try:
            qvs = [
                {
                    'qc': self._decode(qiskit.qpy.load, thing[0]['__value__']),
                    '??': self._decode(np.load, thing[1]['__value__']),
                    'shots': thing[2],
                } 
                for i, thing in enumerate(j['params']['pubs'])
            ]
        except: print(j)
        qcs = [qv['qc'] for qv in qvs]
        if len(qcs) == 1: return qcs[0]
        return qcs