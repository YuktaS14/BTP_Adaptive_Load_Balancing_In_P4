import threading
import socket
import time
import sys
from datetime import datetime

if len(sys.argv) != 4:
    print("Usage: python script.py <num of users> <time_in_seconds> <probe timeperiod>")
    sys.exit(1)

HOST = '10.0.0.52'
PORT = 50007
NUM_USERS = int(sys.argv[1])
TIMEOUT = 50

exit_flag = False
threadsDict = {}
average_per_client = []


def close_session():
    global exit_flag
    print("Closing Session")
    exit_flag = True
    keys_to_remove = list(threadsDict.keys())  # Create a copy of keys
    for i in keys_to_remove:
        threadsDict[i]["timer"].cancel()

        if(len(threadsDict[i]["respTime"]) != 0):
            average_per_client.append(threadsDict[i]["respTime"][0])
        print(f"{i}: client closed")
        del threadsDict[i]  # Remove the key from the dictionary
    exit_flag = True


def client_thread(port, i):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))
    #s.timeout(5)
    count = 0
    total = 0
    global threadsDict

    start_time = time.time()
    while time.time() - start_time < 30:
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
            time.sleep(1)
    
        except KeyboardInterrupt:
            print(f"Average Response time from port {port}: {(total/count)}")
            break
    
    threadsDict[i]["respTime"].append(total/count)
    
    print(f"Average Response time from port {i}: {(total/count)}")

    # s.close()


def receive_thread():
    global exit_flag
    global threadsDict
    port = PORT

    for i in range(NUM_USERS):
        threadsDict[i] = {}
        thread = threading.Thread(target=client_thread, args=(port, i))
        threadsDict[i]["respTime"] = []
        threadsDict[i]["thread"] = thread
        threadsDict[i]["timer"] = threading.Timer(TIMEOUT, close_session)
        threadsDict[i]["timer"].daemon = True
        threadsDict[i]["timer"].start()
        thread.start()
        time.sleep(1)


def input_thread():
    global exit_flag
    try:
        while True:
            message = input("")
            if message == "q":
                close_session()
                break
    except EOFError:
        close_session()


# Start the receive thread
receive_th = threading.Thread(target=receive_thread)
receive_th.daemon = True
receive_th.start()

# Start the input thread
input_th = threading.Thread(target=input_thread)
input_th.daemon = True
input_th.start()

try:
    while not exit_flag:
        continue
except KeyboardInterrupt:
    close_session()


# Calculate overall statistics after all client threads have finished
while threadsDict:
    time.sleep(1)  # Wait for threads to finish
print("Total: ",sum(average_per_client))
print("Count: ", len(average_per_client))
overall_average = sum(average_per_client) / len(average_per_client)
overall_min = min(average_per_client)
overall_max = max(average_per_client)

# Write statistics to file
with open("client.txt", "a") as file:
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data_to_write = f"{current_time} | Average: {overall_average} | Min: {overall_min} | Max: {overall_max} | for {NUM_USERS} clients | run_time: {sys.argv[2]} | probe_freq: {sys.argv[3]}\n"
    file.write(data_to_write)

print("Closing Program")
sys.exit()
