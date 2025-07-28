import socket  # noqa: F401


def decode_data(data):
    print("data:", data)
    return data.decode("utf-8") if data else None


def extract_request_line(request):
    print("request:", request)
    request_line = request.split("\r\n")[0]
    print("request_line:", request_line)
    return request_line if request_line else None


def check_str_endpoint(request):
    request_line = extract_request_line(request)
    if request_line:
        request_list = request_line.split()
        if request_list[0] == "GET" and request_list[1] == "/":
            response = b"""HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"""
            return response
        if request_list[0] == "GET" and request_list[1].startswith("/echo/"):
            str_endpoint = request_list[1][6:]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(str_endpoint)}\r\n\r\n{str_endpoint}"
            return response.encode("utf-8")
        else:
            return b"""HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n"""
    else:
        return b"""HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\n"""


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is up and listening on port 4221...")

    while True:
        conn, addr = server_socket.accept() 
        print(f"Connected to {addr}.")
        buffer_size = 1024
        data = conn.recv(buffer_size)

        request = decode_data(data)
        response = check_str_endpoint(request)
        conn.sendall(response)
        conn.close()
        print(f"Connection to {addr} closed.")


if __name__ == "__main__":
    main()
