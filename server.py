import sys
import socket
import signal
import threading
from handler import handle_request

""" Simple HTTP web server implemented in Python using the socket module. """


def main():
    # Create a TCP socket (AF_INET: IPv4, SOCK_STREAM: TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_port = 3000

    # Bind socket to the server address and port
    server_socket.bind(("127.0.0.1", server_port))

    # Listen for incoming connections
    server_socket.listen(5)
    print("The server is ready to receive connections")

    # Graceful shutdown handler
    def shutdown_server(signum, frame):
        print("\nGraceful shutdown...")
        server_socket.close()
        sys.exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, shutdown_server)  # ctrl+c
    signal.signal(signal.SIGTERM, shutdown_server)  # kill

    while True:
        try:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_request, args=(conn, addr)).start()
        except OSError:
            break


if __name__ == "__main__":
    main()
