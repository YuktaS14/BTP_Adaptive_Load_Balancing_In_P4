import threading
import socket
import sys
import time

HOST = '10.0.0.11'
PORT = 50007
active_client_threads = {}
stop_flag = False
SERVER_ADDR = (HOST, PORT)

if len(sys.argv) != 3:
    print("Usage: python script.py <time_in_seconds> <probe timeperiod>")
    sys.exit(1)

run_time = int(sys.argv[1])
start_time = time.time()
end_time = start_time + run_time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
s.bind(SERVER_ADDR)
print("SERVER STARTED ON PORT ", PORT)
s.listen(50)
connections = 0

s.settimeout(20)  # Set a timeout of 5 seconds for socket operations

TIMEOUT = 20000


def close_session(client_addr=None):
    for conn in active_client_threads.keys():
        active_client_threads[conn]["timer"].cancel()
        print("%s: %s  :Session ended" % (conn, active_client_threads[conn]['addr']))

    active_client_threads.clear()
    global connections
    print("Connections: ", connections)
    #stop_flag = True


def handle_client(i, conn, addr, end_time):
    print('Client connection accepted', addr)
    while i in active_client_threads.keys():
        try:
            data = conn.recv(1024)
            if data:
                processed_data = b'ABCDE'*1024*1024
                conn.send(processed_data)
        except Exception as e:
            print('Error occurred:', e)
            break


def receive_data():
    while True:
        try:
            conn, addr = s.accept()
            global connections
            connections += 1
            print("Connection from:", addr)

            active_client_threads[connections] = {}
            active_client_threads[connections]["addr"] = addr
            active_client_threads[connections]["timer"] = threading.Timer(TIMEOUT, close_session, args=(addr,))
            active_client_threads[connections]["timer"].daemon = True
            active_client_threads[connections]["timer"].start()

            client_thread = threading.Thread(target=handle_client, args=(connections, conn, addr, end_time))
            client_thread.daemon = True
            active_client_threads[connections]["thread"] = client_thread
            client_thread.start()

        except socket.timeout:
            continue


def receive_input_commands():
    global stop_flag, connections
    while True:
        input_msg = raw_input();

        if input_msg == "q":
            with open("server.txt", "a") as file:
                 print("Connections::::  ", connections)
                 file.write("Start time: %s | End time: %s | Number of connections: %s |         Probe_freq : %s | run_time : %s \n" % (
            time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(start_time)),
            time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(end_time)),
            connections,
            sys.argv[2],
            sys.argv[1]))
            close_session()
            connections = 0
            #stop_flag = True
            #break


client_inputs_thread = threading.Thread(target=receive_data)
client_inputs_thread.daemon = True

stdin_commands_thread = threading.Thread(target=receive_input_commands)
stdin_commands_thread.daemon = True

stdin_commands_thread.start()
client_inputs_thread.start()

try:
    while not stop_flag:
        continue
except KeyboardInterrupt:
    close_session()

    

print("\nSERVER CLOSED")
sys.exit()

