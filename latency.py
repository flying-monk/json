# from tcp_latency import measure_latency
# print(measure_latency(host='google.com'))
# print(measure_latency(host='127.0.0.1', port=2727, runs=10, timeout=2.5))

from pythonping import ping
response_list = ping('8.8.8.8', size=40, count=10)