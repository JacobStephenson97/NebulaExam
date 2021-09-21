import unittest
import sys
import requests

data = {
  "workers": [
    {
      "cpu_usage": 3,
      "gpu": "GeForce RTX 2070",
      "gpu_used": "used",
      "ram_usage": "1%",
      "vmem_usage": "0%",
      "worker_id": 1,
      "worker_name": "1"
    },
    {
      "cpu_usage": 3,
      "gpu": "GeForce RTX 2080 TI",
      "gpu_used": "not used",
      "ram_usage": "3%",
      "vmem_usage": "43%",
      "worker_id": 2,
      "worker_name": "2"
    }, 
    {
      "cpu_usage": 16,
      "gpu": "GeForce GTX 1080",
      "gpu_used": "not used",
      "ram_usage": "13%",
      "vmem_usage": "10%",
      "worker_id": 3,
      "worker_name": "3"
    }
  ]
}

class TestCase(unittest.TestCase):
  def testAll(self):
    response = requests.get('http://127.0.0.1:5000/api/workers/all')
    self.assertEqual(data, response.json())
  
  def testId(self):
    results = []
    for worker in data["workers"]:
        if worker['worker_id'] == 2:
            results.append(worker)
    response = requests.get('http://127.0.0.1:5000/api/workers?id=2')
    self.assertEqual(results, response.json())
  
  def testGpuUsed(self):
    results = []
    for worker in data["workers"]:
        if worker['gpu_used'] == "used":
            results.append(worker)
    response = requests.get('http://127.0.0.1:5000/api/gpu?used=true')
    self.assertEqual(results, response.json())
    

if __name__ == '__main__':
  log_file = 'log_file.txt'
  with open(log_file, "w") as f:
      runner = unittest.TextTestRunner(f)
      unittest.main(testRunner=runner)