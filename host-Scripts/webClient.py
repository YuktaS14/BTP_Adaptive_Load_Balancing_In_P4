import requests
import time

# s = time.time()

# requests.get('')

# e = time.time()

# print(e - s)


s = requests.Session()



def streaming(symbols):

    payload = {'symbols': ','.join(symbols)}
    payload = 'symbol' * 1024
    headers = {'connection': 'keep-alive', 'content-type': 'application/json', 'x-powered-by': 'Express', 'transfer-encoding': 'chunked'}
    while True:

        req = requests.Request("GET",'http://10.0.0.52:8080',
                            headers=headers,
                            params=payload).prepare()

        resp = s.send(req, stream=True)

        for line in resp.iter_lines():
            if line:
                yield line

        time.sleep(10)


def read_stream():

    for line in streaming(['AAPL', 'GOOG']):
        print (line)


read_stream()