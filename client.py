import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
for i in range(1,100):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # data = 6
        # s.sendall(data.to_bytes(1, "big"))

        data = str(i)
        s.sendall(data.encode())
        data = s.recv(1024)

print(f"Received {data!r}")