import socket
import sys
import time
import threading
from datetime import datetime

if len(sys.argv) != 4:
    print("Usage: python script.py <num of users> <time_in_seconds> <probe timeperiod>")
    sys.exit(1)

# HOST = 'localhost'
HOST = '10.0.0.52'
PORT = 50006
NUM_USERS = int(sys.argv[1])  # Change this to the number of users you want to simulate

def client_thread(port, i, response_times):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
     
    count = 0
    total = 0
    
    start_time = time.time()  # Start timer for specified time
    while time.time() - start_time < int(sys.argv[2]):  # Send data for specified time
        try:
            data_to_send = b'Hello, server!' * 10
            start_time_send = time.time()

            s.sendall(data_to_send)
            response = s.recv(1024)

            end_time_send = time.time()
    
            response_time = end_time_send - start_time_send
            print(f"Response time from port {port}: {response_time} seconds")
            total += response_time
            count += 1
            time.sleep(0.001)

        except BrokenPipeError:
            print("Broken pipe error occurred. Closing connection.")
            break
        
        except KeyboardInterrupt:
            print(f"Average Response time from port {port}: {(total/count)}")
            break
    
    if count != 0:
        response_times.append(total/count)
    
    print(f"Average Response time from port {i}: {(total/count)}")

    s.close()

# Start threads for each user
threads = []
response_times = []
for i in range(NUM_USERS):
    time.sleep(1)
    port = PORT
    thread = threading.Thread(target=client_thread, args=(port, i, response_times,))
    threads.append(thread)
    # thread.daemon = True
    thread.start()

for thread in threads:
    thread.join()

# Wait for all threads to complete
average_per_client = response_times
if len(average_per_client) != 0:
    overall_average = sum(average_per_client) / len(average_per_client)
overall_min = min(average_per_client)
overall_max = max(average_per_client)

print(f"Overall Average Response Time per client: {overall_average}")
print(f"Overall Min Response Time per client: {overall_min}")
print(f"Overall Max Response Time per client: {overall_max}")

with open("client.txt", "a") as file:
    # Get the current date and time
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Format the data for writing to the file
    data_to_write = f"{current_time} | Average: {overall_average} | Min: {overall_min} | Max: {overall_max} | for {NUM_USERS} clients | run_time: {sys.argv[2]} | probe_freq: {sys.argv[3]}\n"
    
    # Write the data to the file
    file.write(data_to_write)

# Calculate overall statistics