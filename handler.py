import os
import mimetypes


def handle_request(conn, addr):
    try:
        # Receives the request message from the client
        message = conn.recv(1024).decode()

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        http_header = message.split()

        if not http_header:
            conn.send("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
            return

        # Reject non GET request
        if http_header[0] != "GET":
            conn.send("HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode())
            return

        if len(http_header) > 1:
            path = http_header[1]
            # Determine the filename based on the path
            if path == "/" or path == "":
                filename = "index.html"
            else:
                # .html and no-extension form
                filename = path.removeprefix("/")
                if "." not in filename:
                    filename += ".html"

            # Protect against directory traversal
            # Ensure the file is within the allowed directory
            web_root = os.path.join(os.getcwd(), "public")

            # Normalize and join safely
            safe_path = os.path.normpath(os.path.join(web_root, filename))

            if not safe_path.startswith(web_root):
                conn.send("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
                return

            with open(safe_path, "rb") as f:
                output = f.read()

            # Determine the MIME type of the file
            mime_type, _ = mimetypes.guess_type(filename)
            mime_type = mime_type or "application/octet-stream"

            # Send HTTP response header
            header = f"HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\n\r\n"
            conn.send(header.encode())

            # Send the content of the requested file to the connection socket
            conn.sendall(output)
        else:
            conn.send("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
    except IOError:
        try:
            conn.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            conn.send(
                "<html><head></head><body><p>404 Not Found</p></body></html>\r\n".encode()
            )
        except (BrokenPipeError, ConnectionAbortedError):
            pass
    finally:
        # Close the client connection socket
        conn.close()
