import socket
import time

def client(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        start_time = time.time()
        num_requests = 0
        total_response_time = 0
        # s.timeout(5)

        while time.time() - start_time < 30:
            # Send data to the server
            request_time = time.time()
            s.sendall(b"Hello"*50)
            num_requests += 1

            # Receive response from the server
            response = s.recv(1024)
            response_time = time.time() - request_time
            total_response_time += response_time

            # print(f"Response from server: {response.decode()}, Response time: {response_time:.4f} seconds")
            time.sleep(1)

        # Calculate average response time
        average_response_time = total_response_time / num_requests
        print(f"Average response time: {average_response_time:.4f} seconds")

        # Send overall average response time to another socket (server)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            s2.connect(("localhost", 5001))
            s2.sendall(str(average_response_time).encode())

if __name__ == "__main__":
    server_ip = "10.0.0.52"
    server_port = 50007
    client(server_ip, server_port)