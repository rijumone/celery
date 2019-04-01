import json
import requests
import multiprocessing

def send_req(i):
	print('*************************')
	print('requesting {0}'.format(i))
	url = "http://192.168.1.127:5555/api/task/async-apply/get_from_q_process.load"

	payload = json.dumps({
		"args": [i],
		"kwargs":{
			"lazy":"dog"
		}
	})
	headers = {
	    'Content-Type': "application/json",
	    'Authorization': "Basic dXNlcjpwYXNz",
	    'cache-control': "no-cache",
	    'Postman-Token': "e0781b4c-7a58-492a-9814-61e10b1bedcd"
	    }

	response = requests.request("POST", url, data=payload, headers=headers)

	print('response from {0}'.format(i))
	print(response.text)
	print('*************************')

jobs = []

for i in range(1345,1400):
    p = multiprocessing.Process(target=send_req, args=(i, ))
    jobs.append(p)
    p.start()

for job in jobs:
    job.join()


