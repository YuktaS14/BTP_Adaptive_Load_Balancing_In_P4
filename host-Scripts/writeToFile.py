import socket
from datetime import datetime
import time
import sys

def server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Server listening on {ip}:{port}")
        client_responses = []

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if data:
                    client_responses.append(float(data.decode()))
                    print('Connection No : ', len(client_responses))
                    print(f"Received response time from client: {float(data.decode()):.4f} seconds")

                    # Check if received data from 50 clients
                    if len(client_responses) == int(sys.argv[1]):
                        overall_average = sum(client_responses) / len(client_responses)
                        print(f"Overall average response time: {overall_average:.4f} seconds")
                        # Write the overall average to a file
                        with open("average_response_time.txt", "a") as file:
                            # f.write(f"Overall average response time: {overall_average} seconds \n")

                                current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
                                data_to_write = f"{current_time} | Average: {overall_average} | Min: {min(client_responses)} | Max: {max(client_responses)} | for {50} clients | run_time: {sys.argv[2]} | probe_freq: {sys.argv[3]}\n"
    
                                file.write(data_to_write)

                                break   

if __name__ == "__main__":
    server_ip = "localhost"
    server_port = 5001
    server(server_ip, server_port)
