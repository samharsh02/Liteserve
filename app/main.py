import socket
from app.httpresponse import HttpResponse

def decode_data(data):
    print("data:", data)
    return data.decode("utf-8") if data else None


def extract_request_line(request):
    request_line = request.split("\r\n")[0]
    return request_line if request_line else None

def extract_request_headers(request):
    request_header = request.split("\r\n")[1:]
    headers = dict()
    for header in request_header:
        if header == "":
            break
        key, value = header.split(": ")
        headers[key] = value
    return headers

def check_str_endpoint(request):
    request_line = extract_request_line(request)
    headers = extract_request_headers(request)
    if not request_line or len(request_line.split()) < 2:
        return HttpResponse.bad_request()
    method, path, version = request_line.split()
    if method == "GET" and path == "/":
        return HttpResponse.ok()
    elif method == "GET" and path.startswith("/echo/"):
        str_endpoint = path[6:]
        return HttpResponse.ok(body=str_endpoint)
    elif method == "GET" and path == "/user-agent":
        return HttpResponse.ok(body=headers.get("User-Agent", ""))
    else:
        return HttpResponse.bad_request()


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
